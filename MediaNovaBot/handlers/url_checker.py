import re

# ------------------------------------------------------------------------------
# Platforms URL Validator
# ------------------------------------------------------------------------------
def is_valid_platform_url(url: str) -> dict:

    patterns = {
        "instagram": r"^https?://(www\.)?instagram\.com/(reel)/([A-Za-z0-9_-]+)/?",
        "facebook": r"^https?://(www\.)?facebook\.com/share/(v|r)/([A-Za-z0-9_-]+)/?",
    }

    for platform, pattern in patterns.items():
        match = re.match(pattern, url)
        if match:
            return {
                "valid": True,
                "platform": platform,
                "type": match.group(2),
                "shortcode": match.group(3),
            }

    return {"valid": False, "platform": None, "type": None, "shortcode": None}
    
# -- MediaNovaBot-V1.1.0/handlers/url_checker.py