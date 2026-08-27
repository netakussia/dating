import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

from keyboards.menu import main_menu
from keyboards.profile import profile_keyboard
from middlewares.i18n import normalize_locale
from services.localization import LocalizationService
from services.notification_service import NotificationService
from services.promo_service import get_empty_discovery_promo


def test_normalize_locale_supports_telegram_variants_and_falls_back_to_russian():
    assert normalize_locale("ro-RO") == "ro"
    assert normalize_locale("en") == "ru"
    assert normalize_locale(None) == "ru"


def test_ru_and_ro_have_the_same_localization_keys():
    locale_dir = Path(__file__).parents[1] / "data" / "locales"
    with (locale_dir / "ru.json").open(encoding="utf-8") as handle:
        russian = json.load(handle)
    with (locale_dir / "ro.json").open(encoding="utf-8") as handle:
        romanian = json.load(handle)
    assert russian.keys() == romanian.keys()


def test_romanian_ui_uses_translated_labels():
    localizer = LocalizationService()
    assert localizer.get("menu_profile", "ro") == "👤 Profilul meu"
    assert main_menu("ro").keyboard[1][0].text == "👤 Profilul meu"
    assert profile_keyboard(locale="ro").inline_keyboard[-1][0].text == "🌐 Язык / Limba"


def test_romanian_dating_and_empty_state_are_translated():
    from keyboards.dating import dating_keyboard

    assert dating_keyboard(7, "ro").inline_keyboard[0][0].text == "❤️ Îmi place"
    promo = get_empty_discovery_promo(7, locale="ro")
    assert promo["title"] == "Totul este în regulă"
    assert promo["button_text"] == "🔄 Reîmprospătează lista"


def test_help_verification_and_profile_status_keys_are_translated():
    localizer = LocalizationService()
    assert "Ajutor" in localizer.get("help_text", "ro")
    assert "verificat" in localizer.get("verification_verified", "ro").lower()
    assert localizer.get("profile_verified", "ro") == "🟢 Verificat"
    assert "Profilul este ascuns" in localizer.get("profile_moderation_hidden", "ro")


def test_format_returns_unformatted_template_when_placeholder_is_missing():
    localizer = LocalizationService()
    assert localizer.format("notification_like_comment", "ru") == "💌 Кому-то понравилась ваша анкета.\n\n{comment}"
    assert localizer.format("notification_like_comment", "ru", wrong_name="x").endswith("{comment}")


async def test_notification_uses_recipient_profile_locale():
    bot = SimpleNamespace(send_message=AsyncMock())
    session = SimpleNamespace(
        scalar=AsyncMock(return_value=SimpleNamespace(locale="ro")),
    )
    await NotificationService(bot).safe_send_localized(7, session, "notification_like")
    bot.send_message.assert_awaited_once_with(7, "💌 Cineva a apreciat profilul tău.", reply_markup=None)