# PIPELINE: how a stream link becomes clips (and highlights), in full

## Start here (6 lines)
1. Goal: a stream link in, every good moment out as a 40-55 s vertical 1080x1920 clip (or ONE 5-6 min 16:9 highlights video). Every aspect lives in an editable `clip.json`.
2. The procedure is `.claude/skills/clips/SKILL.md` (wins over everything). Key map `CONTROLS.md`, setup `QUICKSTART.md`, defaults `defaults.json`, plan/backlog `PLAN.md` (read only its "Current plan"); all in `.claude/skills/clips/`.
3. Order: `preflight.py` -> lessons `query.py` -> ask once -> download + transcript -> moments -> clips -> edit loop -> checkpoint/finalise -> retro (step 9).
4. All YouTube access runs inside Kaggle kernels (YouTube blocks the VM). All rendering runs on the VM CPU. Never cookies, proxies or bot-check bypasses.
5. Never edit footage to dodge copyright detection. Never print or ask for a key.
6. File map, lessons, incidents, report digests, tools: KNOWLEDGE-BASE.md (this folder). Script names live in `.claude/skills/clips/scripts/`; run `python3` from the repo root. `$ST` = the stream folder `streams/<date>_<slug>`; paths like `docs/moments.json` are inside it; `$S` = `$ST`, `$H` = a `highlights.json`, `HL` = a highlights folder.

## 1. Who does what

| Context | Role | Model | Job |
|---|---|---|---|
| Running a clip job | Lead | Sonnet | preflight, plan, questions, reading candidates, boundaries, titles/hooks, mapping the user's words to keys, retro |
| | Fixed-command agents | Haiku (one agent per batch of simple steps, given exact commands) | download/wait/fetch, transcript, find_moments, visual scan/apply/merge, make_clips, edit_clip runs, checkpoint/finalise, reading contact sheets |
| | Advisor | Opus | only hard calls (two plausible cuts, unclear transcript) |
| | Rule | any agent | agents never decide moments and never see a Kaggle key |
| Building/improving the skill | Orchestrator | Fable (lesson `fable-orchestrates-only`) | plans, specs, checks, commits; ALL execution goes to Sonnet/Haiku |
| | Validator | Fable, read-only | `.claude/skills/clips/docs/validation-brief.md` -> reports (no rendering, no fixing) |
| | Auditor | Fable (else Opus), read-only | `docs/audit-prompt.md`, max 5 proposals, only when `audit_due.py` says DUE and the user agrees |

Seen in practice: the auto-mode classifier refuses sub-agents for second-Kaggle-account calls and GPU runs, so the lead runs those itself (incident `agent-blocked-by-classifier`).

## 2. The flow (steps 0-9)

| # | Step | Command / action | Who |
|---|---|---|---|
| 0 | Preflight, learn, plan | `python3 .claude/skills/clips/scripts/preflight.py [--stream $ST] [--facecam NAME]` then `python3 .claude/skills/lessons/scripts/query.py --stage plan,download,moments,render,layout,captions,zoom,facecam,publish,infra --retros 3`; tell the user a 6-line plan (moments, length, layout, captions, zoom targets, facecam) | Sonnet |
| 1 | Ask once | facecam name or `none`; destinations; video length (routes normal vs long); optional "add her voice quietly". Never ask what `defaults.json` answers | Sonnet |
| 2 | Download (Kaggle CPU kernel) | `scripts/download/kaggle.py download os-dl-NAME "URL"`, then `wait`, then `fetch ... $WORK/dl` -> `video.mp4`, `info.json`, `*.vtt` | Haiku |
| 3 | Transcript | `python3 .claude/skills/clips/scripts/transcript/vtt_to_transcript.py $WORK/dl/video.hi-orig.vtt $WORK/transcript_hi.json hi` | Haiku |
| 3b | Visual moments (parallel with 4) | `visual_scan.py`, reviewer sub-agent, `visual_review_apply.py`, `merge_moments.py` (all `scripts/moments/`) | Haiku |
| 4 | Moments | `find_moments.py`, then the lead writes `$ST/docs/moments.json` | Haiku runs, Sonnet judges |
| 5 | Make clips | `make_clips.py SOURCE TRANSCRIPT MOMENTS $ST --defaults .claude/skills/clips/defaults.json [--facecam NAME\|none] [--destinations a,b] [--no-snap]` | Haiku runs, Sonnet reviews sheets |
| 6 | Pointing zooms (optional) | `scripts/zoom/plan_zooms.py CLIP.json social.mp4 $ST/docs/zoom/<id>`, look at the gridded frames, add events | Sonnet |
| 7 | Edit loop | `edit_clip.py CLIP.json key=value ... --render` | Haiku runs, Sonnet maps words to keys |
| 8 | Save and publish | automatic `checkpoint.py`; `finalise.py --stream $ST --yes` when the user keeps the clips | Haiku |
| 9 | Retro (mandatory) | `retro.py --stream $ST` (section 9) | Sonnet, under 10 min |

