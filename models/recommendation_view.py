from sqlalchemy import BigInteger, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class RecommendationView(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "recommendation_views"
    __table_args__ = (
        UniqueConstraint("viewer_id", "candidate_id", name="uq_recommendation_views_viewer_candidate"),
        Index("ix_recommendation_views_viewer_created", "viewer_id", "created_at"),
        Index("ix_recommendation_views_candidate_created", "candidate_id", "created_at"),
    )

    viewer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    candidate_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    score: Mapped[float] = mapped_column(Float)
