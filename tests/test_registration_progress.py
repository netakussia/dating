from handlers.registration import STEP_ORDER, _step_prompt


def test_registration_progress_bar_is_always_a_separate_single_line():
    prompt = _step_prompt("preview", "ru")
    lines = prompt.splitlines()

    assert lines[0] == f"📝 Шаг {len(STEP_ORDER)}/{len(STEP_ORDER)}"
    assert lines[1] == "🟩" * len(STEP_ORDER)