Step 2 failures (read `$WORK/dl/kaggle-log.txt` when `video.mp4` is missing): `LONG VIDEO` (over 90 min, nothing downloaded: long mode), `AGE-RESTRICTED` (stop, ask for a file/link), `Sign in to confirm` / `NO METADATA` (repeat with a new NAME, up to 3 times, then tell the user), `LIVE` (ask again after it ends), `LIMIT REACHED: kernel ... still QUEUED` (repeat). `$ST` = output of `python3 .claude/skills/clips/scripts/download/stream_folder.py "Title"` = `streams/<YYYY-MM-DD>_<slug>`; `$WORK` is a folder OUTSIDE the repo.

Step 4: read `candidates.md` and the transcript of every strong candidate; set start/end so the WHOLE story (setup, peak, aftermath) is inside on sentence boundaries; look at 3 frames of doubtful ones. `moments.json` = `[{"start","end","title","hook","description","score"}]`; reject weak ones as `{"start","end","status":"rejected","reject_reason":"..."}` (skipped by `make_clips.py` and `make_highlights.py`, reason kept). Cut ALL good moments. Hooks and titles are real lines from the moment (lesson `quality-not-cringe`), Roman letters for Hindi.

## 3. Normal mode vs long mode

| | Normal (90 min or less) | Long mode (over 90 min, or no captions at any length) |
|---|---|---|
| Download | whole video on a Kaggle CPU kernel (`LONG VIDEO` guard stops anything over 90 min) | NEVER whole (6 h = about 9.5 GB): audio-only, captions, comments, heatmap on Kaggle |
| Entry | steps 2-5 | `long_run.py prepare URL --stream $ST [--zone-minutes 15]` |
| Pick | `find_moments.py` | read `docs/candidates.md` (top 30-60); `long_run.py text --from S --to E`; `long_run.py select --stream $ST --top 10` (or `--ids c3,c7`, `--after S`, `--before S`) |
| Video | one file | `long_run.py fetch-windows --stream $ST` (1080p sections, 10 per Kaggle call, stream-copy cuts, frame-identical, clip +-8 s padding, about 0.65 MB/s) |
| Render | `make_clips.py` | `long_run.py render --stream $ST --batch 10 --skip-done [--facecam NAME --destinations a,b]` |
| State | `docs/moments.json` | same file, status `pending, selected, fetched, taken, rejected`, so "next 10" never repeats; `long_run.py status` prints the next command (every command prints `NEXT:`) |

Long-mode rules: every wait is DETACHED and REGISTERED (section 9); `trim.start` may move at most 4 s before its window start; keep window files (gitignored, `streams/<s>/source/windows/`) while edits may come, because `edit_clip.py` re-renders from them (`render --delete-windows` removes them). Highlights from a video over 90 min are NOT built (they need one whole-file source).

Measured on the 625-minute GamerFleet stream (`streams/2026-11-16_gta-v-marathon-stream-gamerfleet`, 37,492 s, Hindi, past live stream, YouTube captions used):

