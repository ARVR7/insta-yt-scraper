---
url: https://www.instagram.com/reel/De95N60JYG2/
platform: instagram
type: reel
author: charlieautomates
posted: 2026-10-26T18:16:08Z
duration_s: 90
views: not exposed
likes: 378
comments: 635
language: en
queued_via: "GitHub issue #83"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "BASE second brain for Claude Code vs Graphify"
category: ai
subcategory: tools
usefulness: mixed
tools: ["Claude Code", "BASE", "Graphify", "Obsidian"]
key_info: "Pitch for BASE, a Claude Code second-brain setup: SessionStart hooks load your projects at the start of each session, keyword-matched knowledge domains pull in relevant files per prompt, and a local dashboard (localhost:3741) shows domains, rules and decisions. The creator says Graphify burns tokens and Obsidian is view-only. Playbook and links are behind a comment-BASE lead magnet."
verdict: pending
registry: registry/verified.md
---

# BASE second brain for Claude Code vs Graphify

## Caption / hashtags
> Comment “BASE” for the playbook and all links
> 
> Setting up a Claude Code second brain this week?
> 
> Watch this first.
> 
> The popular stack looks great on the outside.
> Graphify eats tokens. Obsidian only shows the graph.
> 
> The real problem: nothing feeds Claude on its own.
> 
> BASE does.
> Hooks pull your projects in at session start.
> Domains match keywords to file paths.
> A local dashboard tracks it all.
> 
> #ClaudeCode
> #AIAgents
> #Tech
> #Coding
> #Automation

Hashtags: #claudecode #aiagents #tech #coding #automation.

## Hook (on-screen text)
Don't set up a Claude Code second brain until you watch this

## Call to action
Comment BASE for the playbook and all links

## Transcript (auto)
> If you're using cloud code and want to set up a second brain, watch this video first. 99% of you are rushing to set up obsidian and graphify. And on the outside, it looks great, but here's why you should reconsider this stack. First off, graphify takes a ton of tokens to work through all the files in your workspace. It also requires you to manually carry data in that second brain instead of automatically integrating with your daily cloud use. Plus, in this stack, obsidian is just used to visually show you the brain. Instead of it actually being a core function of the brain. So here's what you should be doing instead. Set up something called base. It creates the knowledge graph, aka second brain, you want directly inside of cloud, and it uses something called hooks to automatically pull all your projects into awareness at session start. Then it selectively uses knowledge domains via keyword matching to connect file paths to all of your other relevant files depending on the conversation you're having. So unlike graphify, it's super cost effective on token use. Only pulling contacts on what's presently being discussed without having to ask. And it self-learns every session, so no blasting your whole subscription in one go. And base comes with a local host second brain viewer and dashboard to track all of your knowledge domains, rules, decisions, and accumulated knowledge over time. So if you're somebody looking to cut through the noise on what a second brain should actually do for their cloud, common base, and I'll send you over the playbook and all links.

## What is shown on screen
Graphify and Obsidian shown with a usage meter filling up; BASE graph (29,086 nodes, 84,814 edges), SessionStart hook output listing handoffs, UserPromptSubmit domain matching (52 domains, 237 rules), localhost dashboard.

## Summary
The hook-based approach (SessionStart plus keyword-matched context injection) is a plausible pattern that Claude Code hooks support. But BASE itself could not be found in public search, so the product, its token savings and the criticism of Graphify are the creator's own claims. Graphify is real and has a mixed record on token savings. The funnel is a comment-for-link lead magnet.

## Comments
Not read: Instagram requires a login to list comments. The count is 635 against 378 likes (comments/likes 1.68; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-27)

| Claim | Verdict | Evidence |
|---|---|---|
| Graphify takes a lot of tokens to build the graph | partly | Graphify uses Claude for non-code docs and images, so building can cost tokens; independent write-ups report large per-query savings afterwards but also that small projects may not benefit |
| Obsidian is only a viewer in that stack | partly | A framing choice by the creator; Obsidian can also store and edit notes, but it does not feed Claude by itself |
| BASE uses hooks to load projects at session start and matches keywords to files | unverified | Plausible with Claude Code SessionStart and UserPromptSubmit hooks, as seen on screen; BASE not found in public search |
| BASE is far cheaper on tokens than Graphify | unverified | No benchmark shown; the usage meters on screen are illustrative |
| Local dashboard shows domains, rules and decisions | unverified | Shown at localhost:3741 in the demo; not independently checked |

Overall: Interesting pattern, unproven product. Treat the token claims as unverified and expect a funnel for the playbook.

## Notes / caveats
- BASE not found in public search; claims come only from the creator.
- Playbook and links are behind a comment-keyword lead magnet.
- Comments not fetched (login required).
