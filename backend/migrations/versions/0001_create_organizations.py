"""create organizations

Revision ID: 0001
Revises:
Create Date: 2026-07-23

Purpose:
Introduces the tenant-root entity required for recruiter signup (Story 1.1).
There is no tenant_id column because an Organization itself *defines* the tenant
boundary — every other table will reference it. Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("organizations")
