"""Add normalized image hash cache for photo safety assessments.

Revision ID: 20260806_photo_safety_cache
Revises: 20260805_trust_system
"""


revision = "20260806_photo_safety_cache"
down_revision = "20260805_trust_system"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
