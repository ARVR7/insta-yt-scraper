---
name: fetch-youtube-video
description: Download metadata, captions and the video of a YouTube video or short with yt-dlp. Use as the first step for any youtube.com or youtu.be link.
---

# fetch-youtube-video

```bash
bash scripts/setup.sh
python3 scripts/fetch_youtube.py "<url>" "$SCRATCH/<video-id>"
```

Writes `meta.json` (title, channel, date, views, likes, description, tags, chapters, `video_error`), `captions.*.vtt` when available, and `video.mp4` (<=720p) when the media is reachable.

## Known behaviour
- Metadata always comes first and is saved even if the media download fails.
- A JS runtime is needed for YouTube extraction; the script passes `node`.
- In the cloud sandbox the media download returned `HTTP 403` and captions `HTTP 429` (googlevideo/timedtext are not reachable). Then `video_error` is set. Fallbacks, in order:
  1. Use `description`, `chapters` and `tags` from `meta.json`; say in the note that no transcript was available.
  2. Ask the user for the transcript or for the downloaded file.
  3. If `captions.*.vtt` exists, use it as the transcript instead of running `analyze-video`.
- Shorts (`/shorts/<id>`) work like normal videos.
- Playlists are ignored (`noplaylist`); only the single video is processed.
