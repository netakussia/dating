"""Release stale locks left by already resolved photo moderation cases.

Revision ID: 20260808_unlock_photo_cases
Revises: 20260807_legacy_schema_alignment
"""


revision = "20260808_unlock_photo_cases"
down_revision = "20260807_legacy_schema_alignment"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
