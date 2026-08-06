"""Align create_all legacy installations with current profile and trust metadata.

Revision ID: 20260807_legacy_schema_alignment
Revises: 20260806_photo_safety_cache
"""

import sqlalchemy as sa
from alembic import op

revision = "20260807_legacy_schema_alignment"
down_revision = "20260806_photo_safety_cache"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE profiles SET photo_file_ids = '[]'::json WHERE photo_file_ids IS NULL")
    op.execute("UPDATE profiles SET locale = 'ru' WHERE locale IS NULL")
    op.execute("UPDATE profiles SET extra_data = '{}'::json WHERE extra_data IS NULL")
    op.alter_column("profiles", "photo_file_ids", existing_type=sa.JSON(), nullable=False)
    op.alter_column("profiles", "locale", existing_type=sa.String(length=8), nullable=False)
    op.alter_column("profiles", "extra_data", existing_type=sa.JSON(), nullable=False)
    op.create_index("ix_profiles_moderation_status", "profiles", ["moderation_status"])
    op.create_index("ix_profiles_verification_status", "profiles", ["verification_status"])
    op.create_index("ix_users_trust_score", "users", ["trust_score"])
    op.create_unique_constraint("uq_reports_reporter_target", "reports", ["reporter_id", "target_user_id"])


def downgrade() -> None:
    op.drop_constraint("uq_reports_reporter_target", "reports", type_="unique")
    op.drop_index("ix_users_trust_score", table_name="users")
    op.drop_index("ix_profiles_verification_status", table_name="profiles")
    op.drop_index("ix_profiles_moderation_status", table_name="profiles")
    op.alter_column("profiles", "extra_data", existing_type=sa.JSON(), nullable=True)
    op.alter_column("profiles", "locale", existing_type=sa.String(length=8), nullable=True)
    op.alter_column("profiles", "photo_file_ids", existing_type=sa.JSON(), nullable=True)
