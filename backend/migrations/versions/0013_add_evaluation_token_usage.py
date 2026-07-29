"""add evaluations.input_tokens / output_tokens

Revision ID: 0013
Revises: 0012
Create Date: 2026-07-28

Purpose:
Story 5.3 — real provider integration. Records operational token usage returned by the
provider on a successful Evaluation run (nullable; the deterministic mock reports none).
This is operational/cost metadata only — never part of any candidate judgment. Cost is
NOT stored here: token counts + provider/model provenance are enough to derive estimated
cost later from a versioned pricing table, keeping pricing out of the Evaluation domain.
"""

import sqlalchemy as sa
from alembic import op

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("evaluations", sa.Column("input_tokens", sa.Integer(), nullable=True))
    op.add_column("evaluations", sa.Column("output_tokens", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("evaluations", "output_tokens")
    op.drop_column("evaluations", "input_tokens")
