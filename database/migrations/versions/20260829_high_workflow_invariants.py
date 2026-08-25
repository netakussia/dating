"""Add report evidence and active-workflow uniqueness invariants.

Revision ID: 20260829_high_workflow_invariants
Revises: 20260828_report_assigned
Create Date: 2026-08-29
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260829_high_workflow_invariants"
down_revision = "20260828_report_assigned"
branch_labels = None
depends_on = None


def _fail_if_active_duplicates(bind, table: str, group_sql: str, where_sql: str) -> None:
    count = bind.execute(
        sa.text(
            f"SELECT count(*) FROM (SELECT {group_sql} FROM {table} "
            f"WHERE {where_sql} GROUP BY {group_sql} HAVING count(*) > 1) duplicates"
        )
    ).scalar_one()
    if count:
        raise RuntimeError(
            f"{table} contains {count} active duplicate group(s); resolve them manually before applying this migration."
        )


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    report_columns = {column["name"] for column in inspector.get_columns("reports")}
    if "evidence_snapshot" not in report_columns:
        op.add_column("reports", sa.Column("evidence_snapshot", sa.JSON(), nullable=True))

    _fail_if_active_duplicates(bind, "appeals", "user_id", "status = 'PENDING'")
    _fail_if_active_duplicates(bind, "verification_requests", "user_id", "status = 'PENDING'")
    _fail_if_active_duplicates(
        bind,
        "moderation_cases",
        "user_id, case_type, COALESCE(source_id, '')",
        "status IN ('PENDING', 'IN_PROGRESS')",
    )

    indexes = {index["name"] for index in inspector.get_indexes("appeals")}
    if "uq_appeals_one_pending_per_user" not in indexes:
        op.create_index(
            "uq_appeals_one_pending_per_user",
            "appeals",
            ["user_id"],
            unique=True,
            postgresql_where=sa.text("status = 'PENDING'"),
        )

    indexes = {index["name"] for index in inspector.get_indexes("verification_requests")}
    if "uq_verification_requests_one_pending_per_user" not in indexes:
        op.create_index(
            "uq_verification_requests_one_pending_per_user",
            "verification_requests",
            ["user_id"],
            unique=True,
            postgresql_where=sa.text("status = 'PENDING'"),
        )

    indexes = {index["name"] for index in inspector.get_indexes("moderation_cases")}
    if "uq_moderation_cases_one_active_event" not in indexes:
        op.execute(
            "CREATE UNIQUE INDEX uq_moderation_cases_one_active_event "
            "ON moderation_cases (user_id, case_type, COALESCE(source_id, '')) "
            "WHERE status IN ('PENDING', 'IN_PROGRESS')"
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    for table, index in (
        ("moderation_cases", "uq_moderation_cases_one_active_event"),
        ("verification_requests", "uq_verification_requests_one_pending_per_user"),
        ("appeals", "uq_appeals_one_pending_per_user"),
    ):
        if index in {item["name"] for item in inspector.get_indexes(table)}:
            op.drop_index(index, table_name=table)
    if "evidence_snapshot" in {column["name"] for column in inspector.get_columns("reports")}:
        op.drop_column("reports", "evidence_snapshot")
