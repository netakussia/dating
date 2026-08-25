"""Align create_all legacy installations with current profile and trust metadata.

Revision ID: 20260807_legacy_schema_alignment
Revises: 20260806_photo_safety_cache
"""


revision = "20260807_legacy_schema_alignment"
down_revision = "20260806_photo_safety_cache"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
