from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from telethon import events
from core.bot import client
from handlers.force_join import force_join

# from handlers.variables import HOME_MESSAGE, HOME_BUTTONS
from handlers.variables import HOME_DIC


# /start command — sent when a user first opens the bot
@client.on(events.NewMessage(pattern="/start"))
@force_join
async def start_handler(event):
    await event.respond(HOME_DIC[0], buttons=HOME_DIC[1], parse_mode="html")
    