from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💘 Смотреть анкеты"), KeyboardButton(text="💕 Мои симпатии")],
            [KeyboardButton(text="👤 Моя анкета"), KeyboardButton(text="🛡 Верификация")],
            [KeyboardButton(text="💌 Признание"), KeyboardButton(text="🆘 Апелляция")],
            [KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True,
    )
