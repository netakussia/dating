import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class ConfessionStatus(str, enum.Enum):
    DELIVERED = "DELIVERED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class Confession(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "confessions"
    sender_hash: Mapped[str] = mapped_column(String(64), index=True)
    submission_key: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, index=True)
    recipient_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    target_username: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    # Pending deep links are tied to a mutable Telegram username.  They must
    # expire before that username can be reassigned to another account.
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[ConfessionStatus] = mapped_column(Enum(ConfessionStatus), default=ConfessionStatus.PENDING)


class ConfessionDailyLimit(Base):
    """Atomic per-day sender counter keyed by the daily salted sender hash."""

    __tablename__ = "confession_daily_limits"
    sender_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
