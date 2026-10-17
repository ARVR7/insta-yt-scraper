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
| 2 | `BLOCKED ...` | fetch failed (login wall, rate limit, network). Queue item: label `needs-input` and say what is needed. Chat: tell the user. Do not ask for cookies |

## What it produces in `$SCRATCH/<id>/`
| File | Use |
|---|---|
| `brief.md` | **Read this, and only this.** Metadata, caption, hashtags, transcript (English translation for other languages), OCR text from the screen, candidate names/URLs/prices/income claims found, and a "Looked up" section with mechanical facts about any GitHub repos (existence, licence, README lines about requirements and limits) and PyPI packages |
| `draft_note.md` | The note with every mechanical part filled in and `TODO` where judgment is needed. `finish-link` completes it; you do not edit it by hand |
| `sheet.jpg` | Contact sheet. Look at it only when `brief.md` says `needs_visual_review: yes` (a talking head with nothing to read is skipped) |
| `transcript.txt`, `screen_text.txt`, `meta.json`, `video.mp4`, `comments.json` | Raw files, only if you need to dig |

## Notes
- It reuses `fetch_instagram.py`, `fetch_youtube.py` and `analyze_video.py`; those skills describe their failure modes.
- A repo marked `NOT FOUND` in "Looked up" means unverified, not fake. The anonymous GitHub API and github.com pages are blocked in the sandbox, so the lookup reads `raw.githubusercontent.com` instead; set `GITHUB_TOKEN` to get stars and dates.
- OCR text is noisy (words run together). Use it to find names and numbers, then confirm them against the contact sheet or a source.
