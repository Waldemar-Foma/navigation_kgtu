from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from utils.constants import DIRECTIONS, GROUPS
from config import REGISTRATION_CHOICE, REGISTER_GROUP, REGISTER_AGE, REGISTER_DIRECTION, REGISTER_NAME, MAIN_MENU
from keyboards import directions_keyboard, groups_keyboard, main_menu_keyboard


db = Database()

async def registration_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    user = update.message.from_user
    
    if choice == "✅ Зарегистрироваться":
        await update.message.reply_text(
            "📝 Введите ваше ФИО (например: Иванов Иван Иванович):"
        )
        return REGISTER_NAME
    else:
        await update.message.reply_text(
            "Хорошо! Вы можете завершить регистрацию позже через настройки.\n\n"
            "Чем могу помочь?",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU

async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_name = update.message.text.strip()
    
    if len(full_name.split()) < 2:
        await update.message.reply_text(
            "Пожалуйста, введите полное ФИО (например: Иванов Иван Иванович):"
        )
        return REGISTER_NAME
    
    context.user_data['full_name'] = full_name
    
    await update.message.reply_text(
        "📝 Выберите вашу учебную группу:",
        reply_markup=groups_keyboard()
    )
    return REGISTER_GROUP

async def register_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group = update.message.text
    
    if group == "🔙 Назад":
        await update.message.reply_text(
            "📝 Введите ваше ФИО (например: Иванов Иван Иванович):"
        )
        return REGISTER_NAME
    
    if group not in GROUPS:
        await update.message.reply_text(
            "Пожалуйста, выберите группу из списка:",
            reply_markup=groups_keyboard()
        )
        return REGISTER_GROUP
    
    context.user_data['group'] = group
    
    await update.message.reply_text("🎂 Сколько вам лет?")
    return REGISTER_AGE

async def register_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        age = int(update.message.text)
        if age < 16 or age > 60:
            await update.message.reply_text("Пожалуйста, введите реальный возраст:")
            return REGISTER_AGE
        context.user_data['age'] = age
        
        await update.message.reply_text(
            "🎯 Выберите направление обучения:",
            reply_markup=directions_keyboard()
        )
        return REGISTER_DIRECTION
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число:")
        return REGISTER_AGE

async def register_direction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    direction = update.message.text
    user = update.message.from_user
    
    if direction == "🔙 Назад":
        await update.message.reply_text("🎂 Сколько вам лет?")
        return REGISTER_AGE
    
    if direction not in DIRECTIONS:
        await update.message.reply_text(
            "Пожалуйста, выберите направление из списка:",
            reply_markup=directions_keyboard()
        )
        return REGISTER_DIRECTION
    
    full_name_parts = context.user_data['full_name'].split()
    first_name = full_name_parts[1] if len(full_name_parts) > 1 else ""
    last_name = full_name_parts[0] if len(full_name_parts) > 0 else ""
    patronymic = full_name_parts[2] if len(full_name_parts) > 2 else ""
    
    db.update_user_info(
        user.id,
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        group_name=context.user_data['group'],
        age=context.user_data['age'],
        direction=direction
    )
    
    await update.message.reply_text(
        "✅ Регистрация завершена!\n\n"
        "Теперь вам доступны все функции бота:",
        reply_markup=main_menu_keyboard()
    )
    return MAIN_MENU