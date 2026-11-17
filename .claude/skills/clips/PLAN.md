# clips skill: plan (one current plan, then the build history)

## Current plan (authoritative, last updated 2026-11-16)
**Reading rule:** this section wins. Everything below the line "Build history" is the spec the agents built from; where an old section disagrees with this one it is marked HISTORY or SUPERSEDED and this section is right. Details of every key live in `defaults.json`, `clip_schema.py` and `CONTROLS.md`.

**What it is.** A stream link in, every good moment out as a 40-55 s vertical clip (1080x1920) whose every aspect lives in an editable `clip.json` (change it by saying it, about a minute to re-render on the VM CPU). Run by a Sonnet session, Haiku for fixed-command steps, Opus only as an advisor.

**Flow as built.** 0 lessons then a 6-line plan; 1 ask once (facecam, destinations); 2 download on a Kaggle CPU kernel (YouTube tested, Twitch untested, age-restricted or bot check: stop); 3 transcript: YouTube captions first; 4 moment finder, the runner sets whole-story boundaries; 5 `make_clips.py`; 6 pointing zooms; 7 edit loop (`edit_clip.py`); 8 save and publish: checkpoint after every step to the session branch (automatic), `finalise.py` squashes the final clips onto main, lessons. Videos over 90 minutes (5-6 h) use LONG MODE (`long_run.py`, built): nothing is downloaded whole.

**Defaults (`defaults.json`):**
| Thing | Default | On request |
|---|---|---|
| Title | static editorial title (`hook.animation none`) | animated title (`hook.animation=reveal`) |
| Animations, progress line, ring, tag, burst | off (`animations.on false`) | only when the user asks, or for highlight videos |
| Layout | `safe-c`: game picture shifted up, facecam left above the bottom 20% zone | `classic` (facecam bottom-right) for destinations without app-button overlap |
| Facecam | rounded 4:3, 300 px, at x 40 y 1250, library item `girl_watching_10s`, passive reaction, her audio dropped | another library item, or none |
| Facecam voice | `facecam.voice=off` | `low`: one quiet English line of hers, about 15 dB under the stream, `audio_usable` library items only |
| Captions | off | on: small, low, never over the stream |
| Output | `output.preset=preview` (30 fps, CRF 20, small, goes to git) | `upload` master (source fps, CRF 16-17, -14 LUFS / -1 dBTP) for clips the user keeps; masters live OUTSIDE git |
| Length | 40-55 s, the whole story | shorter or longer only when the story needs it |

**Versions.**
- **v1 (built and frozen):** everything in the flow above; layout C; static editorial title readable on any background; captions off by default; edges snapped to scene cuts; two-pass loudnorm; `check_layout` PASS; post kit; destinations; versions and undo; facecam library with six verified reactions; the optional quiet voice (`facecam.voice=low`); long mode. v1 final check: one fresh English and one fresh Hindi link, the user watches 3 clips per link on a phone, one fix round, freeze. The validation report is `docs/validation-report.md`; its fixes are done (re-check: `docs/revalidation-report.md`).
- **v1.1 (after the freeze; the highlights video, its animations and its commentary voice-over ARE built since 2026-11-16, see the 'Highlights' section of SKILL.md):** timed reactions (several of her lines on real beats, calm to surprised to laugh); the edit-effects layer (meme text, transitions, freeze zoom, speed ramp, sfx); more animation presets; the `highlights-yt` profile (5-6 min 16:9 video, animations ON in that profile); the chat-activity moment signal.
- **v2 (not built):** comparison videos (Vice City vs GTA 6); (commentary voice-over with a synthetic voice is built for highlights); destination rules verified from real campaign briefs; the YouTube claim-check log.
- **Backlog (parked):** lip-sync on a Kaggle T4; Whisper tuning and a Hindi-tuned model; SmolVLM, Florence-2, YuNet helpers; trained highlight scorer (10-20 streams of data needed); Auto-Editor for a podcast profile; Twitch test; a site that reads `streams/index.json`; Pexels B-roll.

**Decisions since the first spec (newest wins):**
1. Static title by default; animations only on request or for highlights (user, 2026-11-15).
2. Facecam: passive reaction by default, her voice optional and quiet (`facecam.voice=low`), English only; timed reactions are v1.1.
3. Transcript: captions first. The Whisper default on the Kaggle T4 is large-v3, batched 8, with `--lang hi` for Hindi (66% exact / 77% fuzzy word match vs the captions, measured 2026-11-15); it is still below the captions. The earlier large-v3-turbo default was worse (21-25%, repetition loops). Use Whisper only when there are no captions, after telling the user plainly that Hindi will be weak; no CPU Whisper. Active lesson `whisper-t4-large-v3-batched-below-captions` (it supersedes `whisper-t4-worse-than-captions`); tuning is backlog.
4. Output: previews in git, masters outside git in a private Kaggle dataset; `upload` is for clips the user keeps, not the default.
5. Git history was cleaned and rewritten on 2026-11-15: old large files are gone from main and cannot be recovered from git; text notes of old runs are in `archive/`.
6. Limits rule: retry 3-4 times, then tell the user; no lower-quality workaround; a CPU fallback only where it gives the same quality.
7. Privacy: the repo must stay private; `assets/facecam/reference/` holds photo-real AI reference images (see `assets/facecam/PROMPTS.md`).
8. Lessons: one active note per topic; where two notes contradicted each other the older was superseded (2026-11-15).
9. Moments also from the VIDEO (2026-11-16): step 3b `visual_scan.py` (2 fps energy, contact sheets) + a vision sub-agent (Haiku default, Sonnet on request) + `merge_moments.py` consult both signals; off with `moments.visual=off`, the transcript order is unchanged without it; method of claude-video (MIT, `NOTICE.md`, not installed); measured on one Hindi stream only, cheap energy weak alone, reviewer carries the signal (`docs/visual-moments-report.md`; unproven: Haiku reviewer, English, Twitch, 5 h). Lesson `visual-plus-transcript-moments`.
10. Never lose clips (2026-11-16, user: "never lose the clips, push things directly on GitHub branch and to main once finalised"): `checkpoint.py` runs after every render step (make_clips per clip, edit_clip --render, render_highlights, long_run steps) and pushes only safe files to the CURRENT branch `ccr-*` (never source/, masters, windows, `*_upload.mp4`; nothing over 95 MB; key-like files refused); every long job is registered in `streams/<s>/docs/jobs.json` and runs detached (`jobs.py check|resume`); `finalise.py --stream S --yes` puts ONE squashed commit (tree of the branch, parent origin/main, "clips: <stream>, <n> clips (final)") on main, so WIP re-render blobs never enter main; `autosave.sh` (run by the lead when the platform reminder appears and about every 10 minutes; the reminder hook does not call it) pushes the branch and only non-stream files (`.claude/`, `lessons/`, README) to main (`finalise.py --sync-docs`). Optional `backup_sources.py` keeps the 35 MB source windows in a private Kaggle dataset on request. Lesson `checkpoint-every-step-finalise-squash-to-main` (supersedes `push-to-main-in-intervals`). Unproven: a real container loss and resume, the Whisper two-kernel chain on `--resume-call`, a real Kaggle upload by `backup_sources.py`.

---
# Build history (the spec the agents built from; see the Current plan above where it differs)

Goal: ONE front-door skill. Input: a stream link. Output: every good moment as a 40-55 s vertical clip (the whole story of the moment; shorter or longer only when the story needs it), each driven by an editable `clip.json` so the user can change any aspect by saying it ("start 2 s earlier", "captions on", "no facecam") and get a ~30 s CPU re-render. Later features plug in as new `clip.json` layers.

