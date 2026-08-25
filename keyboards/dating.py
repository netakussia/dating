from aiogram.utils.keyboard import InlineKeyboardBuilder


def dating_keyboard(user_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="❤️ Нравится", callback_data=f"like:{user_id}")
    kb.button(text="💌 Написать", callback_data=f"comment:{user_id}")
    kb.button(text="⏭️ Пропустить", callback_data=f"skip:{user_id}")
    kb.button(text="🚩 Пожаловаться", callback_data=f"report:{user_id}")
    kb.button(text="🚫 Заблокировать", callback_data=f"block:{user_id}")
    kb.adjust(2, 2, 1)
    return kb.as_markup()

def choice_keyboard(prefix: str, values: list[tuple[str, str]]):
    kb = InlineKeyboardBuilder()
    for text, value in values:
        kb.button(text=text, callback_data=f"{prefix}:{value}")
    kb.adjust(2)
    return kb.as_markup()

def report_reasons_keyboard(user_id: int):
    kb = InlineKeyboardBuilder()
    for code, label in [
        ("FAKE", "Фейк"),
        ("INSULT", "Оскорбления"),
        ("INAPPROPRIATE_CONTENT", "Неприемлемый контент"),
        ("NSFW", "18+ контент"),
        ("SPAM", "Спам"),
        ("OTHER", "Другое"),
    ]:
        kb.button(text=label, callback_data=f"report_reason:{user_id}:{code}")
    kb.adjust(1)
    return kb.as_markup()
