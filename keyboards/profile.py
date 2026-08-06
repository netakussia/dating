from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_keyboard(visible: bool = True):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙈 Скрыть анкету" if visible else "👀 Показать анкету", callback_data="profile:toggle")
    kb.button(text="✏️ Редактировать анкету", callback_data="profile:edit")
    kb.button(text="📷 Управлять фото", callback_data="profile:photos")
    kb.button(text="⏸ Поставить паузу", callback_data="profile:pause")
    kb.button(text="🗑 Удалить анкету", callback_data="profile:delete")
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
    kb.button(text="Готово", callback_data="photo:done")
    kb.adjust(1, 2, 2, 1)
    return kb.as_markup()


def registration_preview_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Опубликовать", callback_data="profile:publish")
    kb.button(text="Изменить", callback_data="profile:edit")
    kb.button(text="Назад", callback_data="profile:back")
    kb.button(text="❌ Отмена", callback_data="profile:cancel")
    kb.adjust(2)
    return kb.as_markup()
