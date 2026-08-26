from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

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
