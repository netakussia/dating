from aiogram.fsm.state import State, StatesGroup


class ConfessionState(StatesGroup):
    recipient = State()
    text = State()
    confirm = State()
