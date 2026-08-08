"""Create the full application schema from the current SQLAlchemy metadata.

Revision ID: 20260808_schema_baseline
Revises:
Create Date: 2026-08-08
"""

from alembic import op

import models  # noqa: F401
from database.base import Base

revision = "20260808_schema_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    # Keep rollback safe and non-destructive: the baseline only establishes the current schema.
    pass
