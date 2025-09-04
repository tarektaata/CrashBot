import logging
import sys
from config import get_config

config = get_config()

def get_logger(name: str):
    logger = logging.getLogger(name)

    # 🔧 إعداد مستوى اللوج حسب البيئة
    log_level = config.get("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # 📄 تنسيق اللوج
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] → %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 📤 إخراج إلى الكونسول
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 📁 إخراج إلى ملف حسب البيئة
    log_file = config.get("LOG_FILE", "logs/app.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
