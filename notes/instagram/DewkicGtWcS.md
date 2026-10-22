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
title: "Code Mode instead of classic MCP"
category: tech
subcategory: coding
usefulness: helpful
tools: ["mcp", "cloudflare", "typescript"]
key_info: "Same story as an earlier reel (see the Cloudflare Code Mode note): Cloudflare's Code Mode and Anthropic's code-execution-with-MCP pattern are real. Anthropic's post reports 150,000 tokens down to 2,000 (98.7%) for one example, but that is a single scenario and one independent test found about 77%. The 'companies are moving away from MCP' framing is overstated, since the code still calls MCP servers. A TL;DR and alternatives are in 'Your instruction'."
verdict: partly-verified
registry: registry/verified.md
---

# Code Mode instead of classic MCP

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
Companies are quietly moving away from traditional MCP

## Call to action
Comment 'LINK' to get Cloudflare's blog post by DM

## Transcript (auto)
> There's a new shift happening in the AI industry. Companies are moving away from the traditional MCPs and picking a completely different architecture instead. Let's break it down in 30 seconds. So we all know the drill. If an AI agent wants to use the tool, you use an MCP. MCP is the standard. It's how an AI agent discovers the tools and calls them. But this technique has a fundamental problem. You would think that everything is smooth, but it's not. For example, my agent needs to find a customer. That's one tool called. Then it has to flesh the customer's order. That's a second tool called. Every single result goes back to the model before the next step starts. And every tools definition sits inside the model's context throughout the whole time. Now scale that to thousands of tools. Cloudflare hit this exact wall. So they build something they call code mode. Instead of handing the model a big list of tools, they convert the tools into TypeScript API. The model now sees just one tool, which is run code. It writes a small script and that script runs inside a lock sandbox. The in-between data never comes inside the model. Only the final answer does. And their reason is models are simply better than writing code than at calling tools directly. Anthropic published the same pattern. One example dropped 150,000 tokens to just 2,000 tokens. I found this architecture completely fascinating. If you want the complete block from Cloudflare's engineers, just comment, link, and I will DM it to you.

## What is shown on screen
Animated explainer: how MCP works (agent discovering and calling tools), the problem (every result goes back through the model, hundreds of tool schemas in context), then Code Mode (tools converted to a TypeScript API, search_db, get_order, send_email plus 997 more).

## Summary
The creator explains that classic MCP puts every tool definition in the model context and routes every tool result through the model, which does not scale to thousands of tools, and that Cloudflare's Code Mode converts tools into a TypeScript API so the model writes one script that runs in a sandbox and only the final answer returns; Anthropic is said to have published the same pattern with a 150,000 to 2,000 token example.

## Comments
Not read: Instagram requires a login to list comments. The count is 2630 against 6668 likes (comments/likes 0.39; a ratio near or above 1 usually means a prompt to comment, an inference).

## Your instruction

> Also write a tldr of this, what to use instead of mcp

TL;DR
- Problem: with classic MCP, every tool definition sits in the model's context and every tool result is sent back through the model before the next step, so cost and latency grow with the number of tools.
- Fix shown: Code Mode. Expose tools as a code API (TypeScript), give the model one run-code tool, let it write a script that runs in a sandbox, and return only the final answer. Cloudflare built this for its API, and Anthropic has published the same pattern ("Code execution with MCP", reported 150,000 to 2,000 tokens in one example).
- Caveat: it is an optimisation of MCP, not a replacement. The sandboxed code still calls MCP servers or APIs. The 98.7% saving is one example and independent tests report smaller gains (about 77% in one).

What to use instead of (or alongside) classic MCP tool-calling:
1. Code execution with MCP (this reel's pattern): the agent writes code that calls tools as functions, in a sandbox. Best when you have many tools or large intermediate data.
2. On-demand tool loading: keep MCP, but let the agent search for and load only the tool definitions it needs rather than loading them all.
3. Small, curated tool sets: expose only the handful of tools a given agent really needs.
4. Direct APIs, SDKs or CLIs called from a sandbox, without an MCP server in between, when you control both sides.
Rule of thumb: with a few tools and small results, plain MCP is fine; move to code execution when context bloat or many round trips become the problem.
(Options 2 to 4 are general engineering alternatives, not claims from the reel; only option 1 is sourced from the post and the linked articles.)

## Research (checked 2026-10-22)

| Claim | Verdict | Evidence |
|---|---|---|
| Cloudflare built Code Mode to avoid loading thousands of tools | verified | Covered in the earlier note [Cloudflare Code Mode MCP](https://developers.cloudflare.com/agents/model-context-protocol/cloudflare/servers-for-cloudflare/): its MCP server exposes the whole API through two tools where the model writes code in a sandbox. |
| Anthropic published the same pattern | verified | Anthropic's engineering post [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) describes agents writing code against tools loaded on demand. |
| One example dropped from 150,000 to 2,000 tokens (-98.7%) | verified | That figure and percentage appear in Anthropic's post for a document-transfer example, but it is one scenario; an independent benchmark reported about 77% fewer total tokens. |
| Companies are moving away from MCP | partly verified | The code runs against MCP servers or APIs, so this optimises MCP rather than abandoning it; no broad exodus was found. |

Overall: Accurate on the mechanism and sources, overstated on 'moving away from MCP' and on the typical savings.

## Notes / caveats
- The 98.7% saving is a single example from the vendor; independent results are lower.
- Running model-written code requires a properly isolated sandbox and permission controls.
- The alternatives list in 'Your instruction' beyond code execution is general engineering guidance, not from the reel.
- The reel's DM link was not followed.
