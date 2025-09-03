import re
from typing import Optional, Tuple


def validate_full_name(full_name: str) -> Tuple[bool, Optional[str]]:
    name_parts = full_name.strip().split()
    
    if len(name_parts) < 2:
        return False, "ФИО должно содержать минимум фамилию и имя"
    
    if len(name_parts) > 3:
        return False, "ФИО должно содержать не более 3 частей"
    
    for part in name_parts:
        if not part.isalpha():
            return False, "Все части ФИО должны содержать только буквы"
        if len(part) < 2:
            return False, "Каждая часть ФИО должна содержать минимум 2 буквы"
    
    return True, None


def validate_age(age_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    try:
        age = int(age_str)
        if age < 16 or age > 60:
            return False, None, "Возраст должен быть от 16 до 60 лет"
        return True, age, None
    except ValueError:
        return False, None, "Возраст должен быть числом"


def validate_group(group: str, available_groups: list) -> Tuple[bool, Optional[str]]:
    if group not in available_groups:
        return False, "Группа не найдена в списке доступных"
    return True, None


def validate_direction(direction: str, available_directions: list) -> Tuple[bool, Optional[str]]:
    if direction not in available_directions:
        return False, "Направление не найдено в списке доступных"
    return True, None
