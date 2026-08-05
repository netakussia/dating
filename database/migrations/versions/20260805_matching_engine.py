"""Add persistent recommendation view events for matching analytics.

Revision ID: 20260805_matching_engine
Revises:
Create Date: 2026-08-05
"""

import sqlalchemy as sa
from alembic import op

revision = "20260805_matching_engine"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "recommendation_views",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("viewer_id", sa.BigInteger(), nullable=False),
        sa.Column("candidate_id", sa.BigInteger(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["viewer_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recommendation_views_viewer_created", "recommendation_views", ["viewer_id", "created_at"])
    op.create_index("ix_recommendation_views_candidate_created", "recommendation_views", ["candidate_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_recommendation_views_candidate_created", table_name="recommendation_views")
    op.drop_index("ix_recommendation_views_viewer_created", table_name="recommendation_views")
    op.drop_table("recommendation_views")
