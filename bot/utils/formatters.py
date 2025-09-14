from typing import Dict, Any


def format_profile(user_data: tuple) -> str:
    """Типа обратная совместимость поэтому оставил"""
    return (f"👤 Ваш профиль:\n\n"
            f"ФИО: {user_data[1]}\n"
            f"Институт: {user_data[2]}\n"
            f"Специальность: {user_data[3]}\n"
            f"Ближайшее здание: {user_data[4]}")


def format_profile_dict(user_data: Dict[str, Any]) -> str:
    """Форматирование профиля из словаря"""
    return (f"👤 Ваш профиль:\n\n"
            f"ФИО: {user_data['full_name']}\n"
            f"Институт: {user_data['institute']}\n"
            f"Специальность: {user_data['speciality']}\n"
            f"Ближайшее здание: {user_data['building']}\n"
            f"Дата регистрации: {user_data['created_at']}")


def user_data_to_dict(user_data: tuple) -> Dict[str, Any]:
    """Преобразование кортежа с данными пользователя в словарь"""
    if not user_data:
        return {}

    return {
        'user_id': user_data[0],
        'full_name': user_data[1],
        'institute': user_data[2],
        'speciality': user_data[3],
        'building': user_data[4],
        'latitude': user_data[5],
        'longitude': user_data[6],
        'created_at': user_data[7],
        'updated_at': user_data[8]
    }