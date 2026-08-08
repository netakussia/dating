"""Add extensible Trust System records and profile/user trust state.

Revision ID: 20260805_trust_system
Revises: 20260805_matching_engine
Create Date: 2026-08-05
"""

import sqlalchemy as sa
from alembic import op

revision = "20260805_trust_system"
down_revision = "20260805_matching_engine"
branch_labels = None
depends_on = None

verificationstatus = sa.Enum("UNVERIFIED", "PENDING", "VERIFIED", "REJECTED", name="verificationstatus")
moderationstatus = sa.Enum("CLEAR", "UNDER_REVIEW", name="moderationstatus")
verificationdecision = sa.Enum("PENDING", "APPROVED", "REJECTED", "RETAKE_REQUESTED", name="verificationdecision")
moderationcasetype = sa.Enum("REPORT_THRESHOLD", "NSFW", "NO_FACE", name="moderationcasetype")
moderationcasestatus = sa.Enum("PENDING", "RESOLVED", name="moderationcasestatus")


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
