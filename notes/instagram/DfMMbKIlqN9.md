---
url: https://www.instagram.com/p/DfMMbKIlqN9/
platform: instagram
type: post
author: 0xsojalsec
posted: 2026-11-01T07:27:23Z
duration_s: None
views: not exposed
likes: 465
comments: 0
language: n/a
queued_via: "GitHub issue #140"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "blocked (not downloaded)"
  transcript: "none"
  on_screen_text: "n/a"
  comments: "not fetched (Instagram requires login)"
title: "Six steps to build a better agent harness"
category: ai
subcategory: automation
usefulness: helpful
tools: ["Claude Code"]
key_info: "Image post. The caption carries the text: same model, different harness, up to a 6x performance gap, and a six step method: mine past sessions for rules, delete rules you cannot prove help, keep instructions to about 100 lines that point to other rules, cut your tools, back rules with scripts (hooks, linters, tests), and garden the harness by pruning stale rules. The 6x gap comes from the Stanford, MIT and KRAFTON Meta-Harness paper, which cites it from earlier work. The claim that it was built from 57+ papers was not found."
verdict: partly-verified
registry: none
---

# Six steps to build a better agent harness

## Caption / hashtags
> Harness + Opus 5.5 can go limitless, and Stanford research showed why
> 
> Same model, Different harness. 
> Up to 6x performance gap.
> 
> This system was built from 57+ papers on how to wrap a model so it actually gets better. 
> 
> Here's how it works in 6 steps:
> 
> - Step 1: Mine your past sessions
> Every time you had to correct your agent, turn that fix into a rule.
> 
> - Step 2: Delete what you can't prove
> If a rule doesn't improve results, it's just noise eating your context.
> 
> - Step 3: Keep your instructions short
> One giant prompt fails. 
> About 100 lines that point to other rules wins.
> 
> - Step 4: Cut your tools
> Fewer, sharper tools mean higher success and fewer wasted tokens.
> 
> - Step 5: Back rules up with scripts
> Prose is a suggestion. Hooks, linters and tests are guarantees.
> 
> - Step 6: Garden your harness
> Prune stale rules and re-check everything after every big change.
> 
> The best harnesses are small, evidence-based and constantly pruned.
> 
> Opus 5.5 is the engine. 
> The harness decides how far it goes.

## Hook (on-screen text)
Harness plus Opus 5.5 can go limitless

## Call to action
None; no funnel

## Transcript (auto)
None available.

## What is shown on screen
Not available: the image slides could not be read without a login. The caption holds the six steps.

## Summary
Sound, generic advice for configuring a coding agent: short instructions, few tools, rules enforced by scripts, regular pruning. The 6x figure is real but not this post's own result.

## Comments
Not read: Instagram requires a login to list comments. The count is 0 against 465 likes (comments/likes 0.00; a ratio near or above 1 usually means a prompt to comment, an inference).

## Your instruction

> Extract what's written in the image

The image slides could not be read without a login, but the caption holds the full text, so I extracted it: the six steps are listed in key_info and the note. Send a screenshot of the image if it contains anything beyond the caption.

## Research (checked 2026-11-09)

| Claim | Verdict | Evidence |
|---|---|---|
| Same model, different harness gives up to a 6x gap | partly-verified | Meta-Harness paper (Stanford, MIT, KRAFTON) states it, citing prior work; not its own experiment |
| System built from 57+ papers | unverified | No source found |
| Short instructions, fewer tools and script-enforced rules help | partly-verified | Consistent with common agent practice; no data given in the post |

Overall: Sensible harness advice; the 6x number is borrowed from a real paper; the 57 papers claim is unverified.

## Notes / caveats
- Image slides not readable without a login.
- Comments not fetched (none on the post).
