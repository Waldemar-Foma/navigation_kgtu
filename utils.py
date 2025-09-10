from geopy.distance import geodesic
from constants import BUILDINGS


def find_nearest_building(user_lat: float, user_lon: float) -> str:
    user_coords = (user_lat, user_lon)
    nearest = None
    min_distance = float('inf')

    for name, coords in BUILDINGS.items():
        distance = geodesic(user_coords, (coords['lat'], coords['lon'])).meters
        if distance < min_distance:
            min_distance = distance
            nearest = name
    return nearest


def format_profile(user_data: tuple) -> str:
    return (f"👤 Ваш профиль:\n\n"
            f"ФИО: {user_data[1]}\n"
            f"Институт: {user_data[2]}\n"
            f"Специальность: {user_data[3]}\n"
            f"Ближайшее здание: {user_data[4]}")