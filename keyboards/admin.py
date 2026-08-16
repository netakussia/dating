from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🛡 Верификация", callback_data="admin:verifications")
    kb.button(text="📢 Жалобы", callback_data="admin:reports")
    kb.button(text="🖼️ Фото на проверку", callback_data="admin:nsfw")
    kb.button(text="🚫 Заблокированные", callback_data="admin:blocked")
    kb.button(text="⚖️ Апелляции", callback_data="admin:appeals")
    kb.button(text="📜 История решений", callback_data="admin:trust_history")
    kb.button(text="📊 Статистика", callback_data="admin:trust_stats")
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
    kb.button(text="✅ Одобрить фото", callback_data=f"case:restore:{case_id}")
    kb.button(text="✍️ Запросить замену", callback_data=f"case:retake:{case_id}")
    kb.adjust(1)
    return kb.as_markup()


def moderation_keyboard(report_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🚫 Заблокировать пользователя", callback_data=f"moderate:prompt:ban:{report_id}")
    kb.button(text="⏸ Скрыть анкету", callback_data=f"moderate:prompt:hide:{report_id}")
    kb.button(text="✅ Отклонить жалобу", callback_data=f"moderate:prompt:dismiss:{report_id}")
    kb.adjust(1)
    return kb.as_markup()


def appeal_keyboard(appeal_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Ответить", callback_data=f"appeal:reply:{appeal_id}")
    kb.button(text="✅ Разрешить апелляцию", callback_data=f"appeal:restore:{appeal_id}")
    kb.button(text="❌ Отклонить апелляцию", callback_data=f"appeal:prompt:reject:{appeal_id}")
    kb.adjust(1)
    return kb.as_markup()


def confirm_action_keyboard(confirm_data: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data=confirm_data)
    kb.button(text="❌ Отмена", callback_data="admin:reports")
    kb.adjust(2)
    return kb.as_markup()
