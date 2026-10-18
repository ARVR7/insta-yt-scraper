---
name: shorts-visible-stakes-video
description: Build an original, portrait 1080x1920 YouTube Short (about 16s) from a trend script like "visible-stakes countdown + grayscale freeze-frame twist", with code-rendered animation and synthesized audio. Use when asked to generate a Short or Reel from a script.
---

# Shorts: Visible Stakes + Freeze-Frame Twist

Produces a loopable 16s, 1080x1920, 30fps MP4 with original synthesized audio. No camera, no stock footage, no copyrighted music.

## Step 0: Decide what is makeable

- Scripts that need third-party footage or a specific commercial track (game trailers, charting songs) cannot be reproduced. Pick the script that works as an original animation, say why in one line, and proceed.
- Do not ask questions the request already answers ("pick any one" means pick). State the choice and go.

## Step 1: Pipeline (scripts/ folder next to this file)

If `scripts/` exists, copy it to a working dir and run `bash run.sh out.mp4` after editing text/params. It contains:

- `common.py`: physics sim (ball, rim edges, board, floor, net drag), event times, the wall-clock to ball-time mapping, and the timer table.
- `render.py`: PIL frame renderer. Supersample SS=2, camera transform, sprites, net mesh, UI layer, post FX (grayscale, vignette, flash), confetti. Writes raw frames straight into ffmpeg (libx264, crf 16, yuv420p). Uses `multiprocessing.Pool(2)`.
- `audio.py`: numpy/scipy synth (kick, clap, hat, bass, pluck, clang, thud, buzzer, riser, heartbeat, 808 drop, swish), 120 bpm. Writes `audio.wav`.
- `run.sh`: sim check, render, audio, mux (AAC 192k, faststart), ffprobe.

If `scripts/` is missing, rebuild from the spec below.

## Step 2: Timeline spec (all cuts land on 0.5s beats at 120 bpm)

| Time | Beat |
|---|---|
| 0.0-2.0 | Start mid-motion: ball already in flight (slow, 0.375x), live 15.00 countdown, title "MAKE THIS SHOT IN 15 SECONDS / OR EAT A GHOST PEPPER" |
| 2.0-3.5 | Close-up on rim, ball hits rim and bounces out, clang, MISS stamp, timer jumps |
| 3.5-5.5 | Wide shot, second attempt, airball, sad-trombone, AIRBALL stamp |
| 5.5-6.5 | Stakes beat: dim scene, giant pepper, "2 MISSES / 1 SHOT LEFT", sizzle sound |
| 6.5-7.0 | Low-angle launch of shot 3, "LAST SHOT" slam, kick roll, tape-stop cut at 7.0 |
| 7.0-10.0 | Grayscale freeze, ball just above rim, slow push-in, heartbeat + riser, "WILL IT GO IN?", "COMMENT YES or NO", timer frozen at 01.20, 70ms silence before the drop |
| 10.0 | Bass drop: color floods back, white flash, shake, slow-mo (0.25x) into SWISH, confetti, shockwaves, timer settles 00.71 |
| 10.95-11.95 | The 0:11 card: "SHOT 3 OF 3: MADE / 0.71s / PEPPER SAFE / you paused. nice. comment PEPPER" |
| 12.0-14.4 | Slow-mo replay (0.27x) with lowpassed music, "REPLAY" tag |
| 14.4-16.0 | "NEXT: BLINDFOLDED?", "PAUSE AT 0:11" pill, "FOLLOW FOR PART 2", last 0.4s crossfades into frame 0 so it loops |

To retarget the niche, change the stakes text, the object being thrown, and the "NEXT" line. Keep the structure: stakes visible at 0:00, two fast failures, a freeze just before the payoff, a drop on unfreeze, a hidden detail at 0:11 with a pause prompt.

## Step 3: Hard-won constraints

- Environment: no cairo, skia or pip downloads, and github/fonts hosts are blocked. Use PIL + numpy + scipy + ffmpeg. Fonts: Inter Black (`/usr/share/fonts/opentype/inter/`), DejaVu Sans Mono Bold for digits.
- Cost: about 0.65s per frame, so 480 frames take about 3.5 min on 2 cores. Run the full render in the background with `nohup`, and tell the user while waiting.
- Safe zones for Shorts UI: keep text out of the top 200px, the right 120px, and the bottom 300px. Timer sits at y 405-655, stakes pill at y 225-305, dots at y 1515.
- Physics: solve launch velocity analytically to hit a target at time T, then verify by simulation. Required events: attempt 1 has one `rim` event, attempt 2 has no rim/board/swish event, attempt 3 has a `swish` event and no rim/board event. A bank-shot airball was tried first and always dropped in, so the airball is a short shot instead.
- Bugs already fixed (do not reintroduce): floor rectangle must be skipped when the floor is below the frame (PIL raises on y1<y0); scipy `lp`/`hp` cutoffs must be scalars, not arrays; use `np.trapezoid` (not `trapz`); `swish` detection must be limited to y within 60px below the rim plane.
- Audio: everything is original. Cut the pre-drop bus with a 110ms fade at 7.0, mute SFX from 9.93 to 10.0, normalize peak to 0.89, fade the drop bus over the last 0.25s.

## Step 4: Verify before delivering

1. `ffprobe`: h264, 1080x1920, 30fps, 16.0s, AAC present.
2. Contact sheet of 12-14 frames from the final MP4 at 0, 1.5, 2.5, 4, 5.8, 6.7, 8, 9.9, 10.1, 10.6, 11.2, 13, 15, 15.95. Look for text overlap, missing stamps, wrong timer color.
3. RMS per 0.5s of the WAV: expect about -18 dB in the freeze, rising to about -11 dB at 9.5, peak at 10.0 (about -8 dB).

## Step 5: Deliver

Copy the MP4 to `/mnt/user-data/outputs/`, send with SendUserFile (display render), and reply with: upload steps, a suggested title with #shorts, one line on what the video shows, one line on why a trending track was replaced by original audio, and one next action.
