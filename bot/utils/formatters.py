def format_profile(user_data: tuple) -> str:
    return (f"👤 Ваш профиль:\n\n"
            f"ФИО: {user_data[1]}\n"
            f"Институт: {user_data[2]}\n"
            f"Специальность: {user_data[3]}\n"
            f"Ближайшее здание: {user_data[4]}")