---
url: https://www.instagram.com/reel/Dezg3-ElDAH/
platform: instagram
type: reel
author: lindsay.ai
posted: 2026-10-22T17:25:31Z
duration_s: 36
views: not exposed
likes: 16
comments: 23
language: en
queued_via: "GitHub issue #57"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Claude Code watch skill with Gemini"
category: ai
subcategory: tools
usefulness: helpful
tools: ["claude-code", "claude-video", "gemini-api"]
key_info: "The method is real: the open-source claude-video repo (bradautomates/claude-video, MIT) adds a /watch skill that turns a video link into timestamped frames and a transcript, and can send YouTube links straight to the Gemini API when you set a Gemini API key. The on-screen Google docs page shows YouTube URL input is a free preview feature whose pricing and limits may change. The 'agent framework' for client agents and the guide are not named and sit behind a comment-for-DM funnel."
verdict: verified
registry: registry/verified.md
---

# Claude Code watch skill with Gemini

## Caption / hashtags
> Comment “WATCH” and I’ll send you the guide. 👇
> 
> You can teach Claude Code new workflows by combining YouTube knowledge with the right tools and agent framework.
> 
> Here are the 3 pieces that make it work:
> 
> 🎥 A GitHub repo to extract information from YouTube videos.
> 
> 🧠 A Gemini API key from Google AI Studio to analyze videos directly from their links.
> 
> 🤖 An agent framework to turn what Claude learns into specialized agents you can deploy.
> 
> This is the workflow behind the editing, marketing, and social media agents I build.
> 
> The real advantage isn’t just watching tutorials. It’s turning what you learn into systems that do actual work.
> 
> Follow me so you don’t miss the DM.
> 
> #ClaudeCode #GeminiAI #AITools #AIAgents #AIautomation

Hashtags: #claudecode #geminiai #aitools #aiagents #aiautomation.

## Hook (on-screen text)
Teach Claude Code any real-world skill by showing it how to watch YouTube

## Call to action
Comment 'WATCH' for the guide by DM and follow

## Transcript (auto)
> Most people don't realize you can teach Claude code almost any real-world skill just by showing it how to properly watch YouTube. Three's pieces make it work. First, a GitHub repo that gives Claude code the ability to pull information straight out of YouTube videos. Second, a free Gemini API key from Google AI Studio. And because Gemini can work directly from a YouTube link, it takes in the video itself instead of just a transcript. Third, an agent framework that turns what it learned into high-skill agents you can deploy for clients. This is the exact method behind the agents I run for editing, marketing, and social media. The builders using this correctly are pulling ahead fast right now. Comment, watch below, and I'll send you the guide. Make sure you're following so you see my DM.

## What is shown on screen
A Claude Code terminal running '/watch <YouTube link>', the GitHub repo 'claude-video' (10.4k stars at the time of the recording), a Gemini API page ('Using Gemini API keys', free tier) and the docs section 'Pass YouTube URLs' noting it is a free preview feature.

## Summary
The creator says you can teach Claude Code real-world skills by letting it watch YouTube: a GitHub repo to pull information from videos, a free Gemini API key so Gemini analyses the video itself from a link rather than only a transcript, and an agent framework to package what it learns into agents for clients.

## Comments
Not read: Instagram requires a login to list comments. The count is 23 against 16 likes (comments/likes 1.44; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-22)

| Claim | Verdict | Evidence |
|---|---|---|
| A GitHub repo lets Claude Code pull information from YouTube videos | verified | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) (MIT) gives Claude a /watch skill that produces timestamped frames and a transcript; it showed about 19k stars when checked, against 10.4k in the reel's recording. |
| A free Gemini API key lets Gemini analyse the video directly from a YouTube link | verified | The repo says that with a Gemini API key, YouTube links go straight to Google, and the on-screen Google docs show the YouTube URL feature as a free preview whose pricing and limits are likely to change. |
| An agent framework turns what it learned into deployable client agents | unverified | The framework is not named in the reel; it is part of the guide that is sent by DM. |
| This is the exact method behind the creator's editing, marketing and social media agents | unverified | The creator's own claim; not shown. |

Overall: The tooling is real and well described; the commercial agent-building claims are unverified and sit behind a DM funnel.

## Notes / caveats
- The free Gemini YouTube URL feature is a preview and may change or add cost.
- Sending YouTube links or uploaded video to Gemini means that content goes to Google; check privacy needs for private videos.
- Setup needs Python 3.10+, FFmpeg and yt-dlp; Claude Chat and Cowork are not supported according to the repo.
- Whether you can build deployable client agents this way is the creator's claim and was not shown.
