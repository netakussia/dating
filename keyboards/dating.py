from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.localization import LocalizationService


def dating_keyboard(user_id: int, locale: str = "ru"):
    localizer = LocalizationService()
    kb = InlineKeyboardBuilder()
    kb.button(text=localizer.get("dating_like", locale), callback_data=f"like:{user_id}")
    kb.button(text=localizer.get("dating_comment", locale), callback_data=f"comment:{user_id}")
    kb.button(text=localizer.get("dating_skip", locale), callback_data=f"skip:{user_id}")
    kb.button(text=localizer.get("dating_report", locale), callback_data=f"report:{user_id}")
    kb.button(text=localizer.get("dating_block", locale), callback_data=f"block:{user_id}")
    kb.adjust(2, 2, 1)
    return kb.as_markup()

def choice_keyboard(prefix: str, values: list[tuple[str, str]]):
    kb = InlineKeyboardBuilder()
    for text, value in values:
        kb.button(text=text, callback_data=f"{prefix}:{value}")
    kb.adjust(2)
    return kb.as_markup()

def report_reasons_keyboard(user_id: int, locale: str = "ru"):
    localizer = LocalizationService()
    kb = InlineKeyboardBuilder()
    for code, key in [
        ("FAKE", "report_fake"),
        ("INSULT", "report_insult"),
        ("INAPPROPRIATE_CONTENT", "report_inappropriate"),
        ("NSFW", "report_nsfw"),
        ("SPAM", "report_spam"),
        ("OTHER", "report_other"),
    ]:
        kb.button(text=localizer.get(key, locale), callback_data=f"report_reason:{user_id}:{code}")
    kb.adjust(1)
    return kb.as_markup()
