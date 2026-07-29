"""Application error hierarchy + stable machine codes.

Shallow and purposeful. Each error carries a machine-readable ``code`` (clients
rely on this, never on message text) and maps to an HTTP status via its subclass.
Services and handlers raise these; ``error_handlers.py`` renders them.
"""


class ApplicationError(Exception):
    """Base for all expected, handled application errors.

    ``metadata`` is optional, machine-oriented context for clients (e.g.
    ``{"campaign_id": "...", "status": "active"}``). It must **never** contain PII
    or secrets, and is not meant for user-facing messaging.
    """

    error_type: str = "application_error"
    http_status: int = 500

    def __init__(
        self,
        message: str,
        *,
        code: str,
        metadata: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.metadata = metadata


class ValidationError(ApplicationError):
    error_type = "validation_error"
    http_status = 400


class AuthenticationError(ApplicationError):
    error_type = "authentication_error"
    http_status = 401


class AuthorizationError(ApplicationError):
    error_type = "authorization_error"
    http_status = 403


class NotFoundError(ApplicationError):
    error_type = "not_found"
    http_status = 404


class ConflictError(ApplicationError):
    error_type = "conflict"
    http_status = 409


class BusinessRuleViolation(ApplicationError):
    error_type = "business_rule_violation"
    http_status = 422


class UpstreamServiceError(ApplicationError):
    """A dependency we call on the request's behalf failed or misbehaved (e.g. the AI
    provider was unavailable or returned output that failed our validation). This is a
    *system/upstream* condition — never a statement about the user's data. Distinct from a
    valid ESCALATE proposal, which is a successful result, not an error.
    """

    error_type = "upstream_service_error"
    http_status = 502
