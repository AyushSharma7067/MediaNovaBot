import instaloader
from instaloader.exceptions import InstaloaderException


# ------------------------------------------------------------------------------
# Download Handlers 
# ------------------------------------------------------------------------------

"""
Errorless function to get the CDN video link for an Instagram Reel.

Requirements:
    pip install instaloader

Usage:
    result = get_reel_cdn_link("DaS9lk3g36J")
"""


def process_instagram_content(source_code: str) -> dict:
    """
    Fetch the direct CDN video URL for a reel using its shortcode.

    Args:
        source_code: Instagram shortcode (e.g. "DaS9lk3g36J")

    Returns:
        {
            "success": bool,
            "cdn_url": str or None,
            "error": str or None
        }
    """
    try:
        L = instaloader.Instaloader(quiet=True)
        post = instaloader.Post.from_shortcode(L.context, source_code)

        if not post.is_video:
            return {"success": False, "cdn_url": None,
                     "error": "This post is not a video/reel"}

        return {"success": True, "cdn_url": post.video_url, "error": None}

    except InstaloaderException as e:
        return {"success": False, "cdn_url": None, "error": f"Instaloader error: {e}"}

    except Exception as e:
        return {"success": False, "cdn_url": None,
                 "error": f"Unexpected error: {type(e).__name__}: {e}"}
