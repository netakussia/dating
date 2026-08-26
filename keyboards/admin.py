from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard(role_can_manage_admins: bool = False):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛡 Модерация", callback_data="admin:section:moderation")
    kb.button(text="👤 Пользователи", callback_data="admin:section:users")
    kb.button(text="📊 Статистика", callback_data="admin:section:stats")
    kb.button(text="👤 Просмотр анкет", callback_data="admin:browse")
    if role_can_manage_admins:
        kb.button(text="⚙️ Администрирование", callback_data="admin:section:administration")
    kb.adjust(1)
    return kb.as_markup()


def admin_moderation_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📢 Жалобы", callback_data="admin:reports")
    kb.button(text="🖼️ Фото на проверку", callback_data="admin:nsfw")
    kb.button(text="🛡 Верификация", callback_data="admin:verifications")
    kb.button(text="⚖️ Апелляции", callback_data="admin:appeals")
    kb.button(text="📌 Мои кейсы", callback_data="admin:my_cases")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_users_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔎 Просмотр анкет", callback_data="admin:browse")
    kb.button(text="🚫 Заблокированные", callback_data="admin:blocked")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_stats_keyboard(can_view_history: bool = True):
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Общая статистика", callback_data="admin:trust_stats")
    if can_view_history:
        kb.button(text="📜 История решений", callback_data="admin:trust_history")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_administration_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📣 Рассылка", callback_data="admin:broadcast")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_nav_keyboard(
    next_callback: str | None = None,
    back_callback: str = "admin:menu",
    refresh_callback: str | None = None,
    prev_callback: str | None = None,
):
    kb = InlineKeyboardBuilder()
    if refresh_callback:
        kb.button(text="🔄 Обновить", callback_data=refresh_callback)
    if prev_callback:
        kb.button(text="⬅️ Предыдущий", callback_data=prev_callback)
    if next_callback:
        kb.button(text="➡️ Следующий", callback_data=next_callback)
    kb.button(text="⬅️ Назад", callback_data=back_callback)
    kb.button(text="🏠 Главное меню", callback_data="admin:menu")
    kb.adjust(2 if refresh_callback or next_callback or prev_callback else 1)
    return kb.as_markup()


def browse_nav_keyboard(current_user_id: int | None = None):
    next_callback = "admin:browse:next" if current_user_id is None else f"admin:browse:next:{current_user_id}"
    return admin_nav_keyboard(
        next_callback=next_callback,
        back_callback="admin:section:users",
        refresh_callback="admin:browse",
    )


def verification_keyboard(request_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять заявку", callback_data=f"verify:claim:{request_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def verification_decision_keyboard(request_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data=f"verify:approve:{request_id}")
    kb.button(text="🔁 Запросить повтор", callback_data=f"verify:retake:{request_id}")
    kb.button(text="❌ Отклонить", callback_data=f"verify:reject:{request_id}")
    kb.button(text="↩️ Освободить", callback_data=f"verify:release:{request_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def case_keyboard(case_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять кейс", callback_data=f"case:claim:{case_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def case_decision_keyboard(case_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Одобрить фото", callback_data=f"case:restore:{case_id}")
    kb.button(text="✍️ Запросить замену", callback_data=f"case:retake:{case_id}")
    kb.button(text="❌ Отклонить кейс", callback_data=f"case:reject:{case_id}")
    kb.button(text="↩️ Освободить", callback_data=f"case:release:{case_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def moderation_keyboard(report_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять жалобу", callback_data=f"moderate:claim:{report_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def moderation_decision_keyboard(report_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🚫 Заблокировать пользователя", callback_data=f"moderate:prompt:ban:{report_id}")
    kb.button(text="⏸ Скрыть анкету", callback_data=f"moderate:prompt:hide:{report_id}")
    kb.button(text="✅ Отклонить жалобу", callback_data=f"moderate:prompt:dismiss:{report_id}")
    kb.button(text="↩️ Освободить", callback_data=f"moderate:release:{report_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def appeal_keyboard(appeal_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять апелляцию", callback_data=f"appeal:claim:{appeal_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def appeal_decision_keyboard(appeal_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Написать пользователю", callback_data=f"appeal:reply:{appeal_id}")
    kb.button(text="✅ Одобрить апелляцию", callback_data=f"appeal:prompt:restore:{appeal_id}")
    kb.button(text="❌ Отклонить апелляцию", callback_data=f"appeal:prompt:reject:{appeal_id}")
    kb.button(text="↩️ Освободить", callback_data=f"appeal:release:{appeal_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def profile_moderation_keyboard(
    user_id: int,
    next_callback: str | None = None,
    can_unban: bool = False,
    is_banned: bool = False,
    is_frozen: bool = False,
):
    kb = InlineKeyboardBuilder()
    if next_callback:
        kb.button(text="➡️ Следующая", callback_data=next_callback)

    if is_banned:
        if can_unban:
            kb.button(text="✅ Разблокировать", callback_data=f"profilemod:prompt:unban:{user_id}")
    else:
        kb.button(text="🚫 Заблокировать", callback_data=f"profilemod:prompt:ban:{user_id}")

        if is_frozen:
            if can_unban:
                kb.button(text="▶️ Разморозить", callback_data=f"profilemod:prompt:unfreeze:{user_id}")
        else:
            kb.button(text="⏸ Заморозить", callback_data=f"profilemod:prompt:freeze:{user_id}")

    kb.button(text="⬅️ Назад", callback_data="admin:section:users")
    kb.button(text="🏠 В меню", callback_data="admin:menu")
    kb.adjust(2)
    return kb.as_markup()


def confirm_action_keyboard(confirm_data: str, back_data: str = "admin:menu"):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data=confirm_data)
    kb.button(text="❌ Отмена", callback_data=back_data)
    kb.adjust(2)
    return kb.as_markup()


def my_cases_keyboard(items: list[tuple[str, str]] | None = None):
    kb = InlineKeyboardBuilder()
    if items:
        for title, callback_data in items:
            kb.button(text=title, callback_data=callback_data)
    kb.button(text="🔄 Обновить", callback_data="admin:my_cases")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.button(text="🏠 Главное меню", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()
