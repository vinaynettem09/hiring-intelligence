"""create consents

Revision ID: 0008
Revises: 0007
Create Date: 2026-07-28

Purpose:
Story 4.2. Consent is an append-only, versioned domain fact (NOT a mutable boolean on
candidate_evaluations). Each row records a grant for one evaluation, the exact consent
version agreed to, and when; withdrawn_at supports withdrawal later without reshaping.
Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "consents",
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
        sa.Column("consent_version", sa.String(length=64), nullable=False),
        sa.Column("consented_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("withdrawn_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_consents_organization_id", "consents", ["organization_id"])
    op.create_index(
        "ix_consents_candidate_evaluation_id", "consents", ["candidate_evaluation_id"]
    )


def downgrade() -> None:
    op.drop_table("consents")
