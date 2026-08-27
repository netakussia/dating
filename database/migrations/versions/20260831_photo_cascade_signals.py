"""Persist all photo moderation cascade signals for safe cache reuse.

Revision ID: 20260831_photo_cascade_signals
Revises: 20260830_ml_fallback
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260831_photo_cascade_signals"
down_revision = "20260830_ml_fallback"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    
    columns = {column["name"] for column in inspector.get_columns("photo_moderations")}
    
    if "face_score" not in columns:
        op.add_column("photo_moderations", sa.Column("face_score", sa.Float(), nullable=False, server_default="0"))
    if "face_count" not in columns:
        op.add_column("photo_moderations", sa.Column("face_count", sa.Integer(), nullable=False, server_default="0"))
    if "human_score" not in columns:
        op.add_column("photo_moderations", sa.Column("human_score", sa.Float(), nullable=False, server_default="0"))
    if "fallback_reason" not in columns:
        op.add_column("photo_moderations", sa.Column("fallback_reason", sa.String(length=64), nullable=True))


def downgrade() -> None:
    op.drop_column("photo_moderations", "fallback_reason")
    op.drop_column("photo_moderations", "human_score")
    op.drop_column("photo_moderations", "face_count")
    op.drop_column("photo_moderations", "face_score")
