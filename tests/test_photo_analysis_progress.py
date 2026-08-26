from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from keyboards.profile import failed_photo_keyboard
from services.photo_analysis_progress import (
    PHOTO_ANALYSIS_TEXT,
    dismiss_photo_analysis_progress,
    show_photo_analysis_progress,
)


@pytest.mark.asyncio
async def test_photo_analysis_progress_is_shown_and_removed():
    progress = SimpleNamespace(delete=AsyncMock())
    message = SimpleNamespace(answer=AsyncMock(return_value=progress))

    shown = await show_photo_analysis_progress(message)
    await dismiss_photo_analysis_progress(shown)

    message.answer.assert_awaited_once_with(PHOTO_ANALYSIS_TEXT)
    progress.delete.assert_awaited_once()


def test_failed_photo_keyboard_offers_replace_or_manual_review():
    callback_data = {
        button.callback_data
        for row in failed_photo_keyboard().inline_keyboard
        for button in row
    }

    assert callback_data == {"photo:retry_failed", "photo:review_failed"}
