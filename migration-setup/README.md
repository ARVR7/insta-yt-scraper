# Move the VideoGeneration project to a new GitHub account + a new Claude account

Start here. This is the ONLY file you must open. Read the checklist, paste the bootstrap prompt, done.
It is written for a person with ADHD and for a Claude session that follows it: short steps, exact commands, time estimates.
No secret is written in any file of this folder. Only the NAMES of variables and where each key is created.

## Overview (15 lines)

1. The project cuts a YouTube stream into vertical 40-55 s clips (or one 5-6 min highlights video) with captions, zoom and a streamer-reaction overlay.
2. The brain is a Claude skill in the repo: `.claude/skills/clips/SKILL.md`. The memory is a knowledge graph in `lessons/`.
3. Heavy work (download from YouTube, Whisper) runs on free Kaggle GPUs/CPUs; the rendering runs in the Claude cloud VM (ffmpeg, optional Node/HyperFrames).
4. Git holds the code, the skills, the lessons, settings and the SMALL final clips. It does not hold source videos or 60 fps masters.
5. Three accounts are involved: GitHub (the repo), Claude (sessions + environment), Kaggle (GPU, datasets). Only the first two change in this move; Kaggle can stay the same.
6. The repo MUST be PRIVATE (AI-generated reference images of the fictional streamer, streamer clips, settings).
7. Keys live ONLY in the Claude environment (variables or Network secrets), never in chat and never in a file in the repo.
8. Work is saved to a session branch `ccr-*` automatically (`checkpoint.py` after every step, plus `bash .claude/scripts/autosave.sh` run by hand or by a Stop hook you add; no hook is pre-installed, see CLAUDE-ACCOUNT-SETUP.md section 8); final clips go to `main` through `finalise.py` (squashed, fast-forward, no force).
9. Every job starts with `preflight.py` (14 checks, 6 s) and reads the lessons first: "learn first, then plan".
10. The user's style: short answers, no walls of text (the `i-have-adhd` style: paste the text of `CLAUDE-INSTRUCTIONS.md` into claude.ai Settings > Profile; the repo `CLAUDE.md` carries the short form).
11. The move needs: a new private repo with the full history, a Claude environment with 3 variables, and a smoke test.
12. Nothing needs the old accounts afterwards. Revoke them with `REVOKE-AND-SECURITY.md` once `VERIFY.md` is all green.
13. Budget: about 60-90 minutes the first time, most of it waiting for pushes and installs.
14. If a step fails, open `TROUBLESHOOTING.md` (symptom -> fix table).
15. If you are the Claude session reading this: do the bootstrap prompt below, report what is missing, never print a key.

## What is where

```
GIT (private repo, travels with the move)
VideoGeneration/
  CLAUDE.md                       standing rules, loaded by every session by itself (short form of CLAUDE-INSTRUCTIONS.md)
  README.md, LATEST.md            repo overview; GENERATED list of newest clips (do not edit by hand)
  .gitignore                      keeps source/, masters/, caches, renders out of git
  .claude/
    settings.json                 allows kaggle.py without prompts (3 patterns)
    scripts/autosave.sh           commit + push of the session branch (run by hand; no hook calls it)
    REQUIREMENTS.md               what the user asked for and its status
    skills/
      clips/                      THE PIPELINE: SKILL.md (procedure), QUICKSTART.md, CONTROLS.md, PLAN.md, defaults.json
        scripts/                  render_clip, edit_clip, make_clips, check_layout, preflight, finalise, checkpoint, jobs, long_run ...
          download/ transcript/ moments/ zoom/ captions/ commentary/ trials/
        assets/                   fonts/, facecam/ (library + videos + PROMPTS.md + reference/ = private AI images), animations/ (HyperFrames presets)
        destinations/             one JSON per upload target
        docs/                     research, decisions, validation reports, tool notes
      lessons/                    scripts of the knowledge graph (query.py, add_lesson.py, build_graph.py)
      yt-*/                       third-party YouTube helper skills (optional)
  lessons/                        THE MEMORY: preferences, rules, gotchas, decisions, tools, incidents.json, graph.json, INDEX.md
  streams/
    index.json                    GENERATED manifest of all streams and clips
    <date>_<slug>/                one folder per stream: stream.json, clips/<id>/ (social.mp4, clip.json, poster, post.md ...), docs/
  docs/                           audit-prompt.md, self-improvement-design.md
  archive/                        text notes of old runs (history only)
  migration-setup/                THIS FOLDER

OUTSIDE GIT (does NOT travel with the repo; each item says how to get it back)
  source videos                   streams/*/source/ (gitignored). Re-downloaded from the stream link on a Kaggle CPU kernel.
  upload masters                  streams/**/masters/ (60 fps, ~100 MB each). Kaggle private dataset clips-masters-<stream> if you made one; else re-render.
  caches                          ~/.cache/clips-commentary (Kokoro, 1.7 GB), ~/.cache/hyperframes (290 MB), streams/*/docs/cache/ -> rebuilt on demand
  Kaggle datasets                 live on the KAGGLE account, not on GitHub or Claude (see KAGGLE.md)
  environment variables           KAGGLE_APITOKEN, KAGGLE_USERNAME (+ optional HF_Token, no script reads it; optional KAGGLE_USERNAME2, KAGGLE_APITOKEN2) -> CLAUDE-ACCOUNT-SETUP.md
  Claude account preferences      response style `i-have-adhd` (Settings > Profile), connectors, account skills -> CLAUDE-ACCOUNT-SETUP.md
```

