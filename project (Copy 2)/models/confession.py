import enum

from sqlalchemy import BigInteger, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class ConfessionStatus(str, enum.Enum):
    DELIVERED = "DELIVERED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class Confession(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "confessions"
    sender_hash: Mapped[str] = mapped_column(String(64), index=True)
    recipient_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    target_username: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[ConfessionStatus] = mapped_column(Enum(ConfessionStatus), default=ConfessionStatus.PENDING)
