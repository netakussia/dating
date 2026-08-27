from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.localization import LocalizationService


def profile_keyboard(
    visible: bool = True, *, hidden_by_moderation: bool = False, accepts_confessions: bool = True,
    locale: str = "ru",
):
    text = LocalizationService().get
    kb = InlineKeyboardBuilder()
    if hidden_by_moderation:
        kb.button(text=text("profile_hidden", locale), callback_data="profile:blocked")
    else:
        kb.button(text=text("profile_hide" if visible else "profile_show", locale), callback_data="profile:toggle")
    kb.button(text=text("profile_edit", locale), callback_data="profile:edit")
    kb.button(text=text("profile_photos", locale), callback_data="profile:photos")
    kb.button(
        text=text("confessions_on" if accepts_confessions else "confessions_off", locale),
        callback_data="profile:confessions_toggle",
    )
    kb.button(text=text("profile_pause", locale), callback_data="profile:pause")
    kb.button(text=text("profile_delete", locale), callback_data="profile:delete")
    kb.button(text=text("language_button", locale), callback_data="profile:language")
    kb.adjust(2)
    return kb.as_markup()


def photo_management_keyboard(photo_count: int):
    kb = InlineKeyboardBuilder()
    for index in range(photo_count):
        position = index + 1
        kb.button(text=f"⭐ Главная #{position}", callback_data=f"photo:main:{index}")
        kb.button(text="⬅️", callback_data=f"photo:move:{index}:-1")
        kb.button(text="➡️", callback_data=f"photo:move:{index}:1")
        kb.button(text="🔄 Заменить", callback_data=f"photo:replace:{index}")
        kb.button(text="🗑 Удалить", callback_data=f"photo:delete:{index}")
    if photo_count < 3:
        kb.button(text="➕ Добавить фото", callback_data="photo:add")
    kb.button(text="🏠 Главное меню", callback_data="photo:done")
    kb.adjust(1, 2, 2, 1)
    return kb.as_markup()


def photo_upload_keyboard(done_callback: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Готово", callback_data=done_callback)
    return kb.as_markup()


def failed_photo_keyboard(locale: str = "ru"):
    text = LocalizationService().get
    kb = InlineKeyboardBuilder()
    kb.button(text=text("photo_replace", locale), callback_data="photo:retry_failed")
    kb.button(text=text("photo_manual_review", locale), callback_data="photo:review_failed")
    kb.adjust(1)
    return kb.as_markup()


def registration_preview_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Опубликовать", callback_data="profile:publish")
    kb.button(text="✏️ Изменить", callback_data="profile:edit")
    kb.button(text="📷 Изменить фото", callback_data="profile:rephoto")
    kb.button(text="⬅️ Назад", callback_data="profile:back")
    kb.button(text="❌ Отмена", callback_data="profile:cancel")
    kb.adjust(2, 2, 1)
    return kb.as_markup()