## FAST PATH checklist

Tick each box as you go. Times are for a calm first run. Stop at any red box and open `TROUBLESHOOTING.md`.

- [ ] **1. New GitHub account is ready** (5 min). Sign in, enable 2FA. Note the username: `NEW_USER`.
- [ ] **2. Create the NEW PRIVATE repo and copy everything** (10-20 min). Follow option A in [GITHUB-MOVE.md](GITHUB-MOVE.md). Short version:
  ```
  git clone --mirror https://github.com/ARVR7/VideoGeneration.git old.git
  # on github.com: New repository, name VideoGeneration, PRIVATE, EMPTY (no README, no .gitignore, no license)
  cd old.git && git push --mirror https://github.com/NEW_USER/VideoGeneration.git
  ```
  (GitHub's "Import repository" page also works; see GITHUB-MOVE.md, the section about copying later commits.)
- [ ] **3. Check the repo is PRIVATE** (1 min). github.com/NEW_USER/VideoGeneration > Settings > General > bottom: "Change visibility" must say Private.
- [ ] **4. New Claude account: connect GitHub** (3 min). https://claude.ai/connect-github . Then install the Claude GitHub App on the new repo: https://github.com/apps/claude/installations/select_target . Details: [CLAUDE-ACCOUNT-SETUP.md](CLAUDE-ACCOUNT-SETUP.md).
- [ ] **5. Kaggle keys ready** (10 min if you reuse the old Kaggle accounts, 25 min if new ones, phone verification included). [KAGGLE.md](KAGGLE.md). You need: Kaggle username + an API token (Settings > API > Create New Token). The key goes into step 6, never into chat.
- [ ] **6. Create the cloud environment** (10 min). claude.ai/code > Environments > new. Network: unrestricted (simplest) or the host list in CLAUDE-ACCOUNT-SETUP.md. Variables: `KAGGLE_USERNAME`, `KAGGLE_APITOKEN`, optional `HF_Token` (no script reads it; it only avoids Hugging Face rate limits for the Kokoro download), optional `KAGGLE_USERNAME2`, `KAGGLE_APITOKEN2`. Paste the 1-line wrapper from CLAUDE-ACCOUNT-SETUP.md section 4 as the setup script (the box allows only 100 lines; the real script is in the repo). Add the new repo to the environment's Repositories list.
- [ ] **7. Paste the response style `i-have-adhd`** (2 min). claude.ai Settings > Profile (personal preferences); text is in [CLAUDE-INSTRUCTIONS.md](CLAUDE-INSTRUCTIONS.md) section 1.
- [ ] **8. Start the first session and paste the bootstrap prompt** (5 min, below).
- [ ] **9. Smoke test** (5 min, commands below). Everything PASS.
- [ ] **10. Real first job** (30-60 min): `/clips <stream link>` (below).
- [ ] **11. Final verification list** (8 min): run `python3 migration-setup/verify_manifest.py --no-preflight` (PASS, 0 extra, 0 changed; the repo NAME may differ from the old one, it compares trees, not names), then the Fable carry-over check ([FABLE-CARRYOVER-CHECK.md](FABLE-CARRYOVER-CHECK.md), paste it into a session), then [VERIFY.md](VERIFY.md), all boxes ticked.
- [ ] **12. Revoke and clean the old accounts** (15 min): [REVOKE-AND-SECURITY.md](REVOKE-AND-SECURITY.md). Only after step 11.

Total: about 60-90 minutes the first time (steps 1-9 about 50 minutes, step 10 depends on the stream length).

## Bootstrap prompt (paste this into the FIRST new Claude session, with the new repo attached)

```
Read migration-setup/README.md, then every file it links, fully (PIPELINE.md, KNOWLEDGE-BASE.md,
HISTORY-AND-REQUIREMENTS.md, CLAUDE-INSTRUCTIONS.md, GITHUB-MOVE.md, CLAUDE-ACCOUNT-SETUP.md,
KAGGLE.md, VM-SETUP-LOG.md, TROUBLESHOOTING.md, VERIFY.md, REVOKE-AND-SECURITY.md,
MIGRATION-AUDIT.md, MIGRATION-REAUDIT.md), EXCEPT the folder history/ (about 1 MB, it would fill the context):
there read only history/00-README.md, history/04-session-summaries.md and history/01-user-messages.md;
read history/02-conversation.md and history/03-agent-briefs.md only on demand.
Then run: python3 .claude/skills/clips/scripts/preflight.py
Fix what fails (install tools, never print or ask me to paste a key; keys are environment variables).
Then run the smoke test from the README and tick VERIFY.md.
Tell me, in a short list, what is still missing and what I must do myself.
Follow the response style in CLAUDE-INSTRUCTIONS.md (and the repo CLAUDE.md): next action first, numbered steps, one question at a time.
```

## First smoke test (5 minutes, run in the repo root of the new session)

1. Machine check, 14 checks, about 6 s. 12 PASS and 2 WARN is the expected result (WARN `settings-allow` and `audit-due` are fine; any FAIL is not):
   ```
   python3 .claude/skills/clips/scripts/preflight.py
   ```
2. Kaggle check: account 1 prints `reachable: yes` (account 2 too, only if you use a second account; user names only, never a token):
   ```
   python3 .claude/skills/clips/scripts/download/kaggle.py check
   ```
3. Dry run of `edit_clip` on a COPY of a committed clip (changes nothing in the repo, renders nothing; it saves a numbered version inside the copy only):
   ```
   S=$(mktemp -d)
   cp -r streams/2026-11-14_this-is-not-a-game/clips/449-503s_gta-6-logo-goosebumps $S/
   python3 .claude/skills/clips/scripts/edit_clip.py $S/449-503s_gta-6-logo-goosebumps/clip.json captions.on=true --note "smoke test"
   python3 .claude/skills/clips/scripts/edit_clip.py $S/449-503s_gta-6-logo-goosebumps/clip.json --history
   ```
   Expected: `saved as vN` and a `captions: {... "on": false ...} -> {... "on": true ...}` line. Add `--render` only if the source video is on the machine (it is not on a fresh clone).
4. Layout check of a published clip, expected `0 FAIL`:
   ```
   python3 .claude/skills/clips/scripts/check_layout.py streams/2026-11-14_this-is-not-a-game/clips/449-503s_gta-6-logo-goosebumps/clip.json | grep -c " FAIL "
   ```
   (prints `0`; `grep -c` exits 1 when the count is 0, that is fine.)

## The real first job

In the new session, type (the `clips` skill triggers by itself on a stream link):

```
/clips <YouTube stream URL>
Length: about <N> minutes (or: I do not know)
Language: <Hindi / English>
Post to: <social / youtube-shorts / instagram-reels / clean>
Run the setup checks first and tell me what is missing.
```

What happens: preflight, lessons are read, one short question set (facecam, destinations), a Kaggle CPU kernel downloads the stream, moments are picked, clips are rendered (about 1 min each), `LATEST.md` is updated, work is checkpointed to the session branch, `finalise.py` puts the final clips on `main`. Details in [PIPELINE.md](PIPELINE.md).

Over 90 minutes the skill switches to long mode on its own. Never skip the Kaggle step: YouTube blocks the Claude VM, only Kaggle kernels can download.

## Table of contents of this folder

| File | What it is | Who writes / reads it |
|---|---|---|
| [README.md](README.md) | this file: checklist, bootstrap prompt, smoke test | you + the new Claude |
| [PIPELINE.md](PIPELINE.md) | how the clip pipeline works, step by step | read by the new Claude |
| [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md) | the lessons graph, preferences, rules, how to query and extend them | read by the new Claude |
| [HISTORY-AND-REQUIREMENTS.md](HISTORY-AND-REQUIREMENTS.md) | what happened so far and what the user asked for | read by the new Claude |
| [history/00-README.md](history/00-README.md) | FULL history: every user message, the dialogue, agent briefs, compaction summaries (sanitized export of the whole session) | read by the new Claude |
| [CLAUDE-INSTRUCTIONS.md](CLAUDE-INSTRUCTIONS.md) | the response style `i-have-adhd` (paste into Settings > Profile) and the standing instructions for the new account | you paste it into the account |
| [GITHUB-MOVE.md](GITHUB-MOVE.md) | 4 ways to move the repo (mirror, transfer, fork, organization), branch cleanup, private, copying later commits | you |
| [CLAUDE-ACCOUNT-SETUP.md](CLAUDE-ACCOUNT-SETUP.md) | Claude account: GitHub app, environment, variables, network hosts, setup script, hooks, skills | you |
| [setup-environment.sh](setup-environment.sh) | the setup script for the new environment (idempotent, no secrets; over 100 lines, too long for the 100-line box, so it is run by the one-line wrapper in CLAUDE-ACCOUNT-SETUP.md section 4) | run by the one-line wrapper |
| [KAGGLE.md](KAGGLE.md) | the two Kaggle accounts, datasets, phone verification, the key vault datasets | you |
| [VM-SETUP-LOG.md](VM-SETUP-LOG.md) | everything installed on the old VM and how to redo it | new Claude |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | symptom -> fix table | both |
| [VERIFY.md](VERIFY.md) | final checklist with commands and expected output | both |
| [REVOKE-AND-SECURITY.md](REVOKE-AND-SECURITY.md) | what to revoke or delete on the old accounts, security rules | you |
| [MANIFEST.json](MANIFEST.json) | fingerprint of the old repo (file hashes, counts, env var NAMES, dataset names; no secrets), written by the lead's `make_manifest.py` | read by `verify_manifest.py` |
| [make_manifest.py](make_manifest.py) | run in the OLD repo to (re)write MANIFEST.json (lead) | the old session only |
| [verify_manifest.py](verify_manifest.py) | run in the NEW repo: `python3 migration-setup/verify_manifest.py` compares it with MANIFEST.json (read-only; `--no-preflight`, `--kaggle`, `--skip-env`; it compares trees and hashes, NOT the repo name, which differs after a transfer or rename) (lead) | you + the new Claude |
| [MIGRATION-AUDIT.md](MIGRATION-AUDIT.md), [MIGRATION-REAUDIT.md](MIGRATION-REAUDIT.md) | the first audit and the re-audit of this folder (gaps found, fixed or open; they are part of the knowledge) (lead) | read once |
| [FABLE-CARRYOVER-CHECK.md](FABLE-CARRYOVER-CHECK.md) | a prompt for a carry-over auditor agent: after the move, checks that everything arrived (lead) | paste into a session |

Facts in this folder were checked on 2026-11-16 against the repo at branch `main` plus the session branch (`ccr-4e94c80c-rpb12o`).

## Full history

The complete project history (every message you typed, the dialogue, all agent work briefs, the context summaries) is in [history/](history/00-README.md), made by `export_history.py` (secrets redacted automatically).
Read `history/04-session-summaries.md` first, then `history/01-user-messages.md`; the rest is detail. Re-make it with `python3 migration-setup/export_history.py`.
Keep the repo private: skim the files once before it is ever made public (see REVOKE-AND-SECURITY.md).
