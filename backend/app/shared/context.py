"""Request envelope + authenticated context.

The Envelope is created by CorrelationMiddleware (correlation/request ids) and
enriched by AuthMiddleware with tenant_id/actor/role — **only** from a verified
access token. `require_auth` is the dependency protected endpoints use; it derives
the tenant strictly from the verified envelope, never from headers/query/body.
"""

from dataclasses import dataclass

from starlette.requests import Request

from app.shared.errors import AuthenticationError


@dataclass(frozen=True)
class Envelope:
    """Per-request context. tenant_id/actor/role are populated by AuthMiddleware
    when (and only when) a valid access token is present."""

    correlation_id: str
    request_id: str
    tenant_id: str | None = None
    actor: str | None = None
    role: str | None = None


def get_envelope(request: Request) -> Envelope:
    envelope: Envelope | None = getattr(request.state, "envelope", None)
    if envelope is None:  # pragma: no cover - middleware always sets it
        raise RuntimeError("Envelope missing — is CorrelationMiddleware installed?")
    return envelope


@dataclass(frozen=True)
class AuthContext:
    """The authenticated caller. Everything here is server-derived from the token."""

    user_id: str
    organization_id: str
    role: str
    correlation_id: str


def require_auth(request: Request) -> AuthContext:
    """Dependency for protected endpoints. 401s unless a verified token populated
    the envelope. Endpoints get tenant/actor from the return value — never the body."""
    envelope = get_envelope(request)
    if envelope.tenant_id is None or envelope.actor is None or envelope.role is None:
        raise AuthenticationError("Authentication required.", code="NOT_AUTHENTICATED")
    return AuthContext(
        user_id=envelope.actor,
        organization_id=envelope.tenant_id,
        role=envelope.role,
        correlation_id=envelope.correlation_id,
    )
