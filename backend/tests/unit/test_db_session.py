"""get_session dependency behavior (Story 0.4 infra, tested here).

Verifies the one-request-one-session contract: the dependency yields a working
session and closes it when the request finishes.
"""

from types import SimpleNamespace
from typing import cast

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.requests import Request

from app.shared.db import get_session


async def test_get_session_yields_then_closes() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    factory = async_sessionmaker(engine, expire_on_commit=False)
    # Minimal stand-in for the request's app.state.session_factory (duck-typed).
    fake_request = cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(session_factory=factory))),
    )

    agen = get_session(fake_request)
    session = await agen.__anext__()
    result = await session.execute(text("SELECT 1"))
    assert result.scalar() == 1

    # Exhausting the generator runs commit + close in the dependency's finally.
    with pytest.raises(StopAsyncIteration):
        await agen.__anext__()

    await engine.dispose()
