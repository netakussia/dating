from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import handlers.admin as admin_handler
from keyboards.admin import (
    appeal_decision_keyboard,
    case_decision_keyboard,
    confirm_action_keyboard,
    moderation_decision_keyboard,
    verification_decision_keyboard,
)
from models import ModerationCaseStatus, ModerationCaseType, ModerationStatus, ReportStatus, UserRole, UserStatus


def callback_ids(markup):
    return {
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if button.callback_data
    }


def test_moderation_approve_and_reject_actions_are_distinct_for_all_workflows():
    verification = callback_ids(verification_decision_keyboard("id"))
    assert "verify:approve:id" in verification
    assert "verify:reject:id" in verification
    assert "verify:approve:id" != "verify:reject:id"

    photo = callback_ids(case_decision_keyboard("id"))
    assert "case:restore:id" in photo
    assert "case:reject:id" in photo
    assert "case:restore:id" != "case:reject:id"

    reports = callback_ids(moderation_decision_keyboard("id"))
    assert "moderate:prompt:dismiss:id" in reports
    assert "moderate:prompt:hide:id" in reports
    assert "moderate:prompt:dismiss:id" != "moderate:prompt:hide:id"

    appeals = callback_ids(appeal_decision_keyboard("id"))
    assert "appeal:prompt:restore:id" in appeals
    assert "appeal:prompt:reject:id" in appeals
    assert "appeal:prompt:restore:id" != "appeal:prompt:reject:id"
    assert "appeal:execute:reject:id" in callback_ids(
        confirm_action_keyboard("appeal:execute:reject:id", back_data="admin:appeals")
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("action", "expected_restore", "expected_retake", "expected_reject", "expected_message"),
    [
        ("restore", True, False, False, "Фото одобрено"),
        ("retake", False, True, False, "замену фотографии"),
        ("reject", False, False, True, "Фото отклонено"),
    ],
)
async def test_photo_case_decision_passes_correct_action_to_service(
    monkeypatch, action, expected_restore, expected_retake, expected_reject, expected_message
):
    case_id = "12345678-1234-4234-8234-123456789abc"
    case = SimpleNamespace(
        id=case_id,
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status=ModerationCaseStatus.IN_PROGRESS,
        assigned_to=100,
        admin_id=None,
    )
    service = SimpleNamespace(
        resolve_case=AsyncMock(return_value=(case, True, None)),
    )
    callback = SimpleNamespace(
        data=f"case:{action}:{case_id}",
        from_user=SimpleNamespace(id=100),
        message=SimpleNamespace(),
        bot=SimpleNamespace(),
        answer=AsyncMock(),
    )
    settings = SimpleNamespace()

    class CaseSession:
        async def get(self, _model, _case_id):
            return case

    monkeypatch.setattr(admin_handler, "_require_admin_capability", AsyncMock(return_value=True))
    monkeypatch.setattr(admin_handler, "_role_for_admin", AsyncMock(return_value=UserRole.MODERATOR))
    monkeypatch.setattr(admin_handler, "ModerationService", lambda _session: service)
    monkeypatch.setattr(admin_handler, "NotificationService", lambda _bot: SimpleNamespace(safe_send=AsyncMock()))
    monkeypatch.setattr(
        admin_handler,
        "InternalNotificationService",
        lambda _bot, _settings: SimpleNamespace(send_moderation_event=AsyncMock()),
    )
    monkeypatch.setattr(admin_handler, "_safe_edit_message_text", AsyncMock())
    monkeypatch.setattr(admin_handler, "_safe_callback_answer", AsyncMock())

    await admin_handler.moderation_case(callback, CaseSession(), settings)

    assert service.resolve_case.await_args.kwargs["restore"] is expected_restore
    assert service.resolve_case.await_args.kwargs["retake"] is expected_retake
    assert service.resolve_case.await_args.kwargs["reject"] is expected_reject
    assert expected_message in admin_handler._safe_edit_message_text.await_args.args[1]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("restore", "retake", "reject", "expected_status", "expected_visible", "expected_locked"),
    [
        (True, False, False, ModerationStatus.CLEAR, True, False),
        (False, True, False, ModerationStatus.UNDER_REVIEW, False, True),
        (False, False, True, ModerationStatus.UNDER_REVIEW, False, True),
    ],
)
async def test_photo_case_resolution_applies_positive_or_negative_profile_state(
    restore, retake, reject, expected_status, expected_visible, expected_locked
):
    from services.moderation_service import ModerationService

    case = SimpleNamespace(
        id="12345678-1234-4234-8234-123456789abc",
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status=ModerationCaseStatus.IN_PROGRESS,
        assigned_to=100,
        admin_id=None,
    )
    profile = SimpleNamespace(
        moderation_status=ModerationStatus.UNDER_REVIEW,
        is_visible=False,
        moderation_locked=True,
    )

    class ResolveSession:
        async def get(self, model, _case_id):
            return case if model.__name__ == "ModerationCase" else None

        async def execute(self, _query):
            return SimpleNamespace(scalar_one_or_none=lambda: case)

        async def scalar(self, _query):
            return profile

        def add(self, _value):
            return None

        async def flush(self):
            return None

    resolved, changed, reason = await ModerationService(ResolveSession()).resolve_case(
        case.id,
        100,
        restore=restore,
        retake=retake,
        reject=reject,
        actor_role=UserRole.MODERATOR,
    )

    assert resolved is case
    assert changed is True
    assert reason is None
    assert profile.moderation_status == expected_status
    assert profile.is_visible is expected_visible
    assert profile.moderation_locked is expected_locked


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("face_detected", "face_count", "face_score", "human_score", "expected_case_type"),
    [
        (False, 0, 0.0, 0.0, ModerationCaseType.NO_FACE),
        (True, 1, 0.45, 0.291, ModerationCaseType.PHOTO_RETAKE),
    ],
)
async def test_red_photo_case_type_matches_the_detected_face_signal(
    face_detected, face_count, face_score, human_score, expected_case_type
):
    from services.photo_moderation_service import PhotoAssessment, PhotoModerationService

    profile = SimpleNamespace(
        moderation_status=ModerationStatus.CLEAR,
        is_visible=True,
        moderation_locked=False,
    )
    captured = {}

    class PhotoSession:
        async def scalar(self, _query):
            return profile

    service = PhotoModerationService(PhotoSession(), nsfw_threshold=0.85)
    service.repo = SimpleNamespace(
        record_photo=AsyncMock(),
        open_case=AsyncMock(
            side_effect=lambda _user_id, case_type, **_kwargs: (
                captured.update(case_type=case_type),
                True,
            )
        ),
    )

    await service._apply_assessment(
        7,
        "photo",
        None,
        PhotoAssessment(
            nsfw_score=0.006,
            face_detected=face_detected,
            face_score=face_score,
            face_count=face_count,
            human_score=human_score,
        ),
    )

    assert captured["case_type"] == expected_case_type


