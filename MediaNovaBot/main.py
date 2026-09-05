import logging
from config import BOT_TOKEN, missing_required_settings
from handlers.check_deps import check_and_setup

# ─── Logging (one place, applied everywhere) ─────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Bot is starting...")

    missing = missing_required_settings()
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        logger.error("Add them as Replit Secrets before starting the bot.")
        return 1

    # Import the client and handlers only after settings are validated.
    # Telethon rejects an empty API ID/API hash while constructing a client.
    from core.bot import client

    # Importing handlers registers their event callbacks on the client.
    import handlers.user_commands
    import handlers.admin_tasks
    import handlers.force_join
    import handlers.variables
    import handlers.Instagram_downloader
    import handlers.facebook_downloader

    # Python packages are installed by the project package manager. This
    # startup check verifies the external tools needed by download handlers.
    if not check_and_setup():
        logger.error("Required download tools are unavailable. Exiting.")
        return 1

    logger.info("Connecting to Telegram...")
    client.start(bot_token=BOT_TOKEN)

    logger.info("Bot is running! Press Ctrl+C to stop.")
    client.run_until_disconnected()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
