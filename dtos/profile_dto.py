from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProfileDraft:
    gender: str | None = None
    target_gender: str | None = None
    name: str | None = None
    age: int | None = None
    district: str | None = None
    institution: str | None = None
    interests: list[str] = field(default_factory=list)
    bio: str | None = None
    photo_file_ids: list[str] = field(default_factory=list)
    main_photo_file_id: str | None = None
    locale: str = "ru"
    is_visible: bool = True
    extra_data: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        return {
            "gender": self.gender,
            "target_gender": self.target_gender,
            "name": self.name,
            "age": self.age,
            "district": self.district,
            "institution": self.institution,
            "interests": self.interests,
            "bio": self.bio,
            "photo_file_ids": self.photo_file_ids,
            "main_photo_file_id": self.main_photo_file_id,
            "locale": self.locale,
            "is_visible": self.is_visible,
            "extra_data": self.extra_data,
        }
