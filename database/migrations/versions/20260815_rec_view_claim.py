"""Prevent duplicate recommendation delivery during concurrent queue rebuilds.

Revision ID: 20260815_rec_view_claim
Revises: 20260808_unlock_photo_cases
Create Date: 2026-08-15
"""

from alembic import op
from sqlalchemy import inspect, text

revision = "20260815_rec_view_claim"
down_revision = "20260808_unlock_photo_cases"
branch_labels = None
depends_on = None

CONSTRAINT_NAME = "uq_recommendation_views_viewer_candidate"


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    constraints = inspector.get_unique_constraints("recommendation_views")
    if any(set(item.get("column_names") or ()) == {"viewer_id", "candidate_id"} for item in constraints):
        return

    if bind.dialect.name == "postgresql":
        op.execute(
            text(
                """
                DELETE FROM recommendation_views older
                USING recommendation_views newer
                WHERE older.viewer_id = newer.viewer_id
                  AND older.candidate_id = newer.candidate_id
                  AND (older.created_at, older.id) > (newer.created_at, newer.id)
                """
            )
        )
    op.create_unique_constraint(CONSTRAINT_NAME, "recommendation_views", ["viewer_id", "candidate_id"])


def downgrade() -> None:
    bind = op.get_bind()
    constraints = inspect(bind).get_unique_constraints("recommendation_views")
    if any(item.get("name") == CONSTRAINT_NAME for item in constraints):
        op.drop_constraint(CONSTRAINT_NAME, "recommendation_views", type_="unique")
