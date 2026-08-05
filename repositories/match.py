from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Match


class MatchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_between(self, first_user_id: int, second_user_id: int) -> Match | None:
        first, second = sorted((first_user_id, second_user_id))
        return await self.session.scalar(
            select(Match).where(Match.user1_id == first, Match.user2_id == second)
        )

    async def create_once(self, first_user_id: int, second_user_id: int) -> tuple[Match, bool]:
        first, second = sorted((first_user_id, second_user_id))
        existing = await self.get_between(first, second)
        if existing is not None:
            return existing, False
        match = Match(user1_id=first, user2_id=second)
        try:
            async with self.session.begin_nested():
                self.session.add(match)
                await self.session.flush()
        except IntegrityError:
            existing = await self.get_between(first, second)
            if existing is not None:
                return existing, False
            raise
        return match, True

    async def by_user_id(self, user_id: int, limit: int = 50) -> list[Match]:
        statement = (
            select(Match)
            .where((Match.user1_id == user_id) | (Match.user2_id == user_id))
            .order_by(Match.created_at.desc())
            .limit(limit)
        )
        return list((await self.session.scalars(statement)).all())
