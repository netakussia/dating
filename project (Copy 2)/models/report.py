import enum

from sqlalchemy import BigInteger, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class ReportReason(str, enum.Enum):
    FAKE = "FAKE"; INSULT = "INSULT"; INAPPROPRIATE_CONTENT = "INAPPROPRIATE_CONTENT"; NSFW = "NSFW"; SPAM = "SPAM"; OTHER = "OTHER"

class ReportStatus(str, enum.Enum):
    PENDING = "PENDING"; APPROVED = "APPROVED"; DISMISSED = "DISMISSED"

class Report(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "reports"
    reporter_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    target_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    reason: Mapped[ReportReason] = mapped_column(Enum(ReportReason))
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), default=ReportStatus.PENDING)
