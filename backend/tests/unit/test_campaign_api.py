"""Campaign endpoint tests (Story 2.1).

Verifies: creating a campaign requires a valid token; the tenant is taken from the
token (not the body); a created campaign is a draft echoing its role profile.
"""

from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from support import define_minimal_work_sample_via_api

import app.modules.campaigns.models
import app.modules.identity.models  # noqa: F401  register tables
from app.main import create_app
from app.shared.db import Base, get_session

_SIGNUP = {"organization_name": "Acme", "email": "founder@acme.com", "password": "password123"}
_CAMPAIGN = {
    "role_title": "Data Engineer",
    "role_profile": {
        "competencies": [{"name": "SQL", "description": "writes correct joins"}],
        "bar": "senior: independently ships correct queries",
    },
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


async def _signup_and_token(
    client: AsyncClient,
    *,
    org: str = "Acme",
    email: str = "founder@acme.com",
) -> str:
    await client.post(
        "/auth/signup",
        json={"organization_name": org, "email": email, "password": "password123"},
    )
    login = await client.post("/auth/login", json={"email": email, "password": "password123"})
    token: str = login.json()["access_token"]
    return token


async def _create_campaign(client: AsyncClient, token: str) -> str:
    response = await client.post(
        "/campaigns", json=_CAMPAIGN, headers={"Authorization": f"Bearer {token}"}
    )
    campaign_id: str = response.json()["id"]
    return campaign_id


async def test_create_campaign_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/campaigns", json=_CAMPAIGN)
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_create_campaign_returns_draft(client: AsyncClient) -> None:
    token = await _signup_and_token(client)

    response = await client.post(
        "/campaigns", json=_CAMPAIGN, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["status"] == "draft"
    assert body["role_title"] == "Data Engineer"
    assert body["role_profile"]["competencies"][0]["name"] == "SQL"
    assert body["role_profile"]["bar"].startswith("senior")


async def test_create_campaign_rejects_empty_role_profile(client: AsyncClient) -> None:
    token = await _signup_and_token(client)

    response = await client.post(
        "/campaigns",
        json={"role_title": "Data Engineer", "role_profile": {"competencies": [], "bar": "x"}},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json()["code"] == "REQUEST_VALIDATION"


async def test_activate_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/campaigns/some-id/activate")
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_create_then_activate(client: AsyncClient) -> None:
    token = await _signup_and_token(client)
    campaign_id = await _create_campaign(client, token)
    await define_minimal_work_sample_via_api(client, token, campaign_id)  # required to activate

    response = await client.post(
        f"/campaigns/{campaign_id}/activate", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "active"


async def test_activating_twice_conflicts(client: AsyncClient) -> None:
    token = await _signup_and_token(client)
    campaign_id = await _create_campaign(client, token)
    await define_minimal_work_sample_via_api(client, token, campaign_id)
    headers = {"Authorization": f"Bearer {token}"}

    first = await client.post(f"/campaigns/{campaign_id}/activate", headers=headers)
    assert first.status_code == 200

    second = await client.post(f"/campaigns/{campaign_id}/activate", headers=headers)
    assert second.status_code == 409
    assert second.json()["code"] == "CAMPAIGN_NOT_DRAFT"


async def test_cannot_activate_another_orgs_campaign(client: AsyncClient) -> None:
    """The security-regression pattern, repeated for the activate write path: org B
    cannot activate org A's campaign — from B's side it simply does not exist (404)."""
    token_a = await _signup_and_token(client, org="Acme", email="a@acme.com")
    campaign_id = await _create_campaign(client, token_a)
    token_b = await _signup_and_token(client, org="Globex", email="b@globex.com")

    response = await client.post(
        f"/campaigns/{campaign_id}/activate", headers={"Authorization": f"Bearer {token_b}"}
    )

    assert response.status_code == 404
    assert response.json()["code"] == "CAMPAIGN_NOT_FOUND"


async def test_list_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/campaigns")
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_list_returns_summaries(client: AsyncClient) -> None:
    token = await _signup_and_token(client)
    await _create_campaign(client, token)

    response = await client.get("/campaigns", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["limit"] == 20 and body["offset"] == 0
    assert len(body["items"]) == 1
    # List rows are summaries — no role_profile leaks into the list payload.
    assert set(body["items"][0]) == {"id", "role_title", "status", "created_at"}


async def test_detail_returns_full_campaign(client: AsyncClient) -> None:
    token = await _signup_and_token(client)
    campaign_id = await _create_campaign(client, token)

    response = await client.get(
        f"/campaigns/{campaign_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == campaign_id
    assert body["role_profile"]["competencies"][0]["name"] == "SQL"  # full detail


async def test_detail_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/campaigns/some-id")
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_cannot_view_another_orgs_campaign(client: AsyncClient) -> None:
    """Cross-tenant READ isolation at the API — the pattern repeated for GET detail."""
    token_a = await _signup_and_token(client, org="Acme", email="a@acme.com")
    campaign_id = await _create_campaign(client, token_a)
    token_b = await _signup_and_token(client, org="Globex", email="b@globex.com")

    response = await client.get(
        f"/campaigns/{campaign_id}", headers={"Authorization": f"Bearer {token_b}"}
    )

    assert response.status_code == 404
    assert response.json()["code"] == "CAMPAIGN_NOT_FOUND"


async def test_list_shows_only_your_orgs_campaigns(client: AsyncClient) -> None:
    token_a = await _signup_and_token(client, org="Acme", email="a@acme.com")
    await _create_campaign(client, token_a)
    token_b = await _signup_and_token(client, org="Globex", email="b@globex.com")

    response = await client.get("/campaigns", headers={"Authorization": f"Bearer {token_b}"})

    assert response.status_code == 200
    assert response.json()["total"] == 0  # B sees none of A's campaigns
