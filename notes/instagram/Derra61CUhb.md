---
url: https://www.instagram.com/reel/Derra61CUhb/
platform: instagram
type: reel
author: zazencodes
posted: 2026-10-19T16:24:41Z
duration_s: 127
views: not exposed
likes: 41
comments: 3
language: en
queued_via: "GitHub issue #31"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Claude Code software factory demo"
category: ai
subcategory: automation
usefulness: helpful
tools: ["claude-code"]
key_info: "A sponsored demo (by Anthropic) of a Claude Code 'software factory': a loop of spec writer, builder, review sub-agents (UX, UI, security, code quality) and an approver that merges or escalates to a human. The building blocks are real Claude Code features; the shown result is one demo and was not independently checked."
verdict: partly-verified
registry: registry/verified.md
---

# Claude Code software factory demo

## Caption / hashtags
> Here's how to build a Claude Code software factory...
> 
> Here I'm building a real feature on my production site. The factory includes subagents that review UX, UI, security and code quality. Here the factory escalated the result for me to review before merging.
> 
> Watch more in my "Build Your Own AI Software Factory with Claude Code" video on YouTube
> 
> This video is sponsored by Anthropic.
> Try Claude Code: http://clau.de/ZazenCodes
> 
> #Anthropic_Partner #ad #claudecode #subagents #codereview #aiagents #coding #softwareengineering

Hashtags: #anthropic_partner #ad #claudecode #subagents #codereview #aiagents #coding #softwareengineering.

## Hook (on-screen text)
Here's how to build a Claude Code software factory

## Call to action
Watch the full video on YouTube; try Claude Code via the sponsor link

## Transcript (auto)
> the factory works in this loop, a feature comes through the spec writer, which goes into the builder, which then gets verified by various review agents. And once those are done, if we need changes, this happens in a loop. And then we go to the approver, which either merges to main the feature, or we get a human review. And this is a system we can use repeatedly every time we want to build a new feature for our project. And we could imagine in the future, we want, you know, we can bring in data sources from the outside world. Let's see if our factory can handle this feature inside my actual website. This is my production site that we're working in right now. And now we can see we're starting to use our sub agents. Here's the first one, we're creating a spec using the spec writer background agent. And I can see our builder has just started working on this. Okay, sweet, we just went to review and we just kicked off all of our review sub agents. So these guys are representing our review, they're doing it. K, the UX round finished, the UI round finished. And they passed, but we're doing the security over here, considering, okay, that's done code review. This is, this is epic. Oh, look at this, you guys, we can even see the little icons, it's deciding if this feature should be pulled in or not. I'm actually blown away. This is the, this is how I want to develop features now. Why have I not done this yet? So what's hope is deciding, it's escalating. So I think it'll go to the human review. There it is. So it's sitting in the human review phase. And now I need to approve this, click on this. Okay, I can get all sorts of information from the dashboard escalate. Why the build is clean, every acceptance criteria for the human, if both, so here's how I would approve it, I would need to know the ID of this feature. And then I can run factory approve. Let me do that in a new session. So I'm going to clear this. And I'm going to say factory approve. And then this and we're done. It has merged it into my actual code. This is what it did. So it went off onto a branch. It did a few different commits. It kind of built out our feature. And then it merged it back. And that merge was done when I approved it. Very cool.

## What is shown on screen
Terminal and dashboard showing agents running in a loop, review stages passing, an escalation to human review and a 'factory approve' merge.

## Summary
The creator builds a feature on his production site with a pipeline of background sub-agents: a spec writer, a builder, parallel reviewers and an approver. Failures loop back to the builder; a passing build is merged or escalated for human approval. The video is marked as sponsored by Anthropic.

## Comments
Not read: Instagram requires a login to list comments. The count is 3 against 41 likes (comments/likes 0.07; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-19)

| Claim | Verdict | Evidence |
|---|---|---|
| Claude Code supports custom sub-agents with their own context, prompts and tool access | verified | Per Anthropic's [sub-agent docs](https://code.claude.com/docs/en/sub-agents), subagents run in separate context windows with custom system prompts and tool permissions; review-type agents (for example security reviewers) are a documented use. |
| A multi-agent review loop can merge features automatically | partly verified | Shown once in a demo; the factory itself is the creator's own scripting on top of Claude Code, and the quality of the merged code was not independently checked. |
| Sponsorship | disclosed | Caption states it is sponsored by Anthropic (#ad, #Anthropic_Partner). |

Overall: A genuine pattern built on documented features, presented in a sponsored demo.

## Notes / caveats
- Sponsored by Anthropic, so treat enthusiasm as marketing.
- Auto-merge on production code needs strong tests and a human escalation path, as the demo itself includes.
- Only one run was shown; reliability and cost were not measured.
