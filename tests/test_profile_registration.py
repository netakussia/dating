from services.interest_normalizer import normalize_interests
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
