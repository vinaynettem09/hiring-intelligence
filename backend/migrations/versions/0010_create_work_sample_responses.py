"""create work_sample_responses

Revision ID: 0010
Revises: 0009
Create Date: 2026-07-28

Purpose:
Story 4.4 — candidate DRAFT responses (mutable working state, NOT Evidence). One row per
(candidate_evaluation, task); upserted, so autosave never duplicates. Evidence (the
immutable submitted snapshot) is a separate Story 4.5 concern. Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "work_sample_responses",
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
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_work_sample_responses_organization_id", "work_sample_responses", ["organization_id"]
    )
    op.create_index(
        "ix_work_sample_responses_candidate_evaluation_id",
        "work_sample_responses",
        ["candidate_evaluation_id"],
    )
    op.create_unique_constraint(
        "uq_response_eval_task",
        "work_sample_responses",
        ["candidate_evaluation_id", "work_sample_task_id"],
    )


def downgrade() -> None:
    op.drop_table("work_sample_responses")
