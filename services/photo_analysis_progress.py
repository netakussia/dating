from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

PHOTO_ANALYSIS_TEXT = "⏳ Анализируем фото нейросетью. Это займёт несколько секунд…"


async def show_photo_analysis_progress(message: Message) -> Message | None:
    """Show a disposable status without allowing Telegram errors to stop moderation."""
    try:
        return await message.answer(PHOTO_ANALYSIS_TEXT)
    except TelegramBadRequest:
        return None


async def dismiss_photo_analysis_progress(progress: Message | None) -> None:
    if progress is None:
        return
    try:
        await progress.delete()
    except TelegramBadRequest:
        pass
