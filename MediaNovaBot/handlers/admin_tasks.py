from telethon import events
from core.bot import client
from config import ADMIN_ID


# Helper function — checks if the message sender is the admin
def is_admin(event):
    return event.sender_id == ADMIN_ID


# /ping command — only works for the admin, useful for checking if bot is alive
@client.on(events.NewMessage(pattern="/ping"))
async def ping_handler(event):
    if not is_admin(event):
        await event.respond("⛔ You are not allowed to use this command.")
        return

    await event.respond("✅ Bot is alive and running!")


# /stats command — admin only, shows basic info
@client.on(events.NewMessage(pattern="/stats"))
async def stats_handler(event):
    if not is_admin(event):
        await event.respond("⛔ You are not allowed to use this command.")
        return

    await event.respond(
        "📊 Bot Stats:\n\n"
        "Status: Running ✅\n"
        "Add your own stats here!"
    )
