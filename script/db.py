import sqlite3
from typing import Optional


def init_db(db_name: str = 'bot_db.sqlite') -> None:
    """Инициализация базы данных"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Создание таблицы заметок
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    conn.commit()
    conn.close()


def get_connection(db_name: str = 'bot_db.sqlite') -> sqlite3.Connection:
    """Получить соединение с базой данных"""
    return sqlite3.connect(db_name)