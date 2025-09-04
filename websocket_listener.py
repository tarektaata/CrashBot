import asyncio
import websockets
import json
import logging
from config import get_config
from round_manager import save_round

# 🧠 تحميل الإعدادات
config = get_config()
WS_URL = config["SERVER_URL"]

# 📝 إعداد اللوجر
logger = logging.getLogger("websocket")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# 📡 استقبال الرسائل من WebSocket
async def handle_messages(ws):
    async for message in ws:
        try:
            data = json.loads(message)
            if "nextMultiplier" in data:
                save_round(data)
                logger.info(f"🎯 تم حفظ التوقع: x{data['nextMultiplier']}")
            else:
                logger.debug(f"📥 تم تجاهل رسالة غير متوقعة: {data}")
        except json.JSONDecodeError:
            logger.warning(f"⚠️ رسالة غير قابلة للفهم: {message}")
        except Exception as e:
            logger.error(f"❌ خطأ أثناء معالجة الرسالة: {e}")

# 🔁 محاولة الاتصال المستمرة
async def listen():
    while True:
        try:
            logger.info(f"🔌 محاولة الاتصال بـ WebSocket: {WS_URL}")
            async with websockets.connect(WS_URL) as ws:
                logger.info("✅ تم الاتصال بـ WebSocket بنجاح")
                await handle_messages(ws)
        except Exception as e:
            logger.error(f"❌ فشل الاتصال: {e}")
            logger.info("🔄 إعادة المحاولة بعد 5 ثواني...")
            await asyncio.sleep(5)

# 🚀 تشغيل المستمع
def start_listener():
    loop = asyncio.get_event_loop()
    loop.create_task(listen())
