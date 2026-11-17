# VERIFY: the final checklist

Back to [README.md](README.md). Run in the repo root of the NEW session. Tick every box. Time: about 8 minutes. Outputs below were produced on the old VM on 2026-11-16; your numbers (GB free, sha) differ, the shape must match. Anything red: [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 1. Machine

- [ ] **preflight** (6 s)
  ```
  python3 .claude/skills/clips/scripts/preflight.py
  ```
  Expected: 12 PASS + at most 2 WARN (`settings-allow`, `audit-due` are fine) and the last line `PREFLIGHT OK (12 pass, 2 warn, ...)`. Exit code 0.
- [ ] **kaggle check** (5 s)
  ```
  python3 .claude/skills/clips/scripts/download/kaggle.py check
  ```
  Expected, user names only, never a token:
  ```
  ok: kaggle CLI found at /root/kvenv/bin/kaggle and credentials are set
  account 1: user <name>, token set; reachable: yes
  account 2: user <name>, token set (from env KAGGLE_APITOKEN2); reachable: yes
  ```
  (`account 2: not available (...)` is acceptable ONLY if you decided not to use a second account.)
- [ ] **ffmpeg**
  ```
  ffmpeg -version | head -1
  ```
  Expected: `ffmpeg version 6.1.1...` (any 6.x or newer).
- [ ] **node** (animations only)
  ```
  node --version
  ```
  Expected: `v22.x.y` (v22.22.0 on the old VM).
- [ ] **python libs**
  ```
  python3 -c "import numpy, PIL; print('ok')"
  ```
  Expected: `ok`.
- [ ] **optional: HyperFrames and Kokoro**
  ```
  npx --offline hyperframes@0.9.52 --version
  ~/.cache/clips-commentary/venv/bin/python -c "import kokoro; print('kokoro ok')"
  ```
  Expected: `0.9.52` and `kokoro ok`. Not installed = animations/commentary off, everything else works.
- [ ] **no key in the repo**: `git grep -lE "KGAT_[0-9A-Za-z]{16,}"` prints nothing (file names only) (it looks for a full Kaggle token; the word `KGAT_` alone appears in one doc). If it prints anything, revoke that key at once (REVOKE-AND-SECURITY.md).

## 2. GitHub

- [ ] **origin is the NEW private repo**
  ```
  git remote -v
  ```
  Expected: both lines `https://github.com/NEW_USER/VideoGeneration(.git)` (NOT `ARVR7/...`). Then github.com/NEW_USER/VideoGeneration > Settings > General shows **Private**.
- [ ] **main is there**
  ```
  git fetch origin && git log origin/main -1 --format='%h %ad %s' --date=short
  ```
  Expected: a line dated 2026-11-16 or later, like `4f8ecb4 2026-11-16 docs: 1 non-stream files from ccr-4e94c80c-rpb12o (autosave)` (the sha equals the old repo's main when nothing new happened: `git ls-remote https://github.com/ARVR7/VideoGeneration.git refs/heads/main` vs the same command for the new repo).
- [ ] **(optional) the old session branch was copied**: `git ls-remote --heads origin ccr-4e94c80c-rpb12o` prints one line. It is history only; work starts from `main`.
- [ ] **a push works** (fast-forward, no force): `git push origin HEAD` prints `Everything up-to-date` or a normal update. If the session started on a new `ccr-*` branch, let autosave/checkpoint do it and check `git log origin/<branch> -1`.

## 3. Knowledge and layout

- [ ] **lessons graph builds**
  ```
  python3 .claude/skills/lessons/scripts/build_graph.py
  ```
  Expected: `ok: 126 notes, 297 edges` (numbers grow as lessons are added; the word `ok` is the check).
- [ ] **check_layout: 0 FAIL on the 3 published clips** of the first stream (the folder `streams/2026-11-15*` does not exist: the three clips are under `streams/2026-11-14_this-is-not-a-game/`)
  ```
  for c in streams/2026-11-14_this-is-not-a-game/clips/*/; do
    python3 .claude/skills/clips/scripts/check_layout.py "$c/clip.json" > /tmp/cl.txt
    echo "rc=$? FAIL=$(grep -c ' FAIL ' /tmp/cl.txt) $c"
  done
  ```
  Expected: three lines `rc=0 FAIL=0 ...` (12 PASS per clip). Also true for the 15 clips of `streams/2026-11-16_*`.
- [ ] **the clips and lessons skills are found**: in the session, `/clips` autocompletes, and `python3 .claude/skills/lessons/scripts/query.py --help` prints usage.

## 4. Two-minute dry run (changes nothing in the repo)

- [ ] ```
  S=$(mktemp -d)
  cp -r streams/2026-11-14_this-is-not-a-game/clips/449-503s_gta-6-logo-goosebumps $S/
  python3 .claude/skills/clips/scripts/edit_clip.py $S/449-503s_gta-6-logo-goosebumps/clip.json captions.on=true --note "verify dry run"
  python3 .claude/skills/clips/scripts/edit_clip.py $S/449-503s_gta-6-logo-goosebumps/clip.json --history | tail -2
  python3 .claude/skills/clips/scripts/jobs.py check
  git status --short | head -3
  rm -rf "$S"
  ```
  Expected: `saved as vN` and a `captions: {... "on": false ...} -> {... "on": true ...}` line; the history shows `captions.on false -> true`; `jobs.py check` prints `no jobs running (use --all to include finished ones)`; `git status` shows nothing from this test.
  This does NOT render (rendering needs the source video, which a fresh clone does not have). The first real job downloads it.

## 4b. Manifest and carry-over check

- [ ] **manifest**: `python3 migration-setup/verify_manifest.py --no-preflight` prints PASS, 0 extra, 0 changed (it compares file trees and hashes, not the repo name: after a transfer or rename the name differs and that is fine).
- [ ] **Fable carry-over check**: paste [FABLE-CARRYOVER-CHECK.md](FABLE-CARRYOVER-CHECK.md) into a session and read its report (blockers first).

## 5. The real thing

- [ ] **First job done**: `/clips <stream link>` produced clips, `LATEST.md` lists them, `finalise.py --stream streams/<stream> --yes` put them on `main` of the NEW repo (`git log origin/main -1` shows `clips: <stream>, <n> clips (final)`).
- [ ] **Response style** (the `i-have-adhd` text) is pasted in Settings > Profile and active (answers lead with the next action and are numbered).
- [ ] **Keys**: `env | cut -d= -f1 | grep -E 'KAGGLE|HF_'` lists the variable NAMES (never print values).

All green -> go to [REVOKE-AND-SECURITY.md](REVOKE-AND-SECURITY.md).
