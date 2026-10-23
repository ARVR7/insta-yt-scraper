---
url: https://www.instagram.com/reel/De0sKBEz_6w/
platform: instagram
type: reel
author: adonisautomates
posted: 2026-10-23T04:24:21Z
duration_s: 115
views: not exposed
likes: 80
comments: 10
language: en
queued_via: "GitHub issue #63"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "25 dollar AI video stack with Gemini Omni"
category: ai
subcategory: creative
usefulness: mixed
tools: ["Claude", "ChatGPT", "Gemini Omni", "Google AI Plus"]
key_info: "Stack pitched: Claude subscription (about 20 dollars) as director and stitcher, ChatGPT free tier for storyboard images, Google AI Plus (about 5 dollars) for Gemini Omni video. Claim: roughly 100 videos a week for 25 dollars, 2 clips per 5-hour window, Omni ranked top 3 on Arena."
verdict: partly-verified
registry: registry/verified.md
---

# 25 dollar AI video stack with Gemini Omni

## Caption / hashtags
> free sauce

## Hook (on-screen text)
25 dollar AI video pipeline for 100 videos a week

## Call to action
Caption says free sauce; no explicit CTA

## Transcript (auto)
> They're one of the best video stacks right now for creating AI videos is going to be your cloud subscription, which is $20 free charge ability, because that's all you need for image generation. And third, you basically need Google AI Plus, which is like $5. So in $25, you basically have ability for Gemini's Google Omni Extended, which is amazing. It, given on AI Plus video, you are basically able to create every five hours, 20 second video, that means two to 10 second videos, and then it will exhaust approximately two and a half to two percent of your weekly usage. So that means every five hours, because after you create like these two videos, your entire five hour limit is gone. But you basically can create hypothetically, 50 videos like these, which is insane. Plus, if you're actually on additional storage, or you're already purchasing additional storage, you probably already have Google AI Plus. I know shocking, I was very shocked as well. And everybody in your family who has been added, why you already has it as well. So you already have a lot of AI video models, probably at your disposal. But it's still one of the best places out there. I think Google's AI models actually rank the highest. Yes, they're actually rank higher than Seed Dance 2.5. If you can prompt up correctly at this point of time, you can actually check these rankings out on Arena, A-R-E-N-A, Arena LLM. So they basically rank all of these video models. And I think Google Omni has been top three text to video, image to video, all of these things. So basically, it cloud as the director to stitch things together, charge GPT-free, plan can actually make all of the storyboard images and stuff. And you can upload images to Gemini and ask Omni to animate them in a certain way. And then cloud can basically stitch them together to view all of the frames, to check if the rendering is correct. And if the rendering is not correct, it will fill in the blanks with some sort of stills some sort of heroes that you can find of that helps.

## What is shown on screen
Title card only: 25 dollar AI video pipeline for 100 videos a week; word-by-word captions.

## Summary
Gemini Omni video generation in AI Plus is real, but 100 videos a week is a hypothetical based on the creator's own usage numbers; reports of 10-second clips eating large chunks of the limit suggest it is optimistic. The Claude part is not an integrated pipeline: Claude cannot drive the Gemini app, so the steps are manual or need an API/MCP route.

## Comments
Not read: Instagram requires a login to list comments. The count is 10 against 80 likes (comments/likes 0.12; a ratio near or above 1 usually means a prompt to comment, an inference).

## Your instruction

> How do we integrate claude and omni?

No official Claude-Omni integration found. Options: (1) Manual: have Claude write the storyboard, shot list and one prompt per clip, paste prompts into Gemini Omni, download clips, then ask Claude Code to write an ffmpeg concat script. (2) Automated, if Omni reaches the Gemini API: wrap it in a small MCP server or script with a Gemini API key and register it with Claude Code via claude mcp add; today community MCP servers (for example Gemini Media MCP, visualgen-mcp) expose Veo 3.1 text-to-video and image-to-video the same way, and Veo is billed per second, not by the 5 dollar plan. (3) Claude checks results: extract frames with ffmpeg and let Claude review them, as the creator describes. Omni API availability was not confirmed, so option 1 is the only certain route for AI Plus users right now.

## Research (checked 2026-10-23)

| Claim | Verdict | Evidence |
|---|---|---|
| Gemini Omni is available on Google AI Plus | verified | Reports list Omni Flash for AI Plus, Pro and Ultra subscribers in the Gemini app and Flow |
| About 100 videos a week for 25 dollars | unverified | Creator extrapolates from 2.5 percent weekly use per two clips; sources disagree on limits and one review saw ~22 percent of a limit for a single 10s video. Said as hypothetically in the video |
| Omni ranks top 3 and above Seedance 2.5 on Arena | unverified | Not checked on the live leaderboard; rankings change often |
| Clips are 10 seconds, two per 5-hour window | partly | 10 s cap matches reports; per-window quota is from the creator's own usage, Google publishes no per-video quota |
| Claude can act as director and stitch Omni clips | partly | Claude can write storyboards, prompts and a stitching script, but cannot call the Gemini app; automation needs the Gemini API |

Overall: Plausible low-cost workflow, but the 100-a-week number is optimistic and the Claude-Omni link is manual unless you use the API.

## Notes / caveats
- Hypothetical numbers from one creator.
- Omni API availability was not confirmed in sources found; Veo 3.1 is available via API.
- Omni output carries SynthID; video-edit uploads are blocked in some regions.
- Comments not fetched (login required).
