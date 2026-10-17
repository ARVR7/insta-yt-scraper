---
url: https://www.instagram.com/reel/DeToMLxtdSV/
platform: instagram
type: reel
author: aiwithsanskar
posted: 2026-10-10T08:29:51Z
duration_s: 56
views: not exposed
likes: 402
comments: 463
language: en
fetch_status:
  metadata: ok (instaloader, anonymous)
  caption: not returned by Instagram (empty)
  video: downloaded
  transcript: ok (faster-whisper base, auto-generated, may contain errors)
  on_screen_text: read from sampled frames (1 frame / 4s)
verdict: partly-verified
registry: registry/verified.md, registry/hoax.md
---

# Agentic AI YouTube studio (free, open source) – "comment TUBE"

## Caption / hashtags
Not retrievable. Instagram returned an empty caption and no hashtags or mentions.

## Hook (on-screen text)
"THIS AGENTIC AI YOUTUBE STUDIO CAN MAKE YOU LACS OF RUPEES EVERY MONTH ON AUTOPILOT"

## Call to action
End card: **Comment "TUBE"** to get the guides. This is a comment-for-DM funnel, so the repo link is not in the video or caption.

## Transcript (auto)
> Someone has just released a fully agentic AI YouTube studio that can make you money while it runs, for completely free. I'm not kidding, people doing this can make thousands of rupees every month. It comes with a full YouTube team that runs 24/7: an AI researcher that looks at viral videos and sees what it can copy from them, then an AI scriptwriter agent turns it into a full script, then the free AI voice narrates every line, then your editor agent pulls free stock footage, cuts from the long video and makes a 9:16 short for it automatically. Then it drops everything into a review dashboard; you click approve and it uploads to YouTube with the title, description and tags already written. The crazy part is that the full studio is free and open source, so no editor, no voice actor and no monthly subscription. You can have this run 24/7 until you start making profits. Comment "TUBE" and I'll send you the entire set of guides.

## What is shown on screen
The creator screen-records a GitHub README titled **"YouTube AI Agent Studio – AI Powered Free Automated Faceless YouTube Studio"**, tagline "A fully automated, 100% free AI pipeline that researches, scripts, narrates, animates, and uploads faceless YouTube videos – from a single command." The repo appears to be named `youtube-agentic-ai-studio`; the owner name in the browser tab is only partly legible, so it is not recorded here. MIT license, Python 3.10+, Google Gemini badge.

Feature table as read from the README:

| Feature | Details |
|---|---|
| AI Research | Gemini scans for trending topics tailored to your channel niche |
| Script Writing | Full narrated script with hook, sections, and CTA, in JSON |
| Free Voice | Microsoft Edge TTS (no API key, no cost, word-level timing) |
| Stock Images | Auto-downloads from Pexels with topic-aware search |
| Animated Video | Ken Burns zoom, smooth crossfades, captions, progress bars |
| Shorts Support | Generates vertical 9:16 Shorts alongside the main video |
| Human Review | Local web dashboard to watch and approve before publishing |
| Auto Upload | Publishes to YouTube with SEO tags, description, and thumbnail |
| Smart Fallback | 8-model chain auto-switches if any model hits quota |
| Background Music | Drop MP3s in `music_library/`, auto-looped to fit video length |

## Summary
A promo reel for an open-source Python tool that automates a faceless YouTube channel: Gemini picks topics, writes the script, Edge TTS narrates it, Pexels stock footage is animated, and a Shorts version is cut. A local dashboard handles human approval, then it auto-uploads to YouTube.

## Comments
Not read: Instagram requires a login to list comments. The count is 464 against 402 likes. Because the call to action is "comment TUBE", many of those are likely keyword-only funnel replies, so the count says little about real interest (inference, not verified). If you paste the top comments, I'll look for the repo link or corrections.

## Research (checked 2026-10-17)

| Claim | Verdict | Evidence |
|---|---|---|
| Free Edge TTS voice, no API key | verified-with-caveats (unofficial service) | [PyPI](https://pypi.org/project/edge-tts), [GitHub](https://github.com/rany2/edge-tts) |
| Free Pexels stock footage via API | verified-with-caveats (200 req/h, 20k/month, attribution) | [Pexels Help](https://help.pexels.com/hc/en-us/articles/47677890260761-Is-the-Pexels-API-free-to-use) |
| Free Gemini for research and scripts | verified-with-caveats (free-tier quotas vary) | [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) |
| The specific "YouTube AI Agent Studio" repo | unverified (not found in two searches; owner not legible) | see `registry/verified.md` Pending |
| Earns "thousands to lacs of rupees" per month on autopilot | misleading (no evidence; contradicts YouTube policy risk) | [YouTube Help](https://support.google.com/youtube/answer/1311392), `registry/hoax.md` |

Overall: the building blocks are real and free; the money claim is unsubstantiated.

## Notes / caveats
- The earnings framing ("lacs of rupees every month") is promotional and unverified.
- Pexels and Gemini free tiers have usage limits, and YouTube's policies on repetitive or low-effort automated content may affect monetization.
- To find the repo, search GitHub for "youtube-agentic-ai-studio" or "YouTube AI Agent Studio".
