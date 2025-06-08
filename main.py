import argparse
from log_config import logger
from utils import load_json_data, calculate_cpa, merge_data
from db import init_db, upsert_data


def main(start_date: str, end_date: str):
    logger.info(f"Запуск обработки за период: {start_date} - {end_date}")

    fb_data = load_json_data("data/fb_spend.json")
    conv_data = load_json_data("data/network_conv.json")

    fb_filtered = [x for x in fb_data if start_date <= x["date"] <= end_date]
    conv_filtered = [x for x in conv_data if start_date <= x["date"] <= end_date]

    merged = merge_data(fb_filtered, conv_filtered)
    calculated = calculate_cpa(merged)

    conn = init_db()
    upsert_data(conn, calculated)

    logger.success(f"Успешно обновлено {len(calculated)} строк")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", type=str, required=True)
    parser.add_argument("--end-date", type=str, required=True)
    args = parser.parse_args()

    main(args.start_date, args.end_date)
