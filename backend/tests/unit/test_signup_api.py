"""Signup endpoint tests (Story 1.1) — verifies the HTTP contract.

Uses httpx AsyncClient (same event loop as the async SQLite engine) and overrides
the get_session dependency with a test session.
"""

from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.modules.identity.models  # noqa: F401  register tables
from app.main import create_app
from app.shared.db import Base, get_session

_PAYLOAD = {"organization_name": "Acme", "email": "founder@acme.com", "password": "password123"}


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

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client
    await engine.dispose()


async def test_signup_returns_201_and_never_leaks_password(client: AsyncClient) -> None:
    response = await client.post("/auth/signup", json=_PAYLOAD)
    assert response.status_code == 201

    body = response.json()
    assert body["organization"]["name"] == "Acme"
    assert body["user"]["email"] == "founder@acme.com"
    assert body["user"]["role"] == "admin"
    assert "password123" not in response.text
    assert "password_hash" not in response.text


async def test_signup_duplicate_email_conflicts(client: AsyncClient) -> None:
    first = await client.post("/auth/signup", json=_PAYLOAD)
    assert first.status_code == 201

    second = await client.post("/auth/signup", json={**_PAYLOAD, "organization_name": "Other"})
    assert second.status_code == 409
    assert second.json()["code"] == "USER_ALREADY_EXISTS"
