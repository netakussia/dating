from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

DOCUMENT_LABELS = {
    "terms": "📄 Условия использования",
    "privacy": "🔐 Политика конфиденциальности",
    "community": "🛡 Правила сообщества",
    "safety": "🚨 Безопасность знакомств",
    "moderation": "⚖️ Модерация и апелляции",
    "alpha": "📌 Альфа-статус",
}

DOCUMENT_LABELS_RO = {
    "terms": "📄 Termeni de utilizare",
    "privacy": "🔐 Politica de confidențialitate",
    "community": "🛡 Regulile comunității",
    "safety": "🚨 Siguranța întâlnirilor",
    "moderation": "⚖️ Moderare și contestații",
    "alpha": "📌 Statut alfa",
}


def documents_keyboard(*keys: str, include_continue: bool = False, locale: str = "ru") -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    from config import get_settings

    settings = get_settings()
    current: list[InlineKeyboardButton] = []
    for key in keys:
        url = settings.document_urls[key]
        labels = DOCUMENT_LABELS_RO if locale == "ro" else DOCUMENT_LABELS
        current.append(InlineKeyboardButton(text=labels[key], url=url))
        if len(current) == 2:
            rows.append(current)
            current = []
    if current:
        rows.append(current)
    if include_continue:
        continue_text = "✅ Continuă" if locale == "ro" else "✅ Продолжить"
        rows.append([InlineKeyboardButton(text=continue_text, callback_data="legal:accept")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
