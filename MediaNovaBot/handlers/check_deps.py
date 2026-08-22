"""
check_deps.py
─────────────
Handles dependency checking, installation, and daily auto-updates.

Usage in main.py:
    from handlers.check_deps import check_and_setup, start_midnight_updater, bot_is_updating

Usage in any handler:
    from handlers.check_deps import bot_is_updating
    if bot_is_updating():
        await event.respond("⏳ Bot is updating, please try again shortly.")
        return
"""

import subprocess
import logging
import sys
import platform
import shutil
import threading
import time

import schedule

# ─── Logger ──────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ─── Global flag — True while midnight update is running ─────────
is_updating = False


# ═══════════════════════════════════════════════════════════════
# OS DETECTION
# ═══════════════════════════════════════════════════════════════

def get_os() -> str:
    """Returns 'windows' or 'linux'."""
    return "windows" if platform.system().lower() == "windows" else "linux"


# ═══════════════════════════════════════════════════════════════
# SAFE COMMAND RUNNER
# ═══════════════════════════════════════════════════════════════

def run_cmd(cmd: list, timeout: int = 120) -> tuple:
    """
    Runs a command safely using subprocess.
    Returns (success: bool, output: str).
    Never raises — all errors are caught and returned as (False, error_message).
    """
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output

    except subprocess.TimeoutExpired:
        return False, f"Timed out after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError:
        return False, f"Not found: {cmd[0]}"
    except Exception as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════════
# CHECK IF TOOL IS INSTALLED
# ═══════════════════════════════════════════════════════════════

def is_installed(tool: str) -> bool:
    """Returns True if the tool exists anywhere in PATH."""
    return shutil.which(tool) is not None


# ═══════════════════════════════════════════════════════════════
# YT-DLP — INSTALL & UPGRADE
# ═══════════════════════════════════════════════════════════════

def install_ytdlp() -> bool:
    """Install yt-dlp via pip. Returns True on success."""
    logger.info("Installing yt-dlp...")
    ok, out = run_cmd([sys.executable, "-m", "pip", "install", "yt-dlp"])
    if ok:
        logger.info("yt-dlp installed successfully.")
    else:
        logger.error(f"yt-dlp install failed: {out}")
    return ok


