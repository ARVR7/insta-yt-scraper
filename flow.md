# Flow

How a shared link becomes notes and registry entries, and what lives where. Update this file whenever a script, skill or folder is added or changed.

## Pipeline

```
user shares a link
      |
      v
process-link  (.claude/skills/process-link)
      |
      |-- instagram.com  -> fetch-instagram-post -> scripts/fetch_instagram.py  (instaloader)
      |-- youtube.com    -> fetch-youtube-video  -> scripts/fetch_youtube.py    (yt-dlp)
      |         both write meta.json (+ video.mp4, captions) into a scratch dir, not the repo
      v
analyze-video  -> scripts/analyze_video.py  (ffmpeg frames + contact sheet + faster-whisper transcript)
      |         then Claude reads sheet.jpg for on-screen text
      v
write-link-note  -> notes/<platform>/<id>.md
      v
fact-check-claims  (WebSearch / WebFetch, primary sources)  -> "Research" table in the note
      v
update-registries  -> registry/verified.md | registry/hoax.md | registry/sidequests.md
      v
decision.md (why) + flow.md (what changed) -> commit -> push to main
```

## Repository map

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Tells Claude to use `process-link` for every shared link. |
| `README.md` | Short human intro. |
| `decision.md` | Log of decisions and reasons. |
| `flow.md` | This file. |
| `requirements.txt` | Python deps: instaloader, yt-dlp, faster-whisper, numpy, Pillow. ffmpeg is a system dependency. |
| `scripts/setup.sh` | Installs deps and checks for ffmpeg. |
| `scripts/fetch_instagram.py` | `<url> <outdir>` -> `meta.json`, `video.mp4`. |
| `scripts/fetch_youtube.py` | `<url> <outdir>` -> `meta.json`, `captions.*.vtt`, `video.mp4`; metadata survives a blocked download. |
| `scripts/analyze_video.py` | `<video> <outdir> [--every N]` -> `frames/`, `sheet.jpg`, `transcript.txt`. |
| `.claude/skills/*/SKILL.md` | One skill per operation: `process-link`, `fetch-instagram-post`, `fetch-youtube-video`, `analyze-video`, `write-link-note`, `fact-check-claims`, `update-registries`. |
| `notes/instagram/<shortcode>.md` | One note per Instagram link. |
| `notes/youtube/<video-id>.md` | One note per YouTube link. |
| `registry/verified.md` | Verified tools, hacks and facts, plus a Pending verification section. |
| `registry/hoax.md` | Hoaxes and misleading claims with evidence. |
| `registry/sidequests.md` | Non-informative videos, one line each. |

## Data and scratch files
Downloaded videos, frames and transcripts stay in a scratch directory outside the repo. Only the note, registry entries and docs are committed, so the repo stays small and contains no downloaded media.

## Current notes
| Note | Verdict |
|---|---|
| [notes/instagram/DeToMLxtdSV.md](notes/instagram/DeToMLxtdSV.md) | partly-verified (components real, earnings claim misleading) |
