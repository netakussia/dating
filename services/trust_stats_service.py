from sqlalchemy.ext.asyncio import AsyncSession

from repositories.trust import TrustRepository


class TrustStatsService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = TrustRepository(session)

    async def snapshot(self) -> dict[str, float | int]:
        return await self.repo.stats()