| Item | Value |
|---|---|
| `prepare` kernel | 544.7 s: install 13, info 5, comments 6, captions 11, audio 59, moment finder 448 (446 s is ffmpeg audio decode); audio 272 MB; kernel RAM 336 MB |
| Signals | no heatmap; 233 comments (15 timestamped); captions hi-orig 43,048 words |
| Candidates | 702 ranked, 300 kept, 42 zones of 15 min |
| Windows and clips | 2 fetch-windows calls (10 + 5); 15 clips taken, 285 candidates still pending; 2 outputs each (youtube-shorts, instagram-reels) |
| Render per clip (both outputs) | 98-142 s in the first run; retro F4 records 264 s when identical outputs were each encoded; 51-66 s in the last run (identical outputs encoded once, then copied). Previews about 37 MB per output |
| vs the earlier 6 h estimate | prepare 8-12 min (real 9.1 min for 10.4 h); audio 170 MB (real 272 MB, longer stream) |

Real losses (the retro's "0 s lost" only covers the last 2 clips because journal hooks arrived mid-job): about 1.5 h when the plain background `fetch-windows` waiter died while the kernel had finished (fixed by `jobs.py`); a first render stopped at 3/15 clips with "No space left on device" and left two half-written clip folders (fixed: `disk-free` check, `.part.mp4` ignored); `long_run render` reported "6 clips failed" for clips that rendered because the folder carries the snapped start (fixed by slug match).

## 4. Moments (what is picked and how)

`find_moments.py` ranks 40-55 s windows from independent signals (each 0-1; weighted mean of the PRESENT signals, renormalised). Weights: `scripts/moments/weights.json`.

| Signal | Source | Weight |
|---|---|---|
| heatmap | YouTube "most replayed" in `info.json` (100 coarse bins, often absent) | 0.35 |
| audio | ffmpeg 8 kHz mono, 0.5 s hop: loud + sudden rise | 0.25 |
| reaction_words | `scripts/moments/reaction_words.json` (Hindi/Hinglish; English list untested on a real English stream) | 0.25 |
| speech_rate | words per second | 0.15 |
| comments | timestamps like "12:34" in comments, by likes (long mode) | 0.20 |
| external | picks via `--external picks.json` | 0.30 |

Windows start/end on sentence/pause boundaries (never mid-word), 1.5 s lead-in, max 20% overlap; every zone's best is listed (lesson `never-skip-moments`: report windows NOT CUT). `candidates.md` = transcript of each top window plus per-signal scores. No LLM, no key; about 20 s for 32 min.

**Visual moments (step 3b, `moments.visual` default on).** `visual_scan.py` decodes at 2 fps (about 60 s per 30 min of 1080p), computes per-5 s energy (scene cuts, motion, spike, flash, webcam motion when `--cam-box` or `stream.json` `webcam_box` is known) and builds about 14 contact sheets (12 frames, time burned in). A vision sub-agent (Haiku default; Sonnet on request or after two failed apply checks; prompt `.claude/skills/clips/docs/visual-review-prompt.md`) scores each window 0-10 into `docs/visual/reviewer_raw.json`; `visual_review_apply.py` validates (never repairs); `merge_moments.py` writes `docs/moments_merged.json` (NOT `moments.json`, which `make_clips.py` cuts entry by entry). Rules: both agree (transcript >= 0.40 and reviewer >= 6) = top; one strong (transcript >= 0.50 or reviewer >= 8) = kept with a note; visual-only window added only at reviewer >= 7; a reasoned rejection (score <= 3) DEMOTES, never drops; no visual files or `moments.visual=off` = old order exactly; `--write-moments` only adds transcript_score, visual_score, agree, notes. Cost about 23,000 content tokens per 30 min. Energy alone is weak (Spearman 0.12 vs the reviewer); the reviewer carries the signal. Long mode scans only fetched windows (`--windows-dir`).

**Snapping.** `make_clips.py` (default `--snap`) runs `moments/snap_edges.py` before building a clip: `ffmpeg scdet` (threshold 6) on a 12 s window around each edge (about 3 s per edge), moves the edge to the nearest scene cut within 2 s, never inside a spoken word, never outside 40-55 s; writes `docs/snap.json` and `snapped_from`. No cuts = edges unchanged.

## 5. clip.json = the single source of truth; the edit loop

Each clip folder `streams/<stream>/clips/<start>-<end>s_<slug>/` holds `clip.json` (all settings, repo-relative paths), one `<output>.mp4` per destination, `poster.jpg`, `post.md` (generated from `clip.json` `post`), `edit-notes.md`, `versions/`. Top keys: `id, source, source_offset, transcript, trim{start,end}, title, description, score, outputs[], layout, hook, captions, zoom, facecam, animations, audio, output, rights, post`. Schema/validation: `scripts/clip_schema.py` (one-line error naming the key; nothing saved on error). Render: `scripts/render_clip.py`, ONE ffmpeg pass from the source (trim, fit layout, zoom, captions, title, facecam).

```
python3 .claude/skills/clips/scripts/edit_clip.py CLIP.json key=value [key=value ...] [--note "why"] [--render] [--output NAME]
python3 .claude/skills/clips/scripts/edit_clip.py CLIP.json --undo --render      # one version back; repeat for more
python3 .claude/skills/clips/scripts/edit_clip.py CLIP.json --version 2 --render
python3 .claude/skills/clips/scripts/edit_clip.py CLIP.json --history
```
- Relative forms `'trim.start+=-2'`, `'trim.end+=3'`; list append `'zoom.plan+={...}'`; single-quote values with spaces/braces. When `trim.start` moves, `zoom.plan` times shift to stay on the same source moment.
- Each run saves `versions/vN.clip.json` (v1 = file before the first edit) and a line in `edit-notes.md`. Undo/restore is itself a new version; nothing is lost.
- `--render` re-renders EVERY output (about 30-60 s per clip on CPU), refreshes `streams/index.json`, `LATEST.md`, `post.md`, and calls `checkpoint.py`.
- No source on the machine (fresh clone): `--render` is refused BEFORE a version is saved and prints the re-fetch commands (download again, copy to the `source` path of `clip.json`, repeat). Long mode: `long_run.py fetch-windows` again, or `backup_sources.py restore`.
- User words -> keys: `CONTROLS.md` (about 70 rows). Examples: "start 2 s earlier" `'trim.start+=-2'`; "captions on" `captions.on=true`; "no facecam" `facecam.on=false`; "old layout" `layout.profile=classic`; "louder" `audio.target_lufs=-12`.

## 6. Look of a clip (defaults and keys)

| Thing | Default (`defaults.json`) | On request |
|---|---|---|
| Layout | `safe-c`: game picture y 456-1064 (16:9 whole, never cropped), blurred bars, title in the top bar, facecam 300 px 4:3 rounded at x 40 y 1250-1475, nothing in the bottom 384 px or right 162 px (app buttons) | `classic` (game centred, facecam bottom-right); `layout.game_shift_extra=70` clears the top app button (offer once) |
| Title (`hook`) | static editorial: Playfair white, no box, soft shadow, at most 2 lines, one italic word (`hook.emphasis`), auto-contrast (luma above 150 adds a dark scrim, still under 4.5:1 turns charcoal); `hook.y` 0.12 (safe 0.12-0.17, bigger = lower), 4 s | `hook.style=pill`; `hook.animation=reveal` |
| Captions | OFF. On: `minimal`, 3 words, small, low, never over game/facecam/hook (engine refuses), Roman Hinglish via `scripts/captions/roman_map_hinglish.json` (missing words print "NOT IN ROMAN MAP" and stay Devanagari). Styles minimal, hormozi, clean, oneword, pill, lime. Check `check_layout.py CLIP.json --pixels` = PASS | `captions.on=true` |
| Zoom | subtle auto punch-in `zoom.amp` 0.07, ease in/hold/out; pointed-at targets via `zoom.plan` / `zoom.on_words` | `zoom.amp=0.15`, `zoom.auto=false` |
| Animations | OFF (`animations.on false`, no progress line, no events) | `hook.animation=reveal animations.on=true animations.progress_bar=true`; events only after the user agrees |
| Audio | two-pass `loudnorm` -14 LUFS / -1.0 true peak (aim 0.4 lower for AAC), 48 kHz | `audio.target_lufs=-12`; `null` = off |
| Length | 40-55 s whole story (warns outside; shortest 3 s) | longer/shorter only if the story needs it |

**Facecam library** (`.claude/skills/clips/assets/facecam/library.json`): a fictional AI-generated girl (lesson `facecam-ai-generated-only`: only AI-generated or consenting people). Default `girl_watching_10s` (calm, no audio). `audio_usable` reactions: `girl_surprise_10s`, `girl_impressed_20s`, `girl_hype_10s`, `girl_disbelief_10s`, `girl_laugh_10s_patched` (she speaks ENGLISH only, even over a Hindi stream). `girl_gemini-app_10s/20s` are the first takes; `girl_laugh_10s` has no audible laugh. Add one: `python3 .claude/skills/clips/scripts/add_facecam.py FILE NAME --ai-generated [--default]`, read `assets/facecam/NAME_sheet.png`, rerun with `--focus fx,fy --tight 0.9 --calm a,b --segments '{...}'`. The images in `assets/facecam/reference/` are photo-real: keep the repo private. Voice: `facecam.voice=off|low`; `low` plays her library line ONCE about 0.4 s after the loudest stream peak, lip-synced, `facecam.voice_gap_db` under the stream (6-24, default 15, lower = louder; the user found a strong voice AI-sounding), mixed before loudnorm, stream never ducked. On the default facecam it is refused and names the usable items: `facecam.voice=low facecam.video=girl_surprise_10s`, then look for "facecam voice low" in the render output. Offer once, only for `social` output.

**Animations (HyperFrames).** Pinned `hyperframes@0.9.52` (Apache-2.0) via `npx --offline`, then `npx --yes`; Node 22; the first run downloads npm packages and a Chrome (about 2 GB). Presets in `assets/animations/`: `title-reveal`, `callout-ring` (safe-c xy = point of the game picture, x 0-1080 y 0-608), `lower-third-tag` (default `[40,1150]`), `impact-burst`, `progress-bar`; highlights use `hl-title, hl-tag, hl-ring, hl-burst, hl-meme`. Overlays render once to a transparent WebM cached in `streams/<s>/docs/cache/` (gitignored): first clip render 1-2 min, cached about 45 s. If HyperFrames cannot run, the animation is skipped, never the clip: one WARNING, last line `ANIMATION SKIPPED`, exit 0, and you MUST tell a user who asked. Propose 0-3 events per clip in step 0; add only agreed ones. gsap 3.15.0 is vendored in `assets/animations/_lib/gsap.min.js` (GreenSock standard licence).

## 7. Destinations (profiles in `.claude/skills/clips/destinations/`)

| Name | Facecam | Notes |
|---|---|---|
| `social` (default output name) | the clip's own setting (with her) | |
| `youtube-shorts` | yes | up to 3 min, vertical/square (verified); ours stay 40-55 s |
| `instagram-reels` | yes | stay at 90 s or less (official page unreadable, figures conflict) |
| `clean` | no | for clipping sites; the STREAMER'S OWN webcam stays (user decision 2026-11-16) |
| `whop-content-rewards` | no | `verified:false`: rules are per campaign behind a login; renders as `clean` with a warning until the user pastes a brief and the file is filled |
| `youtube-highlights` | no | 16:9 highlights type, commentary required |

`--destinations a,b` writes one named mp4 per destination from the SAME clip.json. Scripts use only `facecam` and `fps` of a profile (`clip_schema.output_for_destination`); `min/max_seconds`, `audio_lufs`, `captions`, `title`, `credit_line_required` are notes for the human. Never guess a site's rules.

## 8. Highlights (one 5-6 min 16:9 video)

For "highlights" instead of clips; needs the WHOLE source as one file (90 min or less).
```
python3 .claude/skills/clips/scripts/make_highlights.py streams/<stream> --minutes 5-6 --video $WORK/dl/video.mp4 [--moments 12] [--order story|score|time] [--titles FILE]
python3 .claude/skills/clips/scripts/commentary/make_commentary.py $S $H [--en-vtt EN.vtt] [--source VIDEO]   # writes commentary-script.md; the LEAD fills the `- at: | text:` lines
python3 .claude/skills/clips/scripts/commentary/make_commentary.py $S $H --ingest
python3 .claude/skills/clips/scripts/commentary/tts.py $H            # Kokoro af_heart on CPU; first time: tts.py --setup
python3 .claude/skills/clips/scripts/render_highlights.py streams/<stream>/highlights/<slug>
python3 .claude/skills/clips/scripts/edit_highlights.py HL OP ... --render
```
- Defaults: animations ON, captions OFF (refused), facecam OFF, gameplay whole, order `story` (2nd best opens, best closes), automatic "crazy editing" (zoom punches, hits, risers, speed ramps, one freeze, transitions slide/zoom-punch/flash/wipe/glitch/fade/cut), original synthesised sfx (`assets/sfx/*.wav`), Anton meme text (OFL). Write real chapter titles in Roman letters, else "Moment at M:SS".
- Commentary (required for YouTube monetisation): the lead writes 0-2 English lines of 6-18 words per segment (about one per 25 s plus intro/outro), Kokoro voices them, peak about 7 dB under the stream's loudest speech (`commentary.level_db -7`), stream ducked at most 4 dB (0.2 s attack, 0.4 s release) only while a line plays, mixed BEFORE the loudnorm. Missing, the render warns `no commentary: not suitable for YouTube monetisation` and post.md says so.
- Output: `preview.mp4` 1080p30, x264 medium, CRF 21 under a size cap (`output.size_cap_mb` 85), -14 LUFS / -1 dBTP; upload preset = source fps up to 60, CRF 17 in `masters/` (about 300 MB). `preview.mp4` is local only (gitignored, 80 MB per render): send it with SendUserFile, never delete it. One early preview is still tracked in git.
- Measured (32 min Hindi test stream, 4 CPUs): 12 segments, 5:56, 79.4 MB, -14.2 LUFS / -1.1 dBTP; `make_highlights` 59-66 s; first full render about 11.5 min; one changed segment re-renders only it plus the final pass (about 6 min). HyperFrames sometimes cancels under load: 3 retries, then the overlay is skipped with a warning.
- UNPROVEN: nobody has watched/listened to the whole video (pacing, effect taste, her voice level are the user's call); steppy `speed_ramp` on the 60 fps upload unless `interp: mci`; facecam corners other than top-right; a second or English stream.

## 9. Saving work, long jobs, self-improvement loop

| Script (`scripts/`) | What it does |
|---|---|
| `checkpoint.py` | after EVERY render step commits ONLY safe files (clip.json, post.md, edit-notes, versions, poster, preview mp4 up to 95 MB, docs/*, LATEST.md, streams/index.json) and pushes the CURRENT branch `ccr-*` (5 tries, merge on rejection, never force). Refuses a file over 95 MB or key-like text. Failure prints `WARNING NOT SAVED TO GITHUB`, never stops a render. `--scan FILE...` lists key-like files |
| `finalise.py --stream streams/<s> [--yes]` | dry run, then ONE squashed commit `clips: <stream>, <n> clips (final)` on top of origin/main (fast-forward, never force); stream content reaches main ONLY this way. `--sync-docs` (called by `.claude/scripts/autosave.sh`, which the lead runs by hand) puts non-stream files on main. Refuses if main changed from another branch (`--accept-main-overwrite` only with the user's OK) |
| `jobs.py` | registry `streams/<s>/docs/jobs.json`. `tick` = FIRST action of every turn while a job is open (idempotent, free; fetches a COMPLETE kernel nobody collected; ALERT + RESUME for a lost job; `--wake` counts wakes, max 12); also `check`, `list`, `resume`, `run --stream S --kind K -- COMMAND` |
| `journal.py` | `docs/journal.jsonl` written by code; the lead adds `journal.py note user_correction "TEXT" --stream $ST` / `agent_error`, and brackets manual steps with `start/end --step moments` |
| `retro.py` | step 9: builds `docs/retro.md`; each finding needs exactly one disposition `lesson: ID` / `check: WHAT` / `doc: PATH` / `backlog: WHAT` / `none: REASON`; `--set F2 "..."`, `--add "..."`, `--check` |
| `preflight.py` | step 0 PASS/WARN/FAIL + one-line FIX: kaggle, ffmpeg, python-libs, node (WARN), disk-free (5 GB), git-remote, autosave-pause, jobs-tick, settings-allow (WARN), docs-paths, stream-writable, facecam-layout, incidents, audit-due |
| `audit_due.py` | AUDIT DUE at 5 retros, an incident at count 2, or 15 new lessons; ask the user first |
| `backup_sources.py` | optional private Kaggle dataset `clips-sources-<stream>` for source windows, ONLY on request |

Backstop (lesson `tick-first-during-jobs`): when a job starts arm `send_later` at ETA + 10 min (prepare about 2 min + 1 min per hour of video, fetch-windows about 10 min, Whisper up to 60 min) saying "jobs.py tick first, then continue"; re-arm every 15 min; 12 wakes max, then tell the user. Monitor on the log is the fast path only; never rely on ScheduleWakeup/Cron surviving a restart. Container lost: clone, `git checkout ccr-...` (branch named in `LATEST.md`, or newest `git branch -r --sort=-committerdate`), `jobs.py check`, run the printed RESUME line (`--resume-call N` re-attaches to an existing kernel, no new quota), re-fetch windows. The incident table is in KNOWLEDGE-BASE.md. Guardrails: the loop never edits settings, hooks, keys or permissions (it prints the change for the user), never force-pushes; one improvement = one small commit.

## 10. Quality: previews in git, masters outside git

- `output.preset=preview` (default): 30 fps, x264 veryfast, CRF 20, AAC 160k, `+faststart`; goes to git.
- `output.preset=upload`: source fps up to 60 (never above the source), x264 slow, CRF 17, AAC 192k, 1080x1920; about 100 MB per 45 s and slow; writes `<clip dir>/masters/<output>_upload.mp4` (gitignored, NEVER committed; GitHub refuses over 100 MB). Default master storage: a private Kaggle dataset `clips-masters-<stream>`, uploaded ONLY when the user asks (commands in SKILL.md section "Quality"). `streams/index.json` does not list masters.
- Source resolution: 1080p H.264 cap by default (4K only helps zoom-ins and decodes 3-6x slower); a source under 1080 px warns. 21:9 and 9:16 sources are not handled.

## 11. Kaggle and Whisper

- Kaggle CPU kernels do ALL YouTube access (names `os-dl-*` download, `os-lp-*` prepare, `os-lw-*` windows, `os-lh-*` Whisper T4). Env names (set in environment settings, never chat): `KAGGLE_USERNAME`, `KAGGLE_APITOKEN`, optional second account `KAGGLE_USERNAME2`, `KAGGLE_APITOKEN2`. `python3 .claude/skills/clips/scripts/download/kaggle.py check` shows both accounts (user names only).
- Two accounts, 30 GPU h/week each. Account 1 is the default and runs all CPU work. Account 2 (`sovere`) runs a GPU kernel only after account 1 stays QUEUED over 20 min or hits a quota error; then the whole windows+Whisper chain moves (recorded in `stream.json` `long.account`). A chain stays on ONE account; `--account 1|2` forces. Any call on a chosen account goes through `kaggle.py --account 2 raw <cli args>` (token only in the child process, output masked). Agents never read the key or the key file. A kernel QUEUED over 20 min is deleted and counts as a failed try; limits rule: 3-4 tries, then `LIMIT REACHED ... Ask the user:`; never lower quality.
- **Whisper findings (2026-11-15, one Hindi reaction stream).** CPU Whisper for Hindi: small unusable, medium RTF 5.5 and worse than captions: never. T4 turbo batched 16: 21% exact, loops, 60 s segments. Best config, now the default: `large-v3`, batched 8, VAD min silence 500 ms, chunk 20, temperature fallback, forced language: 65% exact / 75% fuzzy in tuning, 66% / 77% in production (first 30 s of 3 windows vs YouTube `hi-orig` captions), 0 loops, about 78 s for 3 windows. Still under the 80% parity gate. Flaws: speech dropped at window starts, segments up to 54.7 s, bad word timings (so word times cannot drive captions or snapping), English words in Latin script. Auto language detection said English (0.997) and even TRANSLATED Hindi. So: YouTube captions ALWAYS when they exist (Hindi captions write English words in Devanagari: normal); Whisper only without captions (always for Twitch); tell the user first ("This video has no captions. The Whisper transcript is weak for Hindi ... Go on, or give another link?"); `fetch-windows` STOPS until repeated with `--accept-whisper`; ALWAYS `--lang hi` (or `en`), refused on a Hindi stream without it. Untried: vocal separation (demucs), WhisperX alignment, a Hindi fine-tune, VAD `max_speech_duration_s` about 15.

## 12. Rights and policy (tell the user plainly)

- YouTube reused content (read 2026-11-15): clips "edited together with little or no narrative" are the named risk, it applies EVEN WITH the streamer's permission, and monetisation can go from the WHOLE channel. Real commentary is the safe side. Every `post.md` carries this warning.
- Rockstar/Take-Two: footage tolerated for NON-COMMERCIAL use ("you don't make money through the footage"); a monetised channel or paid campaign is outside it (tolerance, not permission); route = licence request to copyright@take2games.com. No leaked footage; isolated cutscenes and in-game TV/comedy shown alone are flagged. Credit and "no infringement intended" give no cover; fair use is a court decision. Mute game/trailer audio; keep claimed Shorts at 60 s or less.
- NO evasion edits (flip, mirror, pitch, speed, filters), ever (lesson `no-copyright-evasion`). Plan only, not built: the user uploads a private test, reads YouTube Studio "Checks", we record it in `streams/<s>/docs/rights-checks.md`.
- `rights.status`: `private-test` (default), `permitted`, `commentary`. Every post kit has a credit line (streamer + source link). The streamer's rights apply on top of the game's. Whop/Vyro/ClipFarm clipper rules are not public: ask for the campaign brief. Age-restricted video: stop, never a bypass.

## 13. Known limits, UNPROVEN, backlog

- Run on real streams: one Hindi reaction stream (32 min) and one 10.4 h Hindi marathon (captions). NEVER run: English stream, Twitch (VOD links accepted, clip links not; no heat/chat), 4K or 21:9 source. The repo records no result of the planned v1 phone review (3 clips per link, one fix round, freeze).
- Long mode ran with captions only. UNPROVEN: Whisper on a long stream; visual step 3b on long-mode windows (GamerFleet has no `docs/visual/`); container-loss resume in real life; `--resume-call` on the Whisper chain; `backup_sources.py` upload; account-2 move in real use; a fresh machine (npx cache, Chrome, Kokoro install, Kaggle CLI); Haiku as visual reviewer (thresholds fitted on one stream, webcam box set by eye).
- English reaction-word list is weak; the Hinglish Roman map is incomplete (clip 1: 44 words missing in 25 caption lines); `roman.py` from PeakCut was recommended but is NOT in the repo. Facecam: no lip-sync except the one library line; the patched laugh awaits an ear check.
- Generated, do not hand-edit: `streams/index.json`, `LATEST.md`. Local only (not in git): `streams/*/source/`, `masters/`, `docs/cache/`, window files, `.npz`.
- Backlog (statuses corrected against SKILL.md; PLAN.md was stale on the first two; its other three stale lines (validation "fixes in progress", "a real 5-6 h link", Whisper turbo) were fixed on 2026-11-16): highlights video + Kokoro commentary = BUILT. Per-clip effects layer (meme text, ramps, transitions for clips) = NOT built (exists only in highlights; lesson `edit-effects-on-request`). Not built: timed reactions (several lines of hers on beats), chat-activity moment signal (spike minus about 20 s; needs a past-live chat replay or Twitch VOD chat), comparison videos (Vice City vs GTA 6; commentary required, per-source rights), destination rules from real campaign briefs, YouTube claim-check log, lip-sync on a T4, Hinglish Whisper fine-tune / demucs / WhisperX alignment, SmolVLM / Florence-2 / YuNet helpers, trained highlight scorer (needs 10-20 streams; store `docs/training/`), Auto-Editor (podcast profile), a site reading `streams/index.json`, Pexels B-roll, `hook.style=card`, title-candidate writer, review page, language detection, rights gate on export. UNVERIFIED facts: Instagram Reels length, Rockstar page date, GTA VI release date (`.claude/skills/clips/docs/destination-rules.md`, `.claude/skills/clips/docs/rockstar-policy-and-comparison.md`).
