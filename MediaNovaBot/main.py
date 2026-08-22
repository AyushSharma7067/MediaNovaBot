import logging
from core.bot import client
from config import BOT_TOKEN

# stop for now ---------------------------------------
# from handlers.check_deps import check_and_setup, start_midnight_updater

# ─── Logging (one place, applied everywhere) ─────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# ─── Import handlers (registers them on the client) ──────────────
import handlers.user_commands
import handlers.admin_tasks
import handlers.force_join
import handlers.variables
import handlers.Instagram_downloader
import handlers.facebook_downloader


def main():
    logger.info("Bot is starting...")

    # Step 1 — Check and install dependencies
    # logger.info("Step 1: Checking dependencies...")
    # if not check_and_setup():
    #     logger.error("Dependency check failed. Exiting.")
    #     return

    # Step 2 — Start the midnight auto-updater
    # logger.info("Step 2: Starting midnight auto-updater...")
    # start_midnight_updater()

    # Step 3 — Connect and start the bot
    # logger.info("Step 3: Connecting to Telegram...")
    logger.info("Connecting to Telegram...")
    client.start(bot_token=BOT_TOKEN)

    logger.info("Bot is running! Press Ctrl+C to stop.")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
