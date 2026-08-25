import enum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Enum, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from models.user import User


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ALL = "ALL"


class VerificationStatus(str, enum.Enum):
    UNVERIFIED = "UNVERIFIED"
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class ModerationStatus(str, enum.Enum):
    CLEAR = "CLEAR"
    UNDER_REVIEW = "UNDER_REVIEW"


class Profile(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "profiles"
    __table_args__ = (CheckConstraint("age >= 14 AND age <= 99", name="valid_age"),)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    target_gender: Mapped[Gender] = mapped_column(Enum(Gender))
    name: Mapped[str] = mapped_column(String(64))
    age: Mapped[int] = mapped_column(SmallInteger)
    district: Mapped[str] = mapped_column(String(64), index=True)
    institution: Mapped[str] = mapped_column(String(128), index=True)
    interests: Mapped[list[str]] = mapped_column(JSON, default=list)
    bio: Mapped[str] = mapped_column(Text)
    photo_file_id: Mapped[str] = mapped_column(String(255), default="")
    photo_file_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    main_photo_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    locale: Mapped[str] = mapped_column(String(8), default="ru")
    extra_data: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    moderation_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    report_count: Mapped[int] = mapped_column(Integer, default=0)
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), default=VerificationStatus.UNVERIFIED, index=True
    )
    moderation_status: Mapped[ModerationStatus] = mapped_column(
        Enum(ModerationStatus), default=ModerationStatus.CLEAR, index=True
    )
    user: Mapped["User"] = relationship(back_populates="profile")
