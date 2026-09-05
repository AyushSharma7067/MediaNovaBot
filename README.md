# MediaNovaBot

Telegram bot for checking channel membership and creating download links for
public Instagram Reels and Facebook videos.

## Run it

1. Add `API_ID`, `API_HASH`, `BOT_TOKEN`, and `ADMIN_ID` as Replit Secrets.
2. Add the bot as an administrator in `MediaNovaUpdates` so force-join checks
   can read channel membership.
3. Run the project with `python main.py`.

The project installs Python dependencies from `MediaNovaBot/requirements.txt`
and includes FFmpeg for download tooling. Telegram creates a local session in
`MediaNovaBot/data/` after the first successful connection.

## Commands

- `/start` — open the bot
- `/ping` — admin health check
- `/stats` — admin status

Only public links are supported currently. Platform restrictions, private
accounts, expired CDN URLs, and copyright rules still apply.