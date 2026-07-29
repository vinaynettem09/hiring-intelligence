"""Candidate ORM models — the point where **identity is separated from evaluation**.

`Candidate` holds the person's PII (name, email, a pointer to their résumé) and is
owned by the organization. `CandidateEvaluation` is the AI-visible record that joins a
candidate to a campaign; it references the candidate by **id only** and carries no PII,
so the evaluation pipeline (Epics 4-5) can consume evaluations + evidence without ever
reading identity records (INV-006).

Both are tenant-owned (organization_id) so every query routes through a
`TenantScopedRepository`. Models never cross the API boundary — schemas.py does.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Candidate(Base):
    """A person in an organization's pipeline. **PII table** — the AI never reads this
    directly. One identity record per (organization, email), reused across campaigns."""

    __tablename__ = "candidates"
    __table_args__ = (UniqueConstraint("organization_id", "email", name="uq_candidates_org_email"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    # A pointer to the résumé in object storage — NOT the file, and never fed to the AI
    # directly. Nullable: a candidate can be added before (or without) a résumé.
    resume_object_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )


class CandidateEvaluation(Base):
    """A candidate's participation in one campaign — the **AI-visible** record. Holds no
    PII; references the candidate by id. One per (campaign, candidate)."""

    __tablename__ = "candidate_evaluations"
    __table_args__ = (
        UniqueConstraint("campaign_id", "candidate_id", name="uq_evaluation_campaign_candidate"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    # Denormalized tenant owner so isolation is uniform (tenant id on everything).
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("campaigns.id"), nullable=False, index=True
    )
    candidate_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("candidates.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    # Set once when the work sample is submitted (authoritative submission fact, Story 4.5).
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )
