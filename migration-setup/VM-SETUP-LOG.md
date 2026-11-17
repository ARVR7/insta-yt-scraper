# VM-SETUP-LOG: what was installed on the old VM and how to redo it

Back to [README.md](README.md). Facts read on the old VM on 2026-11-16 with read-only commands (`which`, `--version`, `du -sh`, `pip list`). The new environment does most of this by itself through `setup-environment.sh`. Redo a single item only when `preflight.py` or `VERIFY.md` says it is missing.

## Versions on the old VM

| Tool | Version found | Where | Needed for | Redo |
|---|---|---|---|---|
| OS | Linux 6.18; ffmpeg 6.1.1-3ubuntu5 (Ubuntu package) | cloud VM, runs as root | | provided by the Claude cloud image |
| python3 | 3.13.17 (`/usr/bin/python3`) | system | all scripts | provided |
| pip packages (system python) | numpy 2.5.3, pillow 12.3.0, PyYAML 6.0.3, requests 2.34.2, git-filter-repo 2.47.0 | `pip list` | numpy+PIL: layout check, captions, find_moments (required); git-filter-repo: one-off history rewrite only | `python3 -m pip install numpy pillow` (add `--break-system-packages` if pip refuses) |
| ffmpeg / ffprobe | 6.1.1 (`/usr/bin/ffmpeg`, apt) | system | cutting, loudness, rendering (required) | `apt-get install -y ffmpeg` |
| a second ffmpeg | `~/ffbin/ffmpeg` (n9.0.2 static build, 2026-09-30) | used only in early filter experiments | optional, not referenced by scripts | skip |
| poppler-utils (`pdftotext`) | 24.02.0 | apt | reads the account-2 key PDF inside `kaggle.py` (only without `KAGGLE_APITOKEN2`) | `apt-get install -y poppler-utils` |
| Node / npm / npx | 22.22.0 / 10.9.4 / 10.9.4 (`/opt/node22/bin`) | provided by the image | animations only (HyperFrames) | install Node 22 |
| git / gh | 2.43.0 / 2.89.0 | system | | provided |
| uv | 0.11.32 (`~/.local/bin/uv`) | in the image | creating the Kokoro venv with Python 3.12 | `pip install uv` (setup script does it when `SETUP_KOKORO=1`) |
| kaggle CLI | 2.2.5 (+ kagglesdk 0.1.38) in `~/kvenv` | venv, 46 MB | all Kaggle jobs (required) | section 1 |
| HyperFrames | 0.9.52 (pinned) | npx cache under `~/.npm` (492 MB) | animations only | section 5 |
| Chrome headless shell | n/a | `~/.cache/hyperframes/chrome` | HyperFrames render | section 5 |
| Kokoro-82M + torch + spaCy model | kokoro 0.9.4 | `~/.cache/clips-commentary/venv` (1.7 GB), Python 3.12 venv | highlights commentary voice only | section 4 |

## 1. ~/kvenv (the kaggle CLI)

Why a venv: it keeps the kaggle CLI apart from the system packages. `kaggle.py` finds `~/kvenv/bin/kaggle` by itself (also `~/.local/bin/kaggle`, `$KAGGLE_BIN`, or PATH).
```
python3 -m venv ~/kvenv && ~/kvenv/bin/pip install kaggle
~/kvenv/bin/kaggle --version        # Kaggle CLI 2.2.5
```
Time: 1 min.

## 2. poppler-utils / pdftotext

```
apt-get install -y poppler-utils
pdftotext -v
```
Only needed while account 2's key is read from the dataset `kagglegpu2` (KAGGLE.md). With `KAGGLE_USERNAME2` + `KAGGLE_APITOKEN2` set it is not used.

## 3. git-filter-repo (one-off, history rewrite of 2026-11-15)

Installed with pip (`/usr/local/bin/git-filter-repo`, 2.47.0). Used once on 2026-11-15 to remove every blob over 25 MB from the history. Not needed for normal work; do NOT rewrite history again without an explicit user request (lesson `repo-keeps-only-current-work`). Redo only if asked: `python3 -m pip install git-filter-repo`.

## 4. Kokoro voice, `~/.cache/clips-commentary` (1.7 GB) - optional

```
python3 .claude/skills/clips/scripts/commentary/tts.py --setup
~/.cache/clips-commentary/venv/bin/python -c "import kokoro" && echo ok
```
It runs `uv venv -p 3.12 ~/.cache/clips-commentary/venv`, then installs `torch` (CPU wheels from download.pytorch.org), `kokoro==0.9.4`, `numpy`, `soundfile`, then `spacy download en_core_web_sm` (github.com). The first synthesis downloads the Kokoro-82M weights from huggingface.co (about 450 MB, cached in `~/.cache/huggingface`). Python 3.12 is used because Kokoro 0.9.x does not support 3.13. Time: 5-10 minutes. Without Kokoro: the highlights render prints a WARNING and goes on without commentary (commentary is needed for YouTube monetisation of highlights). The same via the environment: `SETUP_KOKORO=1` in the setup script.

