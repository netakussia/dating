import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import ModerationCaseStatus, ModerationStatus, Profile, User, UserStatus
from repositories.trust import TrustRepository


class ModerationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def resolve_case(
        self, case_id: uuid.UUID, admin_id: int, *, restore: bool = False
    ) -> tuple[object | None, bool]:
        case = await self.repo.case(case_id)
        if case is None or case.status != ModerationCaseStatus.PENDING:
            return case, False
        case.status, case.admin_id = ModerationCaseStatus.RESOLVED, admin_id
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == case.user_id))
        if profile:
            profile.moderation_status = ModerationStatus.CLEAR
            if restore:
                profile.moderation_locked = False
                profile.is_visible = True
        await self.repo.log(
            admin_id,
            "moderation_case_resolved",
            target_type="case",
            target_id=str(case.id),
            metadata={"restore": restore},
        )
        await self.session.flush()
        return case, True

    async def suspend(self, user_id: int, admin_id: int, *, reason: str) -> bool:
        user = await self.session.get(User, user_id)
        if user is None or user.status == UserStatus.BANNED:
            return False
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        user.status = UserStatus.SUSPENDED
        if profile:
            profile.is_visible = False
            profile.moderation_locked = True
            profile.moderation_status = ModerationStatus.UNDER_REVIEW
        await self.repo.log(admin_id, "user_suspended", target_type="user", target_id=str(user_id), details=reason)
        return True

    async def ban(self, user_id: int, admin_id: int, *, reason: str) -> bool:
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        if user.status == UserStatus.BANNED:
            return False
        user.status = UserStatus.BANNED
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if profile:
            profile.is_visible = False
            profile.moderation_locked = True
        await self.repo.log(admin_id, "user_banned", target_type="user", target_id=str(user_id), details=reason)
        return True

    async def unban(self, user_id: int, admin_id: int) -> bool:
        user = await self.session.get(User, user_id)
        if user is None or user.status != UserStatus.BANNED:
            return False
        user.status = UserStatus.ACTIVE
        await self.repo.log(admin_id, "user_unbanned", target_type="user", target_id=str(user_id))
        return True
