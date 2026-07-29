"""create candidates and candidate_evaluations

Revision ID: 0006
Revises: 0005
Create Date: 2026-07-28

Purpose:
Adds candidate intake (Story 3.1), separating identity from evaluation:
- `candidates` = the PII table (name, email, résumé pointer), owned by the org, one
  record per (organization, email). The AI never reads this directly (INV-006).
- `candidate_evaluations` = the AI-visible join of a candidate to a campaign, holding no
  PII and referencing the candidate by id; one per (campaign, candidate). Denormalizes
  organization_id so every tenant-owned query filters uniformly. Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "candidates",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("resume_object_key", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_candidates_organization_id", "candidates", ["organization_id"])
    op.create_index("ix_candidates_email", "candidates", ["email"])
    op.create_unique_constraint(
        "uq_candidates_org_email", "candidates", ["organization_id", "email"]
    )

    op.create_table(
        "candidate_evaluations",
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
        sa.Column(
            "candidate_id", sa.String(length=36), sa.ForeignKey("candidates.id"), nullable=False
        ),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_candidate_evaluations_organization_id", "candidate_evaluations", ["organization_id"]
    )
    op.create_index(
        "ix_candidate_evaluations_campaign_id", "candidate_evaluations", ["campaign_id"]
    )
    op.create_index(
        "ix_candidate_evaluations_candidate_id", "candidate_evaluations", ["candidate_id"]
    )
    op.create_unique_constraint(
        "uq_evaluation_campaign_candidate",
        "candidate_evaluations",
        ["campaign_id", "candidate_id"],
    )


def downgrade() -> None:
    op.drop_table("candidate_evaluations")
    op.drop_table("candidates")
