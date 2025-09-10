from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database import Database
from states import EditProfile
from keyboards import (
    get_main_menu_kb,
    get_institutes_kb,
    get_specialities_kb,
    get_location_method_kb,
    get_location_request_kb,
    get_confirm_location_kb,
    get_buildings_kb,
    get_edit_profile_kb
)
from utils import format_profile, find_nearest_building
from constants import INSTITUTES, BUILDINGS

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def show_profile(message: types.Message):
    db = Database()
    user_data = db.get_user(message.from_user.id)

    if user_data:
        await message.answer(format_profile(user_data))
    else:
        await message.answer("Профиль не найден. Пройдите регистрацию.")


@router.message(F.text == "✏️ Редактировать профиль")
async def edit_profile(message: types.Message):
    await message.answer(
        "Что вы хотите изменить?",
        reply_markup=get_edit_profile_kb()
    )


@router.callback_query(F.data == "edit_location")
async def edit_location(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditProfile.location_method)
    await callback.message.answer(
        "Как вы хотите определить ваше местоположение?",
        reply_markup=get_location_method_kb()
    )
    await callback.answer()


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
        db = Database()
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
    db = Database()
    db.update_user_location(
        message.from_user.id,
        message.text,
        coords['lat'],
        coords['lon']
    )

    await state.clear()
    await message.answer("Местоположение обновлено!", reply_markup=get_main_menu_kb())


# Обработчики редактирования других полей (ФИО, институт, специальность)
@router.callback_query(F.data == "edit_full_name")
async def edit_full_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditProfile.full_name)
    await callback.message.answer("Введите новое ФИО:")
    await callback.answer()


@router.callback_query(F.data == "edit_institute")
async def edit_institute(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EditProfile.institute)
    await callback.message.answer("Выберите новый институт:", reply_markup=get_institutes_kb())
    await callback.answer()


@router.callback_query(F.data == "edit_speciality")
async def edit_speciality(callback: types.CallbackQuery, state: FSMContext):
    # Нужно сначала получить текущий институт пользователя
    db = Database()
    user_data = db.get_user(callback.from_user.id)
    if user_data:
        await state.update_data(current_institute=user_data[2])
        await state.set_state(EditProfile.speciality)
        await callback.message.answer(
            "Выберите новую специальность:",
            reply_markup=get_specialities_kb(user_data[2])
        )
    else:
        await callback.message.answer("Профиль не найден. Пройдите регистрацию.")
    await callback.answer()


@router.message(EditProfile.full_name)
async def update_full_name(message: types.Message, state: FSMContext):
    db = Database()
    db.update_user_field(message.from_user.id, "full_name", message.text)
    await state.clear()
    await message.answer("ФИО обновлено!", reply_markup=get_main_menu_kb())


@router.message(EditProfile.institute)
async def update_institute(message: types.Message, state: FSMContext):
    if message.text not in INSTITUTES:
        await message.answer("Пожалуйста, выберите институт из списка:")
        return

    db = Database()
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

    db = Database()
    db.update_user_field(message.from_user.id, "speciality", message.text)
    await state.clear()
    await message.answer("Специальность обновлена!", reply_markup=get_main_menu_kb())