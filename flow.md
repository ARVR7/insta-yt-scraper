# Flow

How a shared link becomes notes and registry entries, and what lives where. Update this file whenever a script, skill or folder is added or changed.

## Entry points

An hourly scheduled task wakes a standing session (`Link Inbox processor`, Sonnet 5.5, repository attached) that runs `process-queue` when open `link` issues exist. Fresh scheduled sessions were tried first and had no GitHub access.

```
Android share sheet -> docs/ web app (GitHub Pages) -> GitHub issue labelled `link` --user asks--> process-queue
Link Inbox page (claude.ai artifact, db collection `links`) --user asks--> process-queue --> process-link (per link)
chat message with a link ------------------------------------------------> process-link
```

The page only queues links and shows results; it cannot run scrapers or wake Claude. `process-queue` reads queued rows with `ArtifactData`, runs the pipeline, and writes status, verdict, summary and the note URL back so the page shows them.

## Pipeline

```
user shares a link  (chat, or the app's issue queue via process-queue)
      |
      v
GitHub Actions: prepare.yml runs prepare_link.py on a runner when the issue is opened -> inbox/<id>/ (Claude's later run reuses it)
      v
prepare_link.py   MECHANICAL, no model tokens (1-3 min)
      |   fetch_instagram.py / fetch_youtube.py -> metadata, caption, video, captions
      |   analyze_video.py -> frames + sheet.jpg, transcript (non-English translated), OCR text
      |   regex candidates (GitHub repos, pip/npm names, URLs, @handles, prices, income claims)
      |   lookups: GitHub raw files (licence, README lines on requirements/limits), PyPI JSON
      |   writes brief.md + draft_note.md; skips links already processed
      v
Claude (the only judgment)
      |   read brief.md (+ sheet.jpg only if flagged), research what the lookups did not cover
      |   categorize per taxonomy.yml, decide usefulness and verdicts
      |   write verdict.json  (title, category, usefulness, key_info, summary, research rows, registry entries)
      v
finish_link.py    MECHANICAL
      |   validates note + taxonomy first, writes notes/<platform>/<id>.md from the draft
      |   adds registry entries (verified / pending / hoax / sidequests), appends decision
      |   build_index.py -> data/library.json, data/taxonomy.json, library/*
      |   regenerates the "Current notes" table below, writes the issue comment
      |   commits and pushes to main with retries
      v
Claude posts the printed comment on the issue and closes it
```

