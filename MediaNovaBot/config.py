import os
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()

# Your Telegram API credentials
# Get API_ID and API_HASH from https://my.telegram.org
# Get BOT_TOKEN from @BotFather on Telegram
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Your Telegram user ID (so only you can run admin commands)
# You can get your ID by messaging @userinfobot on Telegram
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

# Force Join Channel
# You can get the channel ID by forwarding a message from the channel to @userinfobot
FORCE_CHANNEL = "MediaNovaUpdates"
FORCE_CHANNEL_LINK = "https://t.me/MediaNovaUpdates"
FORCE_CHANNEL_TITLE = "MediaNova Updates"
