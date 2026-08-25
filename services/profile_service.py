from __future__ import annotations

import logging

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.profile_dto import ProfileDraft
from models import Appeal, Gender, ModerationCase, ModerationStatus, Profile, User, UserStatus
from repositories.profile import ProfileRepository
from services.interest_normalizer import normalize_interests
from validators.profile_validator import ProfileValidationError, validate_profile_payload

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ProfileRepository(session)

    async def get_profile(self, user_id: int) -> Profile | None:
        return await self.repo.by_user_id(user_id)

    async def _user_status_for(self, user_id: int) -> UserStatus | None:
        user = await self.session.get(User, user_id)
        return user.status if user else None

    def _is_visibility_restricted(self, profile: Profile | None, *, user_status: UserStatus | None = None) -> bool:
        if profile is None:
            return False
        if profile.moderation_locked:
            return True
        if profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            return True
        if user_status in {UserStatus.SUSPENDED, UserStatus.BANNED}:
            return True
        return False

    def _sync_photo_state(self, profile: Profile, photo_ids: list[str]) -> None:
        normalized = list(dict.fromkeys(photo_ids))[:3]
        profile.photo_file_ids = normalized
        profile.extra_data = {**(profile.extra_data or {}), "photo_file_ids": normalized}
        profile.photo_file_id = normalized[0] if normalized else ""
        profile.main_photo_file_id = normalized[0] if normalized else None

    async def create_or_update(self, user_id: int, draft: ProfileDraft) -> Profile:
        payload = draft.to_payload()
        photo_file_ids = list(payload.get("photo_file_ids") or [])
        try:
            validate_profile_payload(payload, photo_file_ids=photo_file_ids)
        except ProfileValidationError as exc:
            logger.warning("Invalid profile payload for user %s: %s", user_id, exc.errors)
            raise

        profile = await self.repo.by_user_id(user_id)
        if profile is None:
            profile = Profile(user_id=user_id)
            self.session.add(profile)

        profile.gender = Gender(payload["gender"]) if payload.get("gender") else profile.gender
        profile.target_gender = (
            Gender(payload["target_gender"]) if payload.get("target_gender") else profile.target_gender
        )
        profile.name = str(payload.get("name") or "").strip()
        profile.age = int(payload.get("age"))
        profile.district = str(payload.get("district") or "").strip()
        profile.institution = str(payload.get("institution") or "").strip()
        profile.interests = normalize_interests(payload.get("interests") or [])
        profile.bio = str(payload.get("bio") or "").strip()

        user_status = await self._user_status_for(user_id)
        if self._is_visibility_restricted(profile, user_status=user_status):
            profile.is_visible = False
        else:
            profile.is_visible = bool(payload.get("is_visible", profile.is_visible))

        if photo_file_ids:
            self._sync_photo_state(profile, photo_file_ids)
        elif getattr(profile, "extra_data", None) is None:
            self._sync_photo_state(profile, [])

        await self.repo.save(profile)
        return profile

    async def pause(self, user_id: int) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def resume(self, user_id: int) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        # Resuming a profile is a user action, never a moderation decision.  In
        # particular it must not be a back door out of a freeze/ban after an
        # edit or a photo replacement.
        user_status = await self._user_status_for(user_id)
        if self._is_visibility_restricted(profile, user_status=user_status):
            profile.is_visible = False
        else:
            profile.is_visible = True
        await self.repo.save(profile)
        return profile

    async def delete(self, user_id: int) -> None:
        user = await self.session.get(User, user_id)
        if user is None:
            return
        # Appeals reference moderation cases with RESTRICT because cases must
        # remain immutable during normal operation. During account deletion,
        # remove the user's private moderation records first so that restriction
        # cannot block the privacy operation.
        execute = getattr(self.session, "execute", None)
        if execute is not None:
            await execute(delete(Appeal).where(Appeal.user_id == user_id))
            await execute(delete(ModerationCase).where(ModerationCase.user_id == user_id))
        # Every social record is tied to users with FK cascades.  Deleting the
        # account, rather than just its profile, fulfils the deletion promise
        # and prevents former matches from retaining a live Telegram contact.
        await self.session.delete(user)
        await self.session.flush()

    async def add_photo(self, user_id: int, photo_file_id: str) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list((profile.extra_data or {}).get("photo_file_ids", list(profile.photo_file_ids or [])))
        if photo_file_id not in photo_ids:
            if len(photo_ids) >= 3:
                raise ValueError("В анкете может быть не более трёх фотографий.")
            photo_ids.append(photo_file_id)
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def remove_photo(self, user_id: int, photo_file_id: str) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list((profile.extra_data or {}).get("photo_file_ids", list(profile.photo_file_ids or [])))
        if photo_file_id in photo_ids:
            photo_ids.remove(photo_file_id)
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def move_photo(self, user_id: int, photo_file_id: str, direction: int) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list(profile.photo_file_ids or [])
        if photo_file_id not in photo_ids:
            return profile
        index = photo_ids.index(photo_file_id)
        target = index + direction
        if not 0 <= target < len(photo_ids):
            return profile
        photo_ids[index], photo_ids[target] = photo_ids[target], photo_ids[index]
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def replace_photo(self, user_id: int, old_file_id: str, new_file_id: str) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list(profile.photo_file_ids or [])
        if new_file_id == old_file_id:
            return profile
        if old_file_id not in photo_ids:
            return profile
        if new_file_id in photo_ids:
            photo_ids.remove(new_file_id)
        index = photo_ids.index(old_file_id)
        photo_ids[index] = new_file_id
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile
