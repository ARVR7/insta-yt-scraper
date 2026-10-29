---
url: https://www.instagram.com/reel/DfCQiUNBHP7/
platform: instagram
type: reel
author: nishantchahar.ai
posted: 2026-10-28T10:50:07Z
duration_s: 38
views: not exposed
likes: 506
comments: 75
language: en
queued_via: "GitHub issue #109"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Anatomy Claude skill for isometric explainers"
category: ai
subcategory: tools
usefulness: helpful
tools: ["Anatomy skill", "Claude Code"]
key_info: "Anatomy is an open-source skill (wheresryan22/anatomy) that turns an idea into an interactive isometric figure in SVG, WebGL and 3D. Install with 'npx skills add wheresryan22/anatomy -g -a claude-code' or clone it into ~/.claude/skills/anatomy, then ask for what you want and give it references. The creator says it also works in other agents. The DM for the skill is unnecessary since the repo is public."
verdict: verified
registry: registry/verified.md
---

# Anatomy Claude skill for isometric explainers

## Caption / hashtags
> Comment "ANATOMY" and I'll DM you the skill 📩
> 
> This one Claude skill breaks down ANYTHING like an anatomy diagram 🧠🔬
> 
> Products, startups, apps, even your resume — dissected, labelled, explained in seconds.
> I've used AI tools for years. 
> 
> This is the most underrated one.
> 
> #claude

Hashtags: #claude.

## Hook (on-screen text)
A skill called Anatomy that many call the greatest ever

## Call to action
Comment ANATOMY to get the skill in DM

## Transcript (auto)
> A few days ago I came across a skill called Anatomy, with many saying it might be the greatest skill ever created. It's called isometric animations for literally everything you want. You can create visual explainers, isometric wire frames, create bento grids with it, or to even reverse engineer anything visually. People are building amazing things with it already, and it's way easier to build similar things using the skill. You can actually install the skill for free for claw code, code, open code, open code, integrity. Once you install it, you can actually give it references, which are already there. And just ask it to build what you want, and that is how simple it is. If you want to try it out just comment on it on me and I'll send it in your DM, and don't forget to follow.

## What is shown on screen
The GitHub README for wheresryan22/anatomy ('A Claude skill that explains an idea by building it as a real, working object'), the install command npx skills add, and isometric example figures.

## Summary
The skill is real, public and MIT-licensed, installable with a single public command, so the comment-for-DM step is a pure engagement funnel. It generates editable isometric SVG and JavaScript figures, with optional WebGL and a beta 3D mode. Reports put its stars at roughly 6,500 in its first days. 'Greatest skill ever' is hype, and as with any third-party skill, read its source before installing. 'Anything, even your resume' is the creator's stretch; its documented use is technical concepts and explainers.

## Comments
Not read: Instagram requires a login to list comments. The count is 75 against 506 likes (comments/likes 0.15; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-29)

| Claim | Verdict | Evidence |
|---|---|---|
| Anatomy is an open-source Claude skill that builds isometric explainers | verified | Public repo wheresryan22/anatomy, MIT licence, generating isometric SVG and JavaScript figures with optional WebGL and a beta 3D mode |
| It installs free with one command | verified | npx skills add wheresryan22/anatomy -g -a claude-code, or clone into ~/.claude/skills/anatomy; needs a recent Node.js |
| It works in other agents such as Open Code | partly | README mentions compatibility with other agent-skill hosts; not tested |
| It can dissect anything, even a resume | unverified | Documented use is technical concepts and explainers |
| Many call it the greatest skill ever | unverified | Popularity is real (thousands of stars) but the superlative is hype |

Overall: A genuine, free, public skill; the DM gate is unnecessary. Review the source before installing.

## Notes / caveats
- 3D mode is beta.
- Third-party skills run with your agent's permissions; read the source first.
- Comments not fetched (login required).
