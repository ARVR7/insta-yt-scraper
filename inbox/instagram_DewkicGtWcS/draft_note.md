---
url: https://www.instagram.com/reel/DewkicGtWcS/
platform: instagram
type: reel
author: saurabhs.builds
posted: 2026-10-21T14:01:20Z
duration_s: 70
views: not exposed
likes: 6668
comments: 2630
language: en
queued_via: "GitHub issue #55"
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
> Companies are quietly moving away from traditional MCP 👀
> 
> The problem: every tool call sends its result back through the model, and every tool’s definition sits in the model’s context the whole time. Scale that to thousands of tools and you hit a wall.
> 
> Cloudflare’s fix is Code Mode:
> → Turn the tools into a TypeScript API
> → The model sees one tool: run_code
> → It writes a small script that runs in a locked sandbox
> → Only the final answer comes back to the model
> 
> Anthropic published the same pattern. One example went from 150,000 tokens to 2,000 (-98.7%).
> 
> Comment “LINK” and I’ll DM you Cloudflare’s full blog post 🔗
> 
> #AI #MCP #AIAgents

Hashtags: #ai #mcp #aiagents.

## Hook (on-screen text)
TODO

## Call to action
TODO

## Transcript (auto)
> There's a new shift happening in the AI industry. Companies are moving away from the traditional MCPs and picking a completely different architecture instead. Let's break it down in 30 seconds. So we all know the drill. If an AI agent wants to use the tool, you use an MCP. MCP is the standard. It's how an AI agent discovers the tools and calls them. But this technique has a fundamental problem. You would think that everything is smooth, but it's not. For example, my agent needs to find a customer. That's one tool called. Then it has to flesh the customer's order. That's a second tool called. Every single result goes back to the model before the next step starts. And every tools definition sits inside the model's context throughout the whole time. Now scale that to thousands of tools. Cloudflare hit this exact wall. So they build something they call code mode. Instead of handing the model a big list of tools, they convert the tools into TypeScript API. The model now sees just one tool, which is run code. It writes a small script and that script runs inside a lock sandbox. The in-between data never comes inside the model. Only the final answer does. And their reason is models are simply better than writing code than at calling tools directly. Anthropic published the same pattern. One example dropped 150,000 tokens to just 2,000 tokens. I found this architecture completely fascinating. If you want the complete block from Cloudflare's engineers, just comment, link, and I will DM it to you.

## What is shown on screen
TODO

## Summary
TODO

## Comments
Not read: Instagram requires a login to list comments. The count is 2630 against 6668 likes (comments/likes 0.39; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-22)

| Claim | Verdict | Evidence |
|---|---|---|
| TODO | TODO | TODO |

Overall: TODO

## Notes / caveats
- TODO
