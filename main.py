import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
from config import (
    TOKEN,
    WAITING_LOCATION,
    ASKING_LOCATION,
    CONFIRMING_BUILDING,
    REGISTRATION_CHOICE,
    REGISTER_GROUP,
    REGISTER_AGE,
    REGISTER_DIRECTION,
    REGISTER_NAME,
    MAIN_MENU,
    SETTINGS,
    MANUAL_BUILDING_SELECTION
)
from handlers import (
    start_command,
    handle_location,
    confirm_building,
    handle_manual_building_selection,
    registration_choice,
    register_group,
    register_age,
    register_direction,
    register_name,
    main_menu,
    settings_menu,
    help_command,
    handle_manual_building_choice
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Диалог прерван. Используйте /start для начала работы.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            WAITING_LOCATION: [
                MessageHandler(filters.LOCATION, handle_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_manual_building_choice)
            ],

            ASKING_LOCATION: [
                MessageHandler(filters.LOCATION, handle_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_manual_building_selection)
            ],

            CONFIRMING_BUILDING: [
                MessageHandler(filters.LOCATION, handle_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_building)
            ],

            MANUAL_BUILDING_SELECTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_manual_building_selection)
            ],

            REGISTRATION_CHOICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, registration_choice)
            ],

            REGISTER_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)
            ],

            REGISTER_GROUP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_group)
            ],

            REGISTER_AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_age)
            ],

            REGISTER_DIRECTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, register_direction)
            ],

            MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)
            ],

            SETTINGS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, settings_menu)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('help', help_command)
        ],
        allow_reentry=True,
        per_message=False
    )

    application.add_handler(conv_handler)

    logger.info("Бот запущен")
    application.run_polling()


if __name__ == '__main__':
    main()