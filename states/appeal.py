from aiogram.fsm.state import State, StatesGroup


class AppealState(StatesGroup):
    enter_text = State()
