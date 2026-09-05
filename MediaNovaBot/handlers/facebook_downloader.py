import yt_dlp


def process_facebook_content(url: str) -> dict:
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

        # Facebook often exposes literal "sd"/"hd" formats, but yt-dlp may
        # return different format IDs. Prefer the named formats and fall back
        # to the best available direct video URLs.
        for fid, tag, label in [("hd", "hd", "720p (HD)"), ("sd", "sd", "360p (SD)")]:
            match = next(
                (f for f in all_formats if f.get("format_id") == fid and f.get("url")),
                None,
            )
            if match and match.get("url"):
                formats.append({"quality": tag, "label": label, "url": match["url"]})

        if not formats:
            candidates = [
                f for f in all_formats
                if f.get("url") and f.get("vcodec") not in (None, "none")
            ]
            candidates.sort(
                key=lambda f: (f.get("height") or 0, f.get("tbr") or 0),
                reverse=True,
            )
            seen_urls = set()
            for index, item in enumerate(candidates[:2]):
                url_value = item["url"]
                if url_value in seen_urls:
                    continue
                seen_urls.add(url_value)
                height = item.get("height")
                label = f"{height}p" if height else f"Format {index + 1}"
                formats.append(
                    {"quality": item.get("format_id", str(index + 1)),
                     "label": label, "url": url_value}
                )

        if not formats:
            return {"success": False, "error": "No downloadable video formats found", "formats": []}

        return {"success": True, "error": None, "formats": formats}

    except Exception as e:
        return {"success": False, "error": str(e), "formats": []}


if __name__ == "__main__":
    test_url = input("Enter Facebook video URL: ").strip()
    result = process_facebook_content(test_url)

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