## Repository map

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Tells Claude to use `process-link` for every shared link. |
| `README.md` | Short human intro. |
| `decision.md` | Log of decisions and reasons. |
| `flow.md` | This file. |
| `requirements.txt` | Python deps: instaloader, yt-dlp, faster-whisper, numpy, Pillow. ffmpeg is a system dependency. |
| `scripts/setup.sh` | Installs deps and checks for ffmpeg. |
| `scripts/fetch_instagram.py` | `<url> <outdir>` -> `meta.json`, `video.mp4`. |
| `scripts/fetch_youtube.py` | `<url> <outdir> [--comments N]` -> `meta.json`, `comments.json`, `captions.*.vtt`, `video.mp4`; metadata survives a blocked download. |
| `scripts/analyze_video.py` | `<video> <outdir> [--every N]` -> `frames/`, `sheet.jpg`, `transcript.txt`. |
| `docs/` | Installable web app (GitHub Pages) with a Web Share Target. Three tabs: **Library** (usefulness ring, a shelf of category tiles that drill into subcategories and locations, search and a filter sheet for sort, usefulness, platform, date, creator and tool; tap a card for a note with summary and what checks out), **Queue** (add a link; each link shows a Waiting / Working / Done track), **Claims** (verified, hoax, side quests as collapsible cards). Settings holds a System / Light / Dark theme switch. Reads the repo through the GitHub API with a fine-grained token stored on the phone (Issues read/write, Contents read-only). |
| `docs/pin.json`, `.github/workflows/set-pin.yml`, `scripts/set_pin.py` | Optional PIN lock: salted hash written by the workflow from a `pin` issue; the app shows a keypad until it is entered; optional fingerprint unlock (WebAuthn) per phone. |
| `scripts/followup_link.py` | Appends a follow-up answer to an existing note and rebuilds the index; no re-fetching. |
| `data/search.json` | Generated full-text index (see `build_index.py`); loaded lazily by the app's search, which shows field-labelled snippets. |
| `taxonomy.yml` | Closed vocabulary: categories with subcategories, aliases, icons and colours; locations (country, city). Single source of truth. |
| `scripts/taxonomy.py` | Shared lookup code plus `check`, `merge-sub`, `merge-cat` and `rename-city` for keeping the taxonomy tidy as it grows. |
| `.github/workflows/prepare.yml` | Runs the scraping on a GitHub runner when a link is queued; commits to `inbox/`. |
| `scripts/prepare_queue.py` | What the workflow runs: finds queued issues, prepares each, commits `inbox/`, labels `prepared`. |
| `inbox/` | Prepared links waiting for the Claude check; deleted by `finish_link.py`. |
| `scripts/recipe_card.py`, `scripts/build_nutrition.py`, `data/nutrition.json` | Recipe macros: ingredient lookup, unit conversion, card JSON and Markdown; the nutrition table and its sanity check. |
| `recipes/<id>.json` | Computed recipe cards the app displays. |
| `scripts/prepare_link.py` | One command for all mechanical work on a link; writes `brief.md` and `draft_note.md`. |
| `scripts/finish_link.py` | One command for everything after the judgment: note, registry, index, flow table, comment, push. |
| `scripts/build_index.py` | Validates notes against the taxonomy and builds `data/library.json`, `data/taxonomy.json` and `library/`. |
| `data/library.json`, `data/taxonomy.json` | Generated index and vocabulary the app reads. |
| `library/README.md`, `library/by-category/`, `library/by-location/`, `library/by-usefulness/` | Generated lists of every link with key info, grouped for reading on GitHub. |
| `.claude/skills/*/SKILL.md` | One skill per operation: `process-link`, `fetch-instagram-post`, `fetch-youtube-video`, `analyze-video`, `analyze-comments`, `write-link-note`, `fact-check-claims`, `update-registries`, `prepare-link`, `finish-link`, `recipe-card`, `categorize-link`, `update-library`, `analyze-comments`, `process-queue`, `shorts-trend-script-approval`, `shorts-visible-stakes-video` (original Shorts workflow, separate from link processing). |
| Link Inbox artifact | https://claude.ai/artifact/FLi1JREBRUV493gipCS5AG (source is not in the repo; it lives on claude.ai). |
| `notes/instagram/<shortcode>.md` | One note per Instagram link. |
| `notes/youtube/<video-id>.md` | One note per YouTube link. |
| `registry/verified.md` | Verified tools, hacks and facts, plus a Pending verification section. |
| `registry/hoax.md` | Hoaxes and misleading claims with evidence. |
| `registry/sidequests.md` | Non-informative videos, one line each. |

## Data and scratch files
Downloaded videos, frames and transcripts stay in a scratch directory outside the repo. Only the note, registry entries and docs are committed, so the repo stays small and contains no downloaded media.

