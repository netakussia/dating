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
    verificationstatus.create(op.get_bind(), checkfirst=True)
    moderationstatus.create(op.get_bind(), checkfirst=True)
    verificationdecision.create(op.get_bind(), checkfirst=True)
    moderationcasetype.create(op.get_bind(), checkfirst=True)
    moderationcasestatus.create(op.get_bind(), checkfirst=True)
    op.add_column("users", sa.Column("trust_score", sa.Integer(), nullable=False, server_default="95"))
    op.add_column("profiles", sa.Column("verification_status", verificationstatus, nullable=False, server_default="UNVERIFIED"))
    op.add_column("profiles", sa.Column("moderation_status", moderationstatus, nullable=False, server_default="CLEAR"))
    op.create_unique_constraint("uq_reports_reporter_target", "reports", ["reporter_id", "target_user_id"])
    op.add_column("admin_logs", sa.Column("target_type", sa.String(32), nullable=True))
    op.add_column("admin_logs", sa.Column("target_id", sa.String(64), nullable=True))
    op.add_column("admin_logs", sa.Column("metadata_json", sa.JSON(), nullable=False, server_default="{}"))
    op.create_table("verification_requests", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("video_file_id", sa.String(255), nullable=False), sa.Column("status", verificationdecision, nullable=False, server_default="PENDING"), sa.Column("admin_id", sa.BigInteger(), nullable=True), sa.Column("comment", sa.Text(), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")))
    op.create_index("ix_verification_requests_user_id", "verification_requests", ["user_id"])
    op.create_index("ix_verification_requests_status", "verification_requests", ["status"])
    op.create_table("moderation_cases", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("case_type", moderationcasetype, nullable=False), sa.Column("status", moderationcasestatus, nullable=False, server_default="PENDING"), sa.Column("source_id", sa.String(64)), sa.Column("details", sa.Text()), sa.Column("admin_id", sa.BigInteger()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")))
    op.create_index("ix_moderation_cases_user_id", "moderation_cases", ["user_id"])
    op.create_index("ix_moderation_cases_case_type", "moderation_cases", ["case_type"])
    op.create_index("ix_moderation_cases_status", "moderation_cases", ["status"])
    op.create_table("photo_moderations", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("photo_file_id", sa.String(255), nullable=False), sa.Column("provider", sa.String(64), nullable=False), sa.Column("nsfw_score", sa.Float(), nullable=False), sa.Column("face_detected", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")))
    op.create_table("trust_score_events", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("delta", sa.Integer(), nullable=False), sa.Column("reason", sa.String(64), nullable=False), sa.Column("reference_type", sa.String(32)), sa.Column("reference_id", sa.String(64)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")))


def downgrade() -> None:
    for table in ("trust_score_events", "photo_moderations", "moderation_cases", "verification_requests"):
        op.drop_table(table)
    op.drop_column("admin_logs", "metadata_json")
    op.drop_column("admin_logs", "target_id")
    op.drop_column("admin_logs", "target_type")
    op.drop_constraint("uq_reports_reporter_target", "reports", type_="unique")
    op.drop_column("profiles", "moderation_status")
    op.drop_column("profiles", "verification_status")
    op.drop_column("users", "trust_score")
