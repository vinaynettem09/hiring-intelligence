"""Persisted Evaluation — the **immutable, evidence-grounded AI proposal**.

An `Evaluation` is a durable historical fact produced from `Frozen Role Profile + Frozen
Work Sample + Immutable Evidence` by the intelligence pipeline. It is **not** a
`CandidateEvaluation` (the candidate's participation lifecycle) and **not** a
`HiringDecision`. AI proposes; a human decides.

Immutability is structural: these rows are inserted and never updated or deleted. A
**rerun** creates a *new* `Evaluation` (next `run_number`) and never touches prior runs —
`UNIQUE(candidate_evaluation_id, run_number)` is the DB backstop, and
`UNIQUE(candidate_evaluation_id, idempotency_key)` stops a double-click creating a
duplicate run. Provenance is flattened into columns so a run stays reconstructable even
after versions move on; `input_fingerprint` is a SHA-256 over the PII-safe input.

No candidate PII is stored anywhere here (competency assessments + citations reference
Evidence by id — the referenced Evidence is itself PII-free and immutable).
"""

from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Evaluation(Base):
    __tablename__ = "evaluations"
    __table_args__ = (
        # One run number per candidate evaluation — the backstop against a duplicate /
        # racing run. A rerun takes the next number; nothing is ever overwritten.
        UniqueConstraint("candidate_evaluation_id", "run_number", name="uq_evaluation_run"),
        # Idempotency: the same key for the same candidate evaluation resolves to the same
        # run (a browser retry never silently creates run 2). NULL keys are unconstrained.
        UniqueConstraint(
            "candidate_evaluation_id", "idempotency_key", name="uq_evaluation_idempotency"
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    candidate_evaluation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("candidate_evaluations.id"), nullable=False, index=True
    )
    run_number: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # --- the validated proposal (never raw provider output) ---
    recommendation: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)  # PLATFORM confidence
    confidence_rationale: Mapped[str] = mapped_column(Text, nullable=False)
    escalation_reason: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # Stored as JSON: [{text, citations:[{evidence_id, task_id}]}]. Typed as dict rows (not
    # list[str]) so the ORM annotation matches what is actually persisted and read back.
    strengths: Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False)
    concerns: Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False)

    # --- evidence coverage (drives confidence + recruiter transparency) ---
    coverage_competencies_total: Mapped[int] = mapped_column(Integer, nullable=False)
    coverage_competencies_assessed: Mapped[int] = mapped_column(Integer, nullable=False)
    coverage_tasks_total: Mapped[int] = mapped_column(Integer, nullable=False)
    coverage_tasks_with_evidence: Mapped[int] = mapped_column(Integer, nullable=False)

    # --- durable provenance (flattened so a run stays reconstructable) ---
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(128), nullable=False)
    model_version: Mapped[str] = mapped_column(String(64), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(64), nullable=False)
    input_schema_version: Mapped[str] = mapped_column(String(64), nullable=False)
    output_schema_version: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence_algorithm_version: Mapped[str] = mapped_column(String(64), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    input_fingerprint: Mapped[str] = mapped_column(String(80), nullable=False, index=True)

    # --- operational token accounting (nullable; the mock reports none) ---
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    assessments: Mapped[list["EvaluationCompetencyAssessment"]] = relationship(
        cascade="all, delete-orphan",
        order_by="EvaluationCompetencyAssessment.display_order",
    )


class EvaluationCompetencyAssessment(Base):
    """A grounded, per-competency observation belonging to one Evaluation. Immutable."""

    __tablename__ = "evaluation_competency_assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    evaluation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("evaluations.id"), nullable=False, index=True
    )
    competency: Mapped[str] = mapped_column(String(120), nullable=False)
    assessment: Mapped[str] = mapped_column(Text, nullable=False)
    provider_signal: Mapped[float | None] = mapped_column(Float, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)

    citations: Mapped[list["EvaluationCitation"]] = relationship(cascade="all, delete-orphan")


class EvaluationCitation(Base):
    """A durable link from an assessment to the immutable Evidence (and its frozen task)
    that supports it. Storing ids (not display text) is what makes historical explanation
    safe: the referenced Evidence never changes. Grounding was already validated before
    persistence; the FKs are the persistence-level backstop."""

    __tablename__ = "evaluation_citations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    evaluation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("evaluations.id"), nullable=False, index=True
    )
    competency_assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("evaluation_competency_assessments.id"), nullable=False, index=True
    )
    evidence_id: Mapped[str] = mapped_column(String(36), ForeignKey("evidence.id"), nullable=False)
    work_sample_task_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("work_sample_tasks.id"), nullable=False
    )
