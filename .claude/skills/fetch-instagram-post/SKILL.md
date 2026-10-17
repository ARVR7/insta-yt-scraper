---
name: fetch-instagram-post
description: Download metadata (author, date, likes, comments, caption, hashtags) and the video of a public Instagram reel or post without logging in. Use as the first step for any instagram.com link.
---

# fetch-instagram-post

```bash
bash scripts/setup.sh                                   # once per session
python3 scripts/fetch_instagram.py "<url>" "$SCRATCH/<shortcode>"
```

Use the scratchpad directory for `$SCRATCH`. The script writes `meta.json` and `video.mp4` and prints the metadata.

## Known behaviour
- Works anonymously through `instaloader`. Plain `curl` and `yt-dlp` hit the login wall, which is why the script uses `instaloader`.
- `caption` often comes back `null` even on public posts. Record that honestly in the note; do not invent one. The creator's call-to-action ("comment X for the link") is usually in the on-screen text or audio instead.
- `views` and `duration_s` can be `null`. Get the duration from `ffprobe`.
- Rate limits: Instagram throttles the shared sandbox IP with HTTP 429 in bursts, and the tools report it vaguely ("Fetching Post metadata failed", "empty media response", a login redirect, "rate-limit for accessing posts anonymously"). A public post that fails once usually works minutes later: `fetch_instagram.py` alternates `instaloader` and `yt-dlp` with pauses (10, 20, 40 s) and ends with `RATE_LIMITED:` when it is probably transient. Never conclude a post is private or login-gated from one failure; do not ask for cookies.
- Carousels/image posts have no video; the script still writes `meta.json`. Look at the post image only if the user supplies it.
- Strip tracking parameters (`?rpxt=...`, `?igsh=...`) from the URL stored in the note; the script already does this.
