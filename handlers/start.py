from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from config import WAITING_LOCATION, ASKING_LOCATION
from utils.constants import BUILDINGS


db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    context.user_data.clear()
    context.user_data["started"] = True

    db.add_user(user.id, user.username, user.first_name, user.last_name)

    await update.message.reply_text(
        f"👋 Добро пожаловать, {user.first_name}!\n\n"
        "📍 Для определения ближайшего корпуса отправьте вашу геопозицию "
        "или выберите корпус вручную:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [{"text": "📍 Отправить геолокацию", "request_location": True}],
                ["🏢 Выбрать корпус вручную"],
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return WAITING_LOCATION

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await start(update, context)
