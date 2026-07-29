"""Opaque identifier generation.

One place mints IDs so switching the scheme is a single change. Currently UUID4
hex; Story 0.9 may switch to ULID (sortable) — only this function changes.
"""

import uuid


def new_id() -> str:
    """Return a new opaque, PII-free identifier."""
    return uuid.uuid4().hex
