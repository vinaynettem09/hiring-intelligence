"""create structured_work_samples and work_sample_tasks

Revision ID: 0009
Revises: 0008
Create Date: 2026-07-28

Purpose:
Story 4.3 — the Structured Work Sample: the evidence-collection instrument for a
campaign. One work sample per campaign; ordered tasks, each mapping to ≥1 campaign
competency (by name) with a recruiter-facing evidence_intent. No scoring/AI here.
Editable while the campaign is a draft; frozen once active. Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "structured_work_samples",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "campaign_id", sa.String(length=36), sa.ForeignKey("campaigns.id"), nullable=False
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("introduction", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_structured_work_samples_organization_id",
        "structured_work_samples",
        ["organization_id"],
    )
    op.create_unique_constraint(
        "uq_structured_work_samples_campaign", "structured_work_samples", ["campaign_id"]
    )

    op.create_table(
        "work_sample_tasks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column(
            "work_sample_id",
            sa.String(length=36),
            sa.ForeignKey("structured_work_samples.id"),
            nullable=False,
        ),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=True),
        sa.Column("evidence_intent", sa.Text(), nullable=False),
        sa.Column("task_type", sa.String(length=32), nullable=False),
        sa.Column("competencies", postgresql.JSONB(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("expected_effort_minutes", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_work_sample_tasks_organization_id", "work_sample_tasks", ["organization_id"]
    )
    op.create_index(
        "ix_work_sample_tasks_work_sample_id", "work_sample_tasks", ["work_sample_id"]
    )


def downgrade() -> None:
    op.drop_table("work_sample_tasks")
    op.drop_table("structured_work_samples")
