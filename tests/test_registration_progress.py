from handlers.registration import STEP_ORDER, _step_prompt
from keyboards.profile import photo_upload_keyboard


def test_registration_progress_bar_is_always_a_separate_single_line():
    prompt = _step_prompt("preview", "ru")
    lines = prompt.splitlines()

    assert lines[0] == f"📝 Шаг {len(STEP_ORDER)}/{len(STEP_ORDER)}"
    assert lines[1] == "🟩" * len(STEP_ORDER)


def test_photo_upload_keyboard_has_explicit_done_action():
    markup = photo_upload_keyboard("registration:photos_done")

    assert markup.inline_keyboard[0][0].callback_data == "registration:photos_done"
