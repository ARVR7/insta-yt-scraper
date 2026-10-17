#!/usr/bin/env python3
"""Fetch metadata and the video of a public Instagram reel/post.

Usage: fetch_instagram.py <url> <outdir>
Writes <outdir>/meta.json and, for videos, <outdir>/video.mp4.
Anonymous access only; Instagram may rate-limit or hide the caption.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

import instaloader


def shortcode(url):
    m = re.search(r"instagram\.com/(?:[\w.]+/)?(?:reel|reels|p|tv)/([\w-]+)", url)
    if not m:
        sys.exit(f"cannot find a shortcode in {url}")
    return m.group(1)


def main(url, outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    code = shortcode(url)
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
    }
    if p.is_video and p.video_url:
        urllib.request.urlretrieve(p.video_url, out / "video.mp4")
        meta["video_file"] = "video.mp4"
    (out / "meta.json").write_text(json.dumps(meta, indent=2, default=str))
    print(json.dumps(meta, indent=2, default=str))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
