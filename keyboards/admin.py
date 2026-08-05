from aiogram.utils.keyboard import InlineKeyboardBuilder
def admin_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🛡 Trust: верификации", callback_data="admin:verifications")
    kb.button(text="📋 Trust: жалобы", callback_data="admin:reports")
    kb.button(text="🔞 Trust: NSFW", callback_data="admin:nsfw")
    kb.button(text="🚫 Trust: заблокированные", callback_data="admin:blocked")
    kb.button(text="⚖️ Trust: апелляции", callback_data="admin:appeals")
    kb.button(text="📜 Trust: история", callback_data="admin:trust_history")
    kb.button(text="📊 Trust: статистика", callback_data="admin:trust_stats")
    kb.button(text="📣 Рассылка", callback_data="admin:broadcast")
    kb.adjust(1)
    return kb.as_markup()


def verification_keyboard(request_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data=f"verify:approve:{request_id}")
    kb.button(text="🔁 Запросить повтор", callback_data=f"verify:retake:{request_id}")
    kb.button(text="❌ Отклонить", callback_data=f"verify:reject:{request_id}")
    kb.adjust(1)
    return kb.as_markup()


def case_keyboard(case_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Закрыть", callback_data=f"case:close:{case_id}")
    kb.button(text="↩️ Разрешить фото", callback_data=f"case:restore:{case_id}")
    kb.adjust(1)
    return kb.as_markup()

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
