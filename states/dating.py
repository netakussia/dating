from aiogram.fsm.state import State, StatesGroup


class DatingState(StatesGroup):
    browsing = State()
    like_comment = State()
    report_reason = State()
