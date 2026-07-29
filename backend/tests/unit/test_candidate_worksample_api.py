"""Candidate work-sample endpoint tests (Story 4.4)."""

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
    "tasks": [
        {
            "prompt": "Investigate a latency regression.",
            "evidence_intent": "Reasoning.",
            "competencies": ["SQL"],
        }
    ],
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


async def _invited_token(client: AsyncClient, outbox: _FakeEmail) -> str:
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
    return match.group(1)


async def test_load_denied_without_consent(client: AsyncClient, outbox: _FakeEmail) -> None:
    link = await _invited_token(client, outbox)
    response = await client.post("/candidate/work-sample", json={"token": link})
    assert response.status_code == 403
    assert response.json()["code"] == "CONSENT_REQUIRED"


async def test_load_and_save_after_consent(client: AsyncClient, outbox: _FakeEmail) -> None:
    link = await _invited_token(client, outbox)
    await client.post("/candidate/consent/grant", json={"token": link})

    loaded = await client.post("/candidate/work-sample", json={"token": link})
    assert loaded.status_code == 200
    body = loaded.json()
    assert body["organization_name"] == "Acme"
    task = body["tasks"][0]
    assert "evidence_intent" not in task  # candidate DTO hides recruiter-only fields
    assert "competencies" not in task

    saved = await client.post(
        "/candidate/work-sample/response",
        json={"token": link, "task_id": task["task_id"], "response_text": "My answer."},
    )
    assert saved.status_code == 200
    assert saved.json()["task_id"] == task["task_id"]

    reload = await client.post("/candidate/work-sample", json={"token": link})
    assert reload.json()["tasks"][0]["response_text"] == "My answer."


async def test_invalid_token_denied(client: AsyncClient) -> None:
    response = await client.post("/candidate/work-sample", json={"token": "bogus"})
    assert response.status_code == 404
    assert response.json()["code"] == "INVITATION_INVALID"
