from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

DOCUMENT_LABELS = {
    "terms": "📄 Условия использования",
    "privacy": "🔐 Политика конфиденциальности",
    "community": "🛡 Правила сообщества",
    "safety": "🚨 Безопасность знакомств",
    "moderation": "⚖️ Модерация и апелляции",
    "alpha": "📌 Альфа-статус",
}


def documents_keyboard(*keys: str, include_continue: bool = False) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    from config import get_settings

    settings = get_settings()
    current: list[InlineKeyboardButton] = []
    for key in keys:
        url = settings.document_urls[key]
        current.append(InlineKeyboardButton(text=DOCUMENT_LABELS[key], url=url))
        if len(current) == 2:
            rows.append(current)
            current = []
    if current:
        rows.append(current)
    if include_continue:
        rows.append([InlineKeyboardButton(text="✅ Продолжить", callback_data="legal:accept")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
