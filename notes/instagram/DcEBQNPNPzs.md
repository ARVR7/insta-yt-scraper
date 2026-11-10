---
url: https://www.instagram.com/reel/DcEBQNPNPzs/
platform: instagram
type: reel
author: kem_glitch
posted: 2026-08-15T13:44:10Z
duration_s: 146
views: not exposed
likes: 9000
comments: 677
language: en
queued_via: "GitHub issue #145"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "ok"
  video: "downloaded"
  transcript: "ok (faster-whisper, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "Knowledge graph memory vs Obsidian and graphify"
category: ai
subcategory: tools
usefulness: mixed
tools: ["graphify", "Obsidian"]
key_info: "A rebuttal to another creator's video. The speaker argues that a real knowledge graph is the most complex memory architecture, that it needs ontological and logical modelling, and that Obsidian-style wikis or graphify auto-generated YAML links are not a knowledge graph unless the agent has multi-hop traversal tooling, otherwise the agent just reads and greps files and eats context. He claims 15 years of experience with knowledge graphs in investment banks and offers help. The video is an opinion piece with no benchmark. Graphify (Graphify-Labs/graphify) is a real MIT licensed skill that builds a queryable graph from a folder (graph.json, GRAPH_REPORT.md) for agents to traverse; it does not claim to replace a hand-modelled ontology. I could not read comments."
verdict: partly-verified
registry: none
---

# Knowledge graph memory vs Obsidian and graphify

## Caption / hashtags
> We like @agentic.james but graph is not obsidian and graphify. That’s a mess! If you’re curious to learn more always happy to help! 
> #ai #artificialintelligence #aiagent

Hashtags: #ai #artificialintelligence #aiagent.

## Hook (on-screen text)
You are wrong about knowledge graphs, and here is why

## Call to action
Reach out for help; keep making videos

## Transcript (auto)
> most people use something like Obsidian with a wiki knowledge graph. You could use something like the graphify open source repo that basically helps your agent build a knowledge graph around a large set of folders and files. Now things get more complicated when you want your agent to actually remember specific. I love your agentic james. I think you're a cool dude. I think you make some awesome videos and I've seen some cool stuff and ways to put together, but you're wrong. You're wrong on this one big time. No, it doesn't get more complicated knowledge graph is the most complicated memory architecture. The reason people like you and others don't realize that is because you haven't had the benefit of 15 years plus experience implementing knowledge graph at scale in things like investment banks. Let me tell you what the issue is. You're not doing it right and I mean that respectfully. It's just frustrating seeing this stuff that I want to help right. In order for knowledge graph to work you have to ontologically and logically model and guess what? It's really hard, right? It's really hard to do. You cannot outsource this stuff to some vibe coded repo or something like obsidian which would just automatically base synthesize from some glob or something tooling right and create some rough yaml and just link everything together and it's not going to work if you have no actual multi hop traversal tooling. If you're just gripping yaml and jumping from bar to bar that is not knowledge graph that is a big fucking mess that your AI needs to read through at minimum at best. It might just be reading the yaml and jumping through things right that your praying to god have been modeled beautifully so that it can find what it needs. Of course it's going to eat up your context. That is not knowledge graph and certainly isn't knowledge graph memory architecture. I am always here to help you if you want to know how to do this stuff properly and actually experience what real knowledge graph is like, right? And if you want to look and explore the ideas of things like graph engineering which I'm not that big of a fan of but if you're curious I can also help you with that, right? Keep making awesome videos. I love them. I get a lot of inspiration. You have some really cool ideas. Don't fall for this car pathy hype and stuff. He's amazing. He's incredibly bright but he's a researcher. He comes up with vague ideas, loose ideas that are not formally tested by practitioners at scale, right? If you want to know more about it, always happy to help. Reach out Chemicalist Keck Club signing out.

## What is shown on screen
Not much; talking head with the creator's screen.

## Summary
Informed opinion that auto-built graphs and wiki links are not the same as a modelled knowledge graph. No evidence shown; the experience claim is unverified.

## Comments
Not read: Instagram requires a login to list comments. The count is 677 against 9000 likes (comments/likes 0.08; a ratio near or above 1 usually means a prompt to comment, an inference).

## Your instruction

> Research on this topic and read comments if possible, I wanna know how can this be built properly for myself and my complex project and repos

Comments could not be read without a login. How to build it properly, from the video's argument and what graphify documents: (1) split memory into two layers: a structural graph that is generated (graphify gives you AST-based nodes and edges for code, via /graphify . producing graph.json) and a curated semantic layer you model yourself (entities, relations and rules for your domain, written as a small ontology). (2) Give the agent real query tools over the graph instead of letting it grep files: expose a few operations such as find-node, neighbours, path-between and subgraph through a small MCP server or CLI, so it can do multi-hop traversal and only load the relevant slice into context. (3) Keep the always-loaded instructions short (CLAUDE.md pointing to the graph tools) and rebuild the generated layer on every commit or session end so it does not go stale. (4) Start small: model one subsystem, check the agent answers cross-file questions better than plain search, then widen. (5) Treat the video's claims as opinion and test them on your own repos; measure tokens and answer quality before and after. I did not set anything up in your repos.

## Research (checked 2026-11-09)

| Claim | Verdict | Evidence |
|---|---|---|
| Graphify is an open source tool that builds a knowledge graph of a codebase for agents | verified | Graphify-Labs/graphify, MIT, graph.json and GRAPH_REPORT.md outputs |
| Wiki links or YAML without multi-hop traversal tooling are not a real knowledge graph memory | unverified | Opinion; no benchmark given |
| 15 years of knowledge graph experience in investment banks | unverified | Self-reported |

Overall: Useful argument about what counts as a knowledge graph; no data; graphify is real.

## Notes / caveats
- Comments not readable.
- No benchmark in the video.
- Language in the video is strong.
