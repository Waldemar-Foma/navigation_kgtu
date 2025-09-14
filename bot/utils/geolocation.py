from geopy.distance import geodesic
from config.constants import BUILDINGS


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
