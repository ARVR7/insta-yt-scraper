---
name: analyze-video
description: Turn a downloaded video file into a transcript, sampled frames and a contact sheet so on-screen text, demos and visuals can be read. Use after fetching any reel or video.
---

# analyze-video

```bash
python3 scripts/analyze_video.py "$SCRATCH/<id>/video.mp4" "$SCRATCH/<id>" [--every 4]
```

Outputs `transcript.txt` (language-tagged, with timestamps), `frames/f*.jpg` and `sheet.jpg`.

Then **Read `sheet.jpg`** (it is a 4-column grid of frames) and note:
- On-screen text, titles, captions and overlays (they often name the tool or the call-to-action).
- Screen recordings: which site/app/repo is shown, feature lists, prices, version numbers. Quote what is legible and say what is not.
- The call-to-action at the end ("comment X", link in bio, paid course).

## Known behaviour
- The transcript is auto-generated (faster-whisper `base`, CPU, int8): names, tool names and numbers can be wrong. Cross-check them against on-screen text and mark uncertain ones.
- Audio is decoded with ffmpeg and passed as a numpy array because faster-whisper's own decoder fails with some PyAV versions.
- The model downloads from the Hugging Face hub on first use; the HF_TOKEN warning is harmless.
- For videos longer than ~10 minutes use `--every 15` to keep the sheet readable.
- Non-English audio is auto-detected. The script then re-runs with the larger `small` model and writes an `## English translation` section and an `## Original (xx)` section. Use the translation for the note, keep the original, and treat both as rough: the first `base` pass on a Hindi reel produced confident-looking English nonsense, so never use a transcript whose language was not English without the second pass. Names and numbers still need checking against on-screen text.
