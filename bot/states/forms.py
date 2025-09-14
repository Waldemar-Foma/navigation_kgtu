from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    full_name = State()
    institute = State()
    speciality = State()
    location_method = State()
    auto_location = State()
    confirm_location = State()
    manual_location = State()

class EditProfile(StatesGroup):
    full_name = State()
    institute = State()
    speciality = State()
    location_method = State()
    auto_location = State()
    confirm_location = State()
    manual_location = State()