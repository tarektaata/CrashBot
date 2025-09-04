import json
from typing import Dict, Any, Optional
from logger import get_logger

logger = get_logger("utils")

def extract_prediction(row: Dict[str, Any]) -> Optional[float]:
    try:
        data = json.loads(row["data"])
        return float(data.get("multiplier", 0))
    except Exception as e:
        logger.warning(f"⚠️ فشل في استخراج التوقع: {e}")
        return None