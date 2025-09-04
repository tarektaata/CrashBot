import sqlite3
from config import get_config

config = get_config()
DB_PATH = config["DB_PATH"]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
