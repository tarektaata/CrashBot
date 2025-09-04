import requests
from config import get_config
from logger import get_logger
from exceptions import TelegramAPIError
from user_manager import link_user, get_user_game_id
from round_manager import get_upcoming_rounds, extract_prediction

config = get_config()
logger = get_logger("telegram")
BASE_URL = f"https://api.telegram.org/bot{config['BOT_TOKEN']}"

def send_message(chat_id: int, text: str, reply_markup: dict = None) -> dict:
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        response = requests.post(url, json=payload)
        result = response.json()
        if not result.get("ok"):
            raise TelegramAPIError(result.get("description", "Unknown error"))
        logger.info(f"✅ Message sent to {chat_id}")
        return result
    except Exception as e:
        logger.error(f"❌ Failed to send message: {e}")
        raise TelegramAPIError(str(e))

def build_keyboard(buttons: list) -> dict:
    return {
        "keyboard": [[{"text": btn} for btn in row] for row in buttons],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }

def handle_update(update: dict) -> dict:
    try:
        message = update.get("message")
        if not message:
            logger.warning("⚠️ لا يوجد رسالة في التحديث")
            return {}

        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        if text.lower() in ["start", "/start", "ابدأ"]:
            reply_text = "👋 أهلاً بك في CrashBot!\nاستخدم الأمر /link <ID> لربط حسابك."
            buttons = [["مساعدة", "حول البوت"]]
            keyboard = build_keyboard(buttons)
            return {
                "chat_id": chat_id,
                "text": reply_text,
                "reply_markup": keyboard
            }

        elif text.lower().startswith("/link"):
            parts = text.split()
            if len(parts) != 2:
                return {
                    "chat_id": chat_id,
                    "text": "❌ صيغة غير صحيحة. استخدم:\n/link <ID>"
                }
            game_id = parts[1]
            link_user(chat_id, game_id)
            return {
                "chat_id": chat_id,
                "text": f"✅ تم ربط حسابك باللعبة: <b>{game_id}</b>"
            }

        elif text.lower().startswith("/next_round"):
            game_id = get_user_game_id(chat_id)
            if not game_id:
                return {
                    "chat_id": chat_id,
                    "text": "⚠️ لم يتم ربط حسابك بعد. استخدم /link <ID> أولاً."
                }

            rounds = get_upcoming_rounds()
            for r in rounds:
                if r["game_id"] == game_id:
                    prediction = extract_prediction(r)
                    if prediction:
                        return {
                            "chat_id": chat_id,
                            "text": f"✈️ الجولة القادمة ستنفجر عند multiplier: <b>{prediction}</b>"
                        }
                    else:
                        return {
                            "chat_id": chat_id,
                            "text": "⚠️ لم يتم استخراج التوقع بعد."
                        }
            return {
                "chat_id": chat_id,
                "text": "🔍 لا توجد جولة قادمة حالياً."
            }

        elif text.lower() in ["مساعدة", "/help"]:
            return {
                "chat_id": chat_id,
                "text": "📚 استخدم /link <ID> لربط حسابك، و /next_round لعرض التوقع القادم."
            }

        elif text.lower() in ["حول البوت", "حول"]:
            return {
                "chat_id": chat_id,
                "text": "🤖 هذا بوت عملي للتوقعات، تم تطويره بدقة وربط مباشر مع اللعبة."
            }

        else:
            return {
                "chat_id": chat_id,
                "text": f"📨 استلمت رسالتك: <b>{text}</b>"
            }

    except Exception as e:
        logger.error(f"❌ خطأ أثناء معالجة التحديث: {e}")
        raise TelegramAPIError(str(e))
