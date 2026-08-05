from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message

from models import Profile


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
    if len(photos) <= 1:
        await message.answer_photo(photos[0], caption=caption, reply_markup=reply_markup)
        return
    media = [
        InputMediaPhoto(media=photo_id, caption=caption if index == 0 else None)
        for index, photo_id in enumerate(photos)
    ]
    await message.answer_media_group(media)
    await message.answer("Выберите действие:", reply_markup=reply_markup)
