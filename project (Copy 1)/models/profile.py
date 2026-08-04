import enum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Enum, ForeignKey, Integer, JSON, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from models.user import User


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ALL = "ALL"


class Profile(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "profiles"
    __table_args__ = (CheckConstraint("age >= 14 AND age <= 99", name="valid_age"),)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    target_gender: Mapped[Gender] = mapped_column(Enum(Gender))
    name: Mapped[str] = mapped_column(String(64))
    age: Mapped[int] = mapped_column(SmallInteger)
    district: Mapped[str] = mapped_column(String(64), index=True)
    institution: Mapped[str] = mapped_column(String(128), index=True)
    interests: Mapped[list[str]] = mapped_column(JSON, default=list)
    bio: Mapped[str] = mapped_column(Text)
    photo_file_id: Mapped[str] = mapped_column(String(255))
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    report_count: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped["User"] = relationship(back_populates="profile")
