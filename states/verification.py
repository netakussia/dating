from aiogram.fsm.state import State, StatesGroup


class VerificationState(StatesGroup):
    waiting_video = State()
