# Quickstart: a fresh session, a link, clips

Read this once on a new machine. `SKILL.md` is the full procedure; this page is only the setup and the first message.

## 1. What to attach to the session
- This repo (`VideoGeneration`) checked out in the session. Everything the skill needs is in it: scripts, facecam library, fonts, defaults, lessons. No source video is stored in git.
- Two secrets in the session's ENVIRONMENT settings (never in chat, never in a file in the repo):
  - `KAGGLE_USERNAME` = your Kaggle user name.
  - `KAGGLE_APITOKEN` = a Kaggle API token (kaggle.com, Settings, API, Create New Token). The scripts also accept `KAGGLE_API_TOKEN` or `~/.kaggle/kaggle.json`.
  The scripts never print these values. If a session asks you to paste a value in chat, refuse and set it in the environment instead.
  - Optional second account (own 30 GPU hours per week): `KAGGLE_USERNAME2` and `KAGGLE_APITOKEN2`. If they are not set, the scripts read the token of the second account (`sovere`) from the private dataset `<your user>/kagglegpu2` (file `kagglegpu2.pdf`, needs `pdftotext`, parsed in memory, never written to a file or printed). `kaggle.py check` shows both accounts (user names only) and whether account 2 answers. **Agents never read the key or the PDF**: for any Kaggle call on a chosen account run `python3 scripts/download/kaggle.py --account 2 raw <kaggle CLI args>` (for example `raw kernels push -p DIR --accelerator NvidiaTeslaT4`); the script puts the token only into the child process and masks all output. `raw` refuses any argument naming `kagglegpu2` and any `datasets download` that is not `<active user>/clips-masters-<stream>`.
- Optional commit trailer: the scripts that commit (`checkpoint.py`, `finalise.py`, `autosave.sh`) add NO `Co-Authored-By` or `Claude-Session` line unless the environment variable `CLAUDE_COMMIT_TRAILER` is set. Its value is the full trailer text; write a line break as `\n`, e.g. `Co-Authored-By: Claude <noreply@anthropic.com>\nClaude-Session: <this session's URL>` (use the attribution lines the session's system reminder gives; never a URL of another account's session). Unset = no trailer.
- Nothing else. No YouTube cookies, no proxies (the skill never uses them).

## 2. Tools the machine needs
| Need | Why | Check | Install |
|---|---|---|---|
| `kaggle` CLI | every download and transcript job runs in a Kaggle kernel (YouTube blocks the VM) | `python3 .claude/skills/clips/scripts/download/kaggle.py check` | `pip install kaggle`. In a venv: `python3 -m venv ~/kvenv && ~/kvenv/bin/pip install kaggle`; the scripts find `~/kvenv/bin/kaggle` and `~/.local/bin/kaggle` by themselves, or put it on PATH: `export PATH=$HOME/kvenv/bin:$PATH`, or point to it: `export KAGGLE_BIN=/path/to/kaggle` |
| ffmpeg + ffprobe | cutting, loudness, scene cuts | `ffmpeg -version`, `ffprobe -version` | `apt-get install -y ffmpeg` |
| python3 with numpy and PIL | layout check, captions, title, find_moments | `python3 -c "import numpy, PIL"` | `pip install numpy pillow` |
| Node 22 + npx | ONLY for animated titles and overlays (`hook.animation=reveal`, `animations.on=true`); not needed for normal clips | `node --version` (v22.x) | install Node 22 (nodejs.org or your package manager) |
| Kokoro voice | ONLY for highlights commentary (required for monetisation); the render warns and goes on without it | `~/.cache/clips-commentary/venv/bin/python -c "import kokoro"` | `python3 .claude/skills/clips/scripts/commentary/tts.py --setup` (needs pypi.org, download.pytorch.org, huggingface.co, github.com once) |
| HyperFrames 0.9.52 | same, animations only | `npx --offline hyperframes@0.9.52 --version` | the first animated render downloads it (npm network) and a Chrome (about 2 GB of disk); if that fails the clip keeps the static title and one WARNING is printed |

Visual moments (optional, on by default when the whole source video is on the machine; step 3b of `SKILL.md`): no new tool is needed (ffmpeg, numpy and PIL are enough, about 1 min of CPU per 30 min of video). Say "no visual review" (`moments.visual=off`) to skip it and "review visually" to ask for it later. A Hindi stream with the streamer's webcam in a corner: tell the session where it is (`--cam-box`), else the 'reaction' part is left out. The optional Gemini reviewer needs your own `GEMINI_API_KEY` in the environment (never in chat or in a file); without it the reviewer is a Haiku or Sonnet sub-agent and nothing needs to be set.

## 3. Network hosts
The environment must allow: `www.kaggle.com` (the CLI may need more Kaggle or storage hosts; if a call is blocked, the proxy message names the host: add it), `pypi.org` and `files.pythonhosted.org` (pip), `github.com` (git push). For animations also `registry.npmjs.org` and the Chrome download host. YouTube itself is reached only from inside Kaggle kernels, so the VM does not need it.

## 4. What to type in a fresh Sonnet session
```
Use the clips skill (.claude/skills/clips/SKILL.md; read it first, then QUICKSTART.md).
Link: <YouTube URL>
Length: about <N> minutes (or: I do not know)
Language: <Hindi / English>
Post to: <social / youtube-shorts / instagram-reels / clean>
Run the setup checks first and tell me what is missing.
```
The session then runs its lessons, asks one short question set (facecam, destinations, anything the defaults do not cover), routes by length (90 minutes or less: normal path; over 90 minutes, or no captions: long mode), and shows `LATEST.md` and the review table.

