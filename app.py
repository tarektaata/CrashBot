from flask import Flask, request, jsonify
from config import get_config
from logger import get_logger
from telegram_utils import handle_update, send_message
from websocket_listener import start_listener
from exceptions import TelegramAPIError, ConfigError
from user_manager import init_user_db
from round_manager import init_round_db
from waitress import serve
import traceback

# 🔧 تحميل الإعدادات
config = get_config()
PORT = config.get("PORT", 5050)  # تأمين قيمة افتراضية

# 📝 إعداد اللوجر
logger = get_logger("app")

# 🚀 إنشاء تطبيق Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ CrashBot is running."

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json(force=True)
        logger.info(f"📩 Received update: {update}")

        response = handle_update(update)

        if isinstance(response, dict) and "chat_id" in response and "text" in response:
            send_message(response["chat_id"], response["text"], response.get("reply_markup"))

        return jsonify({"status": "sent"}), 200

    except TelegramAPIError as e:
        logger.error(f"❌ Telegram error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"🔥 Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

# ✅ نقطة التشغيل
def start_server():
    try:
        logger.info("🚀 Starting CrashBot server...")

        init_user_db()
        init_round_db()

        start_listener()
        logger.info("🔄 WebSocket listener started.")

        logger.info(f"🌐 Running on port {PORT} with waitress...")
        serve(app, host="0.0.0.0", port=PORT)

    except ConfigError as e:
        logger.critical(f"❌ Configuration error: {e}")
        exit(1)

if __name__ == "__main__":
    start_server()
