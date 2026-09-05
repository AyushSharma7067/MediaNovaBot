import os
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()

def _read_int(name: str, default: int = 0) -> int:
    """Read an integer environment variable without crashing at import time."""
    value = os.environ.get(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


# Get API_ID and API_HASH from https://my.telegram.org.
# Get BOT_TOKEN from @BotFather on Telegram.
API_ID = _read_int("API_ID")
API_HASH = os.environ.get("API_HASH", "").strip()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()

# Your Telegram user ID (so only you can run admin commands)
# You can get your ID by messaging @userinfobot on Telegram
ADMIN_ID = _read_int("ADMIN_ID")

# Force Join Channel
# You can get the channel ID by forwarding a message from the channel to @userinfobot
FORCE_CHANNEL = os.environ.get("FORCE_CHANNEL", "MediaNovaUpdates").strip()
FORCE_CHANNEL_LINK = os.environ.get(
    "FORCE_CHANNEL_LINK", f"https://t.me/{FORCE_CHANNEL.lstrip('@')}"
).strip()
FORCE_CHANNEL_TITLE = os.environ.get(
    "FORCE_CHANNEL_TITLE", "MediaNova Updates"
).strip()


def missing_required_settings() -> list[str]:
    """Return required settings that have not been configured."""
    missing = []
    if API_ID <= 0:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if ADMIN_ID <= 0:
        missing.append("ADMIN_ID")
    return missing
