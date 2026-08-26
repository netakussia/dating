import pytest

from services.interest_normalizer import normalize_interests
from services.profile_service import ProfileService
from utils.profile_media import ordered_photo_ids
from validators.profile_validator import ProfileValidationError, validate_profile_payload


def test_validate_profile_payload_rejects_bad_name_and_age():
    payload = {
        "name": "***",
        "age": 10,
        "district": "A" * 200,
        "institution": "B" * 200,
        "bio": "x",
    }

    try:
        validate_profile_payload(payload)
    except ProfileValidationError as exc:
        assert "name" in exc.errors
        assert "age" in exc.errors
        assert "district" in exc.errors
        assert "institution" in exc.errors
        assert "bio" in exc.errors
    else:
        raise AssertionError("Expected validation to fail")


def test_normalize_interests_maps_popular_categories():
    normalized = normalize_interests("Люблю музыку, рок, спорт, программирование, астрономия")

    assert "music" in normalized
    assert "sport" in normalized
    assert "programming" in normalized
    assert "астрономия" in normalized
    assert len(normalized) >= 4


def test_normalize_interests_splits_comma_separated_values_in_list():
    normalized = normalize_interests(["Music, sport, movie"])

    assert "music" in normalized
    assert "sport" in normalized
    assert "cinema" in normalized
    assert len(normalized) == 3


def test_format_interests_returns_hashtag_style_text():
    from services.interest_normalizer import format_interests

    assert format_interests(["music", "sport"]) == "#Music #Sport"


def test_validate_profile_payload_rejects_invalid_gender_values():
    payload = {
        "name": "Аня",
        "age": 24,
        "district": "Центр",
        "institution": "Университет",
        "bio": "Люблю прогулки и кофе.",
        "gender": "UNKNOWN",
        "target_gender": "WRONG",
    }

    try:
        validate_profile_payload(payload, photo_file_ids=["photo-id"])
    except ProfileValidationError as exc:
        assert "gender" in exc.errors
        assert "target_gender" in exc.errors
    else:
        raise AssertionError("Expected validation to fail")


def test_main_photo_is_rendered_first_in_gallery():
    profile = type(
        "Profile",
        (),
        {"photo_file_ids": ["one", "two", "three"], "main_photo_file_id": "two", "photo_file_id": "one"},
    )()

    assert ordered_photo_ids(profile) == ["two", "one", "three"]


class FakeProfileRepository:
    def __init__(self, profile):
        self.profile = profile
        self.save_calls = 0

    async def by_user_id(self, _user_id):
        return self.profile

    async def save(self, _profile):
        self.save_calls += 1


def managed_profile(photo_ids):
    return type(
        "Profile",
        (),
        {
            "photo_file_ids": list(photo_ids),
            "photo_file_id": photo_ids[0] if photo_ids else "",
            "main_photo_file_id": photo_ids[0] if photo_ids else None,
            "extra_data": {"photo_file_ids": list(photo_ids)},
            "moderation_locked": False,
            "moderation_status": None,
            "is_visible": True,
        },
    )()


@pytest.mark.asyncio
async def test_stale_photo_operations_are_safe_noops():
    profile = managed_profile(["one", "two"])
    service = ProfileService(None)
    service.repo = FakeProfileRepository(profile)

    assert await service.move_photo(1, "gone", 1) is profile
    assert await service.replace_photo(1, "gone", "new") is profile
    assert profile.photo_file_ids == ["one", "two"]
    assert service.repo.save_calls == 0


@pytest.mark.asyncio
async def test_add_photo_rejects_stale_fourth_upload():
    profile = managed_profile(["one", "two", "three"])
    service = ProfileService(None)
    service.repo = FakeProfileRepository(profile)

    with pytest.raises(ValueError, match="не более трёх"):
        await service.add_photo(1, "four")

    assert profile.photo_file_ids == ["one", "two", "three"]


@pytest.mark.asyncio
async def test_add_photo_accumulates_up_to_three_ids():
    profile = managed_profile([])
    service = ProfileService(None)
    service.repo = FakeProfileRepository(profile)

    await service.add_photo(1, "one")
    await service.add_photo(1, "two")
    await service.add_photo(1, "three")

    assert profile.photo_file_ids == ["one", "two", "three"]
    assert profile.extra_data["photo_file_ids"] == ["one", "two", "three"]
