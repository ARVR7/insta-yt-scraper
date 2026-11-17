# HISTORY AND REQUIREMENTS: what we built, why, and everything the user asked for

Written 2026-11-16 by the old Claude account's lead session, from the session record. The repo is the source of truth for detail; this file is the story and the list of requirements, so the new Claude understands the intent behind every choice. Keys are never in this file.

## 1. The one-paragraph summary
The user runs a clipping channel. They turn long streams (YouTube now, Twitch later), mostly English or Hindi/Hinglish gaming streams and gameplay, into vertical 9:16 clips (and now 5-6 minute 16:9 highlight videos). The deliverable is ONE skill, `clips` (`.claude/skills/clips/`), that takes a stream link and produces all the good moments as complete 40-55 s clips, every aspect of which can be edited afterwards by saying the change. It must run in a fresh Sonnet session. Haiku sub-agents run fixed-command steps; Opus is only an advisor; Fable plans, orchestrates and validates, and never generates video. A companion skill, `lessons`, records every preference, rule and mistake so each run is better than the last.

## 2. Timeline
| When | What happened |
|---|---|
| 2026-11-10..13 | Exploration: compared clipping tools (OpenShorts, others; `tool-comparison/` was later removed), tested a 32-minute Hindi stream ("This is not a game", GTA 6 reaction). Found: YouTube blocks the VM, so all YouTube access runs in Kaggle CPU kernels; Hindi CPU Whisper is unusable. |
| 2026-11-14 | Built the clip engine: `clip.json` as the single source of truth, `edit_clip.py` (versions, undo), one-ffmpeg-pass renderer, layout "safe-c" (user chose option C), static editorial title, facecam of an AI-generated streamer girl, captions off by default, subtle zooms plus pointing zooms, the moment finder (transcript, loudness, reaction words, replay heat), post kits, `LATEST.md`. Three published test clips. |
| 2026-11-14..15 | Facecam library: six verified reactions (the user generated them in the Gemini app; `facecam.voice` later), patched laugh. Voice research (Maya1, Kokoro, Qwen3-TTS) and two voice demos; the user found the voice too strong and AI-sounding, so voice became optional and quiet. Destinations became profiles. Rights research (YouTube reused-content policy, Rockstar's non-commercial policy). |
| 2026-11-15 | **Long mode** for 5-6 h videos ("Yes it has to be put!"). Quality upgrades: preview vs upload preset, two-pass loudness (-14 LUFS), scene-cut snapping. Repo restructured to `.claude/` + `streams/`. **Git history cleaned** (1.5 GB to 205 MB; every blob over 25 MB removed; force-push approved by the user). Three Fable validations (26 gaps, then 14, then the visual step), each followed by Sonnet/Haiku fix rounds. Whisper on the Kaggle T4 measured worse than captions for Hindi; tuned from 21% to 66% word match; captions stay preferred. A second Kaggle account (`sovere`) was verified and wired in as a GPU fallback. **Highlights** type (16:9, commentary with Kokoro, ducking) built. |
| 2026-11-16 | **Visual moment finder** (frames plus transcript, idea from the claude-video skill) built and validated. **Real job:** "GTA V Marathon Stream" (GamerFleet, 625 minutes): long mode, 15 clips for YouTube Shorts and Instagram Reels, merged to `main` (commit `439b38f`). Incidents (lost detached wait, disk full, false failure status, double encode) led to the safety and self-improvement systems: `checkpoint.py`, `finalise.py`, `jobs.py`, `journal.py`, `retro.py`, `preflight.py`, `incidents.json`, `audit_due.py`. Migration to a new GitHub and Claude account requested: this folder. |

## 3. Every requirement the user stated (grouped; quotes are the user's words)
### Product
- One skill that takes a stream link (YouTube now, Twitch later) and produces all the good moments as complete 40-55 s vertical clips. "Find ALL the best moments."
- Every aspect editable afterwards by saying it: "I hope the skill has option to edit the clips based on our expectations and you are using good tools for that." Re-render in about a minute; versions and undo.
- The skill must be usable in a fresh chat session, run by Sonnet; Haiku for simple steps; Opus advisor only; token efficiency matters.
- "5-6 hrs long: how will you deal with it?" then "Yes it has to be put!": long mode in v1. Then a real 10 h 25 min video worked.
- "Give me 15 clips outta this": N clips on demand, spread across the whole video.
- Highlights: "short videos like 5 6 mins of snappy highlights for YouTube with crazy editing and the format would be normal 16:9 with 1080p resolution, even the clips I am expecting to be best in resolutions."
- Comparison video (Vice City vs GTA 6, top and bottom): requested, **not built** (backlog), with rights gating.
- Chat-spike moment signal (live chat replay; start 20 s before the spike): requested, **not built**.
- An edit-effects layer (transitions, meme text, freeze-zoom, speed ramp, glitch, flash, sound effects, reaction cutaway): partly built inside highlights; for clips it is backlog.
- Reaction-timed facecam (reactions matched to each moment): backlog.
### Look
- Gameplay always whole, never cropped or split. Layout C: game picture up, small rounded facecam of the AI girl lower left, above the bottom 20% app zone. The facecam "a little bit lower" (user asked).
- Captions off by default; minimal and low when on; Roman Hinglish. Static editorial title by default; animations only for highlights or when asked: "The animation is good, but not to be applied on the default video, maybe good for highlights when specifically asked."
- Subtle zooms that hold while the topic is discussed, and a zoom to what he points at.
- The streamer girl is a cute AI-generated Asian girl (the user chose her), speaks **English only**: "I don't want our streamer to speak Hindi she should keep english". She is mostly a passive reaction: "I want her passive reactions and maybe voice but not overpowered voice just mixed with normal voice of the stream" (voice is optional and quiet; default 15 dB under; tweak only when asked).
- For sites other than Instagram and YouTube there may be no streamer reaction at all: the `clean` profile. Clean keeps the stream's own webcam: "Yes, just don't add reaction streamer, rest everything can be there including animations if requested."
- Commentary (highlights): not the user's own voice; human-like, proper flow, not AI-ish; a girl's voice, English; mixed under the stream.
### Quality and process
- Upload preset: source fps up to 60, x264 slow crf 17, 192k AAC, -14 LUFS, -1 dBTP, never upscale; 4K only for chosen windows on request; masters outside git.
- "If you hit certain limitations let me know after 3 4 retries, don't invent something that would compromise the quality."
- "Once done with everything, run a fable agent to validate the entire plan skill pipeline. You don't need to generate videos. Just verify everything and using sonnet/haiku subagents fix the gaps." Then re-verify.
- "Make sure the agents are running properly."
- "I keep getting new ideas and I prefer everything being perfect so I tend to over cook things. Once things are ready we would run a final check but I want a good quality content. Which can be customisable."
- "Push all things to main also in intervals"; "Find ways in which you never lose the clips, maybe push things directly on GitHub branch and to main once finalised. Otherwise our time would be wasted"; "Make a note of it and improve next time. I want you to improve every time. Like a self learning loop."
- "Use whatever best things you can from the above tools (WhisperX, PySceneDetect, Auto-Editor, Remotion, FFmpeg) ... and better local models if available"; PeakCut repo check; claude-video skill: use it in parallel with the transcript to find moments and consult both.
- Compute: CPU first on the VM; the Kaggle T4 is allowed within 30 GPU hours a week per account, with the repo or CPU as fallback; two Kaggle accounts are available.
### Rights and posting
- Destinations as profiles with a post kit per clip (`post.md`): YouTube Shorts title/description/tags, Instagram caption, credit line, rights notes. Whop and similar sites: rules are per campaign behind a login; "We would have to find that" (not verified).
- "Also find out ways we can do something to edit the things to make it copyright free": answered honestly as no evasion filters; what is allowed is commentary (transformative layer), permission, and the platforms' own rules; recorded in `.claude/skills/clips/docs/destination-rules.md` and `.claude/skills/clips/docs/rockstar-policy-and-comparison.md`.
### Migration (this folder)
- Move everything (repo, pipeline, environment variables, VM setup, instructions, memories, knowledge) to another GitHub account and another Claude account; the new mirror repo should be private; a README that the new Claude can follow to have everything set up and running, "100%". Other repos and the platform channels (Instagram, YouTube) are out of scope.

## 4. Decisions and why (the short version; full list in `lessons/`)
| Decision | Why |
|---|---|
| All YouTube access in Kaggle CPU kernels | YouTube blocks the VM; the bot check hits about half of kernel starts, so retry up to 3 times, never use cookies. |
| YouTube auto-captions preferred over Whisper | Captions give word times for free; Whisper (T4, large-v3 batched) measured 66% exact / 77% fuzzy word match vs captions on Hindi, with long segments and bad word times. |
| Long mode fetches only chosen windows (about 35 MB each) | A 10 h stream is about 16 GB at 1080p; never download it whole. |
| Preview in git, masters outside | GitHub refuses files over 100 MB; history stays small. |
| Stream clips reach `main` only via `finalise.py` | Every re-render is another blob; main gets one squashed commit with only final files. |
| `clip.json` is the single source of truth | Every edit is a key=value change plus re-render, with numbered versions and undo. |
| Highlights preview.mp4 is not committed | 80 MB per re-render; delivered with SendUserFile. |
| One encode for outputs with identical settings | Halved the render time (youtube-shorts and instagram-reels are identical). |
| Visual moment finder is an additional signal, never a replacement | Energy alone was weak (Spearman 0.12 vs the reviewer); the reviewer reading frames next to the transcript adds value; absent the visual step the old order is unchanged. |
| The lead runs account-2 and GPU steps itself | Sub-agents are refused by the auto-mode classifier for those calls. |

## 5. Incidents (what went wrong and what now prevents it)
| Date | Incident | Prevention now |
|---|---|---|
| 2026-11-14 | Agents died silently while reported as running | Check file activity and process lists; never trust silence |
| 2026-11-15 | 5-hour usage limit killed several agents | Wait for reset, resume with SendMessage |
| 2026-11-15 | A script overwrote a lesson file with placeholder values | Lesson `read-before-write-same-file`; add_lesson reads before writing |
| 2026-11-15 | Auto-commit swept in a disposable cache | `docs/cache/` in .gitignore |
| 2026-11-15 | Disk full (817 MB free) stopped HyperFrames | Clean scratch dirs; preflight disk check |
| 2026-11-15 | Whisper on the T4 stayed QUEUED for 20 min, three times | `kaggle.py wait` stops after 20 min queued, deletes the kernel, retries; account 2 takes over |
| 2026-11-15 | Sub-agents refused by the auto-mode classifier (second Kaggle key, GPU runs) | The lead runs those steps; key access only through `kaggle.py raw` |
| 2026-11-16 | A plain background wait died while idle; 1.5 h lost on the 10 h stream | Detached jobs with an EXIT line; `jobs.py tick`; job registry |
| 2026-11-16 | Disk full mid-render: 12 clips failed, two clip folders half written | Preflight disk check; `.part.mp4` ignored when judging "done" |
| 2026-11-16 | Render status said "6 clips failed" for clips that rendered (folder name carries the snapped start) | Match clip folders by slug and a start within 4 s |
| 2026-11-16 | Identical destinations encoded twice | Encode once, copy |

## 6. Numbers worth knowing
- Clip render: about 50-60 s of CPU per 45 s clip (4 CPUs); about 10-15 minutes for a 6-minute highlights video. The first 15-clip job: 15 windows fetched in 769 s; 15 clips rendered in about 40 minutes of wall time including a disk-full restart.
- Long mode on the 625-minute stream: pass 1 (info, comments, captions, audio-only, moment finder) took 544.7 s on Kaggle (545 s); 300 candidates in 42 zones; 15 windows downloaded in two Kaggle calls.
- Whisper T4: model load 19 s, about 78 s for 3 windows of 4 minutes (large-v3 batched).
- Clip files: 7-43 MB each at preview preset (30 fps, CRF 20); loudness -14.0 to -14.5 LUFS; true peak -1.0 to -1.5 dBTP.
- Repo: about 205 MB right after the history clean (before the GamerFleet job). `main` holds 30 GamerFleet clip files (15 clips x 2 destinations; the two files of a clip are byte-identical, so git stores each blob once) and 52 `.mp4` files in all. The work branch `ccr-*` is larger (a local `.git` was about 819 MB on 2026-11-16) because it keeps every intermediate render by design; a mirror of `main` plus the newest `ccr-*` branch is the recommended copy, and 9 blobs over 30 MB (final clips, one 79 MB highlights preview) exist in history on purpose.

## 7. What is proven and what is not
**Proven on real data:** the clip engine and edit loop (Hindi stream, 32 min); long mode on a 10 h 25 min Hindi stream (captions present); highlights from the 32-minute test stream; the Whisper T4 path; the two-account GPU fallback by mock and one real account-2 check; the 15-clip job end to end.
**Not proven:** an English stream; Twitch (prepare accepts a VOD id, never tried); 4K sources; a highlights video from a source over 90 minutes (not built: needs a single source file); scene-cut snapping on gameplay with few cuts; the Haiku reviewer for visual moments (Sonnet did it); the `send_later` wake-up and the hooks inside a real render beyond one job; setup on a brand-new machine (cached tools here); a real container loss and resume; Whop rules.

## 8. Open items at the time of the move
- The user's review of the 15 GamerFleet clips (post kits are drafts; titles/descriptions not polished).
- Optional: visual second-opinion check on those windows; 5 reserve moments and 285 further candidates are ready for "next 10".
- The user to listen to the quiet-voice and commentary demos (`.claude/skills/clips/docs/voice-samples/`) and say if the level is right.
- Backlog (v1.1/v2): comparison video, chat-spike signal, timed reactions, effects layer for clips, highlights from sources over 90 minutes, Twitch run, a Whop profile once a campaign brief exists.
