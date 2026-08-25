import re
from collections.abc import Mapping
from typing import Any


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


def validate_profile_payload(payload: Mapping[str, Any], *, photo_file_ids: list[str] | None = None) -> None:
    errors: dict[str, str] = {}

    name = str(payload.get("name") or "").strip()
    if not name:
        errors["name"] = "Имя обязательно."
    elif not 2 <= len(name) <= 32:
        errors["name"] = "Имя должно быть от 2 до 32 символов."
    elif not re.match(r"^[A-Za-zА-Яа-яЁёІЇієїҐґ'’\- ]+$", name):
        errors["name"] = "Имя содержит недопустимые символы."
    else:
        normalized = name.casefold()
        if any(word in normalized for word in _BLOCKED_WORDS):
            errors["name"] = "Имя содержит запрещённые слова."

    age_value = payload.get("age")
    if age_value is None:
        errors["age"] = "Возраст обязателен."
    else:
        try:
            age = int(age_value)
        except (TypeError, ValueError):
            errors["age"] = "Возраст должен быть числом."
        else:
            if not 16 <= age <= 99:
                errors["age"] = "Возраст должен быть от 16 до 99 лет."

    district = str(payload.get("district") or "").strip()
    if not district:
        errors["district"] = "Район обязателен."
    elif len(district) > 64:
        errors["district"] = "Район слишком длинный."

    institution = str(payload.get("institution") or "").strip()
    if not institution:
        errors["institution"] = "Учебное заведение обязательно."
    elif len(institution) > 128:
        errors["institution"] = "Название учреждения слишком длинное."

    gender = payload.get("gender")
    if gender not in {"MALE", "FEMALE"}:
        errors["gender"] = "Пол обязателен."

    target_gender = payload.get("target_gender")
    if target_gender not in {"MALE", "FEMALE", "ALL"}:
        errors["target_gender"] = "Цель поиска указана неверно."

    bio = str(payload.get("bio") or "").strip()
    if not bio:
        errors["bio"] = "Описание обязательно."
    elif not 10 <= len(bio) <= 500:
        errors["bio"] = "Описание должно быть от 10 до 500 символов."

    if photo_file_ids is not None:
        if not photo_file_ids:
            errors["photos"] = "Нужно загрузить хотя бы одну фотографию."
        elif len(photo_file_ids) > 3:
            errors["photos"] = "Можно загрузить не больше трёх фотографий."

    if errors:
        raise ProfileValidationError(errors)
