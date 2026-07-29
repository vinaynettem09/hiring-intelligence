"""HTTP middleware: correlation/envelope first, then authentication.

CorrelationMiddleware creates the envelope; AuthMiddleware enriches it with
tenant/actor/role from a VERIFIED access token. Authentication lives here — no
endpoint ever parses a JWT (reviewer Rule 2). Tenant context comes ONLY from the
token, never from headers/query/body (Rule 1).
"""

import uuid
from collections.abc import Awaitable, Callable
from dataclasses import replace
from typing import Any

import jwt
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.config import get_settings
from app.shared.context import Envelope
from app.shared.tokens import decode_access_token

CORRELATION_HEADER = "X-Correlation-Id"
_BEARER_PREFIX = "Bearer "


def _new_id() -> str:
    return uuid.uuid4().hex


class CorrelationMiddleware(BaseHTTPMiddleware):
    """Attach a correlation id + base Envelope to every request."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        correlation_id = request.headers.get(CORRELATION_HEADER) or _new_id()
        request_id = _new_id()

        request.state.envelope = Envelope(correlation_id=correlation_id, request_id=request_id)

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id,
            request_id=request_id,
        )

        response = await call_next(request)
        response.headers[CORRELATION_HEADER] = correlation_id
        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """Populate the envelope's tenant/actor/role from a verified access token.

    A missing or invalid token leaves the request unauthenticated (the
    require_auth dependency then 401s on protected routes). We never trust
    anything but the verified token.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        envelope: Envelope | None = getattr(request.state, "envelope", None)
        header = request.headers.get("Authorization")

        if envelope is not None and header and header.startswith(_BEARER_PREFIX):
            settings = get_settings()
            claims: dict[str, Any] | None
            try:
                claims = decode_access_token(
                    header[len(_BEARER_PREFIX) :],
                    secret=settings.jwt_secret,
                    algorithm=settings.jwt_algorithm,
                )
            except jwt.PyJWTError:
                claims = None

            if claims is not None:
                request.state.envelope = replace(
                    envelope,
                    tenant_id=claims.get("organization_id"),
                    actor=claims.get("sub"),
                    role=claims.get("role"),
                )
                structlog.contextvars.bind_contextvars(
                    tenant_id=claims.get("organization_id"),
                    actor=claims.get("sub"),
                )

        return await call_next(request)
