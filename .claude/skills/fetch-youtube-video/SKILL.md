---
name: fetch-youtube-video
description: Download metadata, captions and the video of a YouTube video or short with yt-dlp. Use as the first step for any youtube.com or youtu.be link.
---

# fetch-youtube-video

```bash
bash scripts/setup.sh
python3 scripts/fetch_youtube.py "<url>" "$SCRATCH/<video-id>"
```

Add `--comments 100` to also save the top comments to `comments.json` (see `analyze-comments`). Writes `meta.json` (title, channel, date, views, likes, description, tags, chapters, `video_error`), `captions.*.vtt` when available, and `video.mp4` (<=720p) when the media is reachable.

## Known behaviour
- Metadata always comes first and is saved even if the media download fails.
- A JS runtime is needed for YouTube extraction; the script passes `node`.
- In the cloud sandbox the media download returned `HTTP 403` and captions `HTTP 429` (googlevideo/timedtext are not reachable). Then `video_error` is set. Fallbacks, in order:
  1. Use `description`, `chapters` and `tags` from `meta.json`; say in the note that no transcript was available.
  2. Ask the user for the transcript or for the downloaded file.
  3. If `captions.*.vtt` exists, use it as the transcript instead of running `analyze-video`.
- Shorts (`/shorts/<id>`) work like normal videos.
- Playlists are ignored (`noplaylist`); only the single video is processed.

## What cannot be done from the cloud sandbox (tested 2026-10-17)
YouTube blocks this environment's IP for media and transcripts. Everything below failed for a public Short:
- `yt-dlp` with every player client (default, tv_embedded, ios, android, mweb, web_safari, tv): HTTP 403, empty file, or "Sign in to confirm you're not a bot";
- `youtube-transcript-api`: `RequestBlocked`;
- the WebFetch tool on the video page and on a web transcript service: no transcript text.

So for YouTube only **metadata** is available (title, channel, description, tags, chapters, counts). Rules:
- Do not pretend to know what was said. Say in the note that no transcript was available, base the note on the title, description and chapters, and use `verdict: pending`.
- If the title and description do not carry the content (clip reposts, "watch this" titles), keep the note short and say so in `key_info`; ask the owner for the transcript or key points only when the content matters, using `--manual` with their reply.
- Cookies would fix it, but they are not requested or used.
