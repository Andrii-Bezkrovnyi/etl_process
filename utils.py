from collections import defaultdict
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from log_config import logger
import json
from pathlib import Path

@retry(
    stop=stop_after_attempt(3),                  # максимум 3 попытки
    wait=wait_fixed(2),                          # между попытками ждать 2 секунды
    retry=retry_if_exception_type((OSError,))    # повторять при ошибках чтения
)
def load_json_data(path: Path | str) -> list[dict]:
    path = Path(path)
    logger.debug(f"Загрузка файла {path}")

    with open(path, encoding="utf-8") as f:
        return json.load(f)

def merge_data(spend_data, conv_data):
    merged = defaultdict(lambda: {"spend": 0, "conversions": 0})

    for row in spend_data:
        key = (row["date"], row["campaign_id"])
        merged[key]["spend"] = row["spend"]

    for row in conv_data:
        key = (row["date"], row["campaign_id"])
        merged[key]["conversions"] = row["conversions"]

    result = []
    for (date, campaign_id), values in merged.items():
        result.append({
            "date": date,
            "campaign_id": campaign_id,
            "spend": values["spend"],
            "conversions": values["conversions"]
        })
    logger.debug(f"Объединено {len(result)} записей")
    return result

def calculate_cpa(data):
    for row in data:
        conversions = row["conversions"]
        spend = row["spend"]
        row["cpa"] = round(spend / conversions, 2) if conversions else None
    logger.debug("Расчёт CPA завершён")
    return data
