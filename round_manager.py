import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from config import get_config
from logger import get_logger
from exceptions import RoundNotFoundError, StorageError

config = get_config()
logger = get_logger("round_manager")
DB_PATH = config["DB_PATH"]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_round_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rounds (
                game_id TEXT NOT NULL,
                round_number INTEGER NOT NULL,
                data TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (game_id, round_number)
            )
        """)
        conn.commit()
        conn.close()
        logger.info("✅ تم إنشاء جدول الجولات (rounds) بنجاح")
    except Exception as e:
        logger.error(f"❌ فشل في إنشاء جدول الجولات: {e}")
        raise StorageError("فشل في تهيئة قاعدة بيانات الجولات")

def add_round(game_id: str, round_number: int, data: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rounds (game_id, round_number, data)
            VALUES (?, ?, ?)
        """, (game_id, round_number, data))
        conn.commit()
        conn.close()
        logger.info(f"✅ تم إضافة الجولة {round_number} للعبة {game_id}")
    except Exception as e:
        logger.error(f"❌ فشل في إضافة الجولة: {e}")
        raise StorageError("فشل في حفظ بيانات الجولة")

def save_round(data: Dict[str, Any]):
    try:
        game_id = data.get("game_id")
        round_number = data.get("round_number")
        if not game_id or not round_number:
            logger.warning("⚠️ البيانات غير مكتملة، لم يتم الحفظ")
            return
        add_round(game_id, round_number, json.dumps(data))
    except Exception as e:
        logger.error(f"❌ فشل في حفظ الجولة: {e}")

def get_round(game_id: str, round_number: int) -> Dict[str, Any]:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM rounds WHERE game_id = ? AND round_number = ?
        """, (game_id, round_number))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise RoundNotFoundError(f"الجولة {round_number} غير موجودة للعبة {game_id}")

        return dict(row)
    except Exception as e:
        logger.error(f"❌ فشل في جلب الجولة: {e}")
        raise StorageError("فشل في جلب بيانات الجولة")

def get_upcoming_rounds():
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    soon = now + timedelta(minutes=5)
    cursor.execute("SELECT * FROM rounds WHERE start_time BETWEEN ? AND ?", (now, soon))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_round(game_id: str, round_number: int, new_data: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE rounds SET data = ? WHERE game_id = ? AND round_number = ?
        """, (new_data, game_id, round_number))
        if cursor.rowcount == 0:
            raise RoundNotFoundError(f"الجولة {round_number} غير موجودة للعبة {game_id}")
        conn.commit()
        conn.close()
        logger.info(f"🔄 تم تحديث الجولة {round_number} للعبة {game_id}")
    except Exception as e:
        logger.error(f"❌ فشل في تحديث الجولة: {e}")
        raise StorageError("فشل في تحديث بيانات الجولة")

def extract_prediction(row: Dict[str, Any]) -> Optional[float]:
    try:
        data = json.loads(row["data"])
        return data.get("multiplier")
    except Exception as e:
        logger.error(f"❌ فشل في استخراج التوقع: {e}")
        return None
