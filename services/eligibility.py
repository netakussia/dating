from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, ModerationStatus, Profile, User, UserStatus


class EligibilityError(ValueError):
    pass


class EligibilityService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def ensure_source_allowed(self, source_id: int, *, action: str) -> Profile:
        """Check if the source user is allowed to perform an action (e.g., send confessions)."""
        source_profile = await self.session.scalar(select(Profile).where(Profile.user_id == source_id))
        source_user = await self.session.get(User, source_id)
        if source_profile is None or source_user is None:
            raise EligibilityError("Анкета недоступна.")

        if not source_profile.is_visible:
            raise EligibilityError(f"Нельзя {action}: анкета недоступна.")
        if source_profile.moderation_locked:
            raise EligibilityError(f"Нельзя {action}: анкета на проверке модератором.")
        if source_profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            raise EligibilityError(f"Нельзя {action}: анкета на проверке модератором.")
        if source_user.status != UserStatus.ACTIVE:
            raise EligibilityError(f"Нельзя {action}: ваша анкета ограничена или заблокирована.")

        return source_profile

    async def ensure_action_allowed(self, source_id: int, target_id: int, *, action: str) -> tuple[Profile, User]:
        if source_id == target_id:
            raise EligibilityError(f"Нельзя {action} самому себе.")

        target_profile = await self.session.scalar(select(Profile).where(Profile.user_id == target_id))
        target_user = await self.session.get(User, target_id)
        if target_profile is None or target_user is None:
            raise EligibilityError("Анкета недоступна.")

        if not target_profile.is_visible:
            raise EligibilityError("Анкета недоступна.")
        if target_profile.moderation_locked:
            raise EligibilityError("Анкета недоступна.")
        if target_profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            raise EligibilityError("Анкета недоступна.")
        if target_user.status != UserStatus.ACTIVE:
            raise EligibilityError("Анкета недоступна.")

        blocked = await self.session.scalar(
            select(Block.id).where(
                ((Block.blocker_id == source_id) & (Block.blocked_id == target_id))
                | ((Block.blocker_id == target_id) & (Block.blocked_id == source_id))
            )
        )
        if blocked is not None:
            raise EligibilityError("Анкета недоступна.")

        return target_profile, target_user
