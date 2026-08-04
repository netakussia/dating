from aiogram.utils.keyboard import InlineKeyboardBuilder
def profile_keyboard(visible: bool = True):
    kb = InlineKeyboardBuilder(); kb.button(text="⏸ Скрыть" if visible else "▶️ Показать", callback_data="profile:toggle"); kb.button(text="✏️ Заполнить заново", callback_data="profile:edit"); kb.adjust(1); return kb.as_markup()
