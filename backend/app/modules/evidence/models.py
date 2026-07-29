"""Evidence — the immutable, candidate-authored fact produced at submission.

This is the ONLY candidate-response source Epic 5's AI is authorized to evaluate
(INV-012). It **snapshots** the submitted text (a copy, not a pointer to the mutable
`WorkSampleResponse`), so the historical fact survives even if working tables change.
It is append-only: no update/delete path exists. It carries **no candidate PII** — the
evaluation pipeline reads it (plus the frozen task + role profile) without joining
`Candidate`. `candidate_evaluation_id` is an internal pseudonymous link, not identity.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Evidence(Base):
    __tablename__ = "evidence"
    __table_args__ = (
        # One evidence row per (evaluation, task) — the DB backstop against duplicate
        # submission, independent of any service-level "already submitted?" check.
        UniqueConstraint(
            "candidate_evaluation_id", "work_sample_task_id", name="uq_evidence_eval_task"
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
    response_text: Mapped[str] = mapped_column(Text, nullable=False)  # snapshot, verbatim
    source_type: Mapped[str] = mapped_column(String(32), nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
