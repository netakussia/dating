from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Like, Match, RecommendationView, Report, User, UserStatus


class MatchingStatsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def snapshot(self) -> dict[str, float | int]:
        result = await self.session.execute(
            select(
                func.count(User.id),
                func.count(User.id).filter(User.status == UserStatus.ACTIVE),
                select(func.count(Like.id)).scalar_subquery(),
                select(func.count(Match.id)).scalar_subquery(),
                select(func.count(Report.id)).scalar_subquery(),
                select(func.count(RecommendationView.id)).scalar_subquery(),
                select(func.avg(RecommendationView.score)).scalar_subquery(),
            )
        )
        users, active_users, likes, matches, reports, views, average_score = result.one()
        return {
            "users": int(users or 0),
            "active_users": int(active_users or 0),
            "likes": int(likes or 0),
            "matches": int(matches or 0),
            "reports": int(reports or 0),
            "views": int(views or 0),
            "ctr": round(100 * int(likes or 0) / int(views), 2) if views else 0.0,
            "average_compatibility": round(float(average_score or 0), 2),
        }
