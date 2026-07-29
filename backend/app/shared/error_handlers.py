"""Exception handlers: render errors as a stable JSON shape and log at the right level.

Response shape (clients depend on ``code``, not ``message``):
    {"type": ..., "code": ..., "message": ..., "correlation_id": ...}

Logging: expected application errors → WARNING; unexpected errors → ERROR with a
stack trace. The client only ever sees a generic message for unexpected errors —
no internal detail, no PII, ever leaks.
"""

from typing import cast

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.shared.context import Envelope
from app.shared.errors import ApplicationError
from app.shared.logging import get_logger
from app.shared.middleware import CORRELATION_HEADER

log = get_logger(__name__)


def _correlation_id(request: Request) -> str | None:
    envelope: Envelope | None = getattr(request.state, "envelope", None)
    if envelope is not None:
        return envelope.correlation_id
    return request.headers.get(CORRELATION_HEADER)


def _error_response(
    *,
    error_type: str,
    code: str,
    message: str,
    http_status: int,
    correlation_id: str | None,
    metadata: dict[str, object] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=http_status,
        content={
            "type": error_type,
            "code": code,
            "message": message,
            "correlation_id": correlation_id,
            "metadata": metadata,
        },
    )


async def _handle_application_error(request: Request, exc: Exception) -> JSONResponse:
    err = cast(ApplicationError, exc)  # registered only for ApplicationError
    log.warning(
        "application_error",
        code=err.code,
        error_type=err.error_type,
        status=err.http_status,
    )
    return _error_response(
        error_type=err.error_type,
        code=err.code,
        message=err.message,
        http_status=err.http_status,
        correlation_id=_correlation_id(request),
        metadata=err.metadata,
    )


async def _handle_request_validation(request: Request, exc: Exception) -> JSONResponse:
    err = cast(RequestValidationError, exc)
    # Field locations + messages only — never echo the input values (may contain PII).
    details = [{"loc": list(e.get("loc", [])), "msg": e.get("msg", "")} for e in err.errors()]
    log.warning("request_validation_error", error_count=len(details))
    return JSONResponse(
        status_code=400,
        content={
            "type": "validation_error",
            "code": "REQUEST_VALIDATION",
            "message": "Request validation failed.",
            "correlation_id": _correlation_id(request),
            "details": details,
        },
    )


async def _handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
    log.error("unhandled_exception", exc_info=exc)  # full stack in logs only
    return _error_response(
        error_type="internal_error",
        code="INTERNAL_ERROR",
        message="An unexpected error occurred.",
        http_status=500,
        correlation_id=_correlation_id(request),
    )


def register_error_handlers(app: FastAPI) -> None:
    """Wire the handlers onto the app (called from the factory)."""
    app.add_exception_handler(ApplicationError, _handle_application_error)
    app.add_exception_handler(RequestValidationError, _handle_request_validation)
    app.add_exception_handler(Exception, _handle_unexpected)
