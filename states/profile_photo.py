from aiogram.fsm.state import State, StatesGroup


class ProfilePhotoState(StatesGroup):
    waiting_photo = State()
    awaiting_manual_review = State()
