import os
from dotenv import load_dotenv
from pathlib import Path
from functools import lru_cache

# 📍 تحديد مسار ملف .env
env_path = Path(__file__).parent / ".env"

# ✅ التحقق من وجود الملف
if not env_path.exists():
    raise FileNotFoundError(f"❌ ملف .env غير موجود في المسار: {env_path}")

# 🧪 تحميل المتغيرات من ملف .env
load_dotenv(dotenv_path=env_path)

# 🧠 كاش للإعدادات لتسريع الوصول
@lru_cache()
def get_config():
    try:
        port = int(os.getenv("PORT", "5050"))
    except (TypeError, ValueError):
        raise ValueError("❌ قيمة PORT غير صالحة! تأكد من أنها رقم صحيح في ملف .env.")

    config = {
        # 🔑 إعدادات أساسية
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "PORT": port,
        "SERVER_URL": os.getenv("SERVER_URL"),
        "DATA_FILE": os.getenv("DATA_FILE", "users.json"),
        "MODEL_PATH": os.getenv("MODEL_PATH", "model.pkl"),
        "DB_PATH": os.getenv("DB_PATH", "rounds.db"),
        "USER_DB_PATH": os.getenv("USER_DB_PATH", "users.db"),
        "LOG_FILE": os.getenv("LOG_FILE", "logs/project.log"),

        # 🌍 إعدادات عامة
        "ENV": os.getenv("ENV", "production"),
        "TIMEZONE": os.getenv("TIMEZONE", "Africa/Cairo"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),

        # 🛡 إعدادات الأمان
        "MAX_REQUESTS_PER_MINUTE": int(os.getenv("MAX_REQUESTS_PER_MINUTE", 30)),
        "ENABLE_SPAM_PROTECTION": os.getenv("ENABLE_SPAM_PROTECTION", "true").lower() == "true",
    }

    # ✅ تحقق من الإعدادات الأساسية
    if not config["BOT_TOKEN"]:
        raise ValueError("❌ BOT_TOKEN غير مضبوط! ضعه في ملف .env أو إعدادات البيئة.")
    if not config["SERVER_URL"]:
        raise ValueError("❌ SERVER_URL غير مضبوط! ضعه في ملف .env أو إعدادات البيئة.")

    return config

# 🧩 دعم الوصول المباشر لو احتجت
config = get_config()
BOT_TOKEN = config["BOT_TOKEN"]
SERVER_URL = config["SERVER_URL"]
DATA_FILE = config["DATA_FILE"]
MODEL_PATH = config["MODEL_PATH"]
DB_PATH = config["DB_PATH"]
USER_DB_PATH = config["USER_DB_PATH"]
LOG_FILE = config["LOG_FILE"]
