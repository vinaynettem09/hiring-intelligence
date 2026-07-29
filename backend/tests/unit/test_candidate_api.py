"""Candidate intake endpoint tests (Story 3.1)."""

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
_CANDIDATE = {"name": "Ada Lovelace", "email": "ada@x.com"}


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


async def _draft_campaign(client: AsyncClient, token: str) -> str:
    res = await client.post("/campaigns", json=_CAMPAIGN, headers=_auth(token))
    campaign_id: str = res.json()["id"]
    return campaign_id


async def _active_campaign(client: AsyncClient, token: str) -> str:
    campaign_id = await _draft_campaign(client, token)
    await define_minimal_work_sample_via_api(client, token, campaign_id)  # required to activate
    await client.post(f"/campaigns/{campaign_id}/activate", headers=_auth(token))
    return campaign_id


async def test_add_candidate_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/campaigns/x/candidates", json=_CANDIDATE)
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_add_candidate_to_active_campaign(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _active_campaign(client, token)

    response = await client.post(
        f"/campaigns/{campaign_id}/candidates", json=_CANDIDATE, headers=_auth(token)
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "invited"
    assert body["campaign_id"] == campaign_id
    assert body["candidate"]["email"] == "ada@x.com"
    assert body["candidate"]["name"] == "Ada Lovelace"
    assert body["candidate"]["id"]


async def test_add_candidate_to_draft_conflicts(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _draft_campaign(client, token)  # not activated

    response = await client.post(
        f"/campaigns/{campaign_id}/candidates", json=_CANDIDATE, headers=_auth(token)
    )

    assert response.status_code == 409
    assert response.json()["code"] == "CAMPAIGN_NOT_ACTIVE"


async def test_cannot_add_candidate_to_another_orgs_campaign(client: AsyncClient) -> None:
    token_a = await _token(client, org="Acme", email="a@acme.com")
    campaign_id = await _active_campaign(client, token_a)
    token_b = await _token(client, org="Globex", email="b@globex.com")

    response = await client.post(
        f"/campaigns/{campaign_id}/candidates", json=_CANDIDATE, headers=_auth(token_b)
    )

    assert response.status_code == 404
    assert response.json()["code"] == "CAMPAIGN_NOT_FOUND"


_CSV = b"name,email\nAda Lovelace,ada@x.com\nBad Row,not-an-email\nAda Again,ada@x.com\n"


def _csv_file(content: bytes = _CSV) -> dict[str, tuple[str, bytes, str]]:
    return {"file": ("candidates.csv", content, "text/csv")}


async def test_import_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/campaigns/x/candidates/import", files=_csv_file())
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_import_reports_per_row_outcomes(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _active_campaign(client, token)

    response = await client.post(
        f"/campaigns/{campaign_id}/candidates/import", files=_csv_file(), headers=_auth(token)
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert body["imported"] == 1  # Ada
    assert body["failed"] == 1  # bad email
    assert body["skipped"] == 1  # Ada again (dup within file)
    assert len(body["issues"]) == 2


async def test_import_to_draft_conflicts(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _draft_campaign(client, token)  # not activated

    response = await client.post(
        f"/campaigns/{campaign_id}/candidates/import", files=_csv_file(), headers=_auth(token)
    )

    assert response.status_code == 409
    assert response.json()["code"] == "CAMPAIGN_NOT_ACTIVE"


async def test_cannot_import_to_another_orgs_campaign(client: AsyncClient) -> None:
    token_a = await _token(client, org="Acme", email="a@acme.com")
    campaign_id = await _active_campaign(client, token_a)
    token_b = await _token(client, org="Globex", email="b@globex.com")

    response = await client.post(
        f"/campaigns/{campaign_id}/candidates/import", files=_csv_file(), headers=_auth(token_b)
    )

    assert response.status_code == 404
    assert response.json()["code"] == "CAMPAIGN_NOT_FOUND"


async def test_roster_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/campaigns/x/candidates")
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_roster_lists_added_candidates(client: AsyncClient) -> None:
    token = await _token(client)
    campaign_id = await _active_campaign(client, token)
    await client.post(f"/campaigns/{campaign_id}/candidates", json=_CANDIDATE, headers=_auth(token))

    response = await client.get(f"/campaigns/{campaign_id}/candidates", headers=_auth(token))

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["missing_resume"] == 1  # no résumé provided
    assert len(body["items"]) == 1
    entry = body["items"][0]
    assert entry["candidate"]["email"] == "ada@x.com"
    assert entry["status"] == "invited"
    assert entry["has_resume"] is False


async def test_cannot_view_another_orgs_roster(client: AsyncClient) -> None:
    token_a = await _token(client, org="Acme", email="a@acme.com")
    campaign_id = await _active_campaign(client, token_a)
    token_b = await _token(client, org="Globex", email="b@globex.com")

    response = await client.get(f"/campaigns/{campaign_id}/candidates", headers=_auth(token_b))

    assert response.status_code == 404
    assert response.json()["code"] == "CAMPAIGN_NOT_FOUND"
