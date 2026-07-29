"""Login endpoint tests (Story 1.2)."""

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


async def test_login_returns_token_bundle(client: AsyncClient) -> None:
    await client.post("/auth/signup", json=_SIGNUP)
    response = await client.post(
        "/auth/login", json={"email": "founder@acme.com", "password": "password123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["expires_in"] > 0


async def test_login_bad_credentials_returns_401(client: AsyncClient) -> None:
    await client.post("/auth/signup", json=_SIGNUP)
    response = await client.post(
        "/auth/login", json={"email": "founder@acme.com", "password": "nope"}
    )
    assert response.status_code == 401
    assert response.json()["code"] == "INVALID_CREDENTIALS"


async def test_logout_revokes_refresh_then_refresh_fails(client: AsyncClient) -> None:
    await client.post("/auth/signup", json=_SIGNUP)
    login = await client.post(
        "/auth/login", json={"email": "founder@acme.com", "password": "password123"}
    )
    refresh_token = login.json()["refresh_token"]

    logout = await client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert logout.status_code == 204

    after = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert after.status_code == 401
    assert after.json()["code"] == "INVALID_REFRESH_TOKEN"
