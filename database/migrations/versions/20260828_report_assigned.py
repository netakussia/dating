"""Add assigned_to and assigned_at fields to Report model.

Revision ID: 20260828_report_assigned
Revises: 20260828_verif_assigned
Create Date: 2026-08-28
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260828_report_assigned"
down_revision = "20260828_verif_assigned"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("reports")}
    
    if "assigned_to" not in existing_columns:
        with op.batch_alter_table("reports") as batch:
            batch.add_column(
                sa.Column("assigned_to", sa.BigInteger(), nullable=True)
            )
    
    if "assigned_at" not in existing_columns:
        with op.batch_alter_table("reports") as batch:
            batch.add_column(
                sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True)
            )
    
    # Create index for assigned_to
    existing_indexes = {index["name"] for index in inspector.get_indexes("reports")}
    if "ix_reports_assigned_to" not in existing_indexes:
        op.create_index("ix_reports_assigned_to", "reports", ["assigned_to"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("reports")}
    
    if "ix_reports_assigned_to" in existing_indexes:
        op.drop_index("ix_reports_assigned_to", table_name="reports")
    
    existing_columns = {column["name"] for column in inspector.get_columns("reports")}
    if "assigned_to" in existing_columns or "assigned_at" in existing_columns:
        with op.batch_alter_table("reports") as batch:
            if "assigned_to" in existing_columns:
                batch.drop_column("assigned_to")
            if "assigned_at" in existing_columns:
                batch.drop_column("assigned_at")
