#!/usr/bin/env python3
"""Extract frames, a contact sheet and an English/auto-detected transcript from a video.

Usage: analyze_video.py <video.mp4> <outdir> [--every 4]
Writes <outdir>/frames/f*.jpg, <outdir>/sheet.jpg (view it to read on-screen text)
and <outdir>/transcript.txt. Requires ffmpeg on PATH.
"""
import glob
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel
from PIL import Image


def frames(video, out, every):
    fdir = out / "frames"
    fdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", f"fps=1/{every},scale=480:-1",
         str(fdir / "f%02d.jpg")],
        check=True,
    )
    ims = [Image.open(f) for f in sorted(glob.glob(str(fdir / "f*.jpg")))]
    if not ims:
        return
    w, h = ims[0].size
    cols = 4
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out / "sheet.jpg", quality=80)


def transcript(video, out):
    # Decode with ffmpeg and pass a numpy array: faster-whisper's own decoder
    # breaks when the installed PyAV version does not match.
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", video, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True, check=True,
    ).stdout
    if not raw:
        (out / "transcript.txt").write_text("(no audio track)\n")
        return
    audio = np.frombuffer(raw, dtype=np.float32)
    model = WhisperModel("base", compute_type="int8")
    segs, info = model.transcribe(audio)
    lang = info.language
    lines = [f"language: {lang} ({info.language_probability:.2f})"]
    if lang == "en":
        lines += [f"[{s.start:.0f}s] {s.text.strip()}" for s in segs]
    else:
        # The base model garbles non-English speech. Redo it with the larger model, once in
        # the original language and once translated to English (the translation is the
        # readable one; the original is kept for names and checking).
        model = WhisperModel("small", compute_type="int8")
        for task, title in (("translate", "English translation"), ("transcribe", f"Original ({lang})")):
            segs, _ = model.transcribe(audio, language=lang, task=task)
            lines.append(f"## {title}")
            lines += [f"[{s.start:.0f}s] {s.text.strip()}" for s in segs]
    (out / "transcript.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    args = sys.argv[1:]
    every = 4
    if "--every" in args:
        i = args.index("--every")
        every = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    video, outdir = args
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    frames(video, out, every)
    transcript(video, out)


if __name__ == "__main__":
    main()
