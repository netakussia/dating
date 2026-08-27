"""Add the fail-soft ML moderation case type.

Revision ID: 20260830_ml_fallback
Revises: 20260829_workflow_invariants
Create Date: 2026-08-30
"""

from alembic import op

revision = "20260830_ml_fallback"
down_revision = "20260829_workflow_invariants"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # PostgreSQL enum values must be committed before they can be used. The
    # migration runner applies this revision in its own transaction, so the
    # value is available to application transactions immediately afterwards.
    op.execute("ALTER TYPE moderationcasetype ADD VALUE IF NOT EXISTS 'ML_PROVIDER_FALLBACK'")


def downgrade() -> None:
    # PostgreSQL cannot safely remove an enum value without rebuilding all
    # dependent columns. Keep this downgrade intentionally non-destructive.
    pass
