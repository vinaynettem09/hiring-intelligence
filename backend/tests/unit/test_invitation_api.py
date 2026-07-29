"""Invitation endpoint tests — recruiter issue + candidate resolve (Story 4.1)."""

import re
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from support import define_minimal_work_sample_via_api

import app.modules.audit.models
import app.modules.campaigns.models
import app.modules.candidates.models
import app.modules.identity.models
import app.modules.invitations.models  # noqa: F401  register tables
from app.main import create_app
from app.platform.email import EmailMessage, get_email_provider
from app.shared.db import Base, get_session

_CAMPAIGN = {
    "role_title": "Data Engineer",
    "role_profile": {"competencies": [{"name": "SQL"}], "bar": "senior"},
}
_CANDIDATE = {"name": "Ada Lovelace", "email": "ada@x.com"}


class _FakeEmail:
    def __init__(self) -> None:
        self.sent: list[EmailMessage] = []

    async def send(self, message: EmailMessage) -> None:
        self.sent.append(message)


@pytest.fixture
def outbox() -> _FakeEmail:
    return _FakeEmail()


@pytest_asyncio.fixture
async def client(outbox: _FakeEmail) -> AsyncIterator[AsyncClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    app = create_app()

    async def _session_override() -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_session] = _session_override
    app.dependency_overrides[get_email_provider] = lambda: outbox
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http_client:
        yield http_client
    await engine.dispose()


async def _token(client: AsyncClient, *, org: str = "Acme", email: str = "founder@acme.com") -> str:
    await client.post(
        "/auth/signup",
        json={"organization_name": org, "email": email, "password": "password123"},
    )
    login = await client.post("/auth/login", json={"email": email, "password": "password123"})
    access: str = login.json()["access_token"]
    return access


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def _active_evaluation(client: AsyncClient, token: str) -> str:
    created = await client.post("/campaigns", json=_CAMPAIGN, headers=_auth(token))
    campaign_id = created.json()["id"]
    await define_minimal_work_sample_via_api(client, token, campaign_id)  # required to activate
    await client.post(f"/campaigns/{campaign_id}/activate", headers=_auth(token))
    added = await client.post(
        f"/campaigns/{campaign_id}/candidates", json=_CANDIDATE, headers=_auth(token)
    )
    evaluation_id: str = added.json()["id"]
    return evaluation_id


def _link_token(outbox: _FakeEmail) -> str:
    match = re.search(r"/invite/(\S+)", outbox.sent[-1].text_body)
    assert match is not None
    return match.group(1)


async def test_issue_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/evaluations/whatever/invitation")
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_issue_returns_summary_without_token(client: AsyncClient, outbox: _FakeEmail) -> None:
    token = await _token(client)
    evaluation_id = await _active_evaluation(client, token)

    response = await client.post(f"/evaluations/{evaluation_id}/invitation", headers=_auth(token))

    assert response.status_code == 201
    body = response.json()
    assert body["candidate"]["email"] == "ada@x.com"
    assert "token" not in body  # the raw token is only ever in the email
    assert len(outbox.sent) == 1


async def test_cannot_issue_for_another_orgs_evaluation(
    client: AsyncClient, outbox: _FakeEmail
) -> None:
    token_a = await _token(client, org="Acme", email="a@acme.com")
    evaluation_id = await _active_evaluation(client, token_a)
    token_b = await _token(client, org="Globex", email="b@globex.com")

    response = await client.post(f"/evaluations/{evaluation_id}/invitation", headers=_auth(token_b))

    assert response.status_code == 404
    assert response.json()["code"] == "EVALUATION_NOT_FOUND"


async def test_candidate_resolves_valid_invitation(client: AsyncClient, outbox: _FakeEmail) -> None:
    token = await _token(client)
    evaluation_id = await _active_evaluation(client, token)
    await client.post(f"/evaluations/{evaluation_id}/invitation", headers=_auth(token))
    link_token = _link_token(outbox)

    # No recruiter auth — the link token is the authorization.
    response = await client.post("/candidate/invitation", json={"token": link_token})

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_name"] == "Ada Lovelace"
    assert body["organization_name"] == "Acme"
    assert body["role_title"] == "Data Engineer"
    assert body["next_step"] == "consent"


async def test_candidate_invalid_token_is_rejected(client: AsyncClient) -> None:
    response = await client.post("/candidate/invitation", json={"token": "bogus"})
    assert response.status_code == 404
    assert response.json()["code"] == "INVITATION_INVALID"