def test_detected_face_quality_failure_is_not_mislabeled_as_no_face():
    from services.photo_moderation_service import moderation_zone
    from services.photo_safety_providers import PhotoAssessment

    assessment = PhotoAssessment(
        nsfw_score=0.006,
        face_detected=True,
        provider="ml_onnx:cached",
        face_score=0.887,
        face_count=1,
        human_score=0.291,
    )

    assert moderation_zone(assessment) == "GREEN"


@pytest.mark.asyncio
async def test_malformed_appeal_execute_callback_cannot_become_reject(monkeypatch):
    callback = SimpleNamespace(
        data="appeal:execute:12345678-1234-4234-8234-123456789abc",
        from_user=SimpleNamespace(id=100),
        answer=AsyncMock(),
    )
    monkeypatch.setattr(admin_handler, "_require_admin_capability", AsyncMock(return_value=True))

    await admin_handler.appeal_action(callback, SimpleNamespace(), SimpleNamespace(), SimpleNamespace())

    callback.answer.assert_awaited_once()
    assert "Некорректная" in callback.answer.await_args.args[0]


@pytest.mark.asyncio
async def test_unban_restores_the_profile_state_together_with_user_state():
    from services.moderation_service import ModerationService

    user = SimpleNamespace(status=UserStatus.BANNED)
    profile = SimpleNamespace(
        is_visible=False,
        moderation_locked=True,
        moderation_status=ModerationStatus.UNDER_REVIEW,
    )

    class UnbanSession:
        async def get(self, _model, _user_id):
            return user

        async def scalar(self, _query):
            return profile

        def add(self, _value):
            return None

        async def flush(self):
            return None

    changed = await ModerationService(UnbanSession()).unban(7, 100, actor_role=UserRole.OWNER)

    assert changed is True
    assert user.status == UserStatus.ACTIVE
    assert profile.is_visible is True
    assert profile.moderation_locked is False
    assert profile.moderation_status == ModerationStatus.CLEAR


@pytest.mark.asyncio
async def test_report_hide_resolves_report_and_applies_suspension(monkeypatch):
    report = SimpleNamespace(
        id="12345678-1234-4234-8234-123456789abc",
        target_user_id=7,
        status=ReportStatus.PENDING,
        assigned_to=100,
    )
    calls = []

    class ReportRepo:
        def __init__(self, _session):
            return None

        async def get(self, _report_id):
            return report

        async def resolve(self, report_id, status):
            calls.append((report_id, status))
            report.status = status
            return report

    class Nested:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args):
            return False

    service = SimpleNamespace(suspend=AsyncMock(return_value=True))
    callback = SimpleNamespace(
        data="moderate:execute:hide:12345678-1234-4234-8234-123456789abc",
        from_user=SimpleNamespace(id=100),
        bot=SimpleNamespace(),
        message=SimpleNamespace(),
        answer=AsyncMock(),
    )
    session = SimpleNamespace(begin_nested=lambda: Nested())
    settings = SimpleNamespace(report_threshold=3)

    monkeypatch.setattr(admin_handler, "_require_admin_capability", AsyncMock(return_value=True))
    monkeypatch.setattr(admin_handler, "_role_for_admin", AsyncMock(return_value=UserRole.MODERATOR))
    monkeypatch.setattr(admin_handler, "ReportRepository", ReportRepo)
    monkeypatch.setattr(admin_handler, "ModerationService", lambda _session: service)
    monkeypatch.setattr(admin_handler, "NotificationService", lambda _bot: SimpleNamespace(safe_send=AsyncMock()))
    monkeypatch.setattr(
        admin_handler,
        "InternalNotificationService",
        lambda _bot, _settings: SimpleNamespace(send_moderation_event=AsyncMock()),
    )
    monkeypatch.setattr(admin_handler, "_safe_edit_message_text", AsyncMock())
    monkeypatch.setattr(admin_handler, "_safe_callback_answer", AsyncMock())

    await admin_handler.moderate(callback, session, settings)

    assert str(calls[0][0]) == report.id
    assert calls[0][1] == ReportStatus.APPROVED
    service.suspend.assert_awaited_once()
    assert "приостановлена" in admin_handler._safe_edit_message_text.await_args.args[1]