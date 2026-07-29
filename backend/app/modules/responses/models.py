"""Candidate draft response model.

`WorkSampleResponse` is **mutable candidate working state** — what the candidate is
currently writing. It is NOT Evidence. Evidence is the immutable, consent-gated snapshot
created only at final submission (Story 4.5); nothing here carries scores, AI output, or
a "submitted" status. One response per (candidate_evaluation, task); it upserts, so
autosave never accumulates a pseudo-history that AI could later consume.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class WorkSampleResponse(Base):
    __tablename__ = "work_sample_responses"
    __table_args__ = (
        UniqueConstraint(
            "candidate_evaluation_id", "work_sample_task_id", name="uq_response_eval_task"
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    candidate_evaluation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("candidate_evaluations.id"), nullable=False, index=True
    )
    work_sample_task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("work_sample_tasks.id"), nullable=False, index=True
    )
    response_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )
