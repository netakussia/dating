from aiogram.utils.keyboard import InlineKeyboardBuilder
def admin_keyboard():
    kb = InlineKeyboardBuilder(); kb.button(text="📋 Жалобы", callback_data="admin:reports"); kb.button(text="⚖️ Апелляции", callback_data="admin:appeals"); kb.button(text="📣 Рассылка", callback_data="admin:broadcast"); kb.adjust(1); return kb.as_markup()

def moderation_keyboard(report_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🚫 Забанить", callback_data=f"moderate:ban:{report_id}")
    kb.button(text="⏸ Приостановить и скрыть", callback_data=f"moderate:hide:{report_id}")
    kb.button(text="✅ Отклонить жалобу", callback_data=f"moderate:dismiss:{report_id}")
    kb.adjust(1)
    return kb.as_markup()

def appeal_keyboard(appeal_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Ответить", callback_data=f"appeal:reply:{appeal_id}")
    kb.button(text="✅ Восстановить", callback_data=f"appeal:restore:{appeal_id}")
    kb.button(text="❌ Отклонить", callback_data=f"appeal:reject:{appeal_id}")
    kb.adjust(1)
    return kb.as_markup()
