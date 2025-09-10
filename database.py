import sqlite3
from typing import Optional, Tuple

class Database:
    def __init__(self, db_name: str = "users.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    institute TEXT NOT NULL,
                    speciality TEXT NOT NULL,
                    building TEXT,
                    latitude REAL,
                    longitude REAL
                )
            """)

    def user_exists(self, user_id: int) -> bool:
        cursor = self.conn.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None

    def add_user(self, user_data: Tuple):
        with self.conn:
            self.conn.execute("""
                INSERT INTO users 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, user_data)

    def get_user(self, user_id: int) -> Optional[Tuple]:
        cursor = self.conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

    def update_user_field(self, user_id: int, field: str, value: str):
        with self.conn:
            self.conn.execute(f"""
                UPDATE users SET {field} = ? WHERE user_id = ?
            """, (value, user_id))

    def update_user_location(self, user_id: int, building: str, lat: float, lon: float):
        with self.conn:
            self.conn.execute("""
                UPDATE users SET building = ?, latitude = ?, longitude = ? 
                WHERE user_id = ?
            """, (building, lat, lon, user_id))