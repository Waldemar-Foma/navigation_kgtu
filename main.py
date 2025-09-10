import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers.start import router as start_router
from handlers.registration import router as registration_router
from handlers.profile import router as profile_router

# Конфигурация
BOT_TOKEN = "8415484392:AAGQ1ITwzTq1HrHWKl894ojlT2f8usv9w1w"


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(profile_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())