## Flow (what SKILL.md must describe, numbered)
0. Lessons Step 0 (`.claude/skills/lessons`), then tell the user a 6-line plan.
1. Ask once (AskUserQuestion) only what lessons/defaults do not already answer.
2. Download on a Kaggle CPU kernel: `.claude/skills/clips/scripts/download/kaggle.py download NAME URL`, `wait`, `fetch` -> `video.mp4`, `info.json`, `*.vtt`. (YouTube tested; Twitch untested. Age-restricted or bot check: stop.)
3. Transcript: `.claude/skills/clips/scripts/transcript/vtt_to_transcript.py`. No captions on the video -> long mode (`prepare`, then `fetch-windows --whisper`) after warning the user that Whisper is weak for Hindi (see Current plan, decision 3).
4. Moments: `.claude/skills/clips/scripts/moments/find_moments.py` -> `candidates.md`. Claude reads the transcript of every strong candidate, fixes boundaries so the WHOLE moment is inside (setup, peak, reaction; sentence boundaries; 40-55 s, the whole story of the moment (setup, peak, aftermath); shorter or longer only when the story needs it), looks at 3 frames of doubtful ones, writes `moments.json` = `[{"start","end","title","hook","description","score"}]`. Cut ALL good ones; list the rejected ones with a reason.
5. `scripts/make_clips.py SOURCE TRANSCRIPT MOMENTS.json STREAM_DIR [--defaults FILE]` -> `STREAM_DIR/clips/<start>-<end>s_<slug>/clip.json` + `.../social.mp4` (before the 2026-11-15 restructure: `STREAM_DIR/docs/clips/<id>.clip.json` + `STREAM_DIR/NN_<slug>_<start>-<end>s.mp4` + `STREAM_DIR/docs/review.md` (table: file, time range, duration, hook, score, render seconds) + one contact sheet PNG per clip in `docs/sheets/`.)
6. Pointing zooms: `.claude/skills/clips/scripts/zoom/plan_zooms.py`; Claude looks at the gridded frames and adds events to `zoom.plan`; re-render.
7. Edit loop: user says a change -> `scripts/edit_clip.py CLIP.json key=value ... --render` -> send the clip.
8. Publish: push to main, delete VM copies, record lessons.

## clip.json (first sketch, HISTORY: the real keys are in `clip_schema.py` and `defaults.json`: hook.y 0.12, facecam shape rounded, size 300, position left-above-ui, margin [40,1250])
```
{"id","source","transcript","trim":{"start","end"},"title","description","score",
 "layout":{"mode":"fit","bg_blur":30,"bg_dim":0.08,"base_file":null},
 "hook":{"on":true,"text":"...","start":0,"duration":4,"y":0.13,"font_size":64},
 "captions":{"on":false,"style":"minimal","roman":true,"words_per_line":3,"font_size":null,"y_margin":null},
 "zoom":{"auto":true,"amp":0.07,"cam_xy":[x,y],"game_xy":[x,y],"on_words":[{"words":[],"xy":[x,y],"amp":0.55,"gap":4,"tail":1.0}],"plan":[{"t","x","y","amp","dur"}]},
 "facecam":{"on":true,"video":".claude/skills/clips/assets/facecam/girl_gemini-app_10s.mp4","use_seconds":[0,3],"crop":[340,0,600],"size":360,"position":"bottom-right","margin":[28,70]},
 "audio":{"volume":1.0},"output":{"fps":30,"crf":20},"rights":{"status":"private-test"}}
```
Times in `hook`, `zoom.plan` are seconds from the clip start. `defaults.json` in the skill folder holds the default layers (captions off, hook on, facecam on with the calm seconds, subtle auto zoom); `make_clips.py` copies them into each clip.json. Paths may be repo-relative (resolve against the repo root) or absolute.

## render_clip.py CLIP.json [--out FILE] (the engine; HISTORY: built. The helpers named below now live inside render_clip.py because `openshorts-clip/` and `ai-edit-layer/` were removed; the default title is the static editorial title, not the pill; the facecam is a rounded rectangle, not round)
- ONE ffmpeg pass from the SOURCE (no intermediates, no OpenShorts): `-ss/-t` trim -> fit layout (whole 16:9 frame full width, centred, blurred+dimmed copy behind; reuse the filter of `openshorts-clip/scripts/vertical_fit.py`) -> zoom (reuse the scale/crop expressions of `zoom_punch.py`, incl. the hold envelope; mind the lesson: crop must use 1080*Z, not in_w) -> captions (.ass from `ai-edit-layer/scripts/ass_from_words.py` logic, words taken from the transcript inside the trim, shifted to clip time) -> hook (rounded white pill, bold dark text, rendered to a transparent PNG with PIL using `openshorts-clip/fonts/Montserrat-ExtraBold.ttf`; emoji via an installed colour-emoji font if it works, else strip emoji; overlaid for `start..start+duration`) -> facecam (round, looped ping-pong of `use_seconds`, sound dropped; reuse `facecam_video.py` filter). Zoom must NOT move the captions, hook or facecam.
- If `layout.base_file` is set, use that 1080x1920 file instead of the fit layout (lets an OpenShorts plain cut be the base).
- Each layer with `"on": false` (or empty zoom) is skipped. Audio = source audio of the trim, AAC.
- Validate the JSON first: unknown keys or bad values -> a one-line error naming the key. Print the wall time. Output 1080x1920 H.264 yuv420p.
- Import numpy only where needed; no new pip packages beyond PIL/numpy.

## edit_clip.py CLIP.json key=value [key=value ...] [--render]
Dotted keys (`captions.on=true`, `hook.text="..."`, `facecam.size=300`, `facecam.position=top-left`), relative trims (`trim.start=-2`? no: use `trim.start+=-2` / `trim.end+=3`), JSON values for lists (`zoom.plan+={"t":3,"x":0.1,"y":0.6,"amp":0.5,"dur":4}` appends). Validates with the same checker, saves, keeps the previous version as `<id>.clip.prev.json` (one-step undo: `--undo`), and with `--render` re-renders to the same output file. Hook/zoom times are relative to the clip start, so when `trim.start` moves, shift `zoom.plan` times to keep them on the same source moment.

## CONTROLS.md
A table: what the user might say -> which key -> allowed values -> example command. One row per control above.

## Acceptance test (HISTORY, done; stream was on the VM; do not touch YouTube)
Source `$S/stream/dl/video.mp4`, transcript `$S/stream/transcript_hi.json`, info `$S/stream/dl/info.json` with S = the session's work folder outside the repo (it exists only on the machine that ran the test). Candidates: `streams/2026-11-14_this-is-not-a-game/docs/moment-finder/candidates.md`. Cut the three missed moments (rank 2 ~1740-1774 s, rank 3 ~1267-1302 s (start after the old clip that ends ~1267), rank 9 ~460-500 s) as complete moments into `streams/2026-11-14_this-is-not-a-game/clips/`.

## Facecam library and shapes (added 2026-11-14, user request)
User: "new streamer reaction video I wanna use as overlay and not circular but edge rounded rectangle ... later on I can provide different ones while using skill."
- Library: `.claude/skills/clips/assets/facecam/library.json` = `{"default": NAME, "items": {NAME: {"file","focus":[fx,fy],"tight":0-1,"calm":[a,b],"segments":{"calm":[a,b],"surprised":[a,b],"laugh":[a,b]},"ai_generated":true,"added","note"}}}`. Files live in `.claude/skills/clips/assets/facecam/NAME.mp4`.
- `scripts/add_facecam.py FILE NAME [--focus fx,fy] [--tight 0.85] [--calm a,b] [--segments JSON] [--default]`: copies the file in, writes a 2 fps contact sheet `assets/facecam/NAME_sheet.png` (so Claude can LOOK and choose focus, calm range and segments), registers it, `--default` makes it the default for new clips. Before adding a face: confirm it is AI-generated or consented (lesson facecam-ai-generated-only) and store `ai_generated`.
- clip.json `facecam` (new shape; replaces `crop`): `{"on","video": NAME or path,"use_seconds": "all" | "calm" | [a,b],"shape": "rounded" | "circle","radius": 36,"aspect": "4:3","size": 400 (= width in px; height from aspect; circle uses size x size),"focus": null | [fx,fy],"tight": null | 0-1,"border": 0,"border_color": "#ffffff","position","margin":[x,y]}`. `focus`/`tight` null = take them from the library item. The crop is the largest rectangle of the target aspect, `tight` x source height tall, centred on `focus`, clamped inside the frame. Default shape is `rounded` 4:3.
- SKILL.md Step 1 asks which facecam (names from the library, default first) or none; a user-supplied video at any time -> `add_facecam.py`, then `edit_clip.py CLIP.json facecam.video=NAME --render`.
- `make_clips.py --facecam NAME|none` overrides the default for a whole run.
- Timed reactions (v1.1 backlog, see Current plan; the single-line `facecam.voice=low` is built): reaction-synced facecam: play the library item's `segments` (calm most of the time, surprised/laugh on the clip's loud peaks) instead of one loop.

