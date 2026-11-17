# TROUBLESHOOTING: symptom -> fix

Back to [README.md](README.md). Find the symptom (Ctrl+F a word of the message), do the fix. Sources: `lessons/incidents.json`, `lessons/gotchas/*`, `.claude/skills/clips/QUICKSTART.md` section 5, and the validation reports in `.claude/skills/clips/docs/` (`final-validation-report.md`, `revalidation-report.md`, `long-mode-report.md`, `highlights-report.md`).
Run `python3 .claude/skills/clips/scripts/preflight.py` first: most rows below are what its checks print.

## Setup and accounts

| Symptom | Fix |
|---|---|
| `error: the kaggle CLI is not installed` | Not a Kaggle limit, retrying does nothing. `python3 -m venv ~/kvenv && ~/kvenv/bin/pip install kaggle` (or run `bash migration-setup/setup-environment.sh`). |
| `error: Kaggle credentials are missing (KAGGLE_USERNAME and/or KAGGLE_APITOKEN)` | Set the two variables in the Claude environment settings (names only here, values never in chat), then start a NEW session (variables apply at session start). |
| `account 2: not available (...)` in `kaggle.py check` | No second account: GPU jobs stay on account 1. Fix: set `KAGGLE_USERNAME2` + `KAGGLE_APITOKEN2`; or install `pdftotext` (`apt-get install -y poppler-utils`) so the token can be read from the dataset `<account 1>/kagglegpu2` (KAGGLE.md). |
| `account 2 ... cannot download dataset <user>/kagglegpu2` | A NEW account 1 does not own `kagglegpu2`. Use `KAGGLE_APITOKEN2` instead. |
| `reachable: no (...)` for an account | Token wrong/expired/revoked: create a new one (Kaggle > Settings > API > Create New Token) and update the variable. If the message says phone verification: verify the phone on that account. |
| `kaggle.py` says a kernel cannot be found after changing the Kaggle user | Kernel ids contain the user name: old kernels belong to the old user. Start a new job; old masters need a copy (KAGGLE.md). |
| The session asks you to paste a key in chat | Refuse. Put it in the environment settings. Lesson `keys-never-in-chat`. |
| `WARN settings-allow: N commands not in .claude/settings.json allow` | Not a failure. Approve those commands when asked (before a long wait), or a human adds them to `permissions.allow`. Agents never edit settings. |
| Command denied or "the auto mode classifier gave no verdict" | No verdict = it did not run: run it again once as is. A real denial (account-2 key, GPU step, delete): do not retry the same call; say what was blocked; the lead session runs account-2/GPU steps itself, not a sub-agent. Incident `agent-blocked-by-classifier`. |
| An agent stopped after many no-verdict responses | Re-run the agent (or say "continue"). Long agents can be stopped by repeated classifier errors. |
| `preflight`: `git-remote FAIL` | `git remote -v` must show the NEW private repo; the GitHub App must be installed on it; the environment network must allow `github.com`. |
| `git fetch`/`git push` answers 403 after the repo was transferred or renamed (old name `ARVR7/VideoGeneration`) | The old name is dead for the session. Install the Claude GitHub App on the NEW owner's account for that repo (https://github.com/apps/claude/installations/select_target), accept the collaborator invite, then re-attach the repo (see GITHUB-MOVE.md, "What actually happened"). |
| `git push` rejected (non-fast-forward) | `git pull --no-rebase origin <branch>` then push again. Never force. If `finalise.py` says main was changed from another branch: do not force, ask the user. |
| `deny updating a hidden ref` when mirroring | Delete the pull refs before the push: `git for-each-ref --format='delete %(refname)' refs/pull \| git update-ref --stdin` (GITHUB-MOVE.md, option A). |
| Push to the new repo asks for a password or says authentication failed | Use a fine-grained token of the new account (Contents: write on that repo) in git's credential prompt; never in the URL or chat. |
| An old clone from before 2026-11-15 | Dead: history was rewritten. Clone fresh. |
| `WARNING NOT SAVED TO GITHUB` from checkpoint | Run `python3 .claude/skills/clips/scripts/checkpoint.py --stream streams/<stream>` by hand and tell the user if it still fails. |
| `autosave-pause FAIL` | A `.autosave-pause` file is left behind and silently stops autosave: `rm .autosave-pause`. |
| Nothing is pushed at the end of a turn | No hook calls `autosave.sh` (none is pre-installed): run `bash .claude/scripts/autosave.sh` by hand, or add a Stop hook: CLAUDE-ACCOUNT-SETUP.md section 8 (checkpoint.py still saves after every render step). |

## Kaggle jobs

