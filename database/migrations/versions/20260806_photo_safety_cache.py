"""Add normalized image hash cache for photo safety assessments.

Revision ID: 20260806_photo_safety_cache
Revises: 20260805_trust_system
"""

import sqlalchemy as sa
from alembic import op

revision = "20260806_photo_safety_cache"
down_revision = "20260805_trust_system"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("photo_moderations", sa.Column("content_hash", sa.String(64), nullable=True))
    op.create_index("ix_photo_moderations_content_hash", "photo_moderations", ["content_hash"])
    op.create_unique_constraint("uq_photo_moderations_user_hash", "photo_moderations", ["user_id", "content_hash"])


def downgrade() -> None:
    op.drop_constraint("uq_photo_moderations_user_hash", "photo_moderations", type_="unique")
    op.drop_index("ix_photo_moderations_content_hash", table_name="photo_moderations")
    op.drop_column("photo_moderations", "content_hash")
