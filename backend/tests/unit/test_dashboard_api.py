"""Dashboard endpoint tests (Story D1)."""

from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from support import define_minimal_work_sample_via_api

import app.modules.campaigns.models
import app.modules.candidates.models
import app.modules.identity.models  # noqa: F401  register tables
from app.main import create_app
from app.shared.db import Base, get_session

_CAMPAIGN = {
    "role_title": "Data Engineer",
    "role_profile": {"competencies": [{"name": "SQL"}], "bar": "senior"},
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


async def test_dashboard_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/dashboard")
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_dashboard_reflects_only_own_org(client: AsyncClient) -> None:
    token_a = await _token(client, org="Acme", email="a@acme.com")
    created = await client.post("/campaigns", json=_CAMPAIGN, headers=_auth(token_a))
    campaign_id = created.json()["id"]
    await define_minimal_work_sample_via_api(client, token_a, campaign_id)  # required to activate
    await client.post(f"/campaigns/{campaign_id}/activate", headers=_auth(token_a))

    # A fresh org sees a clean, empty dashboard — not A's campaign.
    token_b = await _token(client, org="Globex", email="b@globex.com")
    response = await client.get("/dashboard", headers=_auth(token_b))

    assert response.status_code == 200
    body = response.json()
    assert body["metrics"]["total_campaigns"] == 0
    assert body["recent_campaigns"] == []

    # A sees its own campaign.
    own = await client.get("/dashboard", headers=_auth(token_a))
    assert own.json()["metrics"]["total_campaigns"] == 1
    assert own.json()["metrics"]["active_campaigns"] == 1
