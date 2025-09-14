import asyncio
import logging
from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from handlers.start import router as start_router
from handlers.registration import router as registration_router
from handlers.profile import router as profile_router
from handlers.help import router as help_router
from handlers.audience_route import router as audience_route_router
from handlers.exception import router as exception_router

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(registration_router)
    dp.include_router(profile_router)
    dp.include_router(audience_route_router)
    dp.include_router(exception_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())