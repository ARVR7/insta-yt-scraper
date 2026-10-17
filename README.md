# insta-yt-scraper

Share an Instagram reel/post or a YouTube video/short; get a markdown note, a fact-check, and an entry in a registry of verified tools or hoaxes.

- `notes/` - one note per link
- `registry/` - `verified.md`, `hoax.md`, `sidequests.md`
- `.claude/skills/` - the reusable operations (start at `process-link`)
- `scripts/` - fetch and analysis scripts
- `decision.md` - why things are the way they are
- `flow.md` - how it all fits together

Setup: `bash scripts/setup.sh` (needs ffmpeg).
