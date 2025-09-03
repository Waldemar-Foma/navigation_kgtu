from telegram import ReplyKeyboardMarkup


def settings_keyboard():
    keyboard = [
        ["✏️ Изменить ФИО", "✏️ Изменить группу"],
        ["✏️ Изменить направление", "✏️ Изменить возраст"],
        ["📊 Мои данные"],
        ["🔙 Назад в меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)