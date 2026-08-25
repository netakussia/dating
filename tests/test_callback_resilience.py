from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from handlers.admin import mycase_open
from handlers.callback_fallback import outdated_callback
from handlers.profile import delete_confirm
from repositories.report import ReportRepository
from services.profile_service import ProfileService


@pytest.mark.asyncio
async def test_outdated_callback_always_stops_telegram_loading_indicator():
    callback = SimpleNamespace(answer=AsyncMock())

    await outdated_callback(callback)

    callback.answer.assert_awaited_once_with(
        "Эта кнопка устарела. Откройте актуальный раздел меню.", show_alert=True
    )


@pytest.mark.asyncio
async def test_deleted_admin_case_is_acknowledged(monkeypatch):
    monkeypatch.setattr("handlers.admin._require_admin_capability", AsyncMock(return_value=True))

    async def no_report(self, report_id):
        return None

    monkeypatch.setattr(ReportRepository, "get", no_report)
    message = SimpleNamespace(delete=AsyncMock(), answer=AsyncMock())
    callback = SimpleNamespace(
        data="mycase:report:00000000-0000-0000-0000-000000000001",
        from_user=SimpleNamespace(id=1),
        message=message,
        answer=AsyncMock(),
    )

    await mycase_open(callback, session=SimpleNamespace(), settings=SimpleNamespace())

    callback.answer.assert_awaited_once_with("Жалоба уже удалена.", show_alert=True)


@pytest.mark.asyncio
async def test_deleted_profile_confirmation_does_not_report_success(monkeypatch):
    monkeypatch.setattr(ProfileService, "delete", AsyncMock(return_value=False))
    message = SimpleNamespace(edit_text=AsyncMock())
    callback = SimpleNamespace(from_user=SimpleNamespace(id=1), message=message, answer=AsyncMock())

    await delete_confirm(callback, session=SimpleNamespace())

    callback.answer.assert_awaited_once_with("Анкета уже была удалена.", show_alert=True)
    message.edit_text.assert_not_awaited()
