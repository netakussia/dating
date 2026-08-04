from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class Dislike(UUIDPKMixin, TimestampMixin, Base):
    """A skipped profile. It is kept so the same profile is not shown again."""

    __tablename__ = "dislikes"
    __table_args__ = (UniqueConstraint("from_user_id", "to_user_id"),)

    from_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    to_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
