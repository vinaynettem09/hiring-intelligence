"""create evidence and add candidate_evaluations.submitted_at

Revision ID: 0011
Revises: 0010
Create Date: 2026-07-28

Purpose:
Story 4.5 — final submission. Adds:
- evidence: the immutable, PII-free candidate-authored fact created at submission. It
  snapshots the submitted response text (a copy, not a pointer) with provenance
  (source_type). Unique (candidate_evaluation_id, work_sample_task_id) = DB backstop
  against duplicate submission. Append-only (no update/delete path).
- candidate_evaluations.submitted_at: the authoritative submission timestamp (status
  also moves to 'submitted'). Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "candidate_evaluations",
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "evidence",
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
        sa.Column(
            "work_sample_task_id",
            sa.String(length=36),
            sa.ForeignKey("work_sample_tasks.id"),
            nullable=False,
        ),
        sa.Column("response_text", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_evidence_organization_id", "evidence", ["organization_id"])
    op.create_index("ix_evidence_candidate_evaluation_id", "evidence", ["candidate_evaluation_id"])
    op.create_index("ix_evidence_work_sample_task_id", "evidence", ["work_sample_task_id"])
    op.create_unique_constraint(
        "uq_evidence_eval_task", "evidence", ["candidate_evaluation_id", "work_sample_task_id"]
    )


def downgrade() -> None:
    op.drop_table("evidence")
    op.drop_column("candidate_evaluations", "submitted_at")