## Who runs what (added 2026-11-14, user request)
The skill is RUN by a Sonnet session. Opus is an advisor for hard calls only. Haiku sub-agents do the simple steps.
| Step | Model | Why |
|---|---|---|
| 0 lessons, plan, questions to the user | Sonnet | judgement |
| 2 download, wait, fetch (Kaggle) | Haiku | fixed commands, waiting |
| 3 transcript (captions -> json; or start the Whisper job and fetch it) | Haiku | fixed commands |
| 4 run find_moments.py | Haiku | fixed command |
| 4 read candidates + transcript, set complete-moment boundaries, write titles and hooks, reject weak ones | Sonnet (Opus advice when two cuts of a moment are both plausible or the transcript is unclear) | the core judgement |
| 5 make_clips.py, contact sheets | Haiku | fixed command |
| 5 look at the sheets, decide fixes | Sonnet | judgement |
| 6 plan_zooms frames -> zoom targets | Sonnet | needs to see the frame |
| 7 edit_clip.py for a change the user asked for | Haiku runs it; Sonnet maps the user's words to keys | CONTROLS.md is the map |
| 8 git add/commit/push, delete VM copies, add lessons | Haiku | fixed commands |
Rules: one Haiku agent per batch of simple steps (not one per command); give it exact commands and the expected output; agents never decide moments.

## Transcript and languages (English or Hindi streams)
1. YouTube captions in the video's own language (word-level `.vtt`) -> `vtt_to_transcript.py`. Free, instant. English auto-captions are usually good; Hindi ones are fair and write English words in Devanagari.
2. No captions (always the case for Twitch), or captions clearly bad: Whisper large-v3-turbo on a Kaggle T4, language locked once per source. BUILT (long mode, `long_run.py fetch-windows --whisper`) but measured WORSE than the captions for Hindi on 2026-11-15, so captions come first and the user is warned before Whisper is used (Current plan, decision 3).
3. The transcript drives: moment ranking (reaction words, speech rate), complete-moment boundaries, hook and title (real lines), captions, word-triggered and pointing zooms. Loudness and the YouTube heatmap do not need it.
4. Per language: `scripts/moments/reaction_words.json` needs an English list as well as the Hindi/Hinglish one; Roman map only for Hindi.

## Model upgrades: research and trials (added 2026-11-14, user request)
User: "See if there are superior models that you can use to improve stuff, also since they are offline models you may train them even. But let's keep the size in check and storage in check."
Budget: every model open-licence, runs offline on the VM CPU (4 vCPU, 15 GB RAM) or a free Kaggle T4; at most ~2 GB per model on disk, ~5 GB for all models together; training only on Kaggle T4 or CPU, small models only.
Stages a model could improve (candidates to VERIFY from model cards, not assumed):
1. Transcript, English: faster-whisper large-v3-turbo / distil-large-v3, NVIDIA Parakeet, Moonshine.
2. Transcript, Hindi/Hinglish: Whisper Hindi fine-tunes, AI4Bharat models, a Whisper fine-tune that writes Roman Hinglish directly (would remove the word map).
3. Devanagari -> Roman: AI4Bharat IndicXlit or similar small transliteration model.
4. Moment signal from sound: an audio-event tagger (laughter, shout, scream, gunshot, cheering): YAMNet, PANNs, BEATs, CLAP zero-shot.
5. Moment signal from the picture: a small vision-language model that describes frames (SmolVLM class), only if it runs on CPU in reasonable time.
6. Zoom targets ("what is he pointing at"): a small grounding model (Florence-2 class) to find "minimap", "map", a named object.
7. Streamer-cam position per stream: a tiny face detector (YuNet / MediaPipe) to set cam_xy automatically.
8. TRAINABLE, tiny: a highlight scorer that learns from YouTube "most replayed" heatmaps (features: loudness, speech rate, reaction words, audio events) so it also works on Twitch (no heatmap); later it also learns from the user's keep/reject decisions.
Output: `.claude/skills/clips/docs/model-research.md` (verified table + recommendation per stage + total disk) and `.claude/skills/clips/docs/model-trials.md` (measured CPU trials). Nothing is wired into the skill until the lead reviews both.

## Best parts of OpenShorts to keep (added 2026-11-14, user request)
The clips engine does the gameplay layout, hook, captions, zoom and facecam itself. From OpenShorts (MIT, pinned 68b8c0f) we take only what it does better:
1. **Whisper transcription** (faster-whisper large-v3 on a Kaggle T4, word times): build a transcript-only job from `run.py`'s setup, for videos without captions and all Twitch links. Highest priority.
2. **AI moment picking** (Gemini or local Qwen over the whole transcript, with title, hook, score, "why"): run it as one more opinion and feed its picks to `find_moments.py --external`; never let it cut alone.
3. **Face-tracking layouts** (TRACK, speaker_cut, punch_in) for podcasts and talking-head videos: render its plain cut and use it as `layout.base_file`; our hook, captions, zoom and facecam go on top. Not for gameplay (its webcam and Gemini layouts cut the game).
4. **Scene detection**: use scene-change times to snap clip starts and ends away from mid-shot cuts.
5. **Publishing** (`/api/social/post`): later, behind the rights gate; untested.
Not taken: its captions and hook pill (ours are editable and faster), its GPU render path for gameplay.

## Editing tools from the user's list: status and plan
| Tool | Today | Plan |
|---|---|---|
| FFmpeg + libass + PIL | THE engine (one pass per clip) | keep |
| yt-dlp, faster-whisper | download on Kaggle; Whisper job built (long mode), weaker than captions for Hindi | captions first; Whisper only when there are no captions |
| HyperFrames (Apache-2.0) | tested: transparent hook card in 25 s; NOT wired into the engine | add `hook.style: "card"` (animated HyperFrames card as an overlay layer) and intro/outro cards |
| Claude Code video-editor recipe (style.md from 3-5 reference reels, draft-v1 + edit-notes.md, v2...) | pattern known from the user's brief; the scrape note is missing | `style.md` per channel = our `defaults.json` written from reference reels; `edit-notes.md` per clip (what changed and why); versions v1, v2 instead of one-step undo |
| rea-video (Apache-2.0) | researched, not run | use it once to break 3-5 reference reels into shots and fill `style.md`; never copy footage, text or logos |
| watch / claude-video (MIT) | not installed (user runs `/plugin install`); we extract frames and look | review step: watch each finished clip before sending |
| Sound effects: Openverse (CC0/CC BY), Real SFX, earshot | not used; Openverse downloads were blocked on the VM | `sfx` layer: soft whoosh on a zoom, pop on the hook; licence stored per sound; off by default |
| Remotion | skipped (not open source; HyperFrames covers it) | none |
| lemo-opuscar | skipped (films, not clips) | none |
| Higgsfield editing skills, OpusClip | paid, no credit | only if the user adds credit |
| vidIQ | moment finder and trim only | external picks for `find_moments.py` |

## Build order (HISTORY: items 1-3 built, 4-6 partly built or backlog; see Current plan) (user go-ahead 2026-11-14: "use whatever best things you can from the above tools ... and better local models if available")
Each item is one Sonnet agent with a measured test; Haiku writes the docs; the lead reviews before the next one starts. Engine files (`render_clip.py`, `clip_schema.py`, `edit_clip.py`) are changed by ONE agent at a time.
1. Transcript job: transcript-only Whisper on a Kaggle T4 (model chosen from `docs/model-research.md` + `docs/model-trials.md`), language detect (English / Hindi), output in our transcript format. BUILT as long mode; measured worse than captions for Hindi (Current plan, decision 3).
2. Moment finder upgrades that passed their trial: sound-event signal, English reaction words, the trained highlight scorer (only if it beats the hand weights), OpenShorts/Gemini picks as `--external`.
3. Engine layers: `hook.style: "card"` (HyperFrames transparent overlay, cached per hook text), `sfx` layer (off by default, licence per sound), numbered versions (`v1`, `v2`...) + `edit-notes.md` per clip instead of one-step undo.
4. Style: `style.md` per channel from 3-5 reference reels (rea-video or frames), compiled into `defaults.json`.
5. Auto helpers that passed their trial: face detector for `cam_xy`, grounding model for zoom targets, Roman Hinglish (model or transliteration) to replace the word map.
6. Review: watch each finished clip (frames + audio check) before sending; title candidates; rights gate on export.
Storage rule: after each step delete downloads and caches not needed at run time; the VM keeps only the source of the stream in progress.

