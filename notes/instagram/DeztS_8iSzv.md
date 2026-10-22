---
url: https://www.instagram.com/reel/DeztS_8iSzv/
platform: instagram
type: reel
author: simplyaishow
posted: 2026-10-22T19:15:14Z
duration_s: 74
views: not exposed
likes: 11
comments: 1
language: en
queued_via: "GitHub issue #59"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Harness2 reopen-your-files rule for agents"
category: ai
subcategory: tools
usefulness: helpful
tools: ["harness2", "gemini-3-5-flash", "claude-opus-4-8"]
key_info: "Harness2 (google-research/harness2) is a real open-source framework from Google Cloud AI Research that has a stronger model rewrite the prompts, guardrails and scripts around an agent without retraining it; coverage names Gemini 3.5 Flash as an agent and Claude Opus 4.8 as the editor. The reel's 43 to 78 score is described by the creator as one of the best examples, and the average gain is smaller (coverage reports up to about 11 points per step on benchmarks). The tip itself is practical and free: tell your agent to reopen every file it made and check that numbers match before it says it is done."
verdict: partly-verified
registry: registry/verified.md
---

# Harness2 reopen-your-files rule for agents

## Caption / hashtags
> Google Harness2: One Rule Took This AI Agent From 43 to 78
> 
> Google Harness2: Claude Opus 4.8 wrote one rule into Gemini 3.5 Flash's instructions, reopen every file you made, and its score on a real job went from 43 to 78.
> 
> ▶ Full Deep Dive: "Claude Rebuilt Its Own Setup and Went From 72 to 100: Google Harness2" (link in bio)
> 
> AI-narrated.
> 
> #AI #AINews

Hashtags: #ai #ainews.

## Hook (on-screen text)
Your AI agent says it is done, but did it ever reopen the files it made?

## Call to action
Watch the full deep dive on the creator's YouTube (link in bio)

## Transcript (auto)
> Your AI agent says it's done, but did it ever reopen the files it made? One rule about that nearly doubled an agent's score on a real job. The job? Turn a schedule, a crew roster, and a budget into one set of documents, every number matching. The agent, Google's Gemini 3.5 Flash, scored 43. It never checked its numbers across the files and never reopened what it wrote. So, a second AI, Claude Opus 4.8, read through that run and wrote a rule into its instructions. Before you finish, reopen every file you made. Confirming a file exists is not confirming it is correct. It added a few notes on matching numbers and a small script that does the reopening. Same model, nobody retrained it. Second run, 78. That rewriting loop is Google's free, open-source code, harness-squared. This was one of its best examples. The average gain is smaller, but the rule is yours to steal. Paste it into your own agent's instructions today. So, how does harness-squared Noah rewrite helped with no answer key? The full story? Claude rebuilt its own setup and went from 72 to 100 is on our YouTube.

## What is shown on screen
Animated explainer: 'Done. 3 files created', the job (turn a schedule, crew roster and budget into one set of documents), scores 43 then 78 out of 100, the rule 'Before you finish, reopen every file you made' written into guardrails.md, a harness diagram (system prompt, guardrails, memory, tool guidance, subagents, skills, scripts) and a verify_outputs.py script.

## Summary
The creator explains that Gemini 3.5 Flash scored 43 out of 100 on a real document-generation job because it never reopened its output files; Claude Opus 4.8 reviewed the run and added a rule to the agent's instructions (reopen every file you made; existence is not correctness) plus a small verification script, and the same model then scored 78. The rewriting loop is Google's open-source harness-squared, and the creator says the average gain is smaller.

## Comments
Not read: Instagram requires a login to list comments. The count is 1 against 11 likes (comments/likes 0.09; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-22)

| Claim | Verdict | Evidence |
|---|---|---|
| Harness2 is open-source code from Google that rewrites an agent's surrounding setup | verified | Coverage ([i-scoop](https://www.i-scoop.eu/harness2-google/)) describes google-research/harness2 (Apache 2.0, paper arXiv:2610.14224, not officially supported by Google) as rewriting prompts, guardrails, memory, skills and tool guidance around a fixed model. |
| Claude Opus 4.8 acted as the editor and Gemini 3.5 Flash as the agent | verified | Matches the coverage's description of the experiments. |
| One rule took the agent from 43 to 78 on a real job | unverified | I did not read the paper; the creator presents it as one of the best examples, and coverage reports average gains of about 11 points per step on benchmarks. |
| The reopen-every-file rule is worth adding to your own agents | partly verified | The principle (verify outputs, not just that files exist) is sound and cheap to try, but results will vary by agent and task. |

Overall: A real framework and a useful tip, with the headline number being a best case.

## Notes / caveats
- The 43 to 78 jump is a best-case example; average gains are smaller.
- I relied on secondary coverage and did not read the paper or run the code.
- The video is AI-narrated and promotes the creator's longer YouTube video.
- Benchmarks in coverage are described as directional, not independently validated.
