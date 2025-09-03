from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from utils.constants import BUILDINGS
from config import MAIN_MENU, SETTINGS, ASKING_LOCATION
from keyboards import main_menu_keyboard
from handlers.help import show_help


db = Database()

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    
    if text == "⚙️ Настройки":
        from keyboards import settings_keyboard
        await update.message.reply_text(
            "⚙️ Настройки профиля:",
            reply_markup=settings_keyboard()
        )
        return SETTINGS
    elif text == "🏢 Сменить корпус":
        await update.message.reply_text(
            "📍 Отправьте вашу геопозицию или выберите корпус вручную:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [{"text": "📍 Отправить геолокацию", "request_location": True}],
                    *[[building] for building in BUILDINGS.keys()],
                    ["🔙 Назад"]
                ],
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
        return ASKING_LOCATION
    elif text == "📚 Расписание":
        user_info = db.get_user_info(user.id)
        if user_info and user_info[5]:  # group
            schedule = db.get_schedule(user_info[5])
            if schedule:
                await update.message.reply_text(
                    f"📚 Расписание для группы {user_info[5]}:\n\n{schedule}",
                    reply_markup=main_menu_keyboard()
                )
            else:
                await update.message.reply_text(
                    "❌ Расписание для вашей группы не найдено.",
                    reply_markup=main_menu_keyboard()
                )
        else:
            await update.message.reply_text(
                "❌ Сначала укажите вашу группу в настройках.",
                reply_markup=main_menu_keyboard()
            )
        return MAIN_MENU
    elif text == "📍 Навигация по корпусу":
        current_building = db.get_user_building(user.id)
        if current_building:
            await update.message.reply_text(
                f"🏢 Вы находитесь в корпусе: <b>{current_building}</b>\n\n"
                "Здесь вы можете:\n"
                "• Найти аудиторию\n"
                "• Посмотреть план этажа\n"
                "• Найти деканат\n\n"
                "🚧 Функция навигации в разработке...",
                parse_mode='HTML',
                reply_markup=main_menu_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Сначала укажите ваш корпус.",
                reply_markup=main_menu_keyboard()
            )
        return MAIN_MENU
    elif text == "❓ Помощь":
        await show_help(update, context)
        return MAIN_MENU
    elif text == "🔙 Назад":
        await update.message.reply_text(
            "Главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
    else:
        await update.message.reply_text(
            "Неизвестная команда. Выберите вариант из меню:",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
