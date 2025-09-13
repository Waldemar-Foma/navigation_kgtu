from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from bot.config.settings import DATABASE_NAME
from bot.database.models import Database

router = Router()

@router.message()
async def exception_message(message: types.Message, state: FSMContext):
    user = message.from_user
    db = Database(DATABASE_NAME)

    await message.answer("Простите я не понимаю, пожалуйста используйте команду /start, если бот сломался" if db.user_exists(user.id) else "Простите я не понимаю, пожалуйста используйте команду /start, чтобы пройти регистрацию или если бот сломался")
