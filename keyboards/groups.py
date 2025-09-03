from telegram import ReplyKeyboardMarkup
from utils.constants import GROUPS


def groups_keyboard():
    keyboard = []
    for i in range(0, len(GROUPS), 2):
        row = GROUPS[i:i+2]
        keyboard.append(row)
    keyboard.append(["🔙 Назад"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
