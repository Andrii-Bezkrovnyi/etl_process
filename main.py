import argparse
from typing import List, Dict, Any

from log_config import logger
from utils import load_json_data, calculate_cpa, merge_data
from db import init_db, upsert_data


def main(start_date: str, end_date: str) -> None:
    logger.info(f"Starting processing for period: {start_date} - {end_date}")

    fb_data: List[Dict[str, Any]] = load_json_data("data/fb_spend.json")
    conv_data: List[Dict[str, Any]] = load_json_data("data/network_conv.json")

    fb_filtered: List[Dict[str, Any]] = [
        x for x in fb_data if start_date <= x["date"] <= end_date
    ]
    conv_filtered: List[Dict[str, Any]] = [
        x for x in conv_data if start_date <= x["date"] <= end_date
    ]

    merged: List[Dict[str, Any]] = merge_data(fb_filtered, conv_filtered)
    calculated: List[Dict[str, Any]] = calculate_cpa(merged)

    conn = init_db()
    upsert_data(conn, calculated)

    logger.success(
        f"Successfully updated {len(calculated)} rows from {start_date} to {end_date}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", type=str, required=True)
    parser.add_argument("--end-date", type=str, required=True)
    args = parser.parse_args()

    main(args.start_date, args.end_date)
