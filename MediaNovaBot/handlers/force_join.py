from functools import wraps
from core.bot import client
from config import FORCE_CHANNEL, FORCE_CHANNEL_LINK, FORCE_CHANNEL_TITLE
import logging

from telethon import events, Button

logger = logging.getLogger(__name__)
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantBanned

# ============================================================
# UI — matches the reference design
# ============================================================
WELCOME_TEXT = (
    "👋  <b>Welcome!</b>\n\n"
    "To use this bot you must first <b>join our channel</b>:\n\n"
    f"🎁  <b>{FORCE_CHANNEL_TITLE}</b>\n\n"
    "<i>After joining, press ✅  Joined below.</i>"
)

VERIFIED_TEXT = "✅  <b>Verified!</b> You're all set — send /start to begin."

NOT_JOINED_ALERT = (
  "❌  You haven't joined the channel yet.\n"
  "Join it, then tap the button again."
)

CHECK_ERROR_ALERT = (
  "⚠️  <b>Couldn't verify right now.</b>\n"
  "Please try again in a moment."
)

def join_prompt_buttons():
    """Buttons: URL button to join + inline callback button to re-check."""
    return [
        [Button.url("🎁  Join Channel", FORCE_CHANNEL_LINK)],
        [Button.inline("✅  I've Joined", data=b"check_join")],
    ]


async def send_join_prompt(event):
    await event.respond(
        WELCOME_TEXT, buttons=join_prompt_buttons(), parse_mode="html"
    )

#============================================================
# CORE MEMBERSHIP CHECK
# ============================================================
async def is_member(user_id: int) -> bool:
    """
    Returns True only if the user is a real, non-banned participant
    of FORCE_CHANNEL. Any failure (not joined, bot lacks admin rights,
    network hiccup) safely resolves to False.
    """
    try:
        result = await client(GetParticipantRequest(FORCE_CHANNEL, user_id))
        if isinstance(result.participant, ChannelParticipantBanned):
            return False
        return True
    except UserNotParticipantError:
        return False
    except ChatAdminRequiredError:
        logger.error(
            "Bot is not admin in %s — GetParticipant requires admin rights there.",
            FORCE_CHANNEL,
        )
        return False
    except Exception as e:
        logger.error("is_member() failed for user %s: %s", user_id, e)
        return False

# ============================================================
# DECORATOR — drop this on any handler you want gated
# ============================================================
def force_join(func):
    """
    Usage:
        @client.on(events.NewMessage(pattern="/start"))
        @force_join
        async def start_handler(event):
            ...
    If the sender isn't a channel member, the join prompt is shown
    instead of running the wrapped handler.
    """

    @wraps(func)
    async def wrapper(event):
        user_id = event.sender_id
        try:
            joined = await is_member(user_id)
        except Exception as e:
            logger.error("force_join wrapper error: %s", e)
            joined = False

        if not joined:
            await send_join_prompt(event)
            return None

        return await func(event)

    return wrapper

# ============================================================
# CALLBACK HANDLER — for the inline button
# ============================================================
@client.on(events.CallbackQuery(data=b"check_join"))
async def check_join_callback(event):
    user_id = event.sender_id
    try:
        joined = await is_member(user_id)
    except Exception:
        await event.answer(CHECK_ERROR_ALERT, alert=True)
        return

    if joined:
        await event.edit(VERIFIED_TEXT, buttons=None, parse_mode="html")
    else:
        await event.answer(NOT_JOINED_ALERT, alert=True)