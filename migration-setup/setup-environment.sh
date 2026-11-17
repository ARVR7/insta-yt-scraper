#!/usr/bin/env bash
# setup-environment.sh - this file is too long for the 100-line "Setup script" box of the Claude cloud environment (over 100 lines).
# Do NOT paste it. Paste the one-line wrapper from migration-setup/CLAUDE-ACCOUNT-SETUP.md section 4 (it runs this file from the repo checkout),
# or run it by hand: bash migration-setup/setup-environment.sh
#
# What it does (idempotent: running it twice changes nothing the second time):
#   1. finds the repo checkout (this script normally starts ONE directory ABOVE the repo)
#   2. apt-get install poppler-utils (pdftotext) and ffmpeg, only if missing
#   3. python venv ~/kvenv with the kaggle CLI (kaggle.py finds ~/kvenv/bin/kaggle by itself)
#   4. pip install numpy pillow, only if missing
#   5. checks Node 22 (only needed for animations) and prints a hint when it is missing
#   6. OPTIONAL, off by default:  SETUP_KOKORO=1       -> commentary voice (about 1.7 GB, several minutes)
#                                 SETUP_HYPERFRAMES=1  -> HyperFrames 0.9.52 + Chrome warm-up (about 290 MB)
#
# It NEVER reads or needs a secret. A setup script cannot see the environment's saved variables or
# secrets; KAGGLE_USERNAME / KAGGLE_APITOKEN / HF_Token are only available once the session runs.
# It never exits non-zero on purpose: a failing setup script would stop the whole session from starting.
# Each problem prints one line starting with WARN; read them in the session's first message.
set -u

say()  { printf '[setup] %s\n' "$*"; }
warn() { printf '[setup] WARN %s\n' "$*"; }

HOME="${HOME:-/root}"
SUDO=""
if [ "$(id -u)" != "0" ]; then
  command -v sudo >/dev/null 2>&1 && SUDO="sudo" || SUDO="none"
fi

# --- 1. find the repo (the folder that holds .claude/skills/clips/SKILL.md) ---
REPO=""
for d in . ./* ../*; do
  if [ -f "$d/.claude/skills/clips/SKILL.md" ]; then REPO="$(cd "$d" && pwd)"; break; fi
done
if [ -n "$REPO" ]; then say "repo found: $REPO"; else warn "repo checkout not found from $(pwd) (attach the repo to the environment's Repositories list); continuing with the machine tools only"; fi

# --- 2. system packages: pdftotext (poppler-utils) and ffmpeg ---
need_apt=""
command -v pdftotext >/dev/null 2>&1 || need_apt="$need_apt poppler-utils"
command -v ffmpeg    >/dev/null 2>&1 || need_apt="$need_apt ffmpeg"
command -v ffprobe   >/dev/null 2>&1 || case " $need_apt " in *" ffmpeg "*) ;; *) need_apt="$need_apt ffmpeg";; esac
if [ -n "$need_apt" ]; then
  if [ "$SUDO" = "none" ]; then
    warn "need apt packages:$need_apt but this user is not root and has no sudo: ask for an environment with root"
  elif command -v apt-get >/dev/null 2>&1; then
    say "apt-get install:$need_apt"
    export DEBIAN_FRONTEND=noninteractive
    ( $SUDO apt-get update -qq && $SUDO apt-get install -y -qq $need_apt ) >/dev/null 2>&1 \
      && say "installed:$need_apt" || warn "apt-get failed for:$need_apt (is the network allowing the apt mirrors?)"
  else
    warn "apt-get not found; install by hand:$need_apt"
  fi
else
  say "poppler-utils and ffmpeg already present"
fi

# --- 3. kaggle CLI in ~/kvenv ---
if [ -x "$HOME/kvenv/bin/kaggle" ]; then
  say "kaggle CLI already in ~/kvenv ($("$HOME/kvenv/bin/kaggle" --version 2>/dev/null | head -1))"
else
  say "creating ~/kvenv and installing the kaggle CLI"
  { python3 -m venv "$HOME/kvenv" && "$HOME/kvenv/bin/pip" install -q kaggle; } >/dev/null 2>&1 \
    && say "kaggle CLI installed" || warn "kaggle CLI install failed (needs pypi.org and files.pythonhosted.org; on Debian/Ubuntu also: apt-get install -y python3-venv)"
fi

# --- 4. numpy + pillow for the system python3 ---
if python3 -c "import numpy, PIL" >/dev/null 2>&1; then
  say "numpy and PIL already importable"
else
  say "pip install numpy pillow"
  { python3 -m pip install -q numpy pillow || python3 -m pip install -q --break-system-packages numpy pillow; } >/dev/null 2>&1 \
    && say "numpy and pillow installed" || warn "pip install numpy pillow failed"
fi

# --- 5. Node 22 (animations only) ---
if command -v node >/dev/null 2>&1; then
  nv="$(node --version 2>/dev/null)"
  case "$nv" in
    v22.*) say "node $nv ok" ;;
    *) warn "node is $nv, animations want v22.x (clips without animations work anyway). Install Node 22 from nodejs.org or the package manager" ;;
  esac
else
  warn "node not found: animated titles and HyperFrames will not work; plain clips do. Install Node 22"
fi

# --- 6a. OPTIONAL Kokoro commentary voice (highlights commentary only) ---
if [ "${SETUP_KOKORO:-0}" = "1" ]; then
  if [ -x "$HOME/.cache/clips-commentary/venv/bin/python" ] && "$HOME/.cache/clips-commentary/venv/bin/python" -c "import kokoro" >/dev/null 2>&1; then
    say "Kokoro already installed"
  elif [ -z "$REPO" ]; then
    warn "SETUP_KOKORO=1 but the repo was not found, so tts.py is not reachable"
  else
    command -v uv >/dev/null 2>&1 || { "$HOME/kvenv/bin/pip" install -q uv >/dev/null 2>&1 && export PATH="$HOME/kvenv/bin:$PATH"; }
    say "Kokoro setup (about 1.7 GB; needs pypi.org, download.pytorch.org, huggingface.co, github.com)"
    python3 "$REPO/.claude/skills/clips/scripts/commentary/tts.py" --setup >/dev/null 2>&1 \
      && say "Kokoro ready" || warn "tts.py --setup failed: run it by hand and read the error"
  fi
fi

# --- 6b. OPTIONAL HyperFrames warm-up (animations only) ---
if [ "${SETUP_HYPERFRAMES:-0}" = "1" ]; then
  if command -v npx >/dev/null 2>&1; then
    if npx --offline hyperframes@0.9.52 --version >/dev/null 2>&1; then
      say "HyperFrames 0.9.52 already in the npx cache"
    else
      say "HyperFrames 0.9.52 warm-up (npm registry)"
      npx --yes hyperframes@0.9.52 --version >/dev/null 2>&1 || warn "npx hyperframes@0.9.52 failed (needs registry.npmjs.org)"
    fi
    npx --offline hyperframes@0.9.52 browser ensure >/dev/null 2>&1 \
      && say "Chrome for HyperFrames ready" || warn "HyperFrames Chrome download failed or was skipped (the render then keeps the static title)"
  else
    warn "SETUP_HYPERFRAMES=1 but npx is missing"
  fi
fi

say "done. In the session run: python3 .claude/skills/clips/scripts/preflight.py"
exit 0
