"""Database foundation: declarative base, engine/session factories, and the
per-request session dependency.

Rules (enforced by shape):
- The engine is created **once** in the app factory (see main.py) and stored on
  `app.state`. It is never a module global and never created inside a repository.
- **One request = one session = commit exactly once.** `get_session` opens the
  session, yields it, commits on success, rolls back on error, and always closes.
  Repositories receive this session; they never open or commit their own.
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from starlette.requests import Request


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def create_db_engine(database_url: str) -> AsyncEngine:
    """Create the async engine. Called once from the app factory."""
    return create_async_engine(database_url, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create the session factory bound to the engine."""
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: one session per request, committed once, always closed."""
    factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    session = factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    """FastAPI dependency exposing the session factory for the rare workflow that must
    own its **own** transaction boundaries.

    This is a deliberate, documented exception to the one-request/one-session rule.
    Evaluation execution (Story 5.3, TD-011) must NOT hold a DB transaction open across a
    long-running external model call, so it opens a short read transaction to assemble the
    PII-safe input, **releases it**, calls the provider with no session held, then opens a
    fresh transaction to re-check consent and persist. Only that workflow uses this."""
    factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    return factory