Highlights instead of clips (a 5-6 minute 16:9 YouTube video): add to the message `Type: highlights (5-6 minutes)`; the session runs `make_highlights.py`, then `render_highlights.py` and sends you the video with SendUserFile (`preview.mp4` is not committed to git; SKILL.md, section Highlights; needs ffmpeg and, for the animations, Node 22 + HyperFrames as in section 2; commentary is required for monetisation).

## 4b. While a job runs (what the session does by itself, and what to expect)
- Step 0 of every job is `python3 .claude/skills/clips/scripts/preflight.py`: it checks Kaggle, ffmpeg, disk space (5 GB), that git can reach GitHub, that autosave is not paused, any job left over from an earlier session, and that the docs name only scripts and flags that exist. A FAIL comes with a one-line fix; a WARN about commands your settings do not allow means: approve them now, before a long wait.
- The FIRST action of every turn during a job is `python3 .claude/skills/clips/scripts/jobs.py tick` (no tokens, safe to repeat). It fetches a finished Kaggle kernel that nobody collected and reports anything lost.
- A long wait is backed by `send_later` at ETA + 10 minutes, re-armed every 15 minutes, at most 12 wakes per job (`jobs.py tick --wake` counts them); `Monitor` on the log is only the fast path and `/loop` is for when you are watching live. The session never relies on ScheduleWakeup or cron surviving a container restart; an archived session is woken by nothing, so open a new session and its preflight finds the job.
- Every step writes `streams/<s>/docs/journal.jsonl` by itself; at the end the session writes `docs/retro.md` (step 9): time per step, idle gaps, retries, what you corrected, one disposition per finding. `python3 .claude/skills/clips/scripts/long_run.py status --stream streams/<s>` prints `RETRO MISSING` until it exists. When five retros pile up (or a known incident repeats), the session asks you before spending on a read-only audit of the lessons.

## 5. If something is missing, the session says one of these
- `error: the kaggle CLI is not installed ...` = section 2, first row. Not a Kaggle limit; retrying does nothing.
- `error: Kaggle credentials are missing (...)` = section 1, set the two variables in the environment, start a new session.
- `LONG VIDEO: ...` = the video is over 90 minutes; the session switches to long mode on its own.
- `AGE-RESTRICTED` = give a file or another link.
- `Sign in to confirm you're not a bot` = the session tries again up to 3 times, then asks you for a file or another link.
- `LIMIT REACHED after N tries ...` = a real Kaggle limit (quota, busy T4 queue of up to 20 minutes per try). Wait and ask again, or give another link.
- `account 2: not available (...)` in `kaggle.py check` = no second account: GPU jobs stay on account 1 and a quota or queue limit stops them as before. Fix: set `KAGGLE_USERNAME2` + `KAGGLE_APITOKEN2`, or install `pdftotext` (`apt-get install poppler-utils`) so the token can be read from the dataset. `--account 1|2` on `kaggle.py` and `long_run.py` forces an account.

## 6. Good to know
- Captions are used whenever the video has them. Whisper (T4) is only for videos with no captions, and the default is large-v3 batched 8, VAD 500, chunk 20 (66% exact / 77% fuzzy word match against the captions, measured 2026-11-15), still below them (see `docs/long-mode-report.md`, section "Whisper T4 settings tuning"); the session tells you before it uses it. ALWAYS pass `--lang hi` for Hindi (auto can translate it into English); `long_run.py` refuses a Hindi stream without it.
- Time: a few minutes to download a normal video on Kaggle; long mode about 2 minutes plus 1 minute per hour of video for the first pass, then 15-20 minutes for the first 10 clips. Each clip render takes about 1 minute (animations: 1-2 minutes for the first one).
- Clips go to `streams/<date>_<slug>/`; the newest are listed in `LATEST.md`. Masters (`output.preset=upload`) stay outside git. Work is saved to the session branch after every render step (`checkpoint.py`); the final clips go to main with `finalise.py --stream streams/<stream> --yes` (`SKILL.md` step 8).
- Changing a clip afterwards: say what you want ("start 2 s earlier", "captions on", "no facecam"); the full list is `CONTROLS.md`. On a fresh clone the source video is not there: the session downloads it again first.

## 7. If the container is gone (recovery, 5 lines)
A container is reclaimed when idle; everything checkpointed is on GitHub on the session branch `ccr-*`.
1. New session, clone the repo, `git checkout ccr-...` (the branch named in `LATEST.md`, or the newest one in `git branch -r --sort=-committerdate`).
2. `python3 .claude/skills/clips/scripts/preflight.py` (it runs `jobs.py tick`) or `python3 .claude/skills/clips/scripts/jobs.py check` lists every running job, whether its process is alive, the Kaggle kernel status and the exact RESUME line; run it (a finished kernel is fetched, not run again).
3. Source windows are gitignored (35 MB each): `long_run.py fetch-windows --stream streams/<s>` fetches them again (about 10 min), or `backup_sources.py restore --stream streams/<s>` when the user asked for the optional private dataset `clips-sources-<stream>` (`backup_sources.py backup --stream S --yes`, only on request).
4. Clips, `clip.json`, versions, `docs/` and `docs/jobs.json` come with the clone. Final clips are on main only after `finalise.py --stream streams/<s> --yes`.
