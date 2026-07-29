"""create hiring_decisions

Revision ID: 0014
Revises: 0013
Create Date: 2026-07-29

Purpose:
Story 6.2 — the accountable HUMAN decision. Append-only (a change of mind is a new row),
tenant-owned. References the immutable Evaluation run that informed it (nullable — a
decision can be made without an AI evaluation; AI is advisory, never a gate). The
Evaluation is never modified by a decision. Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "hiring_decisions",
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
        # Nullable: a decision may be made without an AI evaluation (human is sovereign).
        sa.Column(
            "evaluation_id",
            sa.String(length=36),
            sa.ForeignKey("evaluations.id"),
            nullable=True,
        ),
        # Monotonic per candidate_evaluation — the reliable "latest" ordering.
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column(
            "decided_by_user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_hiring_decisions_organization_id", "hiring_decisions", ["organization_id"]
    )
    op.create_index(
        "ix_hiring_decisions_candidate_evaluation_id",
        "hiring_decisions",
        ["candidate_evaluation_id"],
    )


def downgrade() -> None:
    op.drop_table("hiring_decisions")
