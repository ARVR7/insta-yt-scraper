---
url: https://www.instagram.com/p/DehErZxDfkE/
platform: instagram
type: post
author: bestapps.ai
posted: 2026-10-15T13:32:20Z
duration_s: None
views: not exposed
likes: 1555
comments: 813
language: n/a
queued_via: "GitHub issue #70"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "blocked (not downloaded)"
  transcript: "none"
  on_screen_text: "n/a"
  comments: "not fetched (Instagram requires login)"
title: "Colibri runs 744B model without a GPU"
category: ai
subcategory: tools
usefulness: mixed
tools: ["Colibri", "GLM-5.2", "llama-style local inference"]
key_info: "Caption says a 744B model runs on a laptop with no graphics card: only about 11GB of the mixture-of-experts model is active at once, Colibri keeps that in RAM and streams the rest from disk, with one setup script, offline use or a local API endpoint, and a '40K+ stars' repo. Free 'Offline AI Kit' is gated behind commenting GPU."
verdict: partly-verified
registry: registry/verified.md
---

# Colibri runs 744B model without a GPU

## Caption / hashtags
> Comment “GPU” to get the Offline AI Kit 👇
> 
> Someone just ran a 744B AI model on a laptop. No graphics card.
> 
> The trick: only ~11GB of the model is “thinking” at any moment. Colibri keeps that in RAM and streams the rest from your drive, like Netflix instead of a download.
> 
> One setup script. Then it runs fully offline, or as your own AI endpoint for your apps.
> 
> 40K+ devs already starred it on GitHub.
> 
> We packed the repo, the setup commands, and the one-line API swap into a free kit. Comment “GPU” 👇

## Hook (on-screen text)
Someone ran a 744B AI model on a laptop, no graphics card

## Call to action
Comment GPU to get the Offline AI Kit (lead magnet)

## Transcript (auto)
None available.

## What is shown on screen
Not reviewed: carousel slides are not available without an Instagram login.

## Summary
Colibri is a real pure-C engine that streams GLM-5.2 expert weights from disk, so the core claim holds. What the caption leaves out is speed: one write-up reports 0.05 to 0.1 tokens per second on a 25GB-RAM machine. The 40K stars figure conflicts with another source citing about 14.7K, and look-alike copies of the repo exist.

## Comments
Not read: Instagram requires a login to list comments. The count is 813 against 1555 likes (comments/likes 0.52; a ratio near or above 1 usually means a prompt to comment, an inference).

## Your instruction

> Check authenticity from all the slides in this post

Slides could not be read (Instagram carousel needs login). From the caption plus web research: the project is real (Colibri, GLM-5.2, disk-streamed experts), but speed and the 40K stars figure are not confirmed and copycat repos exist. If you send screenshots of the slides as a Follow-up instruction I will check each item.

## Research (checked 2026-10-24)

| Claim | Verdict | Evidence |
|---|---|---|
| Colibri runs a 744B MoE model (GLM-5.2) on a consumer machine with no GPU by streaming experts from disk | verified | Project write-ups and the repo description say about 25GB RAM, pure C, experts streamed from disk |
| Only about 11GB of the model is active at a time | partly | Consistent with MoE routing and an int4 dense core in RAM; exact active size not confirmed |
| Runs fully offline or as your own API endpoint | partly | Described by guides; not tested |
| Usable speed | unverified | Cold inference reported at 0.05 to 0.1 tokens per second by one source; another claims 5 to 12 and conflicts |
| 40K+ GitHub stars | unverified | One aggregator cites 14.7K stars; counts vary and several copies of the repo exist |

Overall: Genuine proof of concept, not a practical way to chat with a 744B model on a laptop. Use the original repo (JustVugg/colibri), not look-alike forks, and do not run setup scripts you have not read.

## Notes / caveats
- Slides were not readable (no login), so the owner instruction to check authenticity from every slide was done from the caption and web research only.
- Several lookalike repos exist, a risk for malware; verify the repo owner.
- Speed is likely very slow on a laptop.
- Lead-magnet funnel; the repo is public.
- Comments not fetched (login required).
