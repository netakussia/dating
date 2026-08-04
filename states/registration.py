from aiogram.fsm.state import State, StatesGroup
class RegistrationState(StatesGroup):
    gender = State(); target_gender = State(); name = State(); age = State(); district = State(); institution = State(); interests = State(); bio = State(); photo = State(); confirmation = State()
