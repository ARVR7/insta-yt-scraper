# Flow

How a shared link becomes notes and registry entries, and what lives where. Update this file whenever a script, skill or folder is added or changed.

## Entry points

An hourly scheduled task (`Process Link Inbox queue`, Sonnet 5.5) starts a fresh session that runs `process-queue` when open `link` issues exist.

```
Android share sheet -> docs/ web app (GitHub Pages) -> GitHub issue labelled `link` --user asks--> process-queue
Link Inbox page (claude.ai artifact, db collection `links`) --user asks--> process-queue --> process-link (per link)
chat message with a link ------------------------------------------------> process-link
```

The page only queues links and shows results; it cannot run scrapers or wake Claude. `process-queue` reads queued rows with `ArtifactData`, runs the pipeline, and writes status, verdict, summary and the note URL back so the page shows them.

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
analyze-comments (YouTube via fetch_youtube.py --comments; Instagram only if the user pastes them)
      |         -> leads + noise ratio, no claim is trusted from comments
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
categorize-link -> category / subcategory / location / also, validated against taxonomy.yml
      v
update-library  -> scripts/build_index.py -> data/library.json + library/*.md (generated)
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
| `scripts/fetch_youtube.py` | `<url> <outdir> [--comments N]` -> `meta.json`, `comments.json`, `captions.*.vtt`, `video.mp4`; metadata survives a blocked download. |
| `scripts/analyze_video.py` | `<video> <outdir> [--every N]` -> `frames/`, `sheet.jpg`, `transcript.txt`. |
| `docs/` | Installable web app (GitHub Pages) with a Web Share Target. Three tabs: **Library** (usefulness ring, a shelf of category tiles that drill into subcategories and locations, search and a filter sheet for sort, usefulness, platform, date, creator and tool; tap a card for a note with summary and what checks out), **Queue** (add a link; each link shows a Waiting / Working / Done track), **Claims** (verified, hoax, side quests as collapsible cards). Settings holds a System / Light / Dark theme switch. Reads the repo through the GitHub API with a fine-grained token stored on the phone (Issues read/write, Contents read-only). |
| `taxonomy.yml` | Closed vocabulary: categories with subcategories, aliases, icons and colours; locations (country, city). Single source of truth. |
| `scripts/taxonomy.py` | Shared lookup code plus `check`, `merge-sub`, `merge-cat` and `rename-city` for keeping the taxonomy tidy as it grows. |
| `scripts/build_index.py` | Validates notes against the taxonomy and builds `data/library.json`, `data/taxonomy.json` and `library/`. |
| `data/library.json`, `data/taxonomy.json` | Generated index and vocabulary the app reads. |
| `library/README.md`, `library/by-category/`, `library/by-location/`, `library/by-usefulness/` | Generated lists of every link with key info, grouped for reading on GitHub. |
| `.claude/skills/*/SKILL.md` | One skill per operation: `process-link`, `fetch-instagram-post`, `fetch-youtube-video`, `analyze-video`, `analyze-comments`, `write-link-note`, `fact-check-claims`, `update-registries`, `categorize-link`, `update-library`, `analyze-comments`, `process-queue`. |
| Link Inbox artifact | https://claude.ai/artifact/FLi1JREBRUV493gipCS5AG (source is not in the repo; it lives on claude.ai). |
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
| [notes/instagram/DegLPFbTBpi.md](notes/instagram/DegLPFbTBpi.md) | partly-verified (product real, "free" misleading, demo unproven) |
