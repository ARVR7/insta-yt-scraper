---
name: prepare-link
description: Run the whole mechanical front half for one Instagram/YouTube link with one command (fetch, frames, transcript with translation, OCR, entity extraction, repo/package lookups) and get a compact brief plus a draft note. Use first for every link, before reading anything else.
---

# prepare-link

```bash
bash scripts/setup.sh                      # once per session
python3 scripts/prepare_link.py "<url>" "$SCRATCH/<id>" [--queued-via "GitHub issue #N"]
```
`$SCRATCH` is the scratchpad directory, never the repo. The command takes about 1-3 minutes (transcription and OCR run on the CPU) and costs no model tokens. It prints three short lines; do not print or read anything else it wrote except as below.

## Exit codes
| Code | Meaning | What to do |
|---|---|---|
| 0 | prepared | continue with `process-link` |
| 3 | `ALREADY_PROCESSED notes/...` | tell the user (or comment on the issue) that the note exists, link it, close the issue; stop |
| 4 | `RATE_LIMITED ...` | Instagram rate-limits the sandbox IP (HTTP 429) in bursts and the tools hide it behind vague errors. The fetcher already retried with pauses. This is **transient, not a login wall and not the user's fault**: do not ask the user for anything and do not mark `needs-input` yet. Queue item: follow the retry labels in `process-queue`. Chat: wait a minute and rerun once, then tell the user it is rate-limited |
| 2 | `BLOCKED ...` | fetch failed (login wall, rate limit, network). Queue item: label `needs-input` and say what is needed. Chat: tell the user. Do not ask for cookies |

## Scraping runs on GitHub runners
When a link is queued from the phone app, `.github/workflows/prepare.yml` runs this same script on a GitHub runner within a minute (clean IP: the cloud sandbox is rate-limited by Instagram and cannot reach YouTube's media servers). It commits the result to `inbox/<platform>_<id>/` and labels the issue `prepared`. Running `prepare_link.py` for such a link prints `OK pre-prepared by GitHub Actions` and points at the inbox files instead of fetching again; `finish_link.py` deletes the inbox entry when the note is written. Use `--force` to scrape again.

## What it produces in `$SCRATCH/<id>/`
| File | Use |
|---|---|
| `brief.md` | **Read this, and only this.** Metadata, caption, hashtags, transcript (English translation for other languages), OCR text from the screen, candidate names/URLs/prices/income claims found, and a "Looked up" section with mechanical facts about any GitHub repos (existence, licence, README lines about requirements and limits) and PyPI packages |
| `draft_note.md` | The note with every mechanical part filled in and `TODO` where judgment is needed. `finish-link` completes it; you do not edit it by hand |
| `sheet.jpg` | Contact sheet. Look at it only when `brief.md` says `needs_visual_review: yes` (a talking head with nothing to read is skipped) |
| `transcript.txt`, `screen_text.txt`, `meta.json`, `video.mp4`, `comments.json` | Raw files, only if you need to dig |

## Notes
- **YouTube gives metadata only** unless the owner added a `YOUTUBE_COOKIES` Actions secret (a Netscape-format cookies file; use a throwaway Google account). YouTube blocks datacenter IPs on GitHub's runners too ("Sign in to confirm you're not a bot") and from the cloud sandbox (media, captions and transcripts are all blocked, see `fetch-youtube-video`). `brief.md` says `gaps: video: ...`; write the note from the title, description and chapters and mark it `pending`.
- It reuses `fetch_instagram.py`, `fetch_youtube.py` and `analyze_video.py`; those skills describe their failure modes.
- A repo marked `NOT FOUND` in "Looked up" means unverified, not fake. The anonymous GitHub API and github.com pages are blocked in the sandbox, so the lookup reads `raw.githubusercontent.com` instead; set `GITHUB_TOKEN` to get stars and dates.
- OCR text is noisy (words run together). Use it to find names and numbers, then confirm them against the contact sheet or a source.
