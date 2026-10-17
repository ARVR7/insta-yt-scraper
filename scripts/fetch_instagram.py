#!/usr/bin/env python3
"""Fetch metadata and the video of a public Instagram reel/post.

Usage: fetch_instagram.py <url> <outdir>
Writes <outdir>/meta.json and, for videos, <outdir>/video.mp4.

Anonymous access only. Instagram rate-limits (HTTP 429) the shared sandbox IP in bursts and the
tools report it as vague errors ("Fetching Post metadata failed", "empty media response", a login
redirect), so this tries instaloader and yt-dlp alternately with growing pauses. If every attempt
fails the exit message starts with RATE_LIMITED (probably transient, retry later) or FAILED.
"""
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import instaloader

PAUSES = [10, 20, 40]


def shortcode(url):
    m = re.search(r"instagram\.com/(?:[\w.]+/)?(?:reel|reels|p|tv)/([\w-]+)", url)
    if not m:
        sys.exit(f"FAILED: cannot find a shortcode in {url}")
    return m.group(1)


def via_instaloader(url, code, out):
    L = instaloader.Instaloader(quiet=True)
    p = instaloader.Post.from_shortcode(L.context, code)
    meta = {
        "url": f"https://www.instagram.com/{'reel' if p.is_video else 'p'}/{code}/",
        "platform": "instagram",
        "shortcode": code,
        "author": p.owner_username,
        "posted_utc": p.date_utc.isoformat(),
        "is_video": p.is_video,
        "duration_s": p.video_duration,
        "views": p.video_view_count,
        "likes": p.likes,
        "comments": p.comments,
        "caption": p.caption,
        "hashtags": p.caption_hashtags,
        "mentions": p.caption_mentions,
        "location": p.location.name if p.location else None,
        "fetched_via": "instaloader",
    }
    if p.is_video and p.video_url:
        urllib.request.urlretrieve(p.video_url, out / "video.mp4")
        meta["video_file"] = "video.mp4"
    return meta


def via_ytdlp(url, code, out):
    import yt_dlp
    opts = {"outtmpl": str(out / "video.%(ext)s"), "format": "bv*+ba/b", "merge_output_format": "mp4",
            "quiet": True, "noplaylist": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    desc = info.get("description") or ""
    return {
        "url": f"https://www.instagram.com/{'reel' if info.get('duration') else 'p'}/{code}/",
        "platform": "instagram",
        "shortcode": code,
        "author": info.get("channel") or info.get("uploader_id") or "",
        "display_name": info.get("uploader"),
        "posted_utc": datetime.fromtimestamp(info["timestamp"], timezone.utc).replace(tzinfo=None).isoformat() if info.get("timestamp") else None,
        "is_video": True,
        "duration_s": info.get("duration"),
        "views": info.get("view_count"),
        "likes": info.get("like_count"),
        "comments": info.get("comment_count"),
        "caption": desc if desc and not desc.startswith("Video by ") else None,
        "hashtags": re.findall(r"#(\w+)", desc),
        "mentions": re.findall(r"@([\w.]+)", desc),
        "location": None,
        "fetched_via": "yt-dlp",
        "video_file": "video.mp4" if (out / "video.mp4").exists() else None,
    }


def main(url, outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    code = shortcode(url)
    errors = []
    for i, fn in enumerate([via_instaloader, via_ytdlp, via_instaloader, via_ytdlp]):
        try:
            meta = fn(url, code, out)
            (out / "meta.json").write_text(json.dumps(meta, indent=2, default=str))
            print(json.dumps(meta, indent=2, default=str))
            return
        except Exception as e:
            errors.append(f"{fn.__name__}: {type(e).__name__}: {str(e)[:140]}")
            print(f"attempt {i + 1} failed: {errors[-1]}", file=sys.stderr)
            if i < len(PAUSES):
                time.sleep(PAUSES[i])
    text = " | ".join(errors)
    transient = re.search(r"429|Too Many|empty media|metadata failed|rate.?limit|login|redirect", text, re.I)
    sys.exit(("RATE_LIMITED: " if transient else "FAILED: ") + text)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
