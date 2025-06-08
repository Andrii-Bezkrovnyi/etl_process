from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import date
import subprocess
from loguru import logger
import sys
import os

# Checking if the script is run from the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron", hour=15, minute=00)
def daily_job():
    today = date.today().isoformat()
    # today = "2025-06-06"  # For testing purposes, you can set a fixed date
    logger.info(f"[Scheduler] Starting scheduled update for {today}")

    result = subprocess.run(
        [sys.executable, "main.py", "--start-date", today, "--end-date", today],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        logger.success(f"[Scheduler] Successfully completed for {today}")
    else:
        logger.error(f"[Scheduler] Error:\n{result.stderr}")


if __name__ == "__main__":
    logger.info("[Scheduler] Started... waiting for scheduled jobs")
    scheduler.start()
