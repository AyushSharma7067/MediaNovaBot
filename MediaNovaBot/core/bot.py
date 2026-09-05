import os

from telethon import TelegramClient
from config import API_ID, API_HASH

# This creates the bot client
# Keep the session in one predictable directory. Telegram creates this file
# after the first successful connection, so it must not be committed.
SESSION_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "bot_session"
)
os.makedirs(os.path.dirname(SESSION_PATH), exist_ok=True)

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
