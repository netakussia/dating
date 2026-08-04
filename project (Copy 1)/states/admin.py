from aiogram.fsm.state import State, StatesGroup
class AdminState(StatesGroup): moderation_queue = State(); broadcast_message = State()
