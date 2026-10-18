#!/usr/bin/env bash
# Usage: bash run.sh out.mp4   (run from this scripts/ directory)
set -e
OUT=${1:-clutch_shot_short.mp4}
python3 common.py >/dev/null            # sanity: sim events must show rim hit (att1), no rim/board hit (att3)
python3 render.py full silent.mp4       # ~3-4 min on 2 cores, 480 frames
python3 audio.py                        # writes audio.wav
ffmpeg -y -loglevel error -i silent.mp4 -i audio.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_name,width,height,duration -of default=nw=1 "$OUT"
