---
name: shorts-trend-script-approval
description: Research trending YouTube Shorts and Instagram Reels (formats and audio), write script options, get the user's approval or tweaks, then hand the approved script to shorts-visible-stakes-video to render.
---

# Shorts: Trend Research, Script, Approval, Then Video

Runs the whole front half of a Shorts workflow: find what is trending, write scripts around it, loop with the user until one is approved, then render. This skill never renders before approval. Rendering is done by the `shorts-visible-stakes-video` skill.

## Step 1: Research (start immediately, do not ask first)

Goal: 3-5 current trends, each with evidence.

1. WebSearch in "standard" mode, several queries in one turn. Include today's month and year in every query:
   - "YouTube Shorts trending [month year]"
   - "Instagram Reels trending audio [month year]"
   - "trending Shorts formats [month year]" and a niche term if the user gave one
   - Trend-report sites and creator newsletters often list view counts, countries and audio names.
2. If results are thin, repeat the weak query in "extended" mode.
3. WebFetch the best 3-5 pages (YouTube Charts, trend reports). If a fetch is blocked, say so and move on. Never use curl, wget, Python requests, archives or mirrors to get around a block.
4. Instagram needs a login. If the Chrome browser tools are available and the user is signed in, open Reels audio/trending pages there. Otherwise rely on reports and say that Instagram data is second-hand.
5. Extract per trend: format name, what happens on screen, audio name, evidence (views, countries, date, source URL), and whether it is makeable as an original animation (no third-party footage or specific licensed track needed).

Rules: never invent view counts or rankings. Anything not found in a source is marked "not found". Show at most 5 trends, ranked by (evidence strength x makeability), best first. Keep the rest in reserve for a "replace" round.

## Step 2: Write 2-3 script options

Use this exact table so it matches what the user already works with:

| Script Option | Duration | Core Trend & Audio Pairing | Timing & Structure Breakdown |

Rules for every script:
- 15-20 seconds. A hook in the first 2 seconds. A visible reason to keep watching (timer, stakes, countdown) at 0:00.
- A twist or payoff in the back half, a hidden detail at a fixed timestamp, and a pause or comment prompt ("Pause at 0:11", "Comment YES or NO").
- A loopable last frame.
- Mark each option "Makeable as original animation: yes/no". Prefer yes. If an option needs third-party footage, say so and propose the closest original version.
- Audio: name the trending sound as the pairing, and state the matching tempo and drop timing. The video itself ships with an original synthesized track, because trending audio cannot be ripped or redistributed. The user adds the trending sound from YouTube's Shorts audio library at upload if they want it.

Recommend one option and say why in one line.

## Step 3: Approval gate (required)

Ask with the AskUserQuestion tool (it must be loaded via ToolSearch first). One question, options:

1. Approve option N (recommended one first)
2. Tweak (ask what: hook, stakes text, niche or object, length, tone, audio feel)
3. Replace (new angle: different niche, different trend from the reserve list, or a fresh research pass)

Loop rules:
- Tweak: apply the change, show only what changed (old line vs new line) plus the updated timing table, and ask again.
- Replace: take the next trend from the reserve list or run Step 1 again with the new angle, write new options, ask again.
- Keep going until the user approves. Do not start rendering on anything weaker than explicit approval.
- If the session is unattended or the user is not responding: deliver the scripts and stop. Say that rendering waits for approval.

## Step 4: Hand off to rendering

Invoke the `shorts-visible-stakes-video` skill with the approved script. Pass: stakes text, thrown object or niche, timing table, and the audio feel (bpm, drop time). Be upfront about limits: the current renderer's scene is the basketball-shot template with the visible-stakes plus freeze-frame structure. Scripts with the same structure are text and timing swaps. A script with a different scene needs new scene code, so tell the user how much extra work that is (minutes versus an hour) before starting.

## Step 5: Deliver

Send the MP4 with SendUserFile. Reply with: the approved script in one line, upload steps, a title with #shorts, the audio to add at upload, and the sources behind the trend (links). Note that Shorts trends fade within roughly 1-2 weeks, so post soon.

## Quick reference

- Format of replies: lead with the next action. Number multi-step instructions. One next action at the end.
- Sources: list links for every trend claim. Mark Instagram data as second-hand when it is.
- Never: invent numbers, bypass blocked domains, claim to have used trending audio when the video uses synthesized audio.
