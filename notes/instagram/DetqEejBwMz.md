---
url: https://www.instagram.com/reel/DetqEejBwMz/
platform: instagram
type: reel
author: decoding_tech_
posted: 2026-10-20T10:51:54Z
duration_s: 139
views: not exposed
likes: 14137
comments: 2120
language: hi
queued_via: "GitHub issue #44"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, translated, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Cloudflare Code Mode MCP explained"
category: tech
subcategory: coding
usefulness: helpful
tools: ["mcp", "cloudflare", "typescript"]
key_info: "Cloudflare's Code Mode is real: its MCP server exposes the whole Cloudflare API through two tools (search and execute), where the model writes code instead of calling many tool definitions, which Cloudflare says takes about 1,000 tokens against about 1.17 million for an equivalent standard MCP server. The 'companies are moving away from MCP' headline is overstated: Code Mode still runs as an MCP server, so it optimises MCP rather than replacing it. 'Other companies are following' was not checked."
verdict: partly-verified
registry: registry/verified.md
---

# Cloudflare Code Mode MCP explained

## Caption / hashtags
> Follow and comment “link” for detailed blog 
> 
> #tech #ai #coding #technology #computerscience 
> 
>  [ Software Engineering, Software Development, Software Engineer, Programming, Coding, Technology, Tech, Web Development, Backend Development, Frontend Development, System Design, Software Architecture, Engineering, Developer, Coding Tips, Programming Tips, Tech Tips, Developer Tips, Engineering Tips, Tech Career ]

Hashtags: #tech #ai #coding #technology #computerscience.

## Hook (on-screen text)
Companies are moving away from MCP, here is the new architecture

## Call to action
Comment 'link' for the detailed blog

## Transcript (auto)
> There is a new shift in the tech industry That is, now companies are moving away from MCP And choosing completely different architecture over it We understand it in detail in 30 seconds We all know that if we want to connect an AI agent with AI tools Then we will use MCP MCP was a standard protocol On its basis, how will AI agents discover and call different tools We could do that with the help of MCP But what was the problem here? Do you think everything is going smoothly? No, let me tell you with an example If my AI tool wants me to find a customer Then our MCP will call a tool regarding that If the second query runs the second definition Then the order placed by my customer will bring it So MCP will call a tool again So what was the problem here? If a new definition comes on a large scale Then we will call a tool again and again Because of which you will add more context And you will spend more token The same problem was faced by Cloudflare On its basis, they made a completely different architecture The name of the architecture is Code Mode MCP What happens in this? You do the definition query Like I told you to find the customer and bring the order You make these definitions accessible by converting them into TypeScript API Meaning you made any query, any definition You will send it to your code box In that code box, your definition will be converted into TypeScript API And through those APIs, you can access all the endpoints of the API In Cloudflare So this particular solution is a big win for Cloudflare Because Cloudflare has thousands of API endpoints They cannot do this by bringing all the endpoints to MCP So they made a code box In which they converted a particular definition into TypeScript API Because of which instead of calling again and again to call You can access the entire API directly through a code So I found this architecture very fascinating And other companies are also following this architecture If you want to read the blog in detail Which is not written by the engineers of Cloudflare Just comment down the link of that particular blog Directly into the audience Thank you so much for watching this video

## What is shown on screen
Animated diagrams: agent calling several MCP servers (old MCP) versus an agent sending code to a code box (new MCP / Code Mode), and an example task 'find customer Rahul and get his orders'. Captions are partly garbled by OCR.

## Summary
In Hindi, the creator explains that classic MCP makes an agent call tools again and again, filling the context and spending tokens, and that Cloudflare solved this with Code Mode: tool definitions become a TypeScript API inside a sandbox, so the agent writes code to reach the thousands of Cloudflare API endpoints directly.

## Comments
Not read: Instagram requires a login to list comments. The count is 2120 against 14137 likes (comments/likes 0.15; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-21)

| Claim | Verdict | Evidence |
|---|---|---|
| Cloudflare built 'Code Mode' MCP to cut tool-call overhead | verified | Cloudflare's post 'Code Mode: give agents an entire API in 1,000 tokens' (Feb 2026) describes an MCP server for the whole Cloudflare API with two tools, search() and execute(), where the model writes code run in a sandbox; [Cloudflare docs list it](https://developers.cloudflare.com/agents/model-context-protocol/cloudflare/servers-for-cloudflare/). |
| Many tool calls bloat context and cost tokens | verified | Cloudflare's own comparison: about 1.17 million tokens for an equivalent standard MCP server versus about 1,000 with Code Mode (vendor figures). |
| Definitions are converted into a TypeScript API in a sandbox ('code box') | partly verified | Matches the design, though the Feb 2026 server has the model write JavaScript against a typed API spec in a Dynamic Worker sandbox. |
| Companies are moving away from MCP | unverified | Code Mode is delivered as an MCP server, so it is an optimisation of MCP rather than a move away; no evidence of a broad industry shift was found. |
| Other companies are following this architecture | unverified | Not checked. |

Overall: Accurate explanation of Cloudflare's Code Mode, but the 'moving away from MCP' headline overstates it.

## Notes / caveats
- The 1,000 versus 1.17 million token figures are Cloudflare's own.
- Only a Hindi transcript, OCR and frames were reviewed; the blog link is sent via comments.
- 'Not written by Cloudflare engineers' in the translated outro is probably a mistranscription of 'written by'.
