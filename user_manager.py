# user_manager.py

import sqlite3
from config import get_config
from logger import get_logger

config = get_config()
logger = get_logger("user_manager")
DB_PATH = config["USER_DB_PATH"]

def init_user_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            game_id TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def link_user(telegram_id: int, game_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (telegram_id, game_id)
        VALUES (?, ?)
    """, (telegram_id, game_id))
    conn.commit()
    conn.close()
    logger.info(f"✅ تم ربط المستخدم {telegram_id} باللعبة {game_id}")

def get_user_game_id(telegram_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT game_id FROM users WHERE telegram_id = ?
    """, (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None