## GPU budget (user, 2026-11-14; PARTLY SUPERSEDED 2026-11-15 by lesson kaggle-gpu-where-it-works-no-quality-fallback)
Kaggle T4: 30 h per week allowed. Use it where it is clearly better. The old rule "every GPU step has a VM CPU fallback" no longer holds: a CPU fallback only where it gives the same quality (never CPU Whisper for Hindi: slow and worse); on failure retry 3 times then tell the user. Log GPU minutes in the stream's run log, not `docs/timing.md` (that file does not exist).
| Step | First choice (Kaggle T4) | Fallback (VM CPU) |
|---|---|---|
| Transcript | Whisper large-v3 / large-v3-turbo, or the Hinglish fine-tune, full precision | none for Hindi (measured slow and worse); tell the user |
| Frame description / zoom grounding over many frames | SmolVLM / Florence-2 in one batch job | same models int8 on a few frames only |
| Fine-tuning (if ever) | T4 | not on the VM |
| AI moment picking (OpenShorts + local Qwen) | T4 | skip; use the moment finder alone |
| Clip rendering, highlight scorer, sound events, face detector | not needed | VM CPU (already fast) |
Planning figure: a 30-min stream should cost under ~15 GPU minutes (transcript) so 30 h covers 100+ streams a week.

## Build step 3 spec: safe areas, versions, hook card, sfx (lead, 2026-11-14)
Priority order A, C, B, D. One agent; engine files only by this agent.
A. **Safe areas (user rule: captions never cover the main area of the stream).** `clip_schema.py` gets `geometry(cj)` -> rectangles (x0,y0,x1,y1 in the 1080x1920 frame) for: `game` (fit layout: the 16:9 picture, y about 656-1264), `facecam`, `hook`, `captions` (worst case: 2 lines at the chosen font size, full allowed width). New `captions.position`: `"auto"` (default) | `"bottom"` | `"top"`; auto = bottom bar, vertically centred between the game picture and the facecam when the facecam is at the bottom, else centred in the bottom bar. Font size shrinks until the widest line fits in 1000 px and the box fits the free space; at most 2 lines. `validate` REFUSES a caption box that overlaps `game` (error names the key), and refuses or auto-moves one that overlaps `facecam` or `hook`. With `layout.base_file` (no known game band) captions stay in the lowest quarter and a note is printed. `scripts/check_layout.py CLIP.json` prints every rectangle and PASS/FAIL for: captions vs game, captions vs facecam, captions vs hook, facecam vs game, hook vs game; `make_clips.py` runs it and writes the result into `review.md`. Prove it with a rendered frame (captions on) AND a pixel test: render the caption layer alone and confirm no caption pixel falls inside the game rectangle.
C. **Versions and edit notes.** Every `edit_clip.py` run saves `<clip dir>/versions/vN.clip.json` and appends one line to `<clip dir>/edit-notes.md` (UTC time, each key old -> new, optional `--note "why"`). `--undo` = back one version, `--version N` = restore version N, `--history` lists them. Remove the `.prev.json` mechanism and files.
B. **`hook.style`: `"pill"` | `"card"` (SUPERSEDED: the default is `editorial`, part E below; pill and card are options).** card = an animated HyperFrames card rendered to a transparent WebM (`npx hyperframes render . --format webm`), cached under the stream's `docs/cache/` by a hash of text+style, overlaid in the same single pass. Template: `.claude/skills/clips/docs/examples/hook_card/`. If npx/HyperFrames fails or free disk is under 2 GB: fall back to the pill and say so.
D. **`sfx` layer, off by default.** `{"on": false, "auto": true, "volume": 0.25, "events": [{"t","sound"}]}`; sounds are ORIGINAL, synthesised with ffmpeg (soft whoosh, pop) into `.claude/skills/clips/assets/sfx/*.wav` (small, no licence issue); auto = whoosh at each zoom start, pop at the hook start; mixed in the same pass.
Docs: update SKILL.md and CONTROLS.md rows for every new key.

## Video-type profiles and the animations layer (user, 2026-11-14)
- **Profiles.** Each video type has its own steps and defaults. Now: `gaming` (streams with a webcam, and plain gameplay videos without one: no streamer cam, so no cam zoom and the facecam overlay matters more). Later: `podcast`, `talking-head` (OpenShorts face-tracking base). The skill asks or detects the type first.
- **Animations layer: OFF by default, only when the user asks.** `"animations": {"on": false, "events": [{"t": seconds, "preset": NAME, "text": "...", "xy": [x,y], "duration": s}]}`. Presets live in `.claude/skills/clips/assets/animations/NAME/` (a HyperFrames HTML+GSAP template, rendered to a transparent WebM, cached, overlaid by ffmpeg in the same pass). Effects that change the picture itself (shake, flash, freeze) are ffmpeg filters listed as presets too.
- First a DEMO on one clip (standalone, engine untouched); the user picks which presets to keep; only those are wired into the engine.

## Build step 3, part E: editorial title with auto contrast (user chose style C, 2026-11-14)
- `hook.style`: `"editorial"` (new default) | `"pill"`. Editorial = style C of `streams/2026-11-14_this-is-not-a-game/docs/title-style-options.py`: Playfair Display (fonts in `.claude/skills/clips/assets/fonts/`), white, no box, soft blurred shadow, max 2 lines inside 920 px, centred about y=250; `hook.emphasis`: one word (or phrase) drawn in Playfair italic; null = no italic. make_clips picks the key noun of the hook as emphasis; the user can change it.
- **Readable on any background** (user: "take care of color in case the bg is white"): `hook.color`: `"auto"` | hex; `hook.scrim`: `"auto"` | 0-1. Auto = sample the title's rectangle on about 6 frames across the hook's time (after layout, before the title is drawn), take the brightest; if its mean luma is high (start with > 150 of 255) draw a soft feathered dark scrim behind the text (opacity rising with luma, capped about 0.55) and strengthen the shadow; text stays white. If even that gives a contrast ratio under 4.5:1 against the scrimmed background, use charcoal text with a light glow instead. Print the measured luma and the choice.
- Prove it on: the three real clips, AND a synthetic pure white source and a pure black source (ffmpeg lavfi), with frames looked at.
- Then re-render the three published clips ONCE with the new default title (same file names) and refresh their sheets and review.md.

## Repo restructure: site-ready layout (user, 2026-11-14). Runs AFTER cleanup phase 1, BEFORE the history rewrite.
Target tree (nothing else at the top level):
```
.claude/
  REQUIREMENTS.md
  skills/
    clips/            SKILL.md, CONTROLS.md, PLAN.md, defaults.json
      scripts/        render_clip, edit_clip, make_clips, clip_schema, check_layout, add_facecam, build_index,
                      download/ (kaggle.py, download_job.py), transcript/ (vtt_to_transcript.py, run.py for the Whisper/GPU path),
                      moments/ (find_moments.py, weights.json, reaction_words.json), zoom/ (plan_zooms.py), captions/ (ass_from_words.py, roman_map_hinglish.json), trials/
      assets/         fonts/, facecam/ (library.json + videos), animations/<preset>/
      docs/           model-research.md, model-trials.md, tool-research.md, decisions.md
    lessons/          SKILL.md, scripts/
    yt-*/             third-party skills, untouched
lessons/              the knowledge graph (stays at the root: the user placed it there)
streams/
  index.json          GENERATED manifest: every stream and clip with the fields a site needs
  <stream-slug>/      stream.json (title, channel, url, language, duration, date added, rights)
    clips/<clip-id>/  clip.mp4, clip.json (settings = source of truth), poster.jpg (frame for a card), edit-notes.md, versions/
    docs/             moments.json, review.md, reports, sheets/
archive/              old text notes
README.md             the tree above, one line per folder
```
Rules: slugs lowercase a-z0-9 and hyphens; clip-id = `<start>-<end>s_<short-slug>`; one folder per clip; no loose media anywhere else; every path inside clip.json, library.json and the manifest is repo-relative. `build_index.py` writes `streams/index.json`: per clip `{id, stream, title, hook, description, duration, start, end, score, video, poster, created, rights}`; `video` is a repo path today and can become a URL later (Git LFS, releases or object storage) without changing the site. The one-skill merge: `openshorts-clip`, `moment-finder` and `ai-edit-layer` stop being separate skills; what is still used moves into `clips/scripts/`.
Acceptance: all scripts compile; `REPO` root detection works from the new place; `edit_clip.py ... --render` re-renders one clip to its new path; `check_layout.py` passes; `lessons` scripts and graph ok with evidence paths fixed; `streams/index.json` validates and lists the 3 clips; `grep` finds no path of the old top-level folder outside archive/ and git history.

