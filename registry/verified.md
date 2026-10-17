# Verified tools, hacks and facts

Items that checked out against primary sources. Newest first within each section. See `.claude/skills/update-registries/SKILL.md` for the entry format.

## Verified

### Higgsfield MCP connector and "Katana" skill for Claude  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** Higgsfield's MCP server for Claude (`https://mcp.higgsfield.ai/mcp`) and "Katana", a skill that rebuilds a reference video (yours or a library preset) with up to five of your photos into a new MP4.
- **How to use / why it matters:** in Claude, Settings → Connectors → add a custom connector with that URL, sign in to Higgsfield, then ask for `/katana` or describe the edit. No separate API key.
- **Caveats:** it spends credits from a Higgsfield plan and an active subscription is required, so it is not free. Instagram/TikTok profile links are not accepted as references; moderation may decline some generations. Claude shows the credit cost before each generation.
- **Evidence:** [Higgsfield blog: Katana](https://higgsfield.ai/blog/higgsfield-katana), [Higgsfield MCP](https://higgsfield.ai/mcp)
- **Source note:** [notes/instagram/DegLPFbTBpi.md](../notes/instagram/DegLPFbTBpi.md)

### YouTube demonetizes mass-produced / template-based AI content  (2026-10-17)
- **Verdict:** verified
- **What it is:** YouTube's Partner Program policy "inauthentic content" (renamed from "repetitious content", clarified 15 July 2025) makes mass-produced, template-looking and unoriginal AI-generated content ineligible for monetization. AI assistance on original, well-researched videos is allowed.
- **Why it matters:** any "fully automated faceless channel" pipeline is exposed to this policy risk; monetization is not guaranteed.
- **Evidence:** [YouTube Help: YPP policies](https://support.google.com/youtube/answer/1311392)
- **Source note:** [notes/instagram/DeToMLxtdSV.md](../notes/instagram/DeToMLxtdSV.md)

### edge-tts (Python library for Microsoft Edge's online TTS)  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** a Python module and CLI that uses the Edge read-aloud TTS service with no API key, Windows or Edge install.
- **How to use / why it matters:** `pip install edge-tts`, then `edge-tts --text "..." --write-media out.mp3`. Free, many voices, word-level timing.
- **Caveats:** it is an unofficial client of an undocumented Microsoft service, so it can break or be blocked; custom SSML was dropped in v5 because Microsoft stopped allowing it. Check the licence terms of the voices before commercial use.
- **Evidence:** [PyPI: edge-tts](https://pypi.org/project/edge-tts), [GitHub: rany2/edge-tts](https://github.com/rany2/edge-tts)
- **Source note:** [notes/instagram/DeToMLxtdSV.md](../notes/instagram/DeToMLxtdSV.md)

### Pexels API (free stock photos and videos)  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** a free API for stock photos and video with an API key.
- **Caveats:** default limit 200 requests/hour and 20,000/month; higher limits are free if you show attribution ("Photo by X on Pexels"); caching responses for ~24h is recommended.
- **Evidence:** [Pexels Help: Is the Pexels API free to use](https://help.pexels.com/hc/en-us/articles/47677890260761-Is-the-Pexels-API-free-to-use), [Pexels API](https://pexels.com/api)
- **Source note:** [notes/instagram/DeToMLxtdSV.md](../notes/instagram/DeToMLxtdSV.md)

### Google Gemini API free tier  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** a free tier of the Gemini API usable with an API key from Google AI Studio.
- **Caveats:** limits (requests per minute/day, tokens) are per model, change often, and secondary sources disagree on the numbers; some models were reported removed from the free tier in 2026. Read the current numbers in AI Studio. Free-tier data may be used by Google to improve products.
- **Evidence:** [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- **Source note:** [notes/instagram/DeToMLxtdSV.md](../notes/instagram/DeToMLxtdSV.md)

## Pending verification

### One prompt makes a full 15 s motion-graphics piece, no After Effects (Higgsfield Katana)  (2026-10-17)
- **Verdict:** unverified
- **What it is:** the reel's claim that a single prompt to Claude via Katana produced the kinetic-type animation shown.
- **Why pending:** Higgsfield describes Katana as a reference-based video editing skill, not prompt-only motion graphics, and the reel never shows a generation, only playback on a laptop.
- **To resolve:** a screen recording of an actual Katana run, or Higgsfield documentation of prompt-only motion graphics.
- **Source note:** [notes/instagram/DegLPFbTBpi.md](../notes/instagram/DegLPFbTBpi.md)

### "YouTube AI Agent Studio" GitHub repo (`youtube-agentic-ai-studio`)  (2026-10-17)
- **Verdict:** unverified
- **What it is:** an MIT-licensed Python pipeline shown in the reel's screen recording: Gemini research and scripts, Edge TTS voice, Pexels footage, Ken Burns animation, Shorts cut, local approval dashboard, YouTube auto-upload, 8-model fallback chain.
- **Why pending:** two web searches for the exact name and tagline found no repo with that name. The owner name in the screen recording is not legible and the creator only gives the link via a comment-for-DM funnel. Similar real projects exist (for example [YouTube Factory Pipeline on PyPI](https://pypi.org/project/youtube-factory-pipeline/0.4.0/)), so the category is real; this specific repo is not confirmed.
- **To resolve:** get the repo URL from the user (comment on the reel) and read its README and source.
- **Source note:** [notes/instagram/DeToMLxtdSV.md](../notes/instagram/DeToMLxtdSV.md)
