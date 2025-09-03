import math


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def find_nearest_building(user_lat, user_lon, buildings):
    nearest_building = None
    min_distance = float('inf')
    
    for building, coords in buildings.items():
        distance = calculate_distance(
            user_lat, user_lon,
            coords["lat"], coords["lon"]
        )
        if distance < min_distance:
            min_distance = distance
            nearest_building = building
    
    return nearest_building, min_distance
