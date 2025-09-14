from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database.models import Database
from states.forms import EditProfile
from keyboards.builders import (
    get_main_menu_kb, get_institutes_kb, get_specialities_kb,
    get_location_method_kb, get_location_request_kb,
    get_confirm_location_kb, get_buildings_kb, get_edit_profile_kb
)
from utils.formatters import format_profile, format_profile_dict, user_data_to_dict
from utils.geolocation import find_nearest_building
from config.constants import INSTITUTES, BUILDINGS
from config.settings import DATABASE_NAME

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def show_profile(message: types.Message):
    db = Database(DATABASE_NAME)

    # Получаем данные в формате словаря
    user_data_dict = db.get_user_dict(message.from_user.id)

    if user_data_dict:
        await message.answer(format_profile_dict(user_data_dict))
    else:
        await message.answer("Профиль не найден. Пройдите регистрацию.")


@router.message(F.text == "✏️ Редактировать профиль")
async def edit_profile(message: types.Message):
    await message.answer(
        "Что вы хотите изменить?",
        reply_markup=get_edit_profile_kb()
    )


@router.callback_query(F.data.startswith("edit_"))
async def process_edit(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]

    db = Database(DATABASE_NAME)
    # Получаем данные в формате словаря
    user_data_dict = db.get_user_dict(callback.from_user.id)

    if not user_data_dict:
        await callback.message.answer("Профиль не найден. Пройдите регистрацию.")
        await callback.answer()
        return

    if action == "full_name":
        await state.set_state(EditProfile.full_name)
        await callback.message.answer("Введите новое ФИО:")
    elif action == "institute":
        await state.set_state(EditProfile.institute)
        await callback.message.answer("Выберите новый институт:", reply_markup=get_institutes_kb())
    elif action == "speciality":
        await state.update_data(current_institute=user_data_dict['institute'])
        await state.set_state(EditProfile.speciality)
        await callback.message.answer(
            "Выберите новую специальность:",
            reply_markup=get_specialities_kb(user_data_dict['institute'])
        )
    elif action == "location":
        await state.set_state(EditProfile.location_method)
        await callback.message.answer(
            "Как вы хотите определить ваше местоположение?",
            reply_markup=get_location_method_kb()
        )

    await callback.answer()


@router.message(EditProfile.full_name)
async def update_full_name(message: types.Message, state: FSMContext):
    db = Database(DATABASE_NAME)
    db.update_user_field(message.from_user.id, "full_name", message.text)
    await state.clear()
    await message.answer("ФИО обновлено!", reply_markup=get_main_menu_kb())


@router.message(EditProfile.institute)
async def update_institute(message: types.Message, state: FSMContext):
    if message.text not in INSTITUTES:
        await message.answer("Пожалуйста, выберите институт из списка:")
        return

    db = Database(DATABASE_NAME)
    db.update_user_field(message.from_user.id, "institute", message.text)
    await state.clear()
    await message.answer("Институт обновлен!", reply_markup=get_main_menu_kb())


@router.message(EditProfile.speciality)
async def update_speciality(message: types.Message, state: FSMContext):
    data = await state.get_data()
    institute = data.get('current_institute')

    if not institute or message.text not in INSTITUTES.get(institute, []):
        await message.answer("Пожалуйста, выберите специальность из списка:")
        return

    db = Database(DATABASE_NAME)
    db.update_user_field(message.from_user.id, "speciality", message.text)
    await state.clear()
    await message.answer("Специальность обновлена!", reply_markup=get_main_menu_kb())


@router.message(EditProfile.location_method)
async def process_edit_location_method(message: types.Message, state: FSMContext):
    if message.text == "📍 Определить автоматически":
        await state.set_state(EditProfile.auto_location)
        await message.answer(
            "Пожалуйста, отправьте ваше местоположение:",
            reply_markup=get_location_request_kb()
        )
    elif message.text == "🗺️ Выбрать вручную":
        await state.set_state(EditProfile.manual_location)
        await message.answer(
            "Выберите здание из списка:",
            reply_markup=get_buildings_kb()
        )
    else:
        await message.answer("Пожалуйста, выберите вариант из предложенных:")


@router.message(EditProfile.auto_location, F.location)
async def process_edit_auto_location(message: types.Message, state: FSMContext):
    user_location = message.location
    nearest = find_nearest_building(
        user_location.latitude,
        user_location.longitude
    )

    await state.update_data(
        building=nearest,
        latitude=user_location.latitude,
        longitude=user_location.longitude
    )

    await state.set_state(EditProfile.confirm_location)
    await message.answer(
        f"Определено ближайшее здание: {nearest}\n\nЭто верно?",
        reply_markup=get_confirm_location_kb()
    )


@router.message(EditProfile.auto_location, F.text == "↩️ Назад к выбору метода")
async def back_to_edit_method(message: types.Message, state: FSMContext):
    await state.set_state(EditProfile.location_method)
    await message.answer(
        "Как вы хотите определить ваше местоположение?",
        reply_markup=get_location_method_kb()
    )


@router.message(EditProfile.confirm_location)
async def process_edit_confirm_location(message: types.Message, state: FSMContext):
    if message.text == "✅ Да, верно":
        data = await state.get_data()
        db = Database(DATABASE_NAME)
        db.update_user_location(
            message.from_user.id,
            data['building'],
            data['latitude'],
            data['longitude']
        )
        await state.clear()
        await message.answer("Местоположение обновлено!", reply_markup=get_main_menu_kb())
    elif message.text == "🔄 Отправить снова":
        await state.set_state(EditProfile.auto_location)
        await message.answer(
            "Пожалуйста, отправьте ваше местоположение:",
            reply_markup=get_location_request_kb()
        )
    elif message.text == "🗺️ Выбрать вручную":
        await state.set_state(EditProfile.manual_location)
        await message.answer(
            "Выберите здание из списка:",
            reply_markup=get_buildings_kb()
        )
    else:
        await message.answer("Пожалуйста, выберите вариант из предложенных:")


@router.message(EditProfile.manual_location)
async def process_edit_manual_location(message: types.Message, state: FSMContext):
    if message.text not in BUILDINGS:
        await message.answer("Пожалуйста, выберите здание из списка:")
        return

    coords = BUILDINGS[message.text]
    db = Database(DATABASE_NAME)
    db.update_user_location(
        message.from_user.id,
        message.text,
        coords['lat'],
        coords['lon']
    )

    await state.clear()
    await message.answer("Местоположение обновлено!", reply_markup=get_main_menu_kb())


# Добавляем обработчик для административных функций (пример)
@router.message(F.text == "📊 Статистика пользователей")
async def show_stats(message: types.Message):
    # Проверка прав администратора (можно реализовать отдельно)
    if message.from_user.id != 123456789:  # Замените на ID администратора
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    db = Database(DATABASE_NAME)
    users = db.get_all_users()

    if not users:
        await message.answer("Нет зарегистрированных пользователей.")
        return

    stats_text = f"📊 Статистика пользователей:\n\nВсего пользователей: {len(users)}\n\n"

    # Группировка по институтам
    institutes = {}
    for user in users:
        institute = user['institute']
        if institute not in institutes:
            institutes[institute] = 0
        institutes[institute] += 1

    stats_text += "📈 Распределение по институтам:\n"
    for institute, count in institutes.items():
        stats_text += f"• {institute}: {count} чел.\n"

    await message.answer(stats_text)