"""Shared test fixtures.

Repository/service tests run against an in-memory async SQLite DB (fast, no
Docker). StaticPool + a single shared connection keeps the in-memory schema
visible across create_all and every session. Full Postgres integration via
Testcontainers/CI service lands in tests/integration.
"""

from collections.abc import AsyncIterator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.modules.audit.models
import app.modules.campaigns.models
import app.modules.candidates.models
import app.modules.consent.models
import app.modules.decisions.models
import app.modules.evaluations.models
import app.modules.evidence.models
import app.modules.identity.models
import app.modules.invitations.models
import app.modules.responses.models
import app.modules.worksample.models  # noqa: F401  register tables on Base.metadata
from app.shared.db import Base


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as db_session:
        yield db_session
    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """A session **factory** over a shared in-memory DB — for workflows that manage their
    own transaction boundaries (evaluation execution, TD-011). Seed with one session +
    commit, then the service opens its own sessions that see the committed data."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()
