"""Add the confession submission key used for idempotent deep-link creation.

Revision ID: 20260827_confession_key
Revises: 20260815_rec_view_claim
Create Date: 2026-08-27
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260827_confession_key"
down_revision = "20260815_rec_view_claim"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("confessions")}
    if "submission_key" not in existing_columns:
        with op.batch_alter_table("confessions") as batch:
            batch.add_column(sa.Column("submission_key", sa.String(length=64), nullable=True))

    existing_indexes = {index["name"] for index in inspector.get_indexes("confessions")}
    if "ix_confessions_submission_key" not in existing_indexes:
        op.create_index("ix_confessions_submission_key", "confessions", ["submission_key"], unique=True)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("confessions")}
    if "ix_confessions_submission_key" in existing_indexes:
        op.drop_index("ix_confessions_submission_key", table_name="confessions")

    existing_columns = {column["name"] for column in inspector.get_columns("confessions")}
    if "submission_key" in existing_columns:
        with op.batch_alter_table("confessions") as batch:
            batch.drop_column("submission_key")
