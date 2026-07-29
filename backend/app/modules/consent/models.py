"""Consent model — an **append-only, versioned domain fact**, not a mutable boolean.

Each row is one grant: who (via evaluation) agreed, to which exact consent version, and
when. Withdrawal is modeled as `withdrawn_at` (set once, never cleared) so it can be
implemented later without reshaping anything. We never mutate what a past grant meant;
a new consent version means a new row (INV-010 / corpus INV-11).

Active consent = a row for the evaluation whose `withdrawn_at` is NULL.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Consent(Base):
    __tablename__ = "consents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    candidate_evaluation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("candidate_evaluations.id"), nullable=False, index=True
    )
    consent_version: Mapped[str] = mapped_column(String(64), nullable=False)
    consented_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # Set once if/when consent is withdrawn (future story). Never un-set.
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
