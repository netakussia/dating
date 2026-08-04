from aiogram.utils.keyboard import InlineKeyboardBuilder


def profile_keyboard(visible: bool = True):
    kb = InlineKeyboardBuilder()
    kb.button(text="⏸ Скрыть" if visible else "▶️ Показать", callback_data="profile:toggle")
    kb.button(text="✏️ Заполнить заново", callback_data="profile:edit")
    kb.button(text="⏸ Пауза", callback_data="profile:pause")
    kb.button(text="🗑 Удалить", callback_data="profile:delete")
    kb.adjust(2)
    return kb.as_markup()


def registration_preview_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="Опубликовать", callback_data="profile:publish")
    kb.button(text="Изменить", callback_data="profile:edit")
    kb.button(text="Назад", callback_data="profile:back")
    kb.button(text="❌ Отмена", callback_data="profile:cancel")
    kb.adjust(2)
    return kb.as_markup()
