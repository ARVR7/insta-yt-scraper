---
name: openshorts-clip
description: Kaggle download of a YouTube stream, YouTube captions to a word-level transcript, and the optional Kaggle GPU run (Whisper + picking). Rendering clips is done by the clips skill. Use when a stream link must be downloaded or needs a GPU transcript.
---

# openshorts-clip: download, transcript, GPU path
Entry point for clip jobs is `.claude/skills/clips/SKILL.md` (the clips engine renders everything on CPU). This skill only keeps the Kaggle helpers.

## Step 0: learn first, then plan (do this before any work)
Run `python3 .claude/skills/lessons/scripts/query.py --stage plan,download,moments,render,layout,captions,zoom,facecam,publish,infra` and apply every active lesson. Tell the user the plan in 6 lines (moments, length, layout, captions, zoom targets, character) before rendering.
Last step of every job: turn each user correction into a lesson (`add_lesson.py`, use `--supersedes` when they change their mind), rebuild the graph, push `lessons/` to main. See `.claude/skills/lessons/SKILL.md`.

## Download (always on a Kaggle CPU kernel)
YouTube blocks the VM. Never bypass bot checks, never use cookies, proxies or other player clients.
1. `python3 .claude/skills/clips/scripts/download/kaggle.py download os-dl-NAME URL`, then `kaggle.py wait os-dl-NAME LOGFILE`.
2. The kernel stops itself if `age_limit >= 18`. If age-restricted or blocked: STOP and ask the user for a file or another link.
3. `kaggle.py fetch os-dl-NAME DIR`: video plus `video.<lang>-orig.vtt` land on the VM.
4. Folder name: `python3 .claude/skills/clips/scripts/download/stream_folder.py "Exact YouTube title"`.
Needs `KAGGLE_USERNAME` + `KAGGLE_API_TOKEN` (or `~/.kaggle/kaggle.json`) and `pip install kaggle`.

## Captions to transcript
`python3 .claude/skills/clips/scripts/transcript/vtt_to_transcript.py video.<lang>-orig.vtt transcript.json <lang>`: word-level transcript from YouTube captions, no speech model (words get the leading space the renderer needs).

## GPU path (only when there are no usable captions)
`run.py` inside a Kaggle kernel does Whisper large-v3 (+ optional LLM picking and its own render). Submit with `kaggle.py push NAME --kernel-source USER/os-dl-NAME --file "/kaggle/input/os-dl-NAME/**/video.mp4" --layout gameplay --clips 4-6 --min 40 --max 55 [--no-hook] [--caption-lang en] [--chunk-minutes 11]`, then `kaggle.py wait` and `kaggle.py fetch`. All options: `python3 .claude/skills/clips/scripts/transcript/run.py --help`. Gemini picking needs a private Kaggle dataset with the key (`--dataset OWNER/SLUG --gemini-key-file ...`); only list file names, never print the key.

## Other
- The stream footage is someone else's: post only with permission or as commentary.
- Keep `fonts/` (Montserrat ExtraBold, used by the clips engine).
- Older notes of the removed CPU/character scripts and run logs: text notes in `archive/`. Git history was rewritten on 2026-11-15, so removed files are not recoverable from it.
