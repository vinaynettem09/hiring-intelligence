"""create campaigns

Revision ID: 0005
Revises: 0004
Create Date: 2026-07-27

Purpose:
Adds the campaigns table (Story 2.1) — the first tenant-owned business resource. A
campaign belongs to exactly one organization (organization_id = the tenant, INV-001)
and is born `draft`. role_profile (competencies + hiring bar) is stored as JSONB so
calibration can evolve while the campaign is draft without a schema change. Hand-
written and readable.
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "campaigns",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "organization_id",
            sa.String(length=36),
            sa.ForeignKey("organizations.id"),
            nullable=False,
        ),
        sa.Column("role_title", sa.String(length=255), nullable=False),
        sa.Column("role_profile", postgresql.JSONB(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_campaigns_organization_id", "campaigns", ["organization_id"])


def downgrade() -> None:
    op.drop_index("ix_campaigns_organization_id", table_name="campaigns")
    op.drop_table("campaigns")