## 5. HyperFrames 0.9.52 + Chrome, `~/.cache/hyperframes` (290 MB) - optional

```
npx --yes hyperframes@0.9.52 --version        # fills the npx cache (needs registry.npmjs.org)
npx --offline hyperframes@0.9.52 browser ensure   # finds or downloads the headless Chrome
npx --offline hyperframes@0.9.52 --version        # prints 0.9.52
```
`render_clip.py` uses `npx --offline hyperframes@0.9.52` when cached, else `npx --yes` (one WARNING) and then downloads Chrome. If that fails the clip keeps the static title. HyperFrames needs several GB of free disk while rendering (lesson `hyperframes-needs-disk`). The `~/.hyperframes` folder only holds config and history.

## 6. The autosave script (run by hand; no hook calls it)

Script: `.claude/scripts/autosave.sh` (in git). It commits and pushes the CURRENT branch only, skips files over 25 MB, `.py` files that do not compile and key-like files, never forces, and does nothing while `.autosave-pause` exists (used during history rewrites). Stream content reaches `main` only through `finalise.py`. No hook calls it: the only hook seen is the platform's own check that reminds to commit and push; in the old sessions the lead ran `bash .claude/scripts/autosave.sh` by hand when that reminder appeared. How to do the same (and how to add a real Stop hook): CLAUDE-ACCOUNT-SETUP.md section 8.

## 7. .gitignore items (what stays out of git, and why)

`__pycache__/`, `*.pyc`, `node_modules/`, `renders/`, `*.tmp`, `.hyperframes/`, `*.part.mp4`, `streams/*/docs/cache/` (disposable animation cache), `streams/*/source/` (source videos), `.autosave-pause`, `streams/**/masters/` (60 fps upload masters ~100 MB), `streams/**/highlights/*/work/`, `streams/*/highlights/*/preview.mp4` (80 MB per render, delivered with SendUserFile; one early preview stays tracked), `*_upload.mp4`, `streams/*/docs/visual/sheets/` and `*.npz` (rebuilt by `visual_scan.py` in 30-70 s).

## 8. Disk habits (the VM disk is small and ephemeral)

- Free disk when found: 13 GB of 252 GB (69% used). `preflight.py` fails below 5 GB (`disk-free`, incident `disk-full-render-stop`: on 2026-11-16 a 15-clip render stopped with 12 clips left because the disk was full).
- Work in scratch dirs OUTSIDE the repo (the session scratchpad or `/tmp/<job>`), delete them when the job is done. The old VM kept ~1.7 GB in `/tmp/claude-0/` (session scratch): clean it with `rm -rf /tmp/claude-0/<old-job-folders>` when space runs short; never delete the repo or `~/.cache/clips-commentary` by accident.
- Windows (35 MB each, `streams/<s>/source/windows/`) and sources are gitignored; delete them after the final render (`long_run.py render --delete-windows`), or back them up to a private Kaggle dataset only when asked (`backup_sources.py`).
- `autosave.sh` skips any file over **25 MB**; `checkpoint.py` and `finalise.py` refuse a file over **95 MB** (GitHub's hard limit is 100 MB). A clip preview of 40 MB is committed by checkpoint (limit 95 MB) but never by autosave.
- Masters go to a private Kaggle dataset, not git. Lesson `push-main-then-delete-from-vm`: push finished work, then delete the VM copy; fetch it again from GitHub when the user asks for a file.

## 9. Session branch rule

Each Claude Code cloud session works on its own branch `ccr-<id>`. Work in progress is saved there automatically after every render step (`checkpoint.py`, never force). Final clips reach `main` only through `python3 .claude/skills/clips/scripts/finalise.py --stream streams/<stream>` (dry run) and `--yes` (one squashed commit). Non-stream files reach `main` through `finalise.py --sync-docs` (called by autosave, fast-forward only). A new session on the new repo works on its own branch (the platform names it). Start from `main`: it has the same tree as the old `ccr-*` branch, which is history only (do not check it out).

## 10. Container gone? (recovery)

1. New session, repo attached, `git checkout` the newest `ccr-*`.
2. `python3 .claude/skills/clips/scripts/preflight.py` (runs `jobs.py tick`), or `python3 .claude/skills/clips/scripts/jobs.py check`.
3. Source windows are gitignored: `long_run.py fetch-windows --stream streams/<s>` (about 10 min) or `backup_sources.py restore --stream streams/<s>`.
4. Clips, `clip.json`, versions and docs come with the clone.
