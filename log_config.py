from loguru import logger
from pathlib import Path

log_path = Path("logs") / "etl.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
log_path.touch(exist_ok=True)

logger.add(
    log_path,
    rotation="1 week",
    retention="1 month",
    encoding="utf-8",
    mode="a"
)
