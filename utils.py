from collections import defaultdict
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from log_config import logger
import json
from pathlib import Path
from typing import Union, List, Dict, Optional


@retry(
    stop=stop_after_attempt(3),                 # maximum 3 attempts
    wait=wait_fixed(2),                         # wait 2 seconds between attempts
    retry=retry_if_exception_type((OSError,))  # retry on reading errors
)
def load_json_data(path: Union[Path, str]) -> List[Dict[str, any]]:
    path = Path(path)
    logger.debug(f"Loading file {path}")

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def merge_data(
        spend_data: List[Dict[str, any]],
        conv_data: List[Dict[str, any]]
) -> List[Dict[str, any]]:
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
    logger.debug(f"Merged {len(result)} records")
    return result


def calculate_cpa(
    data: List[Dict[str, any]]
) -> List[Dict[str, Optional[float]]]:
    for row in data:
        conversions = row["conversions"]
        spend = row["spend"]
        row["cpa"] = round(spend / conversions, 2) if conversions else None
    logger.debug("CPA calculation completed")
    return data
