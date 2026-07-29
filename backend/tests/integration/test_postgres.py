"""PostgreSQL integration test.

Focused on behavior SQLite cannot verify: real commit durability across
connections and the async session lifecycle against Postgres. Assumes migrations
have been applied (CI runs `alembic upgrade head`; locally: `make up && make migrate`).
Does NOT duplicate the fast SQLite unit tests.
"""

import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.modules.identity.repository import OrganizationRepository

pytestmark = pytest.mark.integration

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://app:app@localhost:5432/hiring")


@pytest_asyncio.fixture
async def make_session() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(DATABASE_URL)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


async def test_commit_persists_across_sessions(
    make_session: async_sessionmaker[AsyncSession],
) -> None:
    # Write + commit in one session...
    async with make_session() as session_one:
        created = await OrganizationRepository(session_one).create(name="PG Integration Co")
        organization_id = created.id
        await session_one.commit()

    # ...read back in a fresh session: verifies real durability + async lifecycle.
    async with make_session() as session_two:
        fetched = await OrganizationRepository(session_two).get(organization_id)
        assert fetched is not None
        assert fetched.name == "PG Integration Co"
