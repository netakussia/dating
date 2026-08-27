from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.localization import LocalizationService

_localizer = LocalizationService()
MENU_LABEL_KEYS = (
    "menu_dating", "menu_likes", "menu_profile", "menu_verification",
    "menu_confession", "menu_appeal", "menu_help",
)
MENU_LABELS = frozenset(_localizer.get(key, locale) for locale in ("ru", "ro") for key in MENU_LABEL_KEYS)
MENU_HELP_LABELS = frozenset(_localizer.get("menu_help", locale) for locale in ("ru", "ro"))
MENU_DATING_LABELS = frozenset(_localizer.get("menu_dating", locale) for locale in ("ru", "ro"))
MENU_PROFILE_LABELS = frozenset(_localizer.get("menu_profile", locale) for locale in ("ru", "ro"))
MENU_CONFESSION_LABELS = frozenset(_localizer.get("menu_confession", locale) for locale in ("ru", "ro"))
MENU_VERIFICATION_LABELS = frozenset(_localizer.get("menu_verification", locale) for locale in ("ru", "ro"))


def main_menu(locale: str = "ru") -> ReplyKeyboardMarkup:
    text = LocalizationService().get
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text("menu_dating", locale)), KeyboardButton(text=text("menu_likes", locale))],
            [KeyboardButton(text=text("menu_profile", locale)), KeyboardButton(text=text("menu_verification", locale))],
            [KeyboardButton(text=text("menu_confession", locale)), KeyboardButton(text=text("menu_appeal", locale))],
            [KeyboardButton(text=text("menu_help", locale))],
        ],
        resize_keyboard=True,
    )