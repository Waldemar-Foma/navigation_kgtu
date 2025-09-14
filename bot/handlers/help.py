from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.models import Database
from keyboards.builders import get_main_menu_kb
from config.settings import DATABASE_NAME
from handlers.registration import start_registration


router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message, state: FSMContext):
    user = message.from_user
    db = Database(DATABASE_NAME)
    await message.answer(
        "🤖 <b>Nav. bot - Помощь</b>\n\n"
        "📍 <b>Основные функции:</b>\n"
        "• Навигация по корпусам университета\n"
        "• Просмотр расписания занятий\n"
        "• Управление профилем\n\n"
        "📋 <b>Команды:</b>\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n"
        "👤 <b>Ваши данные:</b>\n"
        f"Username: @{user.username or 'не указан'}\n"
        f"ID: {user.id}\n\n"
        "📞 <b>Поддержка:</b>\n"
        "По вопросам работы бота обращайтесь к администраторам: @Waldemar_r или @strng_dev",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"

    )
    if not db.user_exists(message.from_user.id):
        await start_registration(message, state)