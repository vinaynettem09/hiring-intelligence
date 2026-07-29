"""refresh token metadata

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-24

Purpose:
Adds nullable investigation metadata to refresh_tokens (last_used_at, created_ip,
created_user_agent). Added now — while cheap — so suspicious-activity analysis is
possible later without a data-losing migration. Only last_used_at is populated
today (on refresh). Hand-written and readable.
"""

import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "refresh_tokens", sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("refresh_tokens", sa.Column("created_ip", sa.String(length=45), nullable=True))
    op.add_column(
        "refresh_tokens", sa.Column("created_user_agent", sa.String(length=512), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("refresh_tokens", "created_user_agent")
    op.drop_column("refresh_tokens", "created_ip")
    op.drop_column("refresh_tokens", "last_used_at")
