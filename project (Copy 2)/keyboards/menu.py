from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="💘 Знакомства"), KeyboardButton(text="❤️ Симпатии")], [KeyboardButton(text="👤 Моя анкета"), KeyboardButton(text="💌 Признание")], [KeyboardButton(text="🆘 Апелляция"), KeyboardButton(text="❓ Помощь")]], resize_keyboard=True)
