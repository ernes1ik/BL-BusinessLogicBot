import sqlite3
import os
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class User:
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    registered_at: str


@dataclass
class Note:
    id: int
    user_id: int
    text: str
    created_at: str


class BotLogic:
    def __init__(self, db_name: str = None):
        self.db_name = db_name or os.getenv('DB_PATH', 'bot_db.sqlite')
        self._init_tables()

    def __repr__(self) -> str:
        return f"BotLogic(db_name='{self.db_name}')"

    def __str__(self) -> str:
        return f"Telegram Bot Logic with DB: {self.db_name}"

    def _init_tables(self) -> None:
        """Инициализировать таблицы в базе данных"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

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

    def register_user(self, user_id: int, username: Optional[str],
                      first_name: Optional[str], last_name: Optional[str]) -> bool:
        """Зарегистрировать пользователя"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли уже пользователь
            cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
            if cursor.fetchone():
                return False

            cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))

            conn.commit()
            return True

    def add_note(self, user_id: int, text: str) -> int:
        """Добавить заметку для пользователя"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO notes (user_id, text)
            VALUES (?, ?)
            ''', (user_id, text))

            conn.commit()
            return cursor.lastrowid

    def get_user_notes(self, user_id: int) -> List[Dict[str, Any]]:
        """Получить все заметки пользователя"""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
            SELECT id, text, created_at FROM notes
            WHERE user_id = ?
            ORDER BY created_at DESC
            ''', (user_id,))

            return [dict(row) for row in cursor.fetchall()]

    def delete_note(self, note_id: int, user_id: int) -> bool:
        """Удалить заметку пользователя"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            DELETE FROM notes
            WHERE id = ? AND user_id = ?
            ''', (note_id, user_id))

            conn.commit()
            return cursor.rowcount > 0

    def get_user(self, user_id: int) -> Optional[User]:
        """Получить информацию о пользователе"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            SELECT user_id, username, first_name, last_name, registered_at
            FROM users
            WHERE user_id = ?
            ''', (user_id,))

            row = cursor.fetchone()
            if row:
                return User(*row)
            return None

    def get_welcome_message(self, user_id: int) -> str:
        """Сгенерировать приветственное сообщение"""
        user = self.get_user(user_id)
        if not user:
            return "Добро пожаловать! Пожалуйста, зарегистрируйтесь с помощью команды /start."

        name = user.first_name or user.username or "Пользователь"
        return f"Привет, {name}! Я бот для заметок. Используй /help для списка команд."

    def get_help_message(self) -> str:
        """Сгенерировать сообщение помощи"""
        return (
            "Доступные команды:\n"
            "/start - начать работу с ботом\n"
            "/help - показать это сообщение\n"
            "/add_note <текст> - добавить заметку\n"
            "/notes - показать все заметки\n"
            "/delete_note <id> - удалить заметку"
        )