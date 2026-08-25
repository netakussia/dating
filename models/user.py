import enum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models.profile import Profile


class UserRole(str, enum.Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    HEAD_MODERATOR = "HEAD_MODERATOR"
    CHIEF_MODERATOR = "HEAD_MODERATOR"
    OWNER = "OWNER"
    ADMIN = "ADMIN"


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"


class User(TimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.ACTIVE, index=True)
    # Internal-only value. It must never be rendered in the user interface.
    trust_score: Mapped[int] = mapped_column(Integer, default=95, index=True)
    accepts_confessions: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    profile: Mapped["Profile | None"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
