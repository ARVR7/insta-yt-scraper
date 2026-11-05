---
url: https://www.instagram.com/reel/DfUiikfxHPG/
platform: instagram
type: reel
author: ai.with.etqad
posted: 2026-11-04T13:17:14Z
duration_s: 21
views: not exposed
likes: 929
comments: 2423
language: hi
queued_via: "GitHub issue #123"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, translated, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "AI coding assistant workflow setup"
category: ai
subcategory: tools
usefulness: mixed
tools: ["Claude Code", "Codex", "Cursor", "MCP", "sub-agents"]
key_info: "The reel argues that prompting an AI coding assistant is not enough and you should build a workflow around it: project instructions the assistant always reads, skills, sub-agents, MCP servers, memory, and checks or hooks. The on-screen examples are a DECISIONS.md log of session decisions and the Claude Code permission modes (manual approval, plan, auto) plus an effort setting. The author's own 'setup guide' is gated behind sharing the reel in a DM, which is engagement bait. Whether the guide is any good is unverified."
verdict: partly-verified
registry: registry/verified.md
---

# AI coding assistant workflow setup

## Caption / hashtags
> 📩 SHARE this Reel in DM to get my Setup Guide.
> 
> If you're still just prompting AI to write your code, you're not losing the race. You're not even in it.
> 
> Using AI well today doesn't mean typing better prompts. It means building a workflow around your coding assistant.
> 
> The difference is huge:
> ❌ Prompting: you explain everything from scratch every time
> ✅ Workflow: your assistant already knows your project, your rules, and how you like to work
> 
> ❌ Prompting: you copy, paste, and hope it works
> ✅ Workflow: your setup has tools, commands, and checks built in
> 
> ❌ Prompting: AI is a chatbot
> ✅ Workflow: AI is a teammate
> 
> Whether you use Claude Code, Codex, or Cursor, the setup is what separates people who dabble with AI from people who ship with it.
> 
> I've put together a setup guide, inspired by my own workflow, to help you build yours.
> 
> 📩 SHARE this Reel in DM and I'll send you the guide. Follow for more content like this!
> 
> Keywords: AI coding assistant, Claude Code, Codex, Cursor, AI coding workflow, developer workflow, agentic coding, AI for developers, prompt engineering, software engineering, developer productivity, vibe coding, AI tools for engineers, coding setup, tech careers
> 
> #claude #hiring #viral #trending #ai

Hashtags: #claude #hiring #viral #trending #ai.

## Hook (on-screen text)
If you only prompt your coding assistant, you are using it wrong

## Call to action
Share this reel in DM to get the setup guide, and follow

## Transcript (auto)
> Bro, if you are still coding from AI to prompt, then you are not losing the race, you are not in the race at all. If you really want to use AI in today's time, then make a workflow setup of your coding assistant. In that, scale, sub-agents, MCPs, memory, integrate everything, bro. And how to do it, I have made a setup guide for that which is inspired from my own setup. You share this reel with me and I will send it to you, so that the content is relevant, so follow it.

## What is shown on screen
Claude Code screens showing a DECISIONS.md session log and the Manual, Plan and Auto permission modes with an effort setting, over meme captions about not being in the race.

## Summary
The advice is sound and matches how Claude Code, Codex and Cursor are documented: persistent project instructions, skills, sub-agents, MCP tools, memory and hooks. The author's guide itself could not be seen because it is gated behind a share-in-DM prompt.

## Comments
Not read: Instagram requires a login to list comments. The count is 2423 against 929 likes (comments/likes 2.61; a ratio near or above 1 usually means a prompt to comment, an inference).

## Your instruction

> How do I do this

You can build the workflow yourself without the gated guide. For Claude Code: (1) put a CLAUDE.md in your repo root with your project facts, commands, conventions and rules, so the assistant starts every session knowing them; (2) add skills (folders with a SKILL.md under .claude/skills) for repeatable procedures; (3) define sub-agents (markdown files under .claude/agents) for focused jobs such as review or research; (4) connect tools through MCP servers (claude mcp add) such as GitHub or a database; (5) add hooks in .claude/settings.json to run checks or formatters automatically; (6) keep a DECISIONS.md or similar log so later sessions know why choices were made; (7) use plan mode before big edits and set permission modes deliberately. Cursor and Codex have equivalents (rules files, AGENTS.md, MCP). Start with CLAUDE.md and one or two skills, then add the rest as you hit repeated problems; check Anthropic's Claude Code docs for the exact file formats.

## Research (checked 2026-11-05)

| Claim | Verdict | Evidence |
|---|---|---|
| Coding assistants like Claude Code support project instructions, skills, sub-agents, MCP servers and hooks | verified | These are documented Claude Code features (CLAUDE.md, skills, sub-agents, MCP, hooks, permission modes) |
| A workflow setup beats prompting alone | partly | Reasonable practice and widely recommended, but an opinion; no measured evidence in the reel |
| The author's setup guide is worth getting | unverified | Guide not seen; it is gated behind sharing the reel in a DM |

Overall: Sound general advice; the specific guide is gated and unverified.

## Notes / caveats
- Comments not fetched (login required).
- Setup guide not seen.
- Engagement-bait gate (share in DM).
