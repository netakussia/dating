from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from dtos.profile_dto import ProfileDraft
from models import Gender, Profile
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

    def _sync_photo_state(self, profile: Profile, photo_ids: list[str]) -> None:
        normalized = list(dict.fromkeys(photo_ids))[:3]
        profile.photo_file_ids = normalized
        profile.extra_data = {"photo_file_ids": normalized}
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
        profile.target_gender = Gender(payload["target_gender"]) if payload.get("target_gender") else profile.target_gender
        profile.name = str(payload.get("name") or "").strip()
        profile.age = int(payload.get("age"))
        profile.district = str(payload.get("district") or "").strip()
        profile.institution = str(payload.get("institution") or "").strip()
        profile.interests = normalize_interests(payload.get("interests") or [])
        profile.bio = str(payload.get("bio") or "").strip()
        profile.is_visible = bool(payload.get("is_visible", True))

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
        profile.moderation_locked = True
        await self.repo.save(profile)
        return profile

    async def resume(self, user_id: int) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        profile.is_visible = True
        profile.moderation_locked = False
        await self.repo.save(profile)
        return profile

    async def delete(self, user_id: int) -> None:
        profile = await self.get_profile(user_id)
        if profile is None:
            return
        await self.session.delete(profile)
        await self.session.flush()

    async def add_photo(self, user_id: int, photo_file_id: str) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list((profile.extra_data or {}).get("photo_file_ids", list(profile.photo_file_ids or [])))
        if photo_file_id not in photo_ids:
            photo_ids.append(photo_file_id)
        self._sync_photo_state(profile, photo_ids)
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
        await self.repo.save(profile)
        return profile
