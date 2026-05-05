"""
BHHS Irvine RE Research Bot — entry point.

Normal run:
    python main.py

Manual triggers (bypass scheduler for testing):
    python main.py --run-now daily
    python main.py --run-now weekly
"""
import asyncio
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Ensure data/ exists before the file log handler is created
_DATA_DIR = Path(__file__).parent / "data"
_DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_DATA_DIR / "bot.log"),
    ],
)

logger = logging.getLogger(__name__)


async def main() -> None:
    import memory
    from scheduler import create_scheduler, daily_job, weekly_job

    memory.init_db()

    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        mode = sys.argv[2] if len(sys.argv) > 2 else "daily"
        if mode == "weekly":
            logger.info("Manual trigger: weekly report")
            await weekly_job()
        else:
            logger.info("Manual trigger: daily research")
            await daily_job()
        return

    scheduler = create_scheduler()
    scheduler.start()
    logger.info(
        "Scheduler running — daily 07:00 PT | weekly Friday 16:00 PT. "
        "Ctrl-C to stop."
    )
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    asyncio.run(main())
