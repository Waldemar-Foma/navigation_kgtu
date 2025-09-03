import sqlite3
from datetime import datetime
from typing import Optional, Tuple, Dict, Any


class Database:
    def __init__(self, db_name: str = 'KGTU.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            patronymic TEXT,
            group_name TEXT,
            age INTEGER,
            direction TEXT,
            current_building TEXT,
            registration_date TIMESTAMP,
            last_activity TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            group_name TEXT PRIMARY KEY,
            schedule_data TEXT
        )
        ''')
        
        groups_schedule = {
            "ИБ": "Понедельник: Математика 9:00-10:30, Программирование 11:00-12:30\nВторник: Физика 9:00-10:30, Базы данных 11:00-12:30",
            "ВТ": "Понедельник: Физика 9:00-10:30, Математика 11:00-12:30\nВторник: Программирование 9:00-10:30, Базы данных 11:00-12:30",
            "АП": "Понедельник: Экономика 9:00-10:30, Статистика 11:00-12:30\nВторник: Финансы 9:00-10:30, Маркетинг 11:00-12:30",
            "ИС": "Понедельник: Статистика 9:00-10:30, Экономика 11:00-12:30\nВторник: Маркетинг 9:00-10:30, Финансы 11:00-12:30",
            "ИЭ": "Понедельник: Гражданское право 9:00-10:30, Уголовное право 11:00-12:30\nВторник: Конституционное право 9:00-10:30, Международное право 11:00-12:30",
            "БИ": "Понедельник: Уголовное право 9:00-10:30, Гражданское право 11:00-12:30\nВторник: Международное право 9:00-10:30, Конституционное право 11:00-12:30"
        }
        
        for group_name, schedule in groups_schedule.items():
            cursor.execute('''
            INSERT OR IGNORE INTO schedule (group_name, schedule_data)
            VALUES (?, ?)
            ''', (group_name, schedule))
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR IGNORE INTO users 
        (user_id, username, first_name, last_name, registration_date, last_activity)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, datetime.now(), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def update_user_info(self, user_id: int, **kwargs) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        update_fields = []
        update_values = []
        
        field_mapping = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'patronymic': 'patronymic',
            'group_name': 'group_name',
            'age': 'age',
            'direction': 'direction',
            'current_building': 'current_building'
        }
        
        for key, value in kwargs.items():
            if key in field_mapping:
                update_fields.append(f"{field_mapping[key]} = ?")
                update_values.append(value)
        
        if update_fields:
            update_query = f"UPDATE users SET {', '.join(update_fields)}, last_activity = ? WHERE user_id = ?"
            update_values.extend([datetime.now(), user_id])
            
            cursor.execute(update_query, update_values)
        
        conn.commit()
        conn.close()
    
    def get_user_info(self, user_id: int) -> Optional[Tuple]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return user
    
    def is_user_registered(self, user_id: int) -> bool:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT first_name, last_name, group_name, age, direction FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return user and all(user[0:5])
    
    def get_schedule(self, group_name: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT schedule_data FROM schedule WHERE group_name = ?', (group_name,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
    
    def get_user_building(self, user_id: int) -> Optional[str]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT current_building FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
