"""Submission endpoint tests (Story 4.5)."""

import re
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.modules.audit.models
import app.modules.campaigns.models
import app.modules.candidates.models
import app.modules.consent.models
import app.modules.evidence.models
import app.modules.identity.models
import app.modules.invitations.models
import app.modules.responses.models
import app.modules.worksample.models  # noqa: F401  register tables
from app.main import create_app
from app.platform.email import EmailMessage, get_email_provider
from app.shared.db import Base, get_session

_CAMPAIGN = {
    "role_title": "Data Engineer",
    "role_profile": {"competencies": [{"name": "SQL"}], "bar": "senior"},
}
_WS = {
    "title": "Backend work sample",
    "tasks": [{"prompt": "Explain.", "evidence_intent": "Reasoning.", "competencies": ["SQL"]}],
}


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


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def _consented_link(client: AsyncClient, outbox: _FakeEmail) -> str:
    await client.post(
        "/auth/signup",
        json={"organization_name": "Acme", "email": "founder@acme.com", "password": "password123"},
    )
    login = await client.post(
        "/auth/login", json={"email": "founder@acme.com", "password": "password123"}
    )
    token = login.json()["access_token"]
    created = await client.post("/campaigns", json=_CAMPAIGN, headers=_auth(token))
    campaign_id = created.json()["id"]
    await client.put(f"/campaigns/{campaign_id}/work-sample", json=_WS, headers=_auth(token))
    await client.post(f"/campaigns/{campaign_id}/activate", headers=_auth(token))
    added = await client.post(
        f"/campaigns/{campaign_id}/candidates",
        json={"name": "Ada Lovelace", "email": "ada@x.com"},
        headers=_auth(token),
    )
    await client.post(f"/evaluations/{added.json()['id']}/invitation", headers=_auth(token))
    match = re.search(r"/invite/(\S+)", outbox.sent[-1].text_body)
    assert match is not None
    link = match.group(1)
    await client.post("/candidate/consent/grant", json={"token": link})
    return link


async def test_submit_incomplete_has_stable_error(client: AsyncClient, outbox: _FakeEmail) -> None:
    link = await _consented_link(client, outbox)
    response = await client.post("/candidate/work-sample/submit", json={"token": link})
    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "WORK_SAMPLE_INCOMPLETE"
    assert body["metadata"]["missing_task_positions"] == [1]


async def test_submit_then_return_shows_submitted(client: AsyncClient, outbox: _FakeEmail) -> None:
    link = await _consented_link(client, outbox)
    loaded = await client.post("/candidate/work-sample", json={"token": link})
    task_id = loaded.json()["tasks"][0]["task_id"]
    await client.post(
        "/candidate/work-sample/response",
        json={"token": link, "task_id": task_id, "response_text": "My answer."},
    )

    submitted = await client.post("/candidate/work-sample/submit", json={"token": link})
    assert submitted.status_code == 200
    assert submitted.json()["evidence_count"] == 1
    assert submitted.json()["submitted_at"]

    # Returning shows the authoritative submitted state; edits are locked.
    reload = await client.post("/candidate/work-sample", json={"token": link})
    assert reload.json()["submitted"] is True
    locked = await client.post(
        "/candidate/work-sample/response",
        json={"token": link, "task_id": task_id, "response_text": "edit"},
    )
    assert locked.status_code == 409
    assert locked.json()["code"] == "WORK_SAMPLE_ALREADY_SUBMITTED"


async def test_submit_invalid_token(client: AsyncClient) -> None:
    response = await client.post("/candidate/work-sample/submit", json={"token": "bogus"})
    assert response.status_code == 404
    assert response.json()["code"] == "INVITATION_INVALID"
