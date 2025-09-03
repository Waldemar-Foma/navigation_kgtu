from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from utils.constants import DIRECTIONS, GROUPS
from config import SETTINGS, MAIN_MENU
from keyboards import settings_keyboard, directions_keyboard, groups_keyboard, main_menu_keyboard


db = Database()

async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    
    if text == "✏️ Изменить группу":
        await update.message.reply_text(
            "Выберите новую группу:",
            reply_markup=groups_keyboard()
        )
        context.user_data['setting'] = 'group'
        return SETTINGS
    elif text == "✏️ Изменить направление":
        await update.message.reply_text(
            "Выберите новое направление:",
            reply_markup=directions_keyboard()
        )
        context.user_data['setting'] = 'direction'
        return SETTINGS
    elif text == "✏️ Изменить возраст":
        await update.message.reply_text("Введите новый возраст:")
        context.user_data['setting'] = 'age'
        return SETTINGS
    elif text == "✏️ Изменить ФИО":
        await update.message.reply_text("Введите новое ФИО (например: Иванов Иван Иванович):")
        context.user_data['setting'] = 'name'
        return SETTINGS
    elif text == "📊 Мои данные":
        user_info = db.get_user_info(user.id)
        if user_info:
            full_name = f"{user_info[3] or ''} {user_info[2] or ''} {user_info[4] or ''}".strip()
            
            await update.message.reply_text(
                f"📊 <b>Ваши данные:</b>\n\n"
                f"👤 ФИО: {full_name or 'Не указано'}\n"
                f"📚 Группа: {user_info[5] or 'Не указана'}\n"
                f"🎂 Возраст: {user_info[6] or 'Не указан'}\n"
                f"🎯 Направление: {user_info[7] or 'Не указано'}\n"
                f"🏢 Текущий корпус: {user_info[8] or 'Не указан'}\n"
                f"📅 Регистрация: {user_info[9].split()[0] if user_info[9] else 'Не завершена'}\n\n"
                f"🔗 Username: @{user_info[1] or 'не указан'}",
                parse_mode='HTML',
                reply_markup=settings_keyboard()
            )
        return SETTINGS
    elif text == "🔙 Назад в меню":
        await update.message.reply_text(
            "Главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return MAIN_MENU
    else:
        setting = context.user_data.get('setting')
        if setting == 'group':
            if text in GROUPS:
                db.update_user_info(user.id, group_name=text)
                await update.message.reply_text(
                    "✅ Группа обновлена!",
                    reply_markup=settings_keyboard()
                )
            else:
                await update.message.reply_text(
                    "Пожалуйста, выберите группу из списка:",
                    reply_markup=groups_keyboard()
                )
                return SETTINGS
        elif setting == 'age':
            try:
                age = int(text)
                db.update_user_info(user.id, age=age)
                await update.message.reply_text(
                    "✅ Возраст обновлен!",
                    reply_markup=settings_keyboard()
                )
            except ValueError:
                await update.message.reply_text("Пожалуйста, введите число:")
                return SETTINGS
        elif setting == 'direction':
            if text in DIRECTIONS:
                db.update_user_info(user.id, direction=text)
                await update.message.reply_text(
                    "✅ Направление обновлено!",
                    reply_markup=settings_keyboard()
                )
            else:
                await update.message.reply_text(
                    "Пожалуйста, выберите направление из списка:",
                    reply_markup=directions_keyboard()
                )
                return SETTINGS
        elif setting == 'name':
            full_name = text.strip()
            if len(full_name.split()) < 2:
                await update.message.reply_text("Пожалуйста, введите полное ФИО (например: Иванов Иван Иванович):")
                return SETTINGS
            
            name_parts = full_name.split()
            first_name = name_parts[1] if len(name_parts) > 1 else ""
            last_name = name_parts[0] if len(name_parts) > 0 else ""
            patronymic = name_parts[2] if len(name_parts) > 2 else ""
            
            db.update_user_info(
                user.id,
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic
            )
            await update.message.reply_text(
                "✅ ФИО обновлено!",
                reply_markup=settings_keyboard()
            )
        
        context.user_data.pop('setting', None)
        return SETTINGS
