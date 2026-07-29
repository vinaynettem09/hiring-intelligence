"""Authenticated /me + auth-enforcement tests (Story 1.3).

Verifies: tenant/identity come from the verified token; protected routes 401
without a valid token; the identity endpoint returns the caller's own org.
"""

from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.modules.identity.models  # noqa: F401  register tables
from app.main import create_app
from app.shared.db import Base, get_session

_SIGNUP = {"organization_name": "Acme", "email": "founder@acme.com", "password": "password123"}


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


async def _signup_and_token(client: AsyncClient) -> str:
    await client.post("/auth/signup", json=_SIGNUP)
    login = await client.post(
        "/auth/login", json={"email": _SIGNUP["email"], "password": _SIGNUP["password"]}
    )
    token: str = login.json()["access_token"]
    return token


async def test_me_returns_canonical_identity(client: AsyncClient) -> None:
    token = await _signup_and_token(client)
    response = await client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    body = response.json()
    assert body["email"] == "founder@acme.com"
    assert body["role"] == "admin"
    assert body["organization"]["name"] == "Acme"  # org derived from the token's user
    assert body["id"]
    assert body["organization"]["id"]


async def test_me_without_token_is_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/me")
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"


async def test_me_with_invalid_token_is_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/me", headers={"Authorization": "Bearer not-a-jwt"})
    assert response.status_code == 401
    assert response.json()["code"] == "NOT_AUTHENTICATED"
