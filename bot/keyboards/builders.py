from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
from config.constants import INSTITUTES, BUILDINGS

def get_main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📍 Найти аудиторию"))
    builder.add(KeyboardButton(text="👤 Мой профиль"))
    builder.add(KeyboardButton(text="✏️ Редактировать профиль"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_institutes_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for institute in INSTITUTES.keys():
        builder.add(KeyboardButton(text=institute))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_specialities_kb(institute: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for speciality in INSTITUTES.get(institute, []):
        builder.add(KeyboardButton(text=speciality))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_location_method_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📍 Определить автоматически"))
    builder.add(KeyboardButton(text="🗺️ Выбрать вручную"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_location_request_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="📍 Отправить местоположение",
        request_location=True
    ))
    builder.add(KeyboardButton(text="↩️ Назад к выбору метода"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_confirm_location_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="✅ Да, верно"))
    builder.add(KeyboardButton(text="🔄 Отправить снова"))
    builder.add(KeyboardButton(text="🗺️ Выбрать вручную"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_buildings_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for building in BUILDINGS:
        builder.add(KeyboardButton(text=building))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_edit_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="ФИО", callback_data="edit_full_name")
    builder.button(text="Институт", callback_data="edit_institute")
    builder.button(text="Специальность", callback_data="edit_speciality")
    builder.button(text="Местоположение", callback_data="edit_location")
    builder.adjust(1)
    return builder.as_markup()