import uuid
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    Appeal,
    AppealStatus,
    ModerationCase,
    ModerationCaseStatus,
    ModerationStatus,
    Profile,
    User,
    UserRole,
    UserStatus,
)
from repositories.trust import TrustRepository
from utils.admin_roles import (
    can_access_moderation,
    can_ban,
    can_override_case,
    can_release_cases,
    can_unban,
    normalize_admin_role,
)


class ModerationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def _role_for(self, admin_id: int) -> UserRole:
        user = await self.session.get(User, admin_id)
        return normalize_admin_role(getattr(user, "role", UserRole.USER))

    async def _conflicting_case_for_user(
        self, user_id: int, admin_id: int, *, role: UserRole | None = None
    ) -> ModerationCase | None:
        role = role or await self._role_for(admin_id)
        if can_override_case(role):
            return None
        result = await self.session.execute(
            select(ModerationCase).where(
                ModerationCase.user_id == user_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
            )
        )
        scalars = getattr(result, "scalars", None)
        if scalars is None:
            # Safety fallback for lightweight session stubs used in tests: if the session
            # cannot provide a real SQLAlchemy result, we conservatively deny the action
            # to non-overriding moderators rather than allowing a forbidden ban/freeze.
            return object()
        for case in scalars().all():
            if case.assigned_to not in {None, admin_id}:
                return case
        return None

    async def claim_case(
        self, case_id: uuid.UUID, moderator_id: int, *, actor_role: UserRole | None = None
    ) -> tuple[ModerationCase | None, bool, str | None]:
        case = await self.session.get(ModerationCase, case_id)
        if case is None:
            return None, False, "case_not_found"
        if case.status == ModerationCaseStatus.RESOLVED:
            return case, False, "already_resolved"
        role = actor_role or await self._role_for(moderator_id)
        if not can_access_moderation(role):
            return case, False, "forbidden"
        if case.status == ModerationCaseStatus.IN_PROGRESS and case.assigned_to != moderator_id:
            return case, False, "already_assigned"
        if case.status == ModerationCaseStatus.IN_PROGRESS and case.assigned_to == moderator_id:
            return case, False, "already_claimed"

        result = await self.session.execute(
            update(ModerationCase)
            .where(
                ModerationCase.id == case_id,
                ModerationCase.status == ModerationCaseStatus.PENDING,
                (ModerationCase.assigned_to.is_(None) | (ModerationCase.assigned_to == moderator_id)),
            )
            .values(
                status=ModerationCaseStatus.IN_PROGRESS,
                assigned_to=moderator_id,
                assigned_at=datetime.now(UTC),
            )
            .returning(ModerationCase)
        )
        updated = result.scalar_one_or_none()
        if updated is None:
            refreshed = await self.session.get(ModerationCase, case_id)
            if refreshed is None:
                return None, False, "case_not_found"
            if refreshed.status == ModerationCaseStatus.RESOLVED:
                return refreshed, False, "already_resolved"
            if refreshed.status == ModerationCaseStatus.IN_PROGRESS and refreshed.assigned_to != moderator_id:
                return refreshed, False, "already_assigned"
            return refreshed, False, "already_claimed"

        await self.repo.log(
            moderator_id,
            "CASE_CLAIMED",
            target_type="case",
            target_id=str(updated.id),
            target_user_id=updated.user_id,
            details="moderation case assigned",
            metadata={"case_type": updated.case_type.value, "assigned_to": moderator_id},
        )
        await self.session.flush()
        return updated, True, None

    async def release_case(
        self,
        case_id: uuid.UUID,
        actor_id: int,
        *,
        moderator_id: int | None = None,
    ) -> tuple[ModerationCase | None, bool, str | None]:
        role = await self._role_for(actor_id)
        if not can_release_cases(role):
            return await self.session.get(ModerationCase, case_id), False, "forbidden"
        case = await self.session.get(ModerationCase, case_id)
        if case is None:
            return None, False, "case_not_found"
        if case.status == ModerationCaseStatus.RESOLVED:
            return case, False, "already_resolved"
        if case.assigned_to is None:
            return case, False, "not_assigned"
        if case.assigned_to != actor_id and not can_override_case(role):
            return case, False, "forbidden"
        if moderator_id is not None and case.assigned_to != moderator_id and role == UserRole.MODERATOR:
            return case, False, "forbidden"

        result = await self.session.execute(
            update(ModerationCase)
            .where(
                ModerationCase.id == case_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
                ModerationCase.assigned_to == case.assigned_to,
            )
            .values(status=ModerationCaseStatus.PENDING, assigned_to=None, assigned_at=None)
            .returning(ModerationCase)
        )
        updated = result.scalar_one_or_none()
        if updated is None:
            return case, False, "not_assigned"
        await self.repo.log(
            actor_id,
            "CASE_UNASSIGNED",
            target_type="case",
            target_id=str(updated.id),
            target_user_id=updated.user_id,
            details="moderation case released",
            metadata={"released_from": case.assigned_to, "case_type": updated.case_type.value},
        )
        await self.session.flush()
        return updated, True, None

    async def resolve_case(
        self,
        case_id: uuid.UUID,
        admin_id: int,
        *,
        restore: bool = False,
        retake: bool = False,
        reject: bool = False,
        actor_role: UserRole | None = None,
    ) -> tuple[ModerationCase | None, bool, str | None]:
        case = await self.session.get(ModerationCase, case_id)
        if case is None:
            return None, False, "case_not_found"
        if case.status == ModerationCaseStatus.RESOLVED:
            return case, False, "already_resolved"
        if case.status != ModerationCaseStatus.IN_PROGRESS:
            return case, False, "not_in_progress"

        role = actor_role or await self._role_for(admin_id)
        if not can_access_moderation(role):
            return case, False, "forbidden"

        if case.assigned_to not in {None, admin_id}:
            if not can_override_case(role):
                return case, False, "forbidden"

        if case.assigned_to is None:
            case, claimed, message = await self.claim_case(case_id, admin_id, actor_role=role)
            if not claimed:
                return case, False, message or "claim_required"

        result = await self.session.execute(
            update(ModerationCase)
            .where(
                ModerationCase.id == case_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
                ModerationCase.assigned_to == case.assigned_to,
            )
            .values(status=ModerationCaseStatus.RESOLVED, admin_id=admin_id, assigned_to=admin_id)
            .returning(ModerationCase)
        )
        updated = result.scalar_one_or_none()
        if updated is None:
            refreshed = await self.session.get(ModerationCase, case_id)
            if refreshed and refreshed.status == ModerationCaseStatus.RESOLVED:
                return refreshed, False, "already_resolved"
            return refreshed, False, "already_assigned"
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == updated.user_id))
        if profile:
            profile.moderation_status = ModerationStatus.CLEAR
            if restore:
                profile.moderation_locked = False
                profile.is_visible = True
            elif retake or reject:
                # A negative photo decision keeps the profile hidden until replacement.
                profile.moderation_status = ModerationStatus.UNDER_REVIEW
                profile.moderation_locked = True
                profile.is_visible = False
        await self.repo.log(
            admin_id,
            "CASE_RESOLVED",
            target_type="case",
            target_id=str(updated.id),
            target_user_id=updated.user_id,
            details="moderation case resolved",
            metadata={"restore": restore, "retake": retake, "case_type": updated.case_type.value},
        )
        await self.session.flush()
        return updated, True, None

    async def suspend(
        self, user_id: int, admin_id: int, *, reason: str, actor_role: UserRole | None = None
    ) -> bool:
        role = actor_role or await self._role_for(admin_id)
        if not can_ban(role):
            return False
        if user_id == admin_id:
            return False
        if await self._conflicting_case_for_user(user_id, admin_id, role=role) is not None:
            return False
        user = await self.session.get(User, user_id)
        if user is None or getattr(user, "status", None) == UserStatus.BANNED:
            return False
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        user.status = UserStatus.SUSPENDED
        if profile:
            profile.is_visible = False
            profile.moderation_locked = True
            profile.moderation_status = ModerationStatus.UNDER_REVIEW
        await self.repo.log(
            admin_id,
            "FREEZE",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details=reason,
            metadata={"kind": "freeze"},
        )
        await self.session.flush()
        return True

    async def ban(
        self, user_id: int, admin_id: int, *, reason: str, actor_role: UserRole | None = None
    ) -> bool:
        role = actor_role or await self._role_for(admin_id)
        if not can_ban(role):
            return False
        if user_id == admin_id:
            return False
        if await self._conflicting_case_for_user(user_id, admin_id, role=role) is not None:
            return False
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        if getattr(user, "status", None) == UserStatus.BANNED:
            return False
        user.status = UserStatus.BANNED
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if profile:
            profile.is_visible = False
            profile.moderation_locked = True
        await self.repo.log(
            admin_id,
            "BAN",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details=reason,
            metadata={"kind": "ban"},
        )
        await self.session.flush()
        return True

    async def unban(self, user_id: int, admin_id: int, *, actor_role: UserRole | None = None) -> bool:
        role = actor_role or await self._role_for(admin_id)
        if not can_unban(role):
            return False
        user = await self.session.get(User, user_id)
        if user is None or getattr(user, "status", None) != UserStatus.BANNED:
            return False
        user.status = UserStatus.ACTIVE
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if profile:
            profile.is_visible = True
            profile.moderation_locked = False
            profile.moderation_status = ModerationStatus.CLEAR
        await self.repo.log(
            admin_id,
            "UNBAN",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details="manual unban",
        )
        await self.session.flush()
        return True

    async def restore_appeal_sanction(
        self, appeal: Appeal, admin_id: int, *, actor_role: UserRole | None = None
    ) -> tuple[bool, str | None]:
        role = actor_role or await self._role_for(admin_id)
        if not can_unban(role):
            return False, "forbidden"
        if appeal.status != AppealStatus.PENDING:
            return False, "already_resolved"

        result = await self.session.execute(
            select(ModerationCase).where(
                ModerationCase.user_id == appeal.user_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
            )
        )
        if result.scalars().first() is not None:
            return False, "other_open_sanction"

        user = await self.session.get(User, appeal.user_id)
        if user is None or user.status not in {UserStatus.BANNED, UserStatus.SUSPENDED}:
            return False, "not_restricted"
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == appeal.user_id))
        user.status = UserStatus.ACTIVE
        if profile:
            profile.moderation_locked = False
            profile.moderation_status = ModerationStatus.CLEAR
            profile.is_visible = True
        appeal.status = AppealStatus.APPROVED
        appeal.admin_id = admin_id
        appeal.reviewed_at = datetime.now(UTC)
        await self.repo.log(
            admin_id,
            "appeal_restored",
            target_type="appeal",
            target_id=str(appeal.id),
            target_user_id=appeal.user_id,
        )
        await self.session.flush()
        return True, None
