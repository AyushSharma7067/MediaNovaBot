from telethon import TelegramClient
from config import API_ID, API_HASH

# This creates the bot client
# "bot_session" is the name of the session file saved on disk
client = TelegramClient("bot_session", API_ID, API_HASH)
