from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database import Database
from states import Registration
from keyboards import (get_institutes_kb, get_specialities_kb,
                       get_location_method_kb, get_location_request_kb,
                       get_confirm_location_kb, get_buildings_kb, get_main_menu_kb)
from utils import find_nearest_building, format_profile
from constants import INSTITUTES, BUILDINGS

router = Router()


async def start_registration(message: types.Message, state: FSMContext):
    await state.set_state(Registration.full_name)
    await message.answer("Добро пожаловать! Для регистрации введите ваше ФИО:")


@router.message(Registration.full_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(Registration.institute)
    await message.answer("Выберите ваш институт:", reply_markup=get_institutes_kb())


@router.message(Registration.institute)
async def process_institute(message: types.Message, state: FSMContext):
    if message.text not in INSTITUTES:
        await message.answer("Пожалуйста, выберите институт из списка:")
        return

    await state.update_data(institute=message.text)
    await state.set_state(Registration.speciality)
    await message.answer(
        "Выберите вашу специальность:",
        reply_markup=get_specialities_kb(message.text)
    )


@router.message(Registration.speciality)
async def process_speciality(message: types.Message, state: FSMContext):
    data = await state.get_data()
    institute = data.get('institute')

    if message.text not in INSTITUTES.get(institute, []):
        await message.answer("Пожалуйста, выберите специальность из списка:")
        return

    await state.update_data(speciality=message.text)
    await state.set_state(Registration.location_method)
    await message.answer(
        "Как вы хотите определить ваше местоположение?",
        reply_markup=get_location_method_kb()
    )


@router.message(Registration.location_method)
async def process_location_method(message: types.Message, state: FSMContext):
    if message.text == "📍 Определить автоматически":
        await state.set_state(Registration.auto_location)
        await message.answer(
            "Пожалуйста, отправьте ваше местоположение:",
            reply_markup=get_location_request_kb()
        )
    elif message.text == "🗺️ Выбрать вручную":
        await state.set_state(Registration.manual_location)
        await message.answer(
            "Выберите здание из списка:",
            reply_markup=get_buildings_kb()
        )
    else:
        await message.answer("Пожалуйста, выберите вариант из предложенных:")


@router.message(Registration.auto_location, F.location)
async def process_auto_location(message: types.Message, state: FSMContext):
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

    await state.set_state(Registration.confirm_location)
    await message.answer(
        f"Определено ближайшее здание: {nearest}\n\nЭто верно?",
        reply_markup=get_confirm_location_kb()
    )


@router.message(Registration.auto_location, F.text == "↩️ Назад к выбору метода")
async def back_to_method(message: types.Message, state: FSMContext):
    await state.set_state(Registration.location_method)
    await message.answer(
        "Как вы хотите определить ваше местоположение?",
        reply_markup=get_location_method_kb()
    )


@router.message(Registration.confirm_location)
async def process_confirm_location(message: types.Message, state: FSMContext):
    if message.text == "✅ Да, верно":
        await save_data(message, state)
    elif message.text == "🔄 Отправить снова":
        await state.set_state(Registration.auto_location)
        await message.answer(
            "Пожалуйста, отправьте ваше местоположение:",
            reply_markup=get_location_request_kb()
        )
    elif message.text == "🗺️ Выбрать вручную":
        await state.set_state(Registration.manual_location)
        await message.answer(
            "Выберите здание из списка:",
            reply_markup=get_buildings_kb()
        )
    else:
        await message.answer("Пожалуйста, выберите вариант из предложенных:")


@router.message(Registration.manual_location)
async def process_manual_location(message: types.Message, state: FSMContext):
    if message.text not in BUILDINGS:
        await message.answer("Пожалуйста, выберите здание из списка:")
        return

    coords = BUILDINGS[message.text]
    await state.update_data(
        building=message.text,
        latitude=coords['lat'],
        longitude=coords['lon']
    )
    await save_data(message, state)


async def save_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_data = (
        message.from_user.id,
        data['full_name'],
        data['institute'],
        data['speciality'],
        data['building'],
        data['latitude'],
        data['longitude']
    )

    db = Database()
    db.add_user(user_data)
    await state.clear()

    await message.answer(
        f"Регистрация завершена!\n\n{format_profile(user_data)}",
        reply_markup=get_main_menu_kb()
    )