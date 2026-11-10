---
url: https://www.instagram.com/reel/DfiiJsEiqB1/
platform: instagram
type: reel
author: charliehills
posted: 2026-11-09T23:41:15Z
duration_s: 38
views: not exposed
likes: 6
comments: 0
language: en
queued_via: "GitHub issue #151"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Watch skill turns YouTube videos into skills"
category: ai
subcategory: tools
usefulness: helpful
tools: ["Claude Code", "claude-video watch", "yt-dlp", "ffmpeg"]
key_info: "Watch is a real MIT-licensed Claude Code skill, github.com/bradautomates/claude-video. The /watch command takes a video link or path, downloads it with yt-dlp, grabs frames with ffmpeg and pulls the transcript, so Claude sees the screen and not just the words. Install in Claude Code with /plugin marketplace add bradautomates/claude-video then /plugin install watch@claude-video. The reel's trick: do not ask for a summary, ask Claude to turn the video into a reusable skill, for example a sales training video becoming a /sales-follow-up skill. The 20,000 star claim is plausible: the last figure I found was 17,031 in September. The exact prompt is behind comment WATCH, but the method is fully described."
verdict: verified
registry: none
---

# Watch skill turns YouTube videos into skills

## Caption / hashtags
> Claude can now watch YouTube videos for you and turn what they teach into a skill.
> 
> The free tool is called Watch. It reads the captions and the frames, so Claude sees the screen, not just the words. It works in Claude Code.
> 
> Comment WATCH and I'll send you the install steps and the exact prompt that turns a video into a skill.

## Hook (on-screen text)
Claude can now watch YouTube videos and turn them into skills

## Call to action
Comment WATCH for install steps and the prompt

## Transcript (auto)
> Claw can now watch YouTube videos for you and turn them into skills with one free tool that's got over 20,000 stars on GitHub. It's called watch and it takes three steps. So number one, you paste the GitHub link into Claw code and ask it to install it. Number two, you type slash watch and paste in any video link so it pulls the captions and grabs the framed where something changes on screen, which means Clawed sees what's shown and not just what's said. Number three, you don't ask it for a summary. You ask it to turn that video into a skill with a prompt like this one. So drop the best sales training you can find and Clawed starts writing your full apps that way. So next time you type one slash command and Clawed already knows the method.

## What is shown on screen
The claude-video GitHub repo, the /watch command pulling captions with timestamps and frames where the screen changes, a sales training video, and a generated /sales-follow-up skill writing an email.

## Summary
Accurate description of a real, popular skill, with the useful idea of turning a video into a reusable skill instead of a summary. The comment gate is unnecessary because the repo is public.

## Comments
Not read: Instagram requires a login to list comments. The count is 0 against 6 likes (comments/likes 0.00; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-11-10)

| Claim | Verdict | Evidence |
|---|---|---|
| Watch / claude-video is a free Claude Code skill that reads a video's captions and frames | verified | Repo and several directories confirm; MIT, uses yt-dlp and ffmpeg |
| Over 20,000 GitHub stars | partly-verified | Latest figure found was 17,031 in September 2026; likely higher now, not checked live |
| Turning a video into a skill gives better results than a summary | unverified | Reasonable idea; no test shown |

Overall: Accurate and useful; star count likely close; comment gate unnecessary.

## Notes / caveats
- Star count not checked live.
- Exact prompt not seen.
- Comments not fetched (none on the post).
