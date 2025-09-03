from telegram import ReplyKeyboardMarkup


def main_menu_keyboard():
    keyboard = [
        ["📍 Навигация по корпусу", "📚 Расписание"],
        ["⚙️ Настройки", "❓ Помощь"],
        ["🏢 Сменить корпус"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)