"""Release stale locks left by already resolved photo moderation cases.

Revision ID: 20260808_unlock_photo_cases
Revises: 20260807_legacy_schema_alignment
"""

from alembic import op

revision = "20260808_unlock_photo_cases"
down_revision = "20260807_legacy_schema_alignment"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE profiles AS profile
        SET moderation_locked = FALSE
        WHERE profile.moderation_locked = TRUE
          AND profile.moderation_status = 'CLEAR'
          AND EXISTS (
              SELECT 1 FROM moderation_cases AS resolved_case
              WHERE resolved_case.user_id = profile.user_id
                AND resolved_case.case_type IN ('NSFW', 'NO_FACE')
                AND resolved_case.status = 'RESOLVED'
          )
          AND NOT EXISTS (
              SELECT 1 FROM moderation_cases AS pending_case
              WHERE pending_case.user_id = profile.user_id
                AND pending_case.case_type IN ('NSFW', 'NO_FACE')
                AND pending_case.status = 'PENDING'
          )
        """
    )


def downgrade() -> None:
    # The previous lock state cannot be inferred after a successful reconciliation.
    pass
