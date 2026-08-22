import yt_dlp


def process_facebook_content(url):
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        all_formats = info.get("formats", [])
        formats = []

        # facebook usually gives two literal muxed formats: "sd" and "hd"
        for fid, tag, label in [("hd", "hd", "720p(HD)"), ("sd", "sd", "360p(SD)")]:
            match = next((f for f in all_formats if f.get("format_id") == fid), None)
            if match and match.get("url"):
                formats.append({"quality": tag, "label": label, "url": match["url"]})

        if not formats:
            return {"success": False, "error": "No sd/hd formats found", "formats": []}

        return {"success": True, "error": None, "formats": formats}

    except Exception as e:
        return {"success": False, "error": str(e), "formats": []}


if __name__ == "__main__":
    test_url = input("Enter Facebook video URL: ").strip()
    url_list = []
    result = get_fb_from_ytdlp(test_url)

    print("\nSuccess:", result["success"])

    if result["success"]:
        for f in result["formats"]:
            print(f)
    else:
        print("Error:", result["error"])


# Example result
# {
#     "success": True / False,
#     "error": None / reason,
#     "formats": [{"quality": "hd", "label": "720p(HD)", "url": "..."}],
# }
