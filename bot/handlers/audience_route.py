from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.config.settings import DATABASE_NAME
from bot.database.models import Database
from bot.utils.formatters import format_profile

router = Router()

@router.message(F.text == "📍 Найти аудиторию")
async def get_start_point(message: types.Message, state: FSMContext):
    db = Database(DATABASE_NAME)

    user_data = db.get_user_dict(message.from_user.id)
    print(user_data)

    if user_data:
        print(user_data)
    else:
        await message.answer("Профиль не найден. Пройдите регистрацию.")

