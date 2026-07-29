"""Persisted HiringDecision — the accountable human act at the end of the workflow.

**AI proposes; a human decides; the system records both, separately.** A decision is its
own aggregate: it *references* the immutable Evaluation that informed it (by id) but never
copies or mutates it, and the Evaluation is completely unaware of decisions. It is
**append-only** — a change of mind is a NEW row, so the full decision history survives
(this is what Story 6.3's audit/history reads). No update or delete path exists.

`evaluation_id` is nullable on purpose: the human is sovereign and may decide even where no
AI evaluation was run — AI is advisory, never a gate on the recruiter's authority to decide.
No candidate PII is stored here (the candidate is referenced by CandidateEvaluation id).
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class HiringDecision(Base):
    __tablename__ = "hiring_decisions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    candidate_evaluation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("candidate_evaluations.id"), nullable=False, index=True
    )
    # The exact Evaluation run that informed this decision (nullable — a decision can be
    # made without an AI evaluation). A reference only; the Evaluation is never mutated.
    evaluation_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("evaluations.id"), nullable=True
    )
    # Monotonic per candidate_evaluation (1, 2, 3, …) — the reliable "latest" ordering,
    # independent of clock granularity. Mirrors Evaluation.run_number.
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Who made the accountable decision (a real user, from the verified token).
    decided_by_user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
