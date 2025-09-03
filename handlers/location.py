from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from utils.distance import find_nearest_building
from utils.constants import BUILDINGS
from config import CONFIRMING_BUILDING, MAIN_MENU, REGISTRATION_CHOICE, ASKING_LOCATION, MANUAL_BUILDING_SELECTION, WAITING_LOCATION
from keyboards import main_menu_keyboard


db = Database()

async def handle_manual_building_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    user = update.message.from_user

    if user_response == "🏢 Выбрать корпус вручную":
        await update.message.reply_text(
            "🏢 Выберите ваш корпус из списка:",
            reply_markup=ReplyKeyboardMarkup(
                [[building] for building in BUILDINGS.keys()] + [["🔙 Назад"]],
                resize_keyboard=True
            )
        )
        return MANUAL_BUILDING_SELECTION
    elif user_response == "📍 Отправить геолокацию":
        await update.message.reply_text(
            "Отправьте свою геопозицию:",
            reply_markup=ReplyKeyboardMarkup(
                [[{"text": "📍 Отправить геолокацию", "request_location": True}]],
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
        return ASKING_LOCATION
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите один из вариантов:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [{"text": "📍 Отправить геолокацию", "request_location": True}],
                    ["🏢 Выбрать корпус вручную"]
                ],
                resize_keyboard=True
            )
        )
        return WAITING_LOCATION

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    location = update.message.location

    nearest_building, distance = find_nearest_building(
        location.latitude, location.longitude, BUILDINGS
    )
    context.user_data['nearest_building'] = nearest_building
    context.user_data['user_location'] = (location.latitude, location.longitude)

    await update.message.reply_text(
        f"📍 Ближайший корпус: <b>{nearest_building}</b>\n"
        f"📏 Расстояние: {distance:.0f} метров\n\n"
        "Вы действительно находитесь в этом корпусе?",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(
            [["✅ Да", "❌ Нет"], ["📍 Отправить новую геолокацию"]],
            resize_keyboard=True
        )
    )
    return CONFIRMING_BUILDING


async def confirm_building(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.message.text
    user = update.message.from_user

    if user_response == "📍 Отправить новую геолокацию":
        await update.message.reply_text(
            "Отправьте свою новую геопозицию:",
            reply_markup=ReplyKeyboardMarkup(
                [[{"text": "📍 Отправить геолокацию", "request_location": True}]],
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
        return ASKING_LOCATION

    if user_response == "✅ Да":
        building = context.user_data.get('nearest_building')
        if building:
            db.update_user_info(user.id, current_building=building)

            if db.is_user_registered(user.id):
                await update.message.reply_text(
                    f"🏢 Отлично! Вы в корпусе: <b>{building}</b>\n\n"
                    "Чем могу помочь?",
                    parse_mode='HTML',
                    reply_markup=main_menu_keyboard()
                )
                return MAIN_MENU
            else:
                await update.message.reply_text(
                    "📝 Давайте завершим регистрацию!\n\n"
                    "Хотите пройти регистрацию сейчас?",
                    reply_markup=ReplyKeyboardMarkup(
                        [["✅ Зарегистрироваться", "⏰ Позже"]],
                        resize_keyboard=True
                    )
                )
                return REGISTRATION_CHOICE

    await update.message.reply_text(
        "Выберите ваш корпус вручную или отправьте новую геолокацию:",
        reply_markup=ReplyKeyboardMarkup(
            [[building] for building in BUILDINGS.keys()] + [["📍 Отправить новую геолокацию"]],
            resize_keyboard=True
        )
    )
    return CONFIRMING_BUILDING


async def handle_manual_building_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    selected_building = update.message.text

    if selected_building == "🔙 Назад":
        await update.message.reply_text(
            "📍 Для определения ближайшего корпуса отправьте вашу геопозицию "
            "или выберите корпус вручную:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [{"text": "📍 Отправить геолокацию", "request_location": True}],
                    ["🏢 Выбрать корпус вручную"]
                ],
                resize_keyboard=True
            )
        )
        return WAITING_LOCATION

    if selected_building in BUILDINGS:
        db.update_user_info(user.id, current_building=selected_building)

        if db.is_user_registered(user.id):
            await update.message.reply_text(
                f"🏢 Корпус установлен: <b>{selected_building}</b>\n\n"
                "Чем могу помочь?",
                parse_mode='HTML',
                reply_markup=main_menu_keyboard()
            )
            return MAIN_MENU
        else:
            await update.message.reply_text(
                "📝 Давайте завершим регистрацию!\n\n"
                "Хотите пройти регистрацию сейчас?",
                reply_markup=ReplyKeyboardMarkup(
                    [["✅ Зарегистрироваться", "⏰ Позже"]],
                    resize_keyboard=True
                )
            )
            return REGISTRATION_CHOICE

    await update.message.reply_text(
        "Пожалуйста, выберите корпус из списка:",
        reply_markup=ReplyKeyboardMarkup(
            [[building] for building in BUILDINGS.keys()] + [["🔙 Назад"]],
            resize_keyboard=True
        )
    )
    return MANUAL_BUILDING_SELECTION