## Skills to leverage (user, 2026-11-14): use what is installed, add more later
| Step in the clips flow | Installed skill | Use |
|---|---|---|
| Titles and thumbnail text per clip | `yt-package` | write and lint title candidates (truncation, vagueness); fills the missing title writer |
| Description, tags | `yt-seo` | the social caption per platform |
| Second opinion on moments | `yt-shorts` | its transcript-based picks go into `find_moments.py --external` |
| What works in the niche (hook and length patterns) | `yt-viral` | sets style defaults per channel; needs a niche or channel |
| After posting | `yt-retention`, `yt-audit` | learn from real retention data; feeds the highlight scorer and lessons |
| Engine quality | `code-review`, `simplify` | review after each build step, by a Sonnet agent |
| The skill itself | `skill-creator` | test and tune the clips skill's description and steps |
| Learning | `lessons` | Step 0 and the last step of every job |
| Future site | `artifact-design`, `dataviz` | pages that read `streams/index.json` |
Rule: a skill is wired in only after a short trial on one real clip; each row above is untested until marked DONE. New skills get a row here.

## From the friend's brief (2026-11-14): what we take, what stays optional, what we skip
The user's own rules win where they conflict (captions off by default, subtle zoom, the whole story of the moment, free and CPU-first).
| Idea in the brief | Decision | How |
|---|---|---|
| 9:16 safe zones: bottom 20% and right 15% clear of text and focal points (platform buttons and titles cover them) | ADOPT (needs the user's OK: it moves the facecam) | `check_layout.py` gets a `platform_ui` rectangle check (bottom 384 px, right 162 px); layout option `layout.game_y` to place the game picture higher so facecam and captions sit between it and y=1536. Show a still mock-up first. (Fixed by layout C: the facecam is at y 1250-1475.) |
| Loudness -14 LUFS, true peak -1 dB | ADOPT, default on | `audio.target_lufs: -14`, `audio.true_peak: -1` via ffmpeg `loudnorm` in the same pass |
| Export: match source frame rate, 15-20 Mbps | ADOPT as a preset | `output.preset: "preview"` (today: 30 fps, small) or `"upload"` (source fps, e.g. 60 for gameplay, ~12-18 Mbps); upload masters do not go into git |
| 3-second hook: start on tension, no slow build-up | ADOPT as a check | when setting boundaries the first line must be strong; optional `intro.cold_open` (2-3 s of the peak first), off by default |
| Banding in blurred areas (their film grain point) | ADOPT, minimal | light dither/noise on the blurred bars only; the game picture is not graded |
| IR schema | ADOPT fields | `profile` (genre), `audio` targets; later `cuts: []` (several segments with a J-cut lead) |
| MediaPipe face detection | ADOPT (same as our YuNet item) | sets `cam_xy` automatically; face tracking for the podcast profile later |
| Kinetic captions (heavy font, 1-3 words, centre, yellow highlight, spring pop) | OPTIONAL preset | `captions.style: "kinetic"`; never the default (user wants captions off or minimal and low) |
| Filler and dead-air cuts over 0.25 s | OPTIONAL, off | would break game-footage continuity and reaction timing; maybe for podcasts |
| Pattern interrupt every 3-5 s, slow 100->108% ramps | OPTIONAL | `zoom.energy: "calm"` (default) / `"medium"` / `"high"` |
| Seamless loop ending, J-cuts | OPTIONAL, later | needs multi-segment cuts |
| Vocal chain (high-pass, de-ess, compress, EQ), sfx at -22 to -26 dB, music ducking | OPTIONAL | `audio.polish`, the `sfx` layer; no music (copyright) |
| S-curve, halation, heavy grain | SKIP for gaming | it changes the game's look |
| B-roll cards, Pexels/Pixabay | LATER | podcast and finance profiles |
| Deepgram Nova-3 (~$0.005/min), WhisperX | NOTE | Deepgram = cheap paid fallback for transcripts if the user wants; WhisperX alignment is a candidate inside the Kaggle transcript job |
| Cloudflare R2 / S3 | NOTE | where videos go when the site outgrows git (the manifest's `video` becomes a URL) |
| TwelveLabs, Auphonic, Runway, Creatomate, Shotstack, Klap/Vizard/OpusClip APIs, Remotion, DaVinci MCP, n8n | SKIP | paid or redundant with ffmpeg + HyperFrames + our local models |

## Restructure additions (user, 2026-11-14): find new clips fast, post kit, outputs with and without the facecam
- **Stream folders are date-prefixed:** `streams/2026-11-14_this-is-not-a-game/` (date the clips were made), so the newest sorts last/first everywhere.
- **`LATEST.md` at the repo root (generated):** newest clips first, one row each: date | stream | clip title | length | links to each output video | link to the post kit. The root README links to it in its first line.
- **Per clip folder:** `streams/<date_stream>/clips/<clip-id>/`
  - `social.mp4` (with the facecam) and/or `clean.mp4` (no facecam, for the clipping site); `clip.json` has `"outputs": [{"name":"social","facecam":true},{"name":"clean","facecam":false}]`; other layers are shared. `edit_clip.py` re-renders every output of the clip; `make_clips.py --outputs social,clean`.
  - `post.md`: YouTube Shorts title (under 100 characters, aim under 60), description, tags; Instagram caption and hashtags; credit line (streamer name and source link); rights status; the same fields in `clip.json` under `post` and in the manifest.
  - `poster.jpg`, `clip.json`, `edit-notes.md`, `versions/`.
- **Step 1 question added:** "Streamer girl: with / without / both?" (and which facecam from the library when with).
- Which clipping site and its rules (title on or off, length limits, watermark): answered 2026-11-16, the rules are to be found when a brief is supplied (`whop-content-rewards` stays `verified:false` and renders as `clean` until then); not an open question.

## Build step 4 spec: animations in the engine (user liked the demo, 2026-11-14)
Source: `.claude/skills/clips/assets/animations/*` and `streams/2026-11-14_this-is-not-a-game/docs/animation-demo.md` (the demo's exact commands).
- `hook.animation`: `"none"` (default: static editorial title; since 2026-11-15, see 'Defaults change') | `"reveal"` (only on request or for highlights). Reveal = the `title-reveal` preset with this clip's `hook.text`, `hook.emphasis` (italic, colour `hook.emphasis_color`, default gold #E8C47A), text colour and scrim from the auto-contrast choice, timing from `hook.start` / `hook.duration`. If HyperFrames cannot run: draw the static editorial title and print a warning.
- `animations` (example with animations turned ON; the defaults are `on false`, `progress_bar false`, empty events): `{"on": true, "progress_bar": true, "events": [{"t": s, "preset": "callout-ring" | "lower-third-tag" | "impact-burst", "text": "...", "xy": [x,y], "duration": s}]}`. `events` is empty by default: the skill PROPOSES events in the plan step (time, preset, text) and adds them when the user agrees. `impact-burst` is toned down: no full-frame flash over the facecam, a smaller ring, a shake of a few pixels on the game picture only.
- Rendering: each title/event is a HyperFrames render to a transparent WebM, cached in the stream's `docs/cache/` by a hash of preset + parameters + template file; all overlays and the progress bar are composited in the SAME single ffmpeg pass as today. Templates take their values from a small JSON written next to the template copy (no hand edits). Vendor `gsap.min.js` into `assets/animations/_lib/` so renders work offline.
- `check_layout.py`: add rectangles for the tag and the title animation; the tag must not overlap the facecam or captions; only `callout-ring` and `impact-burst` may sit over the game.
- Versions/edit notes, CONTROLS.md and SKILL.md cover the new keys; SKILL.md's plan step says: propose 0-3 small animations per clip with times, ask, then add.
- Acceptance (done then; the three clips were later re-rendered with the static title, commit 5fc5193): re-render the three published clips with the animated title and the progress bar (same file names); clip 01 also gets the demo's ring (HEADSHOT, about 4.5-6.5 s) and tag (RED DEAD STYLE SLOW-MO, about 8-11.6 s) and the toned-down burst at the scream; LOOK at one frame inside every animation; report the first-render and cached render seconds per clip; `check_layout` passes.

## Model trial results (2026-11-14) and what changes in the build order
- Sound events (YAMNet): NOT wired in as a score (adds almost nothing beyond loudness); optional tag in the review pack ("scream", "laughter").
- Trained highlight scorer: NOT yet (one stream is too little; 10-20 needed). From now on every stream stores its heatmap, signals and the user's keep/reject choices under `docs/training/` so the data builds up.
- Hindi transcript on the VM CPU: NO (whisper small unusable, medium 5.5x real time and worse than YouTube captions). So: YouTube captions first; no captions (Twitch) = Kaggle GPU job only; if Kaggle is down, tell the user instead of a bad CPU transcript.
- Tested later on the Kaggle GPU (2026-11-15): large-v3-turbo, forced Hindi: worse than YouTube captions (Current plan, decision 3). Still to test: the Hinglish Whisper fine-tune (Roman output); then SmolVLM, Florence-2, YuNet from the research list.

## Finalisation order (HISTORY, user: "Finalise everything", 2026-11-15; steps 1-6 done, 7 written as QUICKSTART.md)
1. Step 4 animations (agent running).
2. Research: PeakCut + the five reel tools (WhisperX, PySceneDetect, Auto-Editor, Remotion, FFmpeg) -> docs/peakcut-and-reel-tools.md (agent running). Its recommendations are merged into this plan before step 4 below starts.
3. Restructure into `.claude/` + `streams/` (+ LATEST.md, post kit, outputs with/without the facecam, date-prefixed stream folders) and merge the three helper skills into `clips`. One agent; engine is frozen while it runs.
4. Transcript job on the Kaggle T4 (WhisperX or faster-whisper, per the research), language detect, our transcript format; wired into the flow for videos without captions and Twitch.
5. History clean (DONE 2026-11-15): old large files stripped from git history, every current file verified byte-identical, main and the branch force-pushed. Old large files are gone from main and cannot be recovered.
6. Fresh-clone readiness test (Haiku): clone main into a temp dir, load the skill, compile scripts, run lessons query, render one clip from a tiny source, check streams/index.json and LATEST.md.
7. QUICKSTART.md: what to attach, environment variables and network needed, what to type in a fresh session, what the skill asks; then tell the user it is ready.
Open questions to the user (do not block the build): the clipping site's rules are to be found when a brief is supplied (answered 2026-11-16); keep all five animations (user likes them); safe-zone mock-up.

## Destinations (user, 2026-11-15): various sites (content rewards, Whop, others)
- `destinations/<name>.json` (in the skill folder), one per upload target: `{name, outputs: facecam true/false, title on/off, captions on/off, max/min seconds, resolution, fps, video bitrate cap, audio target LUFS, credit_line required, watermark rules, post_text_format, source_doc_url, verified: true/false, notes}`. Start with: `youtube-shorts`, `instagram-reels`, `clean` (no facecam; generic), and `whop-content-rewards` marked `verified:false` until its rules are read from its own docs.
- clip.json `outputs: [{"name": "<destination>", ...overrides}]`; `make_clips.py --destinations a,b`; `edit_clip.py` re-renders every output; manifest, LATEST.md and post.md list one file per destination.
- Step 1 asks: "Where will these be posted?" (multi-choice) instead of only with/without the girl.
- Rule: a destination profile with `verified:false` renders as "clean" and prints a warning; rules are never guessed.

## Layout C becomes the standard social layout (user: "Go with C", 2026-11-15)
- `layout.profile`: `"safe-c"` (new default for social destinations) | `"classic"` (current: game centred, facecam bottom-right; kept for destinations without app-button overlap or no facecam).
- safe-c geometry (1080x1920): game picture y 456-1064 (shifted up 200 px); blurred bars fill the rest; title in the top bar (about y 140-300, inside the safe width); facecam 300 px wide (4:3, rounded) at x 40-340, y 1250-1475 (user asked for a little lower on 2026-11-15; above the bottom 20% zone y>=1536); captions, when on, between y 1100-1500 on the right of the facecam or below it, never inside the game picture or the bottom 20% / right 15%; animations (tag, ring) follow the new game rectangle.
- The 64 px corner graze of the top app button on the game picture (mock-up B/C) is accepted unless the user asks for a shift of about 70 px more; offer it.
- `check_layout.py`: add `platform_ui` rectangles (bottom 384 px, right 162 px); PASS means facecam, title and captions are outside them; the game picture may touch the right zone only at its corner.
- DONE (step 5, see the build report): safe-c is implemented, the three published clips are re-rendered, `layout.game_shift_extra=70` is offered as the optional extra shift. Facecam size is 300x225 (4:3), y 1250-1475 (lowered from 1090 on 2026-11-15 at the user's request; the three clips are re-rendered).
- After the animations agent finishes: one Sonnet agent implements safe-c, re-renders the three published clips once, and shows before/after. The geometry numbers come from `docs/safe-zone-options.py`.

## YouTube Shorts: what we can change (plan, 2026-11-15)
Facts (see docs/destination-rules.md): Shorts allow up to 3 minutes, square or vertical; YouTube's reused-content policy reviews clips and reactions, applies even with permission, and can remove monetisation channel-wide; commentary or a real narrative is the safe side. Instagram Reels limits are unverified.
What we can do inside the skill (all optional per destination `youtube-shorts`):
1. Add the streamer-side value, not just a cut: a short on-screen context line at the start ("what you are about to see"), our own title, and where it fits the story (the static editorial title does part of this; the animated title only if asked).
2. Commentary voice-over (NOT the user's own voice): a human-sounding synthetic voice with natural flow, chosen by listening tests (research and samples: `docs/voice-research.md`). The script is written by the Sonnet runner from the moment's transcript in a spoken style (short sentences, contractions, natural pauses) and the user approves script and voice each time. Off by default; never a clone of a real person's voice. Audio: the voice sits in the quiet gaps, the game audio ducks under it, final loudness -14 LUFS. Text-only analysis overlay is the alternative.
3. Structure: a clear hook, a payoff and a one-line takeaway card at the end (the HyperFrames end card).
4. Length: 40-55 s stays; allow up to 3 min only for stories that need it.
5. Credit: a credit line in the description (streamer name and source link) and an optional on-screen credit for the first seconds.
6. Metadata: title, description and tags from the YouTube skills; a source link; the policy warning line in post.md.
7. Check before export: `rights.status`, a reminder if the clip has no added commentary.
Not done: nothing here edits footage to avoid detection.

## Comparison videos (user, 2026-11-15): GTA Vice City vs GTA 6, similar places (clubs), top and bottom
- Profile `comparison`: two sources (A = old game, B = new game), each with its own trim; layout top/bottom halves (each 1080x960 or the 16:9 picture centred in its half), a thin divider, a label chip per half ("VICE CITY 2002" / "GTA 6 2026"), shared timeline with optional small offset, one audio source (default: the user's commentary or the new game; never both), animated title, a takeaway end card.
- Finding "similar areas": a trial with frame embeddings (CLIP or SmolVLM descriptions) between the two videos to suggest pairs (club interior, beach, street at night); the user confirms each pair. Needs both videos available (user supplied files or links; the old game footage can be captured by the user).
- Footage sources: user-owned captures, official trailers. Rights and policy: see the research file `docs/rockstar-policy-and-comparison.md` (agent running); no editing to evade detection; commentary and transformation are the honest route.

## PeakCut and reel tools: merged recommendations (research 2026-11-15, docs/peakcut-and-reel-tools.md)
PeakCut (MIT, two days old, FastAPI web app, English-only speech model) is mined for ideas, not run. Each item below goes to a build step:
| # | Item | Goes to |
|---|---|---|
| 1 | `loudnorm` two-pass (I=-14, TP=-1, linear, 48 kHz); pass 1 is audio-only so the one-video-pass rule stays; `audio.target_lufs`, `audio.true_peak` | engine, after layout C |
| 2 | Boundary snap: start and end move to a scene cut within 2 s (`ffmpeg scdet=t=10` on a 12 s window, about 2.5 s each), never inside a spoken word, never outside 40-55 s | moments step before render |
| 3 | `--external` picker prompt from PeakCut's rules (setup line to payoff, skip intros and sponsor reads, honest scores, fixed categories, highlight words, reason, untrusted-text guard); `--external` carries category, hook, reason, highlight_words into candidates.md | moment finder |
| 4 | `roman.py` (MIT, 206 lines + tests, keep the licence notice) as the fallback for words missing from the Hinglish map; loan words it spells by sound are marked for review | captions |
| 5 | Kaggle transcript job on faster-whisper alone (batched, VAD, word timestamps, Hinglish fine-tune); 10-minute word-timing trial before adding WhisperX; WhisperX only for English or Devanagari output | transcript job |
| 6 | Mark transcript lines "(LOUD)" in candidates.md (line max z-score above 1.5) | moment finder |
| 7 | Long streams: fetch only the chosen sections with yt-dlp section ranges, pin the true start by audio cross-correlation | download step (later) |
| 8 | Remotion: reason is "source-available, free for one person, not needed"; Auto-Editor only for a later podcast profile | docs |

## Persona voice: the streamer girl speaks (user idea, 2026-11-15)
The facecam girl is fictional, so a generic female voice can be "her". Options, to be judged by the user's ears on samples (docs/voice-research.md and docs/voice-samples/):
1. Her own audio: if the Gemini-app facecam videos carry her generated voice, gasps or laughs, reuse those sounds; they are already in sync with her face. (Checked by the voice agent.)
2. A synthetic female voice reading short reaction lines written by the Sonnet runner from the transcript; ducks the game audio; off by default; the user approves each script.
0. BUILT in v1 (user decision 2026-11-15: "I want her passive reactions and maybe voice but not overpowered voice just mixed with normal voice of the stream"): option 1 as `facecam.voice` = `off` (default, passive reaction, her audio dropped) | `low` (her library line, `audio_usable` items only, English, played ONCE after the loudest peak, lips in sync through a phase shift of the facecam loop, 0.15 s fades, level from ebur128 and checked in the final file so her speech is about 15 dB under the stream's speech level, never closer than 6 dB under the stream in her own window, nothing ducked, mixed before the two-pass loudnorm so the file stays -14 LUFS / -1 dBTP). Silent when the facecam is off (clean, whop). Say "add her voice quietly" / "no voice" (CONTROLS.md). Timed reactions (several lines on real beats, calm to surprised to laugh segments) stay BACKLOG in v1.1.
3. Later, needs a GPU and a trial: reaction-synced facecam (play her surprised/laugh segment at the loud peaks) and optional lip-sync on a Kaggle T4. Not built; without it her mouth does not match the words.

## Comparison profile: rules from the Rockstar research (2026-11-15, docs/rockstar-policy-and-comparison.md)
- Commentary is REQUIRED (voice from the human-like synthetic voice, or written analysis): no export without a commentary track covering most of the clip; the footage is the example.
- Game and trailer audio muted by default; warn if the mix contains game audio (radio songs have their own owners).
- Rights status per source: Rockstar/Take-Two side (own capture, official marketing, other) and streamer side (own, permission, campaign terms, unknown); block export when the streamer side is unknown.
- Keep claimed-risk Shorts at 60 s or less; credit line per source (a courtesy, no legal cover); the post.md warning text; no flip/speed/filter tools.
- The matching tool only suggests pairs (frame embeddings); a person confirms. Release timing: the research could not verify GTA VI's release date from Rockstar's page; use official marketing only until the user confirms.


## DONE 2026-11-15: restructure (see streams/2026-11-14_this-is-not-a-game/docs/restructure-report.md)
The site-ready layout, LATEST.md, post kit, named outputs and destination profiles above are implemented. Layout C facecam moved lower on user request: x 40, y 1250-1475 (margin [40,1250]); the lower-third tag default moved above it to [40,1150].

## Test runs after the skill is ready (user, 2026-11-15)
1. FULL RUN on a fresh link, in a NEW chat session, with Sonnet as the runner (Haiku for fixed-command steps): download on Kaggle, transcript (captions, or the Kaggle GPU job), moment finder, clips with layout C, static editorial title, facecam from the library, post kits, `streams/index.json` and `LATEST.md`. Time every step, list the gaps, record lessons. Run one English stream and one Hindi stream if possible.
2. COMPARISON run (Vice City vs GTA 6, top and bottom, similar places such as clubs): needs two sources supplied by the user (own captures or links; rights status per source recorded, private-test), pair suggestions by frame embeddings with the user confirming, labels, one audio track, required commentary (synthetic voice or text), post.md warnings.
3. YOUTUBE COPYRIGHT CHECK (compliance, not evasion): the user uploads the finished clip to a PRIVATE or unlisted video and reads YouTube Studio's "Checks" result (YouTube checks copyright on upload). If a claim appears: use YouTube's own options (mute or replace the claimed song, trim the claimed segment, accept the claim, or dispute with a stated fair-use basis), then re-test. We record what was claimed and what fixed it in `streams/<stream>/docs/rights-checks.md` and as lessons. We do NOT build or run tricks that change footage to dodge detection (flip, pitch, speed, filters): they are not a fix for ownership, can still be caught, and can get a channel penalised.

## Edit effects layer (user, 2026-11-15): transitions, meme text, "several edit options", all based on the user's expectations
- `effects`: `[{"t": s, "dur": s, "type": "...", "params": {...}}]`, default empty; the Sonnet runner PROPOSES 0-3 effects per clip in the plan step (time, type, text), the user approves, then they are added; CONTROLS.md maps the user's words to events ("add a meme text 'NO WAY' at the scream").
- Types (verify with docs/effects-research.md): `transition` (ffmpeg xfade between two segments of the SAME moment; needs `segments: [{start,end},...]`; only when the user asks, because it removes footage), `meme_text`, `freeze_zoom`, `speed_ramp`, `shake`, `glitch`, `flash`, `emoji_pop`, `reaction_cutaway` (the facecam girl full screen for 1-2 s), `sfx` (original or openly licensed sounds), `zoom_punch`.
- Tools: ffmpeg filters (xfade, setpts/atempo, rgbashift, tblend, zoompan or scale+crop), HyperFrames for text and sticker pops, synthesised sounds. Fonts only with OFL licences (not Impact); emoji art only with a permissive licence.

## Scope control: v1 definition of done, versions, and the idea backlog (HISTORY wording; Current plan has the same v1 / v1.1 / v2 split) (user, 2026-11-15: "I tend to over cook things... a final check... good quality content, customisable")
Rule: new ideas go into the BACKLOG below and are NOT built until v1 passes its final check, unless the user says "build it now". Quality bar before any new feature: every v1 item passes its check.
**v1 (must work, then freeze):**
1. Fresh link in a new session, Sonnet runner (Haiku for fixed steps): ask-first questions, download on Kaggle, transcript (captions, or the Kaggle GPU job), moment finder with the whole story (40-55 s), 3-5 clips.
2. Each clip: static editorial title (readable on any background; animated title only on request), layout C (facecam lower-left at y 1250, or no facecam), captions off by default and never over the stream, audio at -14 LUFS, edges snapped to scene cuts, `check_layout` PASS, post.md, entries in `streams/index.json` and `LATEST.md`.
3. Editable: every setting changeable by saying it (CONTROLS.md), re-render in about a minute, versions and undo.
4. LONG MODE (user: yes, in v1): a 5-6 hour video is handled by the flow in the section 'Long videos (5-6 hours)': Kaggle prepares audio, captions and candidates, only chosen windows are downloaded, clips render in batches of 10.
5. Facecam library with the verified reaction videos (watching, surprise, impressed, hype, disbelief; laugh pending); one default calm clip.
**v1 final check (the user's review):** run on one fresh English link and one Hindi link; the user watches 3 clips per link on a phone; a list of what to fix; one fix round; freeze.
**v1.1 (after the freeze):** timed reactions with her own voice, the edit-effects layer (meme text, transitions, freeze zoom, speed ramp, sfx), more animation presets.
**v2:** comparison videos (Vice City vs GTA 6), persona/voice-over commentary, destination rules verified from real campaign briefs, YouTube claim-check log.
**Backlog (parked, unbuilt):** lip-sync on a Kaggle T4; Hinglish Whisper fine-tune test and Whisper tuning (non-batched, condition_on_previous_text off); SmolVLM/Florence-2/YuNet helpers; trained highlight scorer (needs 10-20 streams); Auto-Editor for a podcast profile; PySceneDetect beyond scdet; Twitch test; long-stream section fetch; site (reads streams/index.json); Pexels B-roll for podcast/finance profiles.

## Chat-activity moment signal (user idea, 2026-11-15) -> version v1.1 (becomes v1 if Twitch is needed in v1)
Idea: where live chat suddenly floods, a moment just happened. Rule from the user: clip start = the spike minus about 20 s (chat reacts 5-15 s after the event), length 40-55 s, boundaries snapped to sentence and scene cuts as usual.
- Signal: messages per 5-10 s; spike = z-score above 2 against the stream's own rolling median, with a minimum message count; extra weight for emote or reaction words ("LOL", "OMG", "clip it", "W", "KEKW", "no way"), for many different chatters (not one spammer) and for bursts that rise fast. Output into candidates.md as signal `chat` (weight to be tuned like the others).
- Data sources (all fetched on the Kaggle kernel; unverified until a trial): YouTube: chat replay exists only for past LIVE streams and premieres whose replay is on; `yt-dlp --skip-download --write-subs --sub-langs live_chat` writes a JSON of messages with times; the test stream THIS IS NOT A GAME was NOT a live stream (info.json: was_live False), so it has no chat replay; it does have 2,200 comments, many with timestamps like "5:32", a second signal (`comment_timestamps`) available for any video via `--write-comments`. Twitch VODs: chat is kept while the VOD exists; tools to try: TwitchDownloader (lay295, MIT) or chat-downloader (xenova, MIT); Twitch also has no heatmap, so chat would be the main signal there. Viewer-made Twitch clips of a VOD are another strong signal but need API auth.
- Limits: chat can be off, slow-mode or sub-only; spam and bots; chat language; spikes also follow giveaways and raids; chat shows what chat found exciting, not always the clip-worthy moment.
- Trial needed: one past live stream link on YouTube and one Twitch VOD link from the user.

## Long videos (5-6 hours) (user question, 2026-11-15): LONG MODE, recommended for v1
Measured base: our 33-min 1080p source is 875 MB (about 26 MB per minute), so 6 h would be about 9.5 GB: never download it whole. The moment finder processed 32 min of audio in 20 s (about 96x real time).
Flow (all downloads on the Kaggle CPU kernel):
1. Cheap pass for the whole video: info.json (heatmap, comments), captions if any, chat replay if any, and AUDIO ONLY at low bitrate (6 h is about 135-350 MB); no video yet.
2. Moment finder on those: audio loudness, reaction words, heatmap, comment timestamps, chat spikes. Zones scale with length (about one zone per 15 min, so 24 zones for 6 h) and every zone gets its best candidate; the heatmap is coarse for long videos (100 bins, about 3.6 min each at 6 h), so audio and chat get more weight.
3. Candidate list: top 30-60 windows. The runner reads only the candidates' transcript (about 400 words each), never the whole transcript (a talkative 6 h stream can be 50,000+ words). No captions: transcribe only the candidate windows (plus 90 s each side) on the Kaggle T4, not 6 h.
4. Download ONLY the chosen windows at 1080p with `yt-dlp --download-sections` (about 35 MB per 80 s window; 40 windows about 1.4 GB, deleted after rendering). Needs a trial (keyframe cuts, speed).
5. Render in batches: the best 10 first, then more on request; list the rest as candidates with scores. Render time about 1-2 min per clip with animations, about 25 s plain (measured).
6. Memory of what was cut: `streams/<stream>/docs/moments.json` keeps taken and rejected windows, so the next batch continues without repeats.
(Built since, see 'Long mode: built' below; only the trial on a real 5-6 hour link from the user is still missing.)


## Defaults change and two new requirements (user, 2026-11-15)
1. **Animations are not the default** ("good, but not for the default video, maybe for highlights when specifically asked"): defaults.json now has `hook.animation: "none"` (static editorial title), `animations.on: false`, `progress_bar: false`. The animated title, ring, tag, burst and progress line stay available for the highlights profile or on request. The three published clips were re-rendered with the static title (DONE, commit 5fc5193).
2. **Output quality (v1):** `output.preset`: `"preview"` (today: 30 fps, CRF 20, small, goes to git) | `"upload"` (NOT the default: `defaults.json` is `preview`; `upload` is for the final master of clips the user keeps: source frame rate (60 fps), x264 preset slow, CRF 16-17, audio 192 kbps AAC, loudnorm -14 LUFS / -1 dBTP; 1080x1920 vertical, 1920x1080 landscape). Never upscale beyond the source. An upload master of a 45 s clip at 15-20 Mbps is about 85-110 MB: too big for git (GitHub blocks files over 100 MB and the repo would balloon), so masters go outside git (a Kaggle private dataset, a GitHub release asset, or other storage chosen by the user) and `streams/index.json` links to them; git keeps the preview. Decided: masters go to a private Kaggle dataset per stream (next section). Untested option: 1440x2560 vertical for a better YouTube re-encode.
3. **Highlights video (BUILT 2026-11-16: make_highlights.py, render_highlights.py, edit_highlights.py, commentary module; the text below is the original plan; animations are ON in this profile): profile `highlights-yt`.** A 5-6 minute (300-360 s, adjustable) 16:9 1920x1080 60 fps YouTube video: 10-25 moments cut to their punchy core (10-30 s each), ordered as a story ladder (strong hook first, the best last), joined by transitions (xfade slideleft/circleopen, jump cuts), "crazy editing" ON by default in this profile: animated title and chapter cards, meme text on peaks, zoom punches, speed ramps on key frames, glitch and flash, synthesised sound effects, lower-third tags, the progress line; layout = the full 16:9 frame (the streamer's own webcam stays as in the footage); the girl facecam optional (corner, rounded rectangle) or full-screen reaction cutaways; audio: game audio ducked under a commentary track (the human-sounding synthetic voice or text), no copyrighted music (only original or openly licensed with the licence stored). Commentary or a real narrative is REQUIRED because YouTube's reused-content policy names compilations with little or no narrative as the risk case (docs/destination-rules.md); rights status per source as in the comparison profile. Needs: multi-segment timelines in clip.json (`segments`, `transitions`), a retiming map for effect times, the effects layer, a 16:9 layout profile. Step 1 of the skill asks the video type: shorts (default) | highlights | comparison.


## Source resolution and 4K (user question, 2026-11-15) and master storage decision
- **Master storage:** user said "keep wherever possible". Decision: previews in git; upload masters in a private Kaggle dataset per stream (our tools can do this; GitHub rejects files over 100 MB and cannot create releases here); `streams/index.json` records the master's dataset name and file; delete VM copies after upload; fetch on request.
- **4K sources.** Today `download_job.py` asks for 1080p H.264 (avc1), so a 4K video is downloaded at 1080p: our outputs are 1080x1920 (the game picture is 1080 wide) and 1920x1080, so 4K adds no visible detail except inside zoom-ins and a slightly crisper downscale. Estimates (unmeasured): a 4K file is about 3-4x bigger (about 80-100 MB per minute against 26 measured at 1080p), YouTube serves 4K only as VP9 or AV1 which decode slowly on the VM CPU (renders maybe 3-6x slower). Policy: `source.max_height` 1080 (default) or 2160 when the user asks for best quality; with long mode only the chosen windows are downloaded at 4K (about 130 MB each); say the cost before doing it. Untested: the engine's geometry is fractional, so it should accept any 16:9 source, but a real 4K sample is needed to prove it (and 21:9 or 9:16 sources are not handled).


## Final validation (user, 2026-11-15)
When everything above is built: one FABLE agent validates the whole plan, skill, scripts, docs and lessons by reading and dry runs only, following `docs/validation-brief.md` (no video generation, no fixing, no commits) and writes `docs/validation-report.md` with prioritised gaps (P0/P1/P2) and a suggested owner model per gap. Then Sonnet or Haiku agents fix the gaps (P0 first), one fix round, then a second quick validation of the fixed items, then the user's phone review of real clips from one English and one Hindi link.

## Long mode: built (2026-11-15)
Built: `scripts/long_run.py` (prepare, text, select, fetch-windows, render, status), `scripts/download/long_prepare_job.py`, `long_windows_job.py`, `long_whisper_job.py` (kaggle.py commands `prepare`, `windows`, `whisper`), find_moments `--zone-minutes`/`--keep`/no-transcript mode/comments signal/streamed audio, engine `source_offset` plus make_clips `--windows-dir`, SKILL.md "Long mode", CONTROLS.md rows, `docs/long-mode-report.md` (design, measurements, extrapolation). Window cuts are stream copies (frame-identical, measured). Not tested: a real 5-6 h link, Twitch, chat replay. Limits rule: 3 tries, then ask the user; no lower-quality fallback. Whisper in long mode is weaker than captions for Hindi: use it only without captions and say so (Current plan, decision 3).

