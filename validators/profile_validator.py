import re
from collections.abc import Mapping
from typing import Any

from services.localization import LocalizationService


class ProfileValidationError(Exception):
    def __init__(self, errors: dict[str, str]) -> None:
        self.errors = errors
        super().__init__("Profile validation failed")


_BLOCKED_WORDS = {
    "fuck",
    "shit",
    "bitch",
    "сука",
    "пизд",
    "хуй",
    "бляд",
    "ебан",
    "чмыр",
}


def validate_profile_payload(
    payload: Mapping[str, Any], *, photo_file_ids: list[str] | None = None, locale: str = "ru"
) -> None:
    localizer = LocalizationService()

    def error(key: str) -> str:
        return localizer.get(key, locale)

    errors: dict[str, str] = {}

    name = str(payload.get("name") or "").strip()
    if not name:
        errors["name"] = error("validation_name_required")
    elif not 2 <= len(name) <= 32:
        errors["name"] = error("validation_name_length")
    elif not re.match(r"^[A-Za-zА-Яа-яЁёІЇієїҐґ'’\- ]+$", name):
        errors["name"] = error("validation_name_characters")
    else:
        normalized = name.casefold()
        if any(word in normalized for word in _BLOCKED_WORDS):
            errors["name"] = error("validation_name_blocked")

    age_value = payload.get("age")
    if age_value is None:
        errors["age"] = error("validation_age_required")
    else:
        try:
            age = int(age_value)
        except (TypeError, ValueError):
            errors["age"] = error("validation_age_number")
        else:
            if not 16 <= age <= 99:
                errors["age"] = error("validation_age_range")

    district = str(payload.get("district") or "").strip()
    if not district:
        errors["district"] = error("validation_district_required")
    elif len(district) > 64:
        errors["district"] = error("validation_district_length")

    institution = str(payload.get("institution") or "").strip()
    if not institution:
        errors["institution"] = error("validation_institution_required")
    elif len(institution) > 128:
        errors["institution"] = error("validation_institution_length")

    gender = payload.get("gender")
    if gender not in {"MALE", "FEMALE"}:
        errors["gender"] = error("validation_gender_required")

    target_gender = payload.get("target_gender")
    if target_gender not in {"MALE", "FEMALE", "ALL"}:
        errors["target_gender"] = error("validation_target_gender")

    bio = str(payload.get("bio") or "").strip()
    if not bio:
        errors["bio"] = error("validation_bio_required")
    elif not 10 <= len(bio) <= 500:
        errors["bio"] = error("validation_bio_length")

    if photo_file_ids is not None:
        if not photo_file_ids:
            errors["photos"] = error("validation_photos_required")
        elif len(photo_file_ids) > 3:
            errors["photos"] = error("validation_photos_limit")

    if errors:
        raise ProfileValidationError(errors)
