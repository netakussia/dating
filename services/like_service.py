from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from models import Like
from repositories.like import LikeRepository
from services.eligibility import EligibilityError, EligibilityService


@dataclass(frozen=True, slots=True)
class LikeResult:
    like: Like
    created: bool


class LikeService:
    """Owns one-way Like creation and duplicate/self-like protection."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = LikeRepository(session)

    async def create(self, source_id: int, target_id: int, comment: str | None = None) -> LikeResult:
        normalized_comment = comment.strip() if comment else None
        if normalized_comment is not None and not 1 <= len(normalized_comment) <= 200:
            raise ValueError("Комментарий к лайку должен содержать от 1 до 200 символов.")
        try:
            await EligibilityService(self.repo.session).ensure_action_allowed(
                source_id,
                target_id,
                action="поставить лайк",
            )
        except EligibilityError as error:
            raise ValueError(str(error)) from error
        like, created = await self.repo.add(source_id, target_id, normalized_comment)
        return LikeResult(like=like, created=created)
