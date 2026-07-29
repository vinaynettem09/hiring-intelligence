"""Application factory.

Wires the foundations that propagate everywhere — settings, structured logging,
the request Envelope, and the database engine/session — with **no global state**.
The engine is created once here (Story 0.4) and disposed on shutdown; sessions are
handed to handlers via the `get_session` dependency (one per request, commit once).
Run with `--factory`.

Still a scaffold: the only route is a placeholder root. Real endpoints arrive from
Story 0.6+. Don't add feature code ahead of the backlog.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.api.health import router as health_router
from app.config import get_settings
from app.modules.campaigns.api import router as campaigns_router
from app.modules.candidates.api import router as candidates_router
from app.modules.consent.api import router as consent_router
from app.modules.dashboard.api import router as dashboard_router
from app.modules.decisions.api import router as decisions_router
from app.modules.evaluations.api import router as evaluations_router
from app.modules.identity.api import router as identity_router
from app.modules.invitations.api import router as invitations_router
from app.modules.responses.api import router as responses_router
from app.modules.review.api import router as review_router
from app.modules.timeline.api import router as timeline_router
from app.modules.worksample.api import router as worksample_router
from app.shared.context import Envelope, get_envelope
from app.shared.db import create_db_engine, create_session_factory
from app.shared.error_handlers import register_error_handlers
from app.shared.logging import configure_logging, get_logger
from app.shared.middleware import AuthMiddleware, CorrelationMiddleware
from app.version import VERSION


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup already done in create_app; here we only clean up on shutdown.
    yield
    await app.state.engine.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    configure_logging(settings.app_env)
    log = get_logger(__name__)

    app = FastAPI(title="Hiring Intelligence (MVP)", version=VERSION, lifespan=_lifespan)
    # Added inner-first: CorrelationMiddleware (added last) is outermost and runs
    # first to create the envelope; AuthMiddleware then enriches it from the token.
    app.add_middleware(AuthMiddleware)
    app.add_middleware(CorrelationMiddleware)
    register_error_handlers(app)

    # Engine + session factory created ONCE, stored on app.state (never global).
    engine = create_db_engine(settings.database_url)
    app.state.engine = engine
    app.state.session_factory = create_session_factory(engine)

    app.include_router(health_router)
    app.include_router(identity_router)
    app.include_router(campaigns_router)
    app.include_router(candidates_router)
    app.include_router(dashboard_router)
    app.include_router(invitations_router)
    app.include_router(consent_router)
    app.include_router(worksample_router)
    app.include_router(responses_router)
    app.include_router(evaluations_router)
    app.include_router(decisions_router)
    app.include_router(review_router)
    app.include_router(timeline_router)

    @app.get("/")
    async def root(envelope: Envelope = Depends(get_envelope)) -> dict[str, str]:
        # Minimal liveness. Structured status is at /health; identity at /me.
        log.info("root.requested")
        return {"service": "hiring-intelligence", "status": "scaffold"}

    log.info("app.created", app_env=settings.app_env, version=VERSION)
    return app
