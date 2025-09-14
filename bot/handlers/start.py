from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.models import Database
from keyboards.builders import get_main_menu_kb
from config.settings import DATABASE_NAME
from handlers.registration import start_registration

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    db = Database(DATABASE_NAME)

    if db.user_exists(message.from_user.id):
        await message.answer(
            "Добро пожаловать! Выберите действие:",
            reply_markup=get_main_menu_kb()
        )
    else:
        await start_registration(message, state)