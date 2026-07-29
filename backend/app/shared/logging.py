"""Structured logging (structlog).

Configured once, explicitly, from the app factory (`configure_logging`) — not as
an import side effect. Loggers are obtained per-module via `get_logger`. Request
context (correlation id, etc.) is merged in automatically via contextvars, so log
calls never need to pass it manually.
"""

import logging
from typing import Any

import structlog


def configure_logging(app_env: str) -> None:
    """Configure structlog process-wide. Call once, in the app factory.

    Local dev gets a human-readable console renderer; everything else gets JSON
    (ready for aggregation). PII must never be logged (see ARCH-14 AD-123).
    """
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,  # pulls in correlation_id, request_id
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    renderer: Any = (
        structlog.dev.ConsoleRenderer()
        if app_env == "local"
        else structlog.processors.JSONRenderer()
    )
    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> Any:
    """Return a bound structlog logger. Typed as Any to avoid structlog generics
    friction under strict mypy; usage is `log.info("event", key=value)`."""
    return structlog.get_logger(name)
