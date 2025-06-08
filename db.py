import sqlite3
from pathlib import Path
from log_config import logger


DB_PATH = Path("data/daily_stats.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            date TEXT,
            campaign_id TEXT,
            spend REAL,
            conversions INTEGER,
            cpa REAL,
            PRIMARY KEY (date, campaign_id)
        )
    """)
    conn.commit()
    logger.info("Initialized database and ensured table exists")
    return conn

def upsert_data(conn, rows):
    cur = conn.cursor()
    for row in rows:
        cur.execute("""
            INSERT INTO daily_stats (date, campaign_id, spend, conversions, cpa)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(date, campaign_id)
            DO UPDATE SET
                spend=excluded.spend,
                conversions=excluded.conversions,
                cpa=excluded.cpa
        """, (row["date"], row["campaign_id"], row["spend"], row["conversions"], row["cpa"]))
    conn.commit()
    logger.info("Data upserted successfully")

def data_for_date_exists(date_str: str) -> bool:
    if not DB_PATH.exists():
        return False
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM daily_stats WHERE date = ?", (date_str,))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0  # Returns True if data exists for the given date