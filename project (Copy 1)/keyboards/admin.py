from aiogram.utils.keyboard import InlineKeyboardBuilder
def admin_keyboard():
    kb = InlineKeyboardBuilder(); kb.button(text="📋 Жалобы", callback_data="admin:reports"); kb.button(text="📣 Рассылка", callback_data="admin:broadcast"); kb.adjust(1); return kb.as_markup()

def moderation_keyboard(report_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🚫 Забанить", callback_data=f"moderate:ban:{report_id}")
    kb.button(text="🙈 Скрыть анкету", callback_data=f"moderate:hide:{report_id}")
    kb.button(text="✅ Отклонить жалобу", callback_data=f"moderate:dismiss:{report_id}")
    kb.adjust(1)
    return kb.as_markup()