| Symptom | Fix |
|---|---|
| `LONG VIDEO: ...` | The video is over 90 minutes; the skill switches to long mode by itself (`long_run.py prepare`). |
| `AGE-RESTRICTED` | Stop and ask the user for a file or another link; never look for a bypass (lesson `age-restricted-stop`). |
| `Sign in to confirm you're not a bot` | The skill retries up to 3 times, then asks for a file or another link. Never use cookies or proxies (lesson `youtube-blocks-vm`). |
| `LIMIT REACHED after N tries ...` / `QUOTA` | A real Kaggle limit (weekly 30 GPU h, or a busy T4 queue over 20 min). Wait for the reset, or add `--account 2` to EVERY step of the job. |
| Kernel stays QUEUED 20 min | `kaggle.py wait` deletes it and counts one failed try; run the steps again with a new NAME, adding `--account 2` for a GPU job. |
| Account 2 job cannot read a dataset or kernel of account 1 | A kernel cannot read another account's private data. Run the WHOLE chain with the same `--account`, and make sure the dataset exists on that account. |
| Kernel COMPLETE but nothing fetched, or a background wait died while idle (incidents `lost-wait-kernel-done-unfetched`, `detached-wait-died-idle`) | `python3 .claude/skills/clips/scripts/jobs.py tick` (fetches a finished kernel), or `jobs.py check` for the exact RESUME line. Run `tick` as the FIRST action of every turn during a job. A session that was archived is woken by nothing: open a new one, preflight runs `tick`. |
| `video.mp4` not found after fetch (incident `download-folder-bug`) | Fixed: fetch lifts `dl/` up. `preflight` check `stream-writable` smoke-tests it. |
| Whisper transcript is weak for Hindi | Expected: use YouTube captions whenever they exist (lesson `transcript-captions-first-whisper-weak`). Whisper only without captions, after telling the user; ALWAYS `--lang hi` for Hindi (auto may translate to English; `long_run.py` refuses without it). |
| Captions glue together | Words need a leading space (lesson `transcript-leading-space`); `vtt_to_transcript.py` adds it. |
| Moment times drift later in the video | Take times from the YouTube captions, not from other tools (lesson `captions-are-the-clock`). |

## Rendering

| Symptom | Fix |
|---|---|
| Render stopped, `no space left` (incident `disk-full-render-stop`) | `df -h`; delete finished scratch dirs and `/tmp` leftovers; keep 5+ GB free (`preflight` `disk-free`); then `long_run.py render --stream streams/<s> --skip-done`. |
| `ffmpeg` / `ffprobe` does not run | `apt-get install -y ffmpeg`. |
| `ModuleNotFoundError: numpy` or PIL | `python3 -m pip install numpy pillow`. |
| Animations missing, static title instead; `WARNING animations ...` | Node 22 or HyperFrames/Chrome missing. `npx --yes hyperframes@0.9.52 --version` then `npx --offline hyperframes@0.9.52 browser ensure`; needs registry.npmjs.org and disk (lesson `hyperframes-needs-disk`). A cancelled overlay render is retried 3 times. |
| Highlights have no commentary; `tts.py` exits 3 | Kokoro not installed: `python3 .claude/skills/clips/scripts/commentary/tts.py --setup` (needs pypi.org, download.pytorch.org, huggingface.co, github.com). |
| `check_layout.py` FAIL | Run it on the clip JSON to see which zone fails (platform UI zones: bottom 384 px, right 162 px). `layout.profile=classic` clips only print NOTE. Fix with the key in `CONTROLS.md`, for example `layout.game_shift_extra=70`. Missing facecam (incident `missing-facecam-or-layout-check`): `preflight --facecam NAME`. |
| Webcam/split layout crops most of the game | Do not force it; use `--layout gameplay` on CPU (lessons `webcam-layout-crops-game-cpu`, `gemini-auto-layout-cuts-stream`). |
| ffmpeg crop wrong when scaling with zoom | Crop expressions must use the scaled size (1080*Z), not `in_w` (lesson `ffmpeg-crop-in-w-fixed`); the engine already does. |
| Output louder than the limit | Two-pass loudnorm with true peak -0.4 dB headroom (lesson `loudnorm-aac-headroom`). |
| Highlights preview too big | `output.size_cap_mb` (5-95, default 85); masters via `output.preset=upload` (lesson `highlights-preview-size-cap`). |
| Edit refused: no source video | On a fresh clone the source is not there: the session re-downloads it first (re-fetch commands are printed). |
| `facecam.voice=low` refused | Only works with a surprise facecam variant (e.g. `girl_surprise_10s`); the message names the usable items. |

## Lessons, index, docs

| Symptom | Fix |
|---|---|
| `lessons ... no topic with two active notes` / graph out of date | `python3 .claude/skills/lessons/scripts/build_graph.py` (prints `ok: N notes, M edges`). Old notes get `status: superseded`. |
| `stale-docs`: SKILL.md cites a script or flag that does not exist | Fix the doc (check `preflight` `docs-paths`); one small commit. |
| `incidents` check FAIL | A new incident row needs its check written first in `preflight.py`; or the user defers it (`"deferred"`). |
| `LATEST.md` / `streams/index.json` out of date | `python3 .claude/skills/clips/scripts/build_index.py`. |
| Clip rights worry (YouTube reused-content, Rockstar policy) | Not a bug: each `post.md` carries the warning; commentary makes highlights safer; monetised channels need a licence (lessons `youtube-reused-content-needs-commentary`, `rockstar-policy-non-commercial`). Posting is the user's decision. |

## Still stuck?

1. Read the error line completely; every script prints ONE line with the fix.
2. `python3 .claude/skills/lessons/scripts/query.py --help` and search the lessons for a word of the error.
3. Open `KNOWLEDGE-BASE.md` and `PIPELINE.md` in this folder, then ask the user ONE short question.
