"""Candidate invitation model — a secure, opaque magic link granting access to **one**
CandidateEvaluation (this person's participation in this campaign), and nothing else.

Only the SHA-256 hash of the token is stored; the raw token exists only in the email
link. The invitation is the candidate's trust boundary — separate from recruiter JWTs.
"""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Invitation(Base):
    __tablename__ = "invitations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    # Tenant owner (denormalized for uniform scoping on the recruiter side).
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    # Access is granted to a specific participation, not just a person (INV-009).
    candidate_evaluation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("candidate_evaluations.id"), nullable=False, index=True
    )
    # Only the hash is stored — the raw token is never persisted.
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    accessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
