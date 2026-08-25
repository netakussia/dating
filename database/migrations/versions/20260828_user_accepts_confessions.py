"""Add accepts_confessions field to User model.

Revision ID: 20260828_user_confessions
Revises: 20260827_confession_key
Create Date: 2026-08-28
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260828_user_confessions"
down_revision = "20260827_confession_key"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    
    if "accepts_confessions" not in existing_columns:
        with op.batch_alter_table("users") as batch:
            batch.add_column(
                sa.Column("accepts_confessions", sa.Boolean(), nullable=False, server_default="true")
            )
        
        # Create index for the new column
        existing_indexes = {index["name"] for index in inspector.get_indexes("users")}
        if "ix_users_accepts_confessions" not in existing_indexes:
            op.create_index("ix_users_accepts_confessions", "users", ["accepts_confessions"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("users")}
    
    if "ix_users_accepts_confessions" in existing_indexes:
        op.drop_index("ix_users_accepts_confessions", table_name="users")
    
    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    if "accepts_confessions" in existing_columns:
        with op.batch_alter_table("users") as batch:
            batch.drop_column("accepts_confessions")
