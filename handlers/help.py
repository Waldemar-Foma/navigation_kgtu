from telegram import Update
from telegram.ext import ContextTypes
from config import MAIN_MENU
from keyboards import main_menu_keyboard

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    help_text = (
        "🤖 <b>Nav. bot - Помощь</b>\n\n"
        "📍 <b>Основные функции:</b>\n"
        "• Навигация по корпусам университета\n"
        "• Просмотр расписания занятий\n"
        "• Управление профилем\n\n"
        "📋 <b>Команды:</b>\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n"
        "/cancel - Отменить текущее действие\n\n"
        "👤 <b>Ваши данные:</b>\n"
        f"Username: @{user.username or 'не указан'}\n"
        f"ID: {user.id}\n\n"
        "📞 <b>Поддержка:</b>\n"
        "По вопросам работы бота обращайтесь к администратору – @Waldemar_r"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode='HTML',
        reply_markup=main_menu_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_help(update, context)
    return MAIN_MENU