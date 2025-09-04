class RoundNotFoundError(Exception):
    def __init__(self, message="❌ الجولة المطلوبة غير موجودة."):
        super().__init__(message)

class StorageError(Exception):
    def __init__(self, message="❌ فشل في التعامل مع قاعدة البيانات."):
        super().__init__(message)

class WebSocketError(Exception):
    def __init__(self, message="❌ خطأ في الاتصال بـ WebSocket."):
        super().__init__(message)

class TelegramAPIError(Exception):
    def __init__(self, message="❌ خطأ في الاتصال بـ Telegram API."):
        super().__init__(message)

class ConfigError(Exception):
    def __init__(self, message="❌ إعدادات المشروع غير مكتملة أو غير صحيحة."):
        super().__init__(message)

class InvalidTokenError(Exception):
    def __init__(self, message="❌ التوكن غير صالح أو مفقود."):
        super().__init__(message)
