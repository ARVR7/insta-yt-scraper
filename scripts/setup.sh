#!/usr/bin/env bash
# Install the tools the scrape scripts need. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")/.."
pip install -q -r requirements.txt
command -v ffmpeg >/dev/null || { echo "ffmpeg is required (apt-get install -y ffmpeg)" >&2; exit 1; }
echo "ok"
