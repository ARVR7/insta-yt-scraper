---
url: https://www.instagram.com/reel/DdmtlwqBPJ-/
platform: instagram
type: reel
author: wassimyounes_
posted: 2026-09-22T21:35:22Z
duration_s: 21
views: not exposed
likes: 1279
comments: 1225
language: en
queued_via: "GitHub issue #61"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Uncensored Qwen Image 2.1 on a laptop"
category: ai
subcategory: tools
usefulness: mixed
tools: ["Qwen-Image-2.1", "ComfyUI", "GGUF"]
key_info: "Creator says Nano Banana 2 went open source and uncensored, and that Qwen Image 2.1 beats it and runs in about 5 GB. What the screenshots actually show: Qwen-Image-2.1 open weights, plus a community refusal-ablated ('Heretic') text encoder in GGUF (Q4_K_M, 4.68 GB) for ComfyUI. Nano Banana 2 is not open source."
verdict: partly-verified
registry: registry/verified.md
---

# Uncensored Qwen Image 2.1 on a laptop

## Caption / hashtags
> Comment “IMAGE” 🐉 I’ll send qwen 2.1 image gen model! Which is better than Nanobana 2! #ainews #opensource #ai

Hashtags: #ainews #opensource #ai.

## Hook (on-screen text)
Nano Banana 2 just went fully open source and uncensored

## Call to action
Comment IMAGE to get the link (lead-magnet DM)

## Transcript (auto)
> Nano Banana 2 just went fully open source and get it local uncensored. One image 2.1 is better than Nano Banana 2, and it runs on a 5 gigabyte. So if you guys do want this, comment down below image and I'll send this over. Plot twist though natively, this is essentially already uncensored, so I don't know why people even did this, but you know what? If you guys are kind of worried you could have this as well, I guess.

## What is shown on screen
Screenshots of X posts (Pradeep Kapoor, @Israfilv2) and a Hugging Face page for pottokao/Qwen-Image-2.1-Text-Encoder-Heretic-GGUF; benchmark bars with Qwen Image 2.1 at 60.28 vs Nano Banana 2.0 at 59.82.

## Summary
A 21-second reel with a misleading headline. Nano Banana 2 (Google) was not open sourced; the post is about Qwen-Image-2.1 and an uncensored text-encoder variant. The 'better than Nano Banana 2' claim rests on a 0.46-point gap in the vendor's own chart.

## Comments
Not read: Instagram requires a login to list comments. The count is 1225 against 1279 likes (comments/likes 0.96; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-23)

| Claim | Verdict | Evidence |
|---|---|---|
| Nano Banana 2 went open source and uncensored | unverified | Nano Banana is a hosted Google model; the on-screen sources are about Qwen-Image-2.1, so the headline looks like a misstatement |
| Qwen Image 2.1 is better than Nano Banana 2 | partly | Qwen's own chart shows 60.28 vs 59.82; not independent, no error ranges, gap is tiny |
| Runs on about 4-5 GB | partly | The 4.68 GB figure is the quantised (Q4_K_M) text encoder file only; the image model and VAE are extra, so total memory is higher |
| Uncensored variant exists, refusals drop 100/100 to 5/100 | partly | A refusal-ablated encoder with those figures is reported by secondary sources; the pottokao repo itself was not opened, and the creator says the base model is already mostly uncensored |
| Weights are open | partly | Open weights reported, but under a research licence (non-commercial) according to a comparison site; the Hugging Face card in the video shows apache-2.0 for the encoder only |

Overall: Real underlying release, wrong headline. Treat as a lead-magnet reel; the Hugging Face repos are on screen, so no need to comment for a DM.

## Notes / caveats
- Comment-for-link funnel; the repo name is visible in the video.
- Benchmark is vendor-published.
- Uncensored image models can produce harmful content; check the licence and local laws.
- Comments not fetched (login required).
