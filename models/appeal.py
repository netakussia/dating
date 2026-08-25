import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class AppealStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Appeal(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "appeals"
    __table_args__ = (
        Index(
            "uq_appeals_one_pending_per_user",
            "user_id",
            unique=True,
            postgresql_where="status = 'PENDING'",
        ),
    )

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[AppealStatus] = mapped_column(Enum(AppealStatus), default=AppealStatus.PENDING, index=True)
    assigned_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    admin_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
