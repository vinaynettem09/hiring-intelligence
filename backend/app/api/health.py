"""System health endpoint.

Structured on purpose: the response shape scales as dependencies are added.
Today it reports the application and the database; more checks slot into `checks`
without changing the contract. Returns HTTP 200 as a liveness signal even when a
dependency is degraded (a stricter readiness split can come later if needed).
"""

from typing import Any

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request

from app.version import VERSION

router = APIRouter(tags=["system"])


async def _check_database(engine: AsyncEngine) -> bool:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:
        return False
    return True


@router.get("/health")
async def health(request: Request) -> dict[str, Any]:
    engine: AsyncEngine = request.app.state.engine
    checks = {
        "application": "healthy",
        "database": "healthy" if await _check_database(engine) else "unhealthy",
    }
    status = "healthy" if all(v == "healthy" for v in checks.values()) else "degraded"
    return {"status": status, "checks": checks, "version": VERSION}
