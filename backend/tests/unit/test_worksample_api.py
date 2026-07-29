"""Work Sample endpoint tests (Story 4.3)."""

from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.modules.campaigns.models
import app.modules.identity.models
import app.modules.worksample.models  # noqa: F401  register tables
from app.main import create_app
from app.shared.db import Base, get_session

_CAMPAIGN = {
    "role_title": "Data Engineer",
    "role_profile": {"competencies": [{"name": "SQL"}, {"name": "Python"}], "bar": "senior"},
}
_WS = {
    "title": "Backend work sample",
    "tasks": [
        {
            "prompt": "Investigate a latency regression.",
            "evidence_intent": "Structured debugging + production reasoning.",
            "competencies": ["SQL", "Python"],
            "expected_effort_minutes": 15,
        }
    ],
}


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
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
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http_client:
        yield http_client
    await engine.dispose()


async def _token(client: AsyncClient, *, org: str = "Acme", email: str = "founder@acme.com") -> str:
    await client.post(
        "/auth/signup",
        json={"organization_name": org, "email": email, "password": "password123"},
    )
    login = await client.post("/auth/login", json={"email": email, "password": "password123"})
    token: str = login.json()["access_token"]
    return token


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def _draft(client: AsyncClient, token: str) -> str:
    created = await client.post("/campaigns", json=_CAMPAIGN, headers=_auth(token))
    campaign_id: str = created.json()["id"]
    return campaign_id


async def test_get_empty_then_define(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _draft(client, token)

    empty = await client.get(f"/campaigns/{campaign_id}/work-sample", headers=_auth(token))
    assert empty.status_code == 200
    assert empty.json()["exists"] is False
    assert empty.json()["coverage"]["uncovered"] == ["SQL", "Python"]

    defined = await client.put(
        f"/campaigns/{campaign_id}/work-sample", json=_WS, headers=_auth(token)
    )
    assert defined.status_code == 200
    body = defined.json()
    assert body["exists"] is True
    assert body["editable"] is True
    assert len(body["tasks"]) == 1
    assert body["estimated_minutes"] == 15
    assert body["coverage"]["uncovered"] == []


async def test_define_rejects_unknown_competency(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _draft(client, token)
    bad = {
        "title": "WS",
        "tasks": [
            {"prompt": "x", "evidence_intent": "y", "competencies": ["Kubernetes"]},
        ],
    }
    response = await client.put(
        f"/campaigns/{campaign_id}/work-sample", json=bad, headers=_auth(token)
    )
    assert response.status_code == 400
    assert response.json()["code"] == "WORK_SAMPLE_INVALID"


async def test_activation_blocked_without_work_sample(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _draft(client, token)
    response = await client.post(f"/campaigns/{campaign_id}/activate", headers=_auth(token))
    assert response.status_code == 422
    assert response.json()["code"] == "CAMPAIGN_INCOMPLETE"


async def test_frozen_after_activation(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _draft(client, token)
    await client.put(f"/campaigns/{campaign_id}/work-sample", json=_WS, headers=_auth(token))
    await client.post(f"/campaigns/{campaign_id}/activate", headers=_auth(token))

    response = await client.put(
        f"/campaigns/{campaign_id}/work-sample", json=_WS, headers=_auth(token)
    )
    assert response.status_code == 409
    assert response.json()["code"] == "WORK_SAMPLE_LOCKED"


async def test_cannot_read_another_orgs_work_sample(client: AsyncClient) -> None:
    token_a = await _token(client, org="Acme", email="a@acme.com")
    campaign_id = await _draft(client, token_a)
    token_b = await _token(client, org="Globex", email="b@globex.com")

    response = await client.get(f"/campaigns/{campaign_id}/work-sample", headers=_auth(token_b))
    assert response.status_code == 404
    assert response.json()["code"] == "CAMPAIGN_NOT_FOUND"
