---
url: https://www.instagram.com/reel/Dfhog8VtWDx/
platform: instagram
type: reel
author: kem_glitch
posted: 2026-11-09T15:18:06Z
duration_s: 174
views: not exposed
likes: 217
comments: 40
language: en
queued_via: "GitHub issue #149"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "APIS plan implement verify loop for AI coding"
category: ai
subcategory: automation
usefulness: helpful
tools: ["Claude Code", "BMAD"]
key_info: "The creator's workflow, the APIS methodology: align, plan, implement, verify in a loop. Align: talk through what to build and not build, find reference projects. Plan: a planning skill maps the codebase conventions, researches current docs and gotchas, gives every task a validation command, sets checks at five levels (lint, unit, integration, manual walkthrough, extras) and defines the orchestration. Implement: in a fresh window an execution skill runs the plan; the orchestrator writes no code, writes a strict brief for each subagent and checks what they return against the actual files. Verify: a verification skill drives the app; anything wrong goes back to align, never patched. For bigger team builds he suggests BMAD (Brian Madison), free and open source, with agents for research, requirements, design, architecture and build and a written record such as brief, PRD and architecture. The advice is process opinion with no benchmark."
verdict: partly-verified
registry: none
---

# APIS plan implement verify loop for AI coding

## Caption / hashtags
> How I develop with AI and when I look for something more robust. 
> #ai #artificialintelligence #openai

Hashtags: #ai #artificialintelligence #openai.

## Hook (on-screen text)
How I develop with AI and when I need something more robust

## Call to action
Keep it simple and keep levelling up

## Transcript (auto)
> Hi friends, people ask me how I develop with AI. Today, I'll show you what I do and what I reach for when that's not enough. I follow what I call the apis methodology, which is a line plan implement and verify in a loop. It begins with intent, right, alignment. Before any code, I talk through with the model in the session, what we're building and what we're not. It's a bit like map PoCock's Gromy skill. This is where most of the work happens because the aim is for the model to genuinely understand what I'm after. Often that means finding good references like the look and feel of maybe an older project or an open source one that already does it well. When I'm happy, I trigger my planning skill in the same session on an existing code base. It would map the structure, the conventions and the patterns to copy. Then it researches the latest docs, best practices and known gotchas before it writes a word. Every task carries its own validation command and the plan sets checks at five levels from linting, unit test integration, a manual walkthrough and any extra tours. And it defines the orchestration. That is how the build runs and the effort every build a reviewer and grader work app. Once the plan's on record, I sometimes review it but often don't. I open a fresh window and I run my execution skill with the plan argument. It's orchestrated writes no code. It manages the build, writes a strict brief for each sub agent and checks everything they return against the actual files. At the end, I verify the way I use a word through a verification skill that drives the app with tooling I set up for it. Anything that's off goes back to the align. I never patch it. It's a loop. Mostly that's all I need. When it isn't, I may use an extended version with extra steps like enumeration or I look to something like be mad by Brian Madison. It's free open source. It gives you a team of agents that own different parts of the development life cycle from research and requirements gathering to design architecture and the build itself. I wouldn't reach for be mad for everything. There's certainly not small changes but for a bigger build or when a whole team has to agree on what's being built, it's definitely worth considering. AI tends to turn unstated assumptions into code and be mad makes the important decisions explicit, leaving a written record at each step like the brief, PRD and architecture. I don't usually bring up other methods but be mad has come a long way since it's all the more rigid days and it's definitely worth a look. More importantly, keep it simple, stupid and keep leveling up friends. ChemicalsCatClub signing out.

## What is shown on screen
Not read.

## Summary
A clear, practical agent workflow. Based on experience, not measured. BMAD was not checked in this run.

## Comments
Not read: Instagram requires a login to list comments. The count is 40 against 217 likes (comments/likes 0.18; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-11-09)

| Claim | Verdict | Evidence |
|---|---|---|
| Plan, implement, verify with per-task validation commands improves results | unverified | Reasonable practice; no data given |
| BMAD is a free open source multi-agent method by Brian Madison | unverified | Not checked in this run |

Overall: Useful workflow description; unmeasured.

## Notes / caveats
- BMAD not checked.
- Comments few.