def upgrade_ytdlp() -> bool:
    """Upgrade yt-dlp to the latest version. Returns True on success."""
    logger.info("Upgrading yt-dlp...")
    ok, out = run_cmd([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
    if ok:
        _, version = run_cmd(["yt-dlp", "--version"])
        logger.info(f"yt-dlp upgraded. Version: {version}")
    else:
        logger.error(f"yt-dlp upgrade failed: {out}")
    return ok


# ═══════════════════════════════════════════════════════════════
# FFMPEG — INSTALL & UPGRADE
# ═══════════════════════════════════════════════════════════════

def install_ffmpeg() -> bool:
    """
    Install ffmpeg based on OS.
    Linux  → apt-get
    Windows → winget (fallback: chocolatey)
    Returns True on success.
    """
    os_name = get_os()
    logger.info(f"Installing ffmpeg on {os_name}...")

    if os_name == "linux":
        ok, out = run_cmd(["sudo", "apt-get", "install", "-y", "ffmpeg"])

    else:  # windows
        # Try winget first
        ok, out = run_cmd(["winget", "install", "Gyan.FFmpeg", "--silent"])
        if not ok:
            logger.warning("winget failed, trying chocolatey...")
            ok, out = run_cmd(["choco", "install", "ffmpeg", "-y"])

    if ok:
        logger.info("ffmpeg installed successfully.")
    else:
        logger.error(f"ffmpeg install failed: {out}")
        logger.error("Install manually: https://ffmpeg.org/download.html")
    return ok


def upgrade_ffmpeg() -> bool:
    """
    Upgrade ffmpeg based on OS.
    Returns True on success.
    """
    os_name = get_os()
    logger.info(f"Upgrading ffmpeg on {os_name}...")

    if os_name == "linux":
        ok, out = run_cmd(["sudo", "apt-get", "install", "--only-upgrade", "-y", "ffmpeg"])

    else:  # windows
        ok, out = run_cmd(["winget", "upgrade", "Gyan.FFmpeg", "--silent"])
        if not ok:
            ok, out = run_cmd(["choco", "upgrade", "ffmpeg", "-y"])

    if ok:
        _, info = run_cmd(["ffmpeg", "-version"])
        logger.info(f"ffmpeg upgraded. {info.splitlines()[0]}")
    else:
        logger.warning(f"ffmpeg upgrade failed (non-critical): {out}")

    # ffmpeg upgrade failing is not critical — return True anyway
    # because the existing version still works
    return True


# ═══════════════════════════════════════════════════════════════
# STARTUP CHECK — called once when bot starts
# ═══════════════════════════════════════════════════════════════

def check_and_setup() -> bool:
    """
    Detects OS, checks yt-dlp and ffmpeg, installs them if missing.
    Call this once at bot startup before client.start().

    Returns:
        True  — all dependencies are ready, bot can start.
        False — something failed to install, bot may not work.
    """
    os_name = get_os()
    logger.info(f"── Dependency Check ── OS: {os_name.upper()}")

    all_ok = True

    # ── yt-dlp ──────────────────────────────────
    if is_installed("yt-dlp"):
        _, version = run_cmd(["yt-dlp", "--version"])
        logger.info(f"[yt-dlp] Already installed. Version: {version}")
    else:
        logger.warning("[yt-dlp] Not found. Installing...")
        if not install_ytdlp():
            all_ok = False

    # ── ffmpeg ──────────────────────────────────
    if is_installed("ffmpeg"):
        _, info = run_cmd(["ffmpeg", "-version"])
        logger.info(f"[ffmpeg] Already installed. {info.splitlines()[0]}")
    else:
        logger.warning("[ffmpeg] Not found. Installing...")
        if not install_ffmpeg():
            all_ok = False

    # ── Result ──────────────────────────────────
    if all_ok:
        logger.info("── All dependencies ready. Bot starting. ──")
    else:
        logger.error("── Some dependencies failed. Bot may not work correctly. ──")

    return all_ok


# ═══════════════════════════════════════════════════════════════
# MIDNIGHT UPDATER — runs every day at 00:00
# ═══════════════════════════════════════════════════════════════

def _do_midnight_update():
    """
    Called automatically every day at 00:00.
    Sets is_updating = True while running — handlers should
    check bot_is_updating() and pause download requests.
    """
    global is_updating

    logger.info("══ Midnight update started ══")
    is_updating = True

    try:
        ytdlp_ok = upgrade_ytdlp()
        ffmpeg_ok = upgrade_ffmpeg()

        if ytdlp_ok and ffmpeg_ok:
            logger.info("══ Midnight update complete. All tools up to date. ══")
        else:
            logger.warning("══ Midnight update finished with some warnings. ══")

    except Exception as e:
        logger.error(f"Unexpected error during midnight update: {e}")

    finally:
        # Always release the flag — even if something crashed
        is_updating = False


def _schedule_loop():
    """Background thread — checks schedule every 30 seconds."""
    while True:
        schedule.run_pending()
        time.sleep(30)


def start_midnight_updater():
    """
    Schedules the daily update at 00:00 and starts a background thread.
    Call this once in main.py after check_and_setup().
    The thread is a daemon — it stops automatically when the bot stops.
    """
    schedule.every().day.at("00:00").do(_do_midnight_update)
    logger.info("Midnight auto-updater scheduled at 00:00 daily.")

    thread = threading.Thread(target=_schedule_loop, daemon=True)
    thread.name = "MidnightUpdater"
    thread.start()
    logger.info("Midnight updater thread running in background.")


# ═══════════════════════════════════════════════════════════════
# PUBLIC FLAG — use this in any handler
# ═══════════════════════════════════════════════════════════════

def bot_is_updating() -> bool:
    """
    Returns True if the midnight update is currently running.

    Use this in every download handler:
        if bot_is_updating():
            await event.respond("⏳ Bot is updating, please try again in a moment.")
            return
    """
    return is_updating
