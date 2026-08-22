from telethon import events, Button
from handlers.force_join import force_join
from handlers.Instagram_downloader import process_instagram_content
from handlers.facebook_downloader import process_facebook_content
from handlers.url_checker import is_valid_platform_url
from core.bot import client
import os


HOME_MESSAGE = (
    "<b>🎬 Welcome to MediaNova Bot</b>\n\n"
    "📥 Download Instagram Reels\n"
    "🔜 YouTube & X — Coming Soon\n\n"
    "🔗 <i>Send a valid Reel link to get started.</i>"
)

HOME_BUTTONS = [
    [
        Button.inline("👤 My Profile", data="profile"),
        Button.url("📢 Channel", "https://t.me/MediaNovaUpdates"),
    ],
    [Button.inline("📜 Terms & Policies", data="terms")],
]

TERMS_MESSAGE = (
    "<b>📜 Terms & Policies</b>\n\n"
    "By using this bot, you agree to the following:\n\n"
    "1️⃣ <b>Non‑Affiliation</b>: This bot is not affiliated with Instagram, YouTube, Facebook, or any other platform.\n\n"
    "2️⃣ <b>Personal Use Only</b>: You may use this bot solely for personal purposes. Commercial or unauthorized distribution of content is prohibited.\n\n"
    "3️⃣ <b>Respect Copyright</b>: Downloaded content must not be used to infringe on copyrights or intellectual property rights.\n\n"
    "4️⃣ <b>Privacy</b>: The bot does not store your personal data or the links you provide. All requests are processed in real time.\n\n"
    "5️⃣ <b>Responsibility</b>: You are fully responsible for how you use the downloaded content. Misuse may lead to restrictions.\n\n"
    "✅ <i>By continuing, you confirm that you understand and accept these terms.</i>"
)


BACK_BUTTON = [Button.inline("🔙 Back", b"back")]


HOME_DIC = [HOME_MESSAGE, HOME_BUTTONS]


# ============================================================
# Profile Button Logic  — for the inline button
# ============================================================


@client.on(events.CallbackQuery(data=b"profile"))
@force_join
async def profile_callback(event):
    # get sender info
    user = await event.get_sender()  # Get sender full info
    user_id = user.id  # Get user ID
    username = f"@{user.username}" if user.username else "No username"  # Get username
    first_name = user.first_name

    # use case of event.delete
    await event.delete()

    # Make a dir
    # Parent directory (already exists)
    # parent_dir = "telegram-bot"

    # Subdirectory you want to create inside parent
    sub_dir = "user_profile_pic"

    # Full path to the new directory
    # path = os.path.join(parent_dir, sub_dir)
    path = f"{sub_dir}"

    # Path to the image( profile pic)
    file_path = f"{path}/{user_id}.jpg"

    # Create the subirectory if it doesn't exist
    os.makedirs(path, exist_ok=True)

    # Download profile photo (saved locally as 'profile.jpg')
    try:
        await client.download_profile_photo(user_id, file=file_path)
    except Exception as e:  # Handle errors (e.g., no profile photo)
        print(f"Error downloading profile photo: {e}")

    # Create the profile message
    msg = (
        f"👤 <b>{first_name}'s</b> <i>Profile</i>\n\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        "<i>(tap to copy)</i>\n\n"
        f"📛 <b>Username:</b> {username}\n\n"
    )

    # Sending (image + text + button) to the user
    await client.send_file(
        event.chat_id, file_path, caption=msg, buttons=BACK_BUTTON, parse_mode="html"
    )

    #  Delete the image after sending
    # Check if file exists before deleting
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"⚠️ File '{file_path}' does not exist.")


# ============================================================
# Back button Logic  — for the inline button
# ============================================================
@client.on(events.CallbackQuery(data=b"back"))
@force_join
async def back_callback(event):
    # await event.delete()
    await event.edit(HOME_DIC[0], buttons=HOME_DIC[1], parse_mode="html")


# ============================================================
# Terms Button Logic  — for the inline button
# ============================================================
@client.on(events.CallbackQuery(data=b"terms"))
@force_join
async def terms_callback(event):
    # await event.delete()
    await event.edit(TERMS_MESSAGE, buttons=BACK_BUTTON, parse_mode="html")


# ============================================================
# Get users send messages or links
# ============================================================
@client.on(events.NewMessage(func=lambda e: not e.is_channel))
async def handler(event):
    text = event.text.strip()
    if text.startswith("/"):
        return

    if text.startswith("https://"):
        # Check if the URL is a valid Instagram URL
        checker = is_valid_platform_url(text)

        if checker["valid"]:
            final_msg = await event.respond("🔗 Valid URL Found! Processing...")

            # Check the platform and type------------
            if checker["platform"] == "instagram" and checker["type"] == "reel":
                # Process the Instagram content
                instagram_result = process_instagram_content(checker["shortcode"])

                if instagram_result["success"]:
                    await final_msg.edit(
                        f"🎥 Video URL: {instagram_result['cdn_url']}",
                        link_preview=True,
                    )
                    # await event.respond(
                    #     "🎬 <b>Your Video Link:</b>",
                    #     buttons=[
                    #         [Button.url("⬇️ Click to download", result["cdn_url"])]
                    #     ],
                    #     parse_mode="html",
                    #     link_preview=True,
                    # )

                else:
                    await final_msg.edit(f"❌ Error: {instagram_result['error']}")

            else:
                # Creating facebook link
                facebook_link = f"https://www.facebook.com/share/{checker['type']}/{checker['shortcode']}/"

                # Process the Facebook content
                facebook_result = process_facebook_content(facebook_link)

                # Ectract the video url
                buttons_text = ""
                video_dict = {}

                if facebook_result.get("success"):
                    for f in facebook_result["formats"]:
                        label = f.get("label")
                        url = f.get("url")
                        if label and url:
                            video_dict[label] = url
                            # clickable text line
                            buttons_text += f"🎬 <a href='{url}'>{label}</a>\n"

                await final_msg.edit(
                    f"<b>Available Formats:</b>\n\n{buttons_text}",
                    parse_mode="html",
                    link_preview=False,
                )

        else:
            await event.respond(
                "⚠️ <b>Invalid URL Format.</b>\n\n"
                "<i>Please check your link format and send a valid URL.</i>",
                parse_mode="html",
            )

    else:
        await event.respond(
            "⚠️ <b>Invalid URL.</b>\n\n<i>Please send a valid URL.</i>",
            parse_mode="html",
        )
