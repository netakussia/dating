"""Add persistent recommendation view events for matching analytics.

Revision ID: 20260805_matching_engine
Revises:
Create Date: 2026-08-05
"""


revision = "20260805_matching_engine"
down_revision = "20260808_schema_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
