---
url: https://www.instagram.com/reel/DfpU3LeNFh_/
platform: instagram
type: reel
author: kem_glitch
posted: 2026-11-12T15:00:47Z
duration_s: 168
views: not exposed
likes: 124
comments: 29
language: en
queued_via: "GitHub issue #154"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: TODO
category: TODO
subcategory: TODO
usefulness: TODO
tools: []
key_info: "TODO"
verdict: TODO
registry: TODO
---

# TODO

## Caption / hashtags
> Does the harness improve outputs? Well, yes ..kinda when it’s raining on a Tuesday! 
> #ai #artificialintelligence #openai @nous_research @openai @anthropicai

Hashtags: #ai #artificialintelligence #openai.

## Hook (on-screen text)
TODO

## Call to action
TODO

## Transcript (auto)
> Hi friends I'm sure a lot of you have heard that the harness matters more than the model that you're using. I think that conversation conflates a couple of things. There's building a harness from scratch which is what some teams do when they run agents through the API and there's what most of us do which is scripting on top of the harness we already use. I call that a meta harness. So what we need to know is when those numbers matter and where the practical signal is for getting better outputs. So today I'm putting one model opus 5.5 inside three harnesses which are Claude code codex and Hermes and I'm going to challenge an idea from hugging face. They took lfm 2.5 which is a small 2.6 bill parameter model from liquid AI and ran it inside different harnesses. Same weights and it sold 62% of its tasks inside one and 33% inside Claude code. So before we begin let's talk about what a harness is. It's everything wrapped around the model. That's the system prompt which is just a set of instructions you never see. The tools it's allowed to use the loop that the program itself runs till the job is done and the checks it runs before it tells you it's finished. For my test I used opus in all three each in its own bucket container fully scripted. I give them the same six real bugs from sweet bench three times each and the project's own test decide what's a pass. Before I typed a single word Claude code had already sent the model about 11,000 tokens of instructions and tools and opus works completely differently in each one. Claude code gave it 26 tools and it used one which was the command line. In Hermes it used the tools it was given to search, read and edit the code and in codex it took the fewest steps and finish fastest. So what happened? Well even though they worked so differently the results were the same across the board. All three solved 16 of the 18 tasks but what did change was the speed and the bill where codex was the fastest and Hermes surprisingly was the cheapest. But one thing really did stand out is 72 runs opus reproduced the bug before changing the code twice. That's because none of the three harnesses told it to do so. So I wrote one page of extra instructions telling it how to work once more script that won't let it finish until those checks pass and on that one bug they kept getting wrong opus more than doubled its pass rate and that's the lesson. If you're building a harness from scratch to run your own agents it still really matters but for the rest of us with a model this good inside any of the leading harnesses what makes the difference in my test was the layer on top your skills your scripts and your checks that's the meta harness and it's really just files and folders. So let's keep leveling up friends chemicalist care club signing out.

## What is shown on screen
TODO

## Summary
TODO

## Comments
Not read: Instagram requires a login to list comments. The count is 29 against 124 likes (comments/likes 0.23; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-11-12)

| Claim | Verdict | Evidence |
|---|---|---|
| TODO | TODO | TODO |

Overall: TODO

## Notes / caveats
- TODO