## Current notes
| Note | Category · usefulness · verdict |
|---|---|
| [notes/instagram/DfChs7UzB-t.md](notes/instagram/DfChs7UzB-t.md) | AI · helpful · verified |
| [notes/instagram/DfBtGcYo5yX.md](notes/instagram/DfBtGcYo5yX.md) | Tech & dev · helpful · verified |
| [notes/instagram/DfA1ccrSE_4.md](notes/instagram/DfA1ccrSE_4.md) | Money · misleading · partly-verified |
| [notes/instagram/DfAujDfBAbO.md](notes/instagram/DfAujDfBAbO.md) | AI · mixed · partly-verified |
| [notes/instagram/De_9XCHixR2.md](notes/instagram/De_9XCHixR2.md) | Money · mixed · partly-verified |
| [notes/instagram/De95N60JYG2.md](notes/instagram/De95N60JYG2.md) | AI · mixed · pending |
| [notes/instagram/De9yxpuIG6X.md](notes/instagram/De9yxpuIG6X.md) | AI · helpful · partly-verified |
| [notes/instagram/De9l-_tzb0a.md](notes/instagram/De9l-_tzb0a.md) | Money · mixed · partly-verified |
| [notes/instagram/De7_2tUS54h.md](notes/instagram/De7_2tUS54h.md) | Money · mixed · partly-verified |
| [notes/instagram/De7FvKcFJKl.md](notes/instagram/De7FvKcFJKl.md) | Entertainment · noise · sidequest |
| [notes/instagram/De63EgSxsXo.md](notes/instagram/De63EgSxsXo.md) | Money · mixed · partly-verified |
| [notes/instagram/De62WbvxkZB.md](notes/instagram/De62WbvxkZB.md) | AI · helpful · verified |
| [notes/instagram/De5Q_FgjpZN.md](notes/instagram/De5Q_FgjpZN.md) | Money · mixed · partly-verified |
| [notes/instagram/De5NPnBqVqV.md](notes/instagram/De5NPnBqVqV.md) | Money · misleading · partly-verified |
| [notes/instagram/De5C72nPV5Y.md](notes/instagram/De5C72nPV5Y.md) | Money · misleading · partly-verified |
| [notes/instagram/De4_1YTT5CV.md](notes/instagram/De4_1YTT5CV.md) | Tech & dev · helpful · partly-verified |
| [notes/instagram/De4rnuLEWb_.md](notes/instagram/De4rnuLEWb_.md) | AI · mixed · partly-verified |
| [notes/instagram/De4Lndsh9UB.md](notes/instagram/De4Lndsh9UB.md) | Tech & dev · helpful · partly-verified |
| [notes/instagram/De4LWBAPeeI.md](notes/instagram/De4LWBAPeeI.md) | Money · mixed · partly-verified |
| [notes/instagram/De4JTo0h0fr.md](notes/instagram/De4JTo0h0fr.md) | Money · misleading · pending |
| [notes/instagram/De3i_K1vg2l.md](notes/instagram/De3i_K1vg2l.md) | AI · mixed · pending |
| [notes/instagram/De12Kb6P4wG.md](notes/instagram/De12Kb6P4wG.md) | AI · mixed · partly-verified |
| [notes/instagram/De1v8QLqcnn.md](notes/instagram/De1v8QLqcnn.md) | AI · helpful · partly-verified |
| [notes/instagram/De0sKBEz_6w.md](notes/instagram/De0sKBEz_6w.md) | AI · mixed · partly-verified |
| [notes/instagram/De0Aoqixw-y.md](notes/instagram/De0Aoqixw-y.md) | Money · mixed · partly-verified |
| [notes/instagram/DeztS_8iSzv.md](notes/instagram/DeztS_8iSzv.md) | AI · helpful · partly-verified |
| [notes/instagram/Dezg3-ElDAH.md](notes/instagram/Dezg3-ElDAH.md) | AI · helpful · verified |
| [notes/instagram/Dex05t6RrB9.md](notes/instagram/Dex05t6RrB9.md) | Money · misleading · partly-verified |
| [notes/instagram/Dewv1q7tvKg.md](notes/instagram/Dewv1q7tvKg.md) | AI · mixed · pending |
| [notes/instagram/DewkicGtWcS.md](notes/instagram/DewkicGtWcS.md) | Tech & dev · helpful · partly-verified |
| [notes/instagram/DewguD7pH9n.md](notes/instagram/DewguD7pH9n.md) | Money · helpful · partly-verified |
| [notes/instagram/DewXLi2vVWR.md](notes/instagram/DewXLi2vVWR.md) | AI · helpful · verified |
| [notes/instagram/DevhsdCt6KH.md](notes/instagram/DevhsdCt6KH.md) | Money · misleading · partly-verified |
| [notes/instagram/DeuaI4ItktU.md](notes/instagram/DeuaI4ItktU.md) | Tech & dev · misleading · partly-verified |
| [notes/instagram/DeuNjnMEVux.md](notes/instagram/DeuNjnMEVux.md) | Money · mixed · pending |
| [notes/instagram/DeuDQgFtzzX.md](notes/instagram/DeuDQgFtzzX.md) | AI · mixed · partly-verified |
| [notes/instagram/DetqEejBwMz.md](notes/instagram/DetqEejBwMz.md) | Tech & dev · helpful · partly-verified |
| [notes/instagram/DesmCd0P_-g.md](notes/instagram/DesmCd0P_-g.md) | AI · mixed · partly-verified |
| [notes/instagram/DesWw43N0he.md](notes/instagram/DesWw43N0he.md) | Money · mixed · partly-verified |
| [notes/instagram/DesCGsjTQcy.md](notes/instagram/DesCGsjTQcy.md) | AI · mixed · partly-verified |
| [notes/instagram/Derq5syKEOL.md](notes/instagram/Derq5syKEOL.md) | AI · mixed · partly-verified |
| [notes/instagram/Derra61CUhb.md](notes/instagram/Derra61CUhb.md) | AI · helpful · partly-verified |
| [notes/instagram/Derp4yJoTmP.md](notes/instagram/Derp4yJoTmP.md) | AI · helpful · partly-verified |
| [notes/instagram/Deqni2Tic2N.md](notes/instagram/Deqni2Tic2N.md) | Tech & dev · helpful · verified |
| [notes/instagram/Deqmd98M2vB.md](notes/instagram/Deqmd98M2vB.md) | AI · mixed · partly-verified |
| [notes/instagram/DeqjfBoRhjA.md](notes/instagram/DeqjfBoRhjA.md) | Food · helpful · verified |
| [notes/instagram/DeqVUsUz1cT.md](notes/instagram/DeqVUsUz1cT.md) | AI · misleading · pending |
| [notes/instagram/DepP3GEy6F3.md](notes/instagram/DepP3GEy6F3.md) | Money · helpful · sidequest |
| [notes/instagram/Deo0IRdNC-S.md](notes/instagram/Deo0IRdNC-S.md) | Tech & dev · mixed · pending |
| [notes/instagram/DeoTMAkotoo.md](notes/instagram/DeoTMAkotoo.md) | Entertainment · noise · sidequest |
| [notes/instagram/DenEaIdxmZk.md](notes/instagram/DenEaIdxmZk.md) | Money · mixed · partly-verified |
| [notes/instagram/Demp5EUT6GV.md](notes/instagram/Demp5EUT6GV.md) | AI · helpful · verified |
| [notes/instagram/DemnycCjEYg.md](notes/instagram/DemnycCjEYg.md) | Money · mixed · partly-verified |
| [notes/instagram/DemUJJRJjM1.md](notes/instagram/DemUJJRJjM1.md) | Tech & dev · mixed · partly-verified |
| [notes/instagram/DemQhAjSIEH.md](notes/instagram/DemQhAjSIEH.md) | AI · mixed · sidequest |
| [notes/instagram/DemHB0GhG_R.md](notes/instagram/DemHB0GhG_R.md) | AI · mixed · partly-verified |
| [notes/instagram/DelxZzcvW49.md](notes/instagram/DelxZzcvW49.md) | AI · mixed · partly-verified |
| [notes/instagram/Dek6wBjJgnA.md](notes/instagram/Dek6wBjJgnA.md) | AI · helpful · partly-verified |
| [notes/instagram/DehErZxDfkE.md](notes/instagram/DehErZxDfkE.md) | AI · mixed · partly-verified |
| [notes/instagram/DegUW7YG_O1.md](notes/instagram/DegUW7YG_O1.md) | AI · helpful · verified |
| [notes/instagram/DegLPFbTBpi.md](notes/instagram/DegLPFbTBpi.md) | AI · mixed · partly-verified |
| [notes/instagram/Deep2H2yNsr.md](notes/instagram/Deep2H2yNsr.md) | Money · mixed · pending |
| [notes/instagram/DedHV-3lel2.md](notes/instagram/DedHV-3lel2.md) | AI · mixed · pending |
| [notes/instagram/DecpuNXDoYj.md](notes/instagram/DecpuNXDoYj.md) | AI · mixed · partly-verified |
| [notes/instagram/DeZ0mMDxj6d.md](notes/instagram/DeZ0mMDxj6d.md) | Money · mixed · pending |
| [notes/instagram/DeVyGbyJGcl.md](notes/instagram/DeVyGbyJGcl.md) | AI · mixed · pending |
| [notes/instagram/DeUK2NZS3Ig.md](notes/instagram/DeUK2NZS3Ig.md) | AI · mixed · pending |
| [notes/instagram/DeToMLxtdSV.md](notes/instagram/DeToMLxtdSV.md) | AI · mixed · partly-verified |
| [notes/instagram/DeSArmKIhid.md](notes/instagram/DeSArmKIhid.md) | AI · helpful · verified |
| [notes/instagram/DeOxisYD6ap.md](notes/instagram/DeOxisYD6ap.md) | AI · mixed · pending |
| [notes/instagram/DeMoCfwCHE8.md](notes/instagram/DeMoCfwCHE8.md) | Money · mixed · pending |
| [notes/instagram/DeMlHQjxpnA.md](notes/instagram/DeMlHQjxpnA.md) | AI · mixed · partly-verified |
| [notes/instagram/DeHt0APsh-e.md](notes/instagram/DeHt0APsh-e.md) | Money · mixed · partly-verified |
| [notes/instagram/DeGKrmWh89C.md](notes/instagram/DeGKrmWh89C.md) | AI · mixed · partly-verified |
| [notes/instagram/DeET_LNFrz5.md](notes/instagram/DeET_LNFrz5.md) | AI · mixed · pending |
| [notes/instagram/DeCH_lVqG-k.md](notes/instagram/DeCH_lVqG-k.md) | AI · mixed · pending |
| [notes/instagram/DeCDNPzJkfN.md](notes/instagram/DeCDNPzJkfN.md) | AI · helpful · partly-verified |
| [notes/instagram/DeB_xCxDT_F.md](notes/instagram/DeB_xCxDT_F.md) | AI · mixed · pending |
| [notes/instagram/Dd4PDA1xYuc.md](notes/instagram/Dd4PDA1xYuc.md) | AI · mixed · partly-verified |
| [notes/instagram/Dd2HKWYzQ69.md](notes/instagram/Dd2HKWYzQ69.md) | AI · helpful · partly-verified |
| [notes/instagram/Dd1_GC-sJVz.md](notes/instagram/Dd1_GC-sJVz.md) | AI · mixed · partly-verified |
| [notes/instagram/Ddvk-Dxgc8z.md](notes/instagram/Ddvk-Dxgc8z.md) | AI · helpful · partly-verified |
| [notes/instagram/DdtdmRetwB3.md](notes/instagram/DdtdmRetwB3.md) | AI · misleading · partly-verified |
| [notes/instagram/Ddq8NW4S-Wn.md](notes/instagram/Ddq8NW4S-Wn.md) | Tech & dev · helpful · partly-verified |
| [notes/instagram/DdoVuGLR0BP.md](notes/instagram/DdoVuGLR0BP.md) | Entertainment · noise · sidequest |
| [notes/instagram/DdmtlwqBPJ-.md](notes/instagram/DdmtlwqBPJ-.md) | AI · mixed · partly-verified |
| [notes/instagram/DdjLCONTvnG.md](notes/instagram/DdjLCONTvnG.md) | Money · mixed · partly-verified |
| [notes/instagram/DdgmWeIt1AE.md](notes/instagram/DdgmWeIt1AE.md) | Money · helpful · verified |
| [notes/instagram/DdZSikeJ5Wr.md](notes/instagram/DdZSikeJ5Wr.md) | AI · mixed · pending |
| [notes/instagram/DdL_g4yT7R_.md](notes/instagram/DdL_g4yT7R_.md) | Tech & dev · helpful · partly-verified |
| [notes/instagram/DdIettJRFYB.md](notes/instagram/DdIettJRFYB.md) | Money · helpful · partly-verified |
| [notes/instagram/DdBGaAgnQyL.md](notes/instagram/DdBGaAgnQyL.md) | AI · helpful · verified |
| [notes/instagram/Dc36DK9zjdV.md](notes/instagram/Dc36DK9zjdV.md) | AI · misleading · partly-verified |
| [notes/instagram/Db-83ucolWr.md](notes/instagram/Db-83ucolWr.md) | AI · mixed · pending |
| [notes/instagram/Dbk7in3JzR1.md](notes/instagram/Dbk7in3JzR1.md) | Money · misleading · pending |
| [notes/instagram/DbB8h50urJb.md](notes/instagram/DbB8h50urJb.md) | Money · misleading · partly-verified |
| [notes/instagram/Da0PIzmv5RG.md](notes/instagram/Da0PIzmv5RG.md) | Money · mixed · partly-verified |
| [notes/instagram/DafrdobMFBG.md](notes/instagram/DafrdobMFBG.md) | AI · mixed · partly-verified |
| [notes/instagram/DZVxhkDTBAK.md](notes/instagram/DZVxhkDTBAK.md) | Money · misleading · partly-verified |
| [notes/instagram/DX_0DQIyplz.md](notes/instagram/DX_0DQIyplz.md) | Money · helpful · partly-verified |
| [notes/youtube/R4yihx8sEO8.md](notes/youtube/R4yihx8sEO8.md) | Health & fitness · mixed · pending |
