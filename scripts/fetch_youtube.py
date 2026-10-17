#!/usr/bin/env python3
"""Fetch metadata, captions and the video of a YouTube video or short.

Usage: fetch_youtube.py <url> <outdir> [--comments N]
Writes <outdir>/comments.json (top N comments, only with --comments), <outdir>/meta.json, <outdir>/captions.*.vtt (best effort) and <outdir>/video.mp4.
"""
import json
import sys
from pathlib import Path

import yt_dlp


def main(url, outdir, n_comments=0):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    base = {
        "quiet": True,
        "noplaylist": True,
        "js_runtimes": {"node": {}},  # YouTube extraction needs a JS runtime
    }
    opts = {
        **base,
        "outtmpl": str(out / "video.%(ext)s"),
        "format": "bv*[height<=720]+ba/b[height<=720]/b",
        "merge_output_format": "mp4",
    }
    if n_comments:
        base["getcomments"] = True
        base["extractor_args"] = {"youtube": {"max_comments": [str(n_comments), "0", "0", "0"]}}
    # Metadata first, so it survives even when the media download is blocked.
    with yt_dlp.YoutubeDL({**base, "skip_download": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    video_error = None
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:  # e.g. HTTP 403 when the network blocks googlevideo
        video_error = str(e)
        print(f"video download failed: {e}", file=sys.stderr)
    # Captions are best effort: YouTube rate-limits them (HTTP 429) and that must
    # not lose the video. Only the original-language tracks, never auto-translations.
    try:
        subs = {
            **base,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en", "en-orig", "hi", "hi-orig"],
            "outtmpl": str(out / "captions.%(ext)s"),
        }
        with yt_dlp.YoutubeDL(subs) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"captions skipped: {e}", file=sys.stderr)
    if n_comments:
        comments = [
            {k: c.get(k) for k in ("author", "text", "like_count", "is_pinned", "author_is_uploader", "parent")}
            for c in info.get("comments") or []
        ]
        (out / "comments.json").write_text(json.dumps(comments, indent=2, ensure_ascii=False))
    meta = {
        "url": info.get("webpage_url"),
        "platform": "youtube",
        "video_id": info.get("id"),
        "title": info.get("title"),
        "author": info.get("uploader"),
        "channel_url": info.get("channel_url"),
        "posted": info.get("upload_date"),
        "duration_s": info.get("duration"),
        "views": info.get("view_count"),
        "likes": info.get("like_count"),
        "comments": info.get("comment_count"),
        "description": info.get("description"),
        "tags": info.get("tags"),
        "chapters": info.get("chapters"),
        "video_error": video_error,
    }
    for f in out.glob("video.*"):
        if f.suffix == ".mp4":
            meta["video_file"] = f.name
    (out / "meta.json").write_text(json.dumps(meta, indent=2, default=str))
    print(json.dumps(meta, indent=2, default=str))


if __name__ == "__main__":
    args = sys.argv[1:]
    n = 0
    if "--comments" in args:
        i = args.index("--comments")
        n = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    main(args[0], args[1], n)
