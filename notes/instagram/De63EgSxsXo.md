---
url: https://www.instagram.com/reel/De63EgSxsXo/
platform: instagram
type: reel
author: swapsays_wtf
posted: 2026-10-25T13:55:01Z
duration_s: 44
views: not exposed
likes: 3604
comments: 5590
language: hi
queued_via: "GitHub issue #79"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, translated, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Claude trader skills and trade simulator"
category: money
subcategory: investing
usefulness: mixed
tools: ["Claude Code", "day-trader-skill"]
key_info: "Claims Claude 'killed day traders': a free pack of 11 skills (chart scanner, news monitor, entry timer, exit evaluator and a 'time machine' that replays a trade 10,000 times to show outcome statistics) to use before risking money, compared to Bloomberg software costing thousands. The repo is not named; it most likely matches Jakeschincariol/day-trader-skill (an open-source 11-skill day-trading pack), but the exact skill names were not confirmed there."
verdict: partly-verified
registry: registry/verified.md
---

# Claude trader skills and trade simulator

## Caption / hashtags
> Automate your entire stock market research with Claude using all these simulations!!
> 
> Comment anything below to get the link 🖇️

## Hook (on-screen text)
Claude just killed day traders

## Call to action
Comment anything for the link and setup guide (lead magnet)

## Transcript (auto)
> Claude just killed day traders. Because before trading in the stock market, you can simulate your trade 10,000 times within Claude. This is called Trader Skill and it is completely free. There are 11 different skills in it. It scans thousands of charts and identifies potential opportunities. Second, it tracks breaking market news. And it helps in evaluating the entry and exit timing of a trade. But its most crazy part is its time machine skill. It simulates the different possible scenarios of your trade. So that you can see their potential outcomes and detailed statistics before investing money. And this is the type of software for which Bloomberg charges thousands of dollars from people. To setup this, just paste it in the link in Claude and ask it to install this skill. If you want a complete setup guide of this skill, comment anything below and I will send it to you right away.

## What is shown on screen
Slash commands /trader-scanner, /trader-news, /trader-entry, /trader-exit, /trader-timemachine; a TSLA 5-minute chart with entry 364.18, stop 358.32, target 370.04; '231 charts to 42 setups'; replay of the day x10,000 with target-first / stop-first / open-at-close outcomes.

## Summary
A free open-source pack of this kind plausibly exists and a 10,000-run replay can show how a given stop and target behave on historical price paths. But 'Claude killed day traders' and the Bloomberg comparison are hype: a backtest or replay on past data does not predict profit, most retail day traders lose money, and nothing here is evidence of an edge. Not financial advice.

## Comments
Not read: Instagram requires a login to list comments. The count is 5590 against 3604 likes (comments/likes 1.55; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-26)

| Claim | Verdict | Evidence |
|---|---|---|
| An open-source 11-skill Claude day-trading pack with chart scanning, news and entry/exit timing exists | partly | Directory listing describes Jakeschincariol/day-trader-skill with 11 skills and outcome replay; exact names (trader-timemachine etc.) not confirmed in the repo, and the reel never names it |
| Simulating a trade 10,000 times shows its potential outcomes | partly | Monte Carlo or path replays can show how stop/target interact with historical moves; they depend on assumptions and do not predict live results |
| It replaces Bloomberg software that costs thousands | misleading | Bloomberg Terminal offers real-time market data, execution and research; a skill pack that scans charts is not equivalent |
| Claude killed day traders | misleading | Hyperbole; no performance evidence is shown |
| Completely free | partly | The skill pack is free; Claude and any market data you need may not be |

Overall: Fun tool, bad framing. A simulator is not an edge. Treat as education, not signals, and paper trade first.

## Notes / caveats
- Not financial advice.
- Repo identification is a best match, unconfirmed.
- Backtests and replays overfit and ignore slippage, fees and emotions.
- Lead-magnet funnel; the repo may be public.
- Comments not fetched (login required).
