**Newest clips: [LATEST.md](LATEST.md)** (generated, newest first, one row per clip with links to every video and its post kit).

# VideoGeneration

Short-form video: cutting vertical clips (40-55 s) from long streams and videos, with the streamer-reaction overlay. Everything that runs lives in `.claude/`, everything that was made lives in `streams/`, so a website can render straight from the repo (`streams/index.json`).

```
README.md                    this file
CLAUDE.md                    standing rules loaded in every Claude session (12 rules, first commands, answer format)
migration-setup/             the account/repo move kit: README (checklist, bootstrap prompt), audits, manifest, verify scripts, full history/
docs/                        audit-prompt.md, self-improvement-design.md
LATEST.md                    GENERATED: newest clips first (date, stream, title, length, links to each video, post kit), then the highlights videos (folder, length, segments, commentary yes/no)
.gitignore
.claude/
  REQUIREMENTS.md            what the user asked for and its status
  scripts/autosave.sh        commit + push of the session branch, run by the lead when the platform reminder appears and about every 10 minutes (no hook calls it) (stream content reaches main only through clips/scripts/finalise.py; pauses while .autosave-pause exists)
  skills/
    clips/                   ENTRY POINT: stream link in, editable clips out
      SKILL.md CONTROLS.md PLAN.md QUICKSTART.md defaults.json
      destinations/          one JSON per upload target (youtube-shorts, instagram-reels, clean, whop-content-rewards)
      scripts/               engine: render_clip, edit_clip, make_clips, clip_schema, check_layout, add_facecam, build_index
        download/            kaggle.py, download_job.py, stream_folder.py (makes streams/<date>_<slug>/)
        transcript/          vtt_to_transcript.py, run.py (Whisper / GPU path)
        moments/             find_moments.py, weights.json, reaction_words.json
        zoom/                plan_zooms.py
        captions/            ass_from_words.py, roman_map_hinglish.json
        trials/              model trial scripts
      assets/                fonts/, facecam/ (library.json + videos + PROMPTS.md, reference/ = private AI reference images), animations/ (HyperFrames presets)
      docs/                  research, decisions, destination rules, tool notes, openshorts notes, examples
    lessons/                 the lessons skill (scripts for the knowledge graph)
    yt-*/                    YouTube helper skills (third party, untouched)
lessons/                     the knowledge graph: the user's preferences, rules and gotchas (read before every clip job)
streams/
  index.json                 GENERATED manifest of every stream, clip and highlights video (what a site reads)
  <YYYY-MM-DD>_<slug>/       one folder per stream
    stream.json              title, channel, url, language, duration, date added, rights
    clips/<start>-<end>s_<slug>/   one folder per clip: social.mp4 (and clean.mp4 ...), clip.json (all settings), poster.jpg, post.md, edit-notes.md, versions/
    highlights/<slug>/       one 16:9 highlights video: highlights.json, post.md, render-report.json, commentary-script.md, versions/ (preview.mp4 is local only, gitignored: sent with SendUserFile)
    docs/                    moments.json, review.md, sheets/, reports, transcript, demo/
archive/                     text notes of removed old runs (history)
```

New clip job: read `.claude/skills/clips/SKILL.md` (Step 0 runs `python3 .claude/skills/lessons/scripts/query.py ...`). Rebuild the manifest and LATEST.md: `python3 .claude/skills/clips/scripts/build_index.py`.

Source videos are not in git (`streams/*/source/` is ignored; clip.json `source_local` names the file on the machine that has it). Git keeps the small preview of each clip; the full-quality upload masters live outside git (an optional private Kaggle dataset per stream, `clips-masters-<stream>`; `streams/index.json` does not list masters). Highlights videos (`preview.mp4`, 80 MB) are also not committed (one early preview is still tracked and stays in history); `LATEST.md` and `streams/index.json` list them with their path, length, segments and commentary, and say the file is local only.

History: the git history was rewritten on 2026-11-15 and old large files are gone from main; they cannot be recovered from git. Only text notes of old runs survive, in `archive/` (see `archive/cleanup-2026-11-14.md` and `archive/restructure-2026-11-15.md`). The old `video-project/` and old clip sets were removed on 2026-11-14.

Privacy: this repo must stay private. `.claude/skills/clips/assets/facecam/reference/` holds photo-real AI-generated reference images of the fictional streamer girl (see the note at the top of `assets/facecam/PROMPTS.md`).

Plan and decisions: `.claude/skills/clips/PLAN.md` (start with its "Current plan" section).

Full history: `migration-setup/history/00-README.md` (every user message, conversation, agent briefs and session summaries since 2026-10-24).

Repo name: the repo was transferred to the new GitHub account as `soverellp/clipper` (the old `ARVR7/VideoGeneration` name returns 403; the old account stayed a collaborator). A Claude session sees it only if the Claude GitHub App is installed on the new owner for that repo (https://github.com/apps/claude/installations/select_target); see `migration-setup/GITHUB-MOVE.md`.
