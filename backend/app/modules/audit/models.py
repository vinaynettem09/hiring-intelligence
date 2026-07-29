"""Audit event model — the platform's **append-only** record of meaningful lifecycle
actions (a Tier-0 product invariant). Rows are inserted and never updated or deleted.
Tenant-scoped (organization_id on every row). `details` never contains secrets (no raw
tokens) or unnecessary PII.
"""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    actor_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # recruiter|candidate|system
    actor_user_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)  # e.g. "invitation.issued"
    target_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    # Machine-oriented context only — never secrets/raw tokens; PII-minimized.
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
