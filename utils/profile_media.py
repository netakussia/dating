import logging
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from aiogram.exceptions import TelegramBadRequest

from models import Profile

logger = logging.getLogger(__name__)


def ordered_photo_ids(profile: Profile) -> list[str]:
    """Return gallery order with the chosen main image first."""
    photos = list(profile.photo_file_ids or [])
    main = profile.main_photo_file_id
    if main in photos:
        photos.remove(main)
        photos.insert(0, main)
    return photos or ([profile.photo_file_id] if profile.photo_file_id else [])


async def send_profile_gallery(
    message: Message, profile: Profile, caption: str, reply_markup: InlineKeyboardMarkup
) -> None:
    photos = ordered_photo_ids(profile)
    if not photos:
        await message.answer(caption, reply_markup=reply_markup)
        return
    # Single photo case: try sending photo, fallback to text or placeholder if Telegram rejects media
    if len(photos) <= 1:
        try:
            await message.answer_photo(photos[0], caption=caption, reply_markup=reply_markup)
            return
        except TelegramBadRequest as e:
            logger.warning("Failed to send photo for profile %s: %s. Falling back to text message.", profile.user_id, e)
            # Send text fallback and optionally a generic placeholder image link
            fallback_text = f"{caption}\n\n[image unavailable]"
            await message.answer(fallback_text, reply_markup=reply_markup)
            return
    # Multiple photos: try media group, fallback to single-photo sends or text
    media = [
        InputMediaPhoto(media=photo_id, caption=caption if index == 0 else None)
        for index, photo_id in enumerate(photos)
    ]
    try:
        await message.answer_media_group(media)
        await message.answer("Выберите действие:", reply_markup=reply_markup)
    except TelegramBadRequest as e:
        logger.warning("Failed to send media group for profile %s: %s. Attempting individual sends/fallback.", profile.user_id, e)
        # Try sending first photo alone, then text
        first = photos[0]
        try:
            await message.answer_photo(first, caption=caption, reply_markup=reply_markup)
        except TelegramBadRequest as e2:
            logger.warning("Failed to send first photo fallback for profile %s: %s. Sending text-only fallback.", profile.user_id, e2)
            await message.answer(f"{caption}\n\n[image unavailable]", reply_markup=reply_markup)
        else:
            # if first photo succeeded, prompt for action
            await message.answer("Выберите действие:", reply_markup=reply_markup)
