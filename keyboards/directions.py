from telegram import ReplyKeyboardMarkup
from utils.constants import DIRECTIONS


def directions_keyboard():
    keyboard = []
    for i in range(0, len(DIRECTIONS), 2):
        row = DIRECTIONS[i:i+2]
        keyboard.append(row)
    keyboard.append(["🔙 Назад"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)