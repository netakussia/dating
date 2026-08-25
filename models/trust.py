import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class VerificationDecision(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RETAKE_REQUESTED = "RETAKE_REQUESTED"


class ModerationCaseType(str, enum.Enum):
    REPORT_THRESHOLD = "REPORT_THRESHOLD"
    NSFW = "NSFW"
    NO_FACE = "NO_FACE"


class ModerationCaseStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class VerificationRequest(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "verification_requests"
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    video_file_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[VerificationDecision] = mapped_column(
        Enum(VerificationDecision), default=VerificationDecision.PENDING, index=True
    )
    assigned_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    admin_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)


class ModerationCase(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "moderation_cases"
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    case_type: Mapped[ModerationCaseType] = mapped_column(Enum(ModerationCaseType), index=True)
    status: Mapped[ModerationCaseStatus] = mapped_column(
        Enum(ModerationCaseStatus), default=ModerationCaseStatus.PENDING, index=True
    )
    assigned_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)


class PhotoModeration(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "photo_moderations"
    __table_args__ = (UniqueConstraint("user_id", "content_hash", name="uq_photo_moderations_user_hash"),)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    photo_file_id: Mapped[str] = mapped_column(String(255), index=True)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    provider: Mapped[str] = mapped_column(String(64), default="heuristic")
    nsfw_score: Mapped[float] = mapped_column(Float, default=0.0)
    face_detected: Mapped[bool] = mapped_column(default=True)


class TrustScoreEvent(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "trust_score_events"
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    delta: Mapped[int] = mapped_column()
    reason: Mapped[str] = mapped_column(String(64), index=True)
    reference_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reference_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
