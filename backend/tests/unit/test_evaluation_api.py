"""Evaluation API (Story 5.2): evaluate / rerun / history, auth, idempotency, tenant 404.
Seeds a real submitted evaluation via the service helper (same in-memory DB), then drives
the endpoints over HTTP with a real recruiter token."""

from collections.abc import AsyncIterator
from typing import Any

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from support import SubmittedEvaluation, submitted_evaluation

import app.modules.evaluations.models  # noqa: F401  register tables
from app.main import create_app
from app.shared.db import Base, get_session, get_session_factory


@pytest_asyncio.fixture
async def api() -> AsyncIterator[tuple[AsyncClient, async_sessionmaker[AsyncSession]]]:
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
    # Evaluation endpoints own their transaction boundaries (TD-011) → they take the
    # factory, not a request session. Override it to the test's factory.
    app.dependency_overrides[get_session_factory] = lambda: factory
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client, factory
    await engine.dispose()


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def _seed(factory: async_sessionmaker[AsyncSession], **kwargs: Any) -> SubmittedEvaluation:
    async with factory() as session:
        setup = await submitted_evaluation(session, **kwargs)
        await session.commit()
    return setup


async def _login(client: AsyncClient, email: str) -> str:
    login = await client.post("/auth/login", json={"email": email, "password": "password123"})
    token: str = login.json()["access_token"]
    return token


async def _signup(client: AsyncClient, *, org: str, email: str) -> None:
    await client.post(
        "/auth/signup", json={"organization_name": org, "email": email, "password": "password123"}
    )


async def test_evaluate_requires_auth(
    api: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, factory = api
    setup = await _seed(factory)
    res = await client.post(f"/evaluations/{setup.evaluation_id}/evaluate")
    assert res.status_code == 401


async def test_evaluate_returns_persisted_run(
    api: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, factory = api
    setup = await _seed(factory, user_email="founder@acme.com")
    token = await _login(client, "founder@acme.com")

    res = await client.post(f"/evaluations/{setup.evaluation_id}/evaluate", headers=_auth(token))
    assert res.status_code == 200
    body = res.json()
    assert body["run_number"] == 1
    assert body["recommendation"] == "PROCEED"
    assert body["provenance"]["provider"] == "mock"  # honest: mock, not real intelligence
    assert body["input_fingerprint"].startswith("sha256:")
    assert body["competency_assessments"]
    assert "decision" not in body  # a proposal, never a decision


async def test_evaluate_is_idempotent(
    api: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, factory = api
    setup = await _seed(factory, user_email="founder@acme.com")
    token = await _login(client, "founder@acme.com")

    first = await client.post(f"/evaluations/{setup.evaluation_id}/evaluate", headers=_auth(token))
    second = await client.post(f"/evaluations/{setup.evaluation_id}/evaluate", headers=_auth(token))
    assert first.json()["id"] == second.json()["id"]

    history = await client.get(f"/evaluations/{setup.evaluation_id}", headers=_auth(token))
    assert history.json()["run_count"] == 1


async def test_idempotency_key_returns_same_run(
    api: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, factory = api
    setup = await _seed(factory, user_email="founder@acme.com")
    token = await _login(client, "founder@acme.com")
    headers = {**_auth(token), "Idempotency-Key": "req-1"}

    first = await client.post(f"/evaluations/{setup.evaluation_id}/evaluate", headers=headers)
    second = await client.post(f"/evaluations/{setup.evaluation_id}/evaluate", headers=headers)
    assert first.json()["id"] == second.json()["id"]


async def test_rerun_creates_new_run(
    api: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, factory = api
    setup = await _seed(factory, user_email="founder@acme.com")
    token = await _login(client, "founder@acme.com")

    await client.post(f"/evaluations/{setup.evaluation_id}/evaluate", headers=_auth(token))
    rerun = await client.post(f"/evaluations/{setup.evaluation_id}/rerun", headers=_auth(token))
    assert rerun.status_code == 201
    assert rerun.json()["run_number"] == 2

    history = await client.get(f"/evaluations/{setup.evaluation_id}", headers=_auth(token))
    body = history.json()
    assert body["run_count"] == 2
    assert body["latest"]["run_number"] == 2


async def test_history_before_evaluation_is_empty(
    api: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, factory = api
    setup = await _seed(factory, user_email="founder@acme.com")
    token = await _login(client, "founder@acme.com")
    res = await client.get(f"/evaluations/{setup.evaluation_id}", headers=_auth(token))
    assert res.status_code == 200
    assert res.json() == {
        "candidate_evaluation_id": setup.evaluation_id,
        "run_count": 0,
        "latest": None,
        "runs": [],
    }


async def test_other_tenant_gets_404(
    api: tuple[AsyncClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, factory = api
    setup = await _seed(factory, org="Acme", user_email="a@acme.com")
    await _signup(client, org="Globex", email="b@globex.com")
    intruder = await _login(client, "b@globex.com")

    evaluate = await client.post(
        f"/evaluations/{setup.evaluation_id}/evaluate", headers=_auth(intruder)
    )
    assert evaluate.status_code == 404
    read = await client.get(f"/evaluations/{setup.evaluation_id}", headers=_auth(intruder))
    assert read.status_code == 404
