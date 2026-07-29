"""create evaluations, evaluation_competency_assessments, evaluation_citations

Revision ID: 0012
Revises: 0011
Create Date: 2026-07-28

Purpose:
Story 5.2 — immutable intelligence persistence. Adds the persisted Evaluation aggregate:

- evaluations: an immutable, evidence-grounded AI *proposal* (never a HiringDecision).
  Flattened provenance columns keep a run reconstructable after versions move on;
  input_fingerprint is a SHA-256 over the PII-safe input. Two DB backstops preserve the
  core invariants without relying on app code:
    * unique(candidate_evaluation_id, run_number)     -> reruns never collide/overwrite
    * unique(candidate_evaluation_id, idempotency_key) -> a retry never creates run 2
      (NULL keys are unconstrained — a partial index on Postgres/SQLite).
- evaluation_competency_assessments: grounded per-competency observations (immutable).
- evaluation_citations: durable links from an assessment to immutable Evidence + its
  frozen work-sample task, so historical explanation stays safe (Evidence never changes).

Append-only: no update/delete paths exist in the repository. Hand-written and readable;
PostgreSQL-first (the unique/idempotency guarantees are proven against real Postgres in
tests/integration).
"""

import sqlalchemy as sa
from alembic import op

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "evaluations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "candidate_evaluation_id",
            sa.String(length=36),
            sa.ForeignKey("candidate_evaluations.id"),
            nullable=False,
        ),
        sa.Column("run_number", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
        # validated proposal
        sa.Column("recommendation", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("confidence_rationale", sa.Text(), nullable=False),
        sa.Column("escalation_reason", sa.String(length=32), nullable=True),
        sa.Column("strengths", sa.JSON(), nullable=False),
        sa.Column("concerns", sa.JSON(), nullable=False),
        # coverage
        sa.Column("coverage_competencies_total", sa.Integer(), nullable=False),
        sa.Column("coverage_competencies_assessed", sa.Integer(), nullable=False),
        sa.Column("coverage_tasks_total", sa.Integer(), nullable=False),
        sa.Column("coverage_tasks_with_evidence", sa.Integer(), nullable=False),
        # provenance (durable)
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("model_version", sa.String(length=64), nullable=False),
        sa.Column("prompt_version", sa.String(length=64), nullable=False),
        sa.Column("input_schema_version", sa.String(length=64), nullable=False),
        sa.Column("output_schema_version", sa.String(length=64), nullable=False),
        sa.Column("confidence_algorithm_version", sa.String(length=64), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("input_fingerprint", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_evaluations_organization_id", "evaluations", ["organization_id"])
    op.create_index(
        "ix_evaluations_candidate_evaluation_id", "evaluations", ["candidate_evaluation_id"]
    )
    op.create_index("ix_evaluations_input_fingerprint", "evaluations", ["input_fingerprint"])
    op.create_unique_constraint(
        "uq_evaluation_run", "evaluations", ["candidate_evaluation_id", "run_number"]
    )
    op.create_unique_constraint(
        "uq_evaluation_idempotency", "evaluations", ["candidate_evaluation_id", "idempotency_key"]
    )

    op.create_table(
        "evaluation_competency_assessments",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "evaluation_id",
            sa.String(length=36),
            sa.ForeignKey("evaluations.id"),
            nullable=False,
        ),
        sa.Column("competency", sa.String(length=120), nullable=False),
        sa.Column("assessment", sa.Text(), nullable=False),
        sa.Column("provider_signal", sa.Float(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False),
    )
    op.create_index(
        "ix_eval_assessments_organization_id",
        "evaluation_competency_assessments",
        ["organization_id"],
    )
    op.create_index(
        "ix_eval_assessments_evaluation_id",
        "evaluation_competency_assessments",
        ["evaluation_id"],
    )

    op.create_table(
        "evaluation_citations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "evaluation_id",
            sa.String(length=36),
            sa.ForeignKey("evaluations.id"),
            nullable=False,
        ),
        sa.Column(
            "competency_assessment_id",
            sa.String(length=36),
            sa.ForeignKey("evaluation_competency_assessments.id"),
            nullable=False,
        ),
        sa.Column(
            "evidence_id", sa.String(length=36), sa.ForeignKey("evidence.id"), nullable=False
        ),
        sa.Column(
            "work_sample_task_id",
            sa.String(length=36),
            sa.ForeignKey("work_sample_tasks.id"),
            nullable=False,
        ),
    )
    op.create_index(
        "ix_eval_citations_organization_id", "evaluation_citations", ["organization_id"]
    )
    op.create_index(
        "ix_eval_citations_evaluation_id", "evaluation_citations", ["evaluation_id"]
    )
    op.create_index(
        "ix_eval_citations_assessment_id",
        "evaluation_citations",
        ["competency_assessment_id"],
    )


def downgrade() -> None:
    op.drop_table("evaluation_citations")
    op.drop_table("evaluation_competency_assessments")
    op.drop_table("evaluations")
