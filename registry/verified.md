# Verified tools, hacks and facts

Items that checked out against primary sources. Newest first within each section. See `.claude/skills/update-registries/SKILL.md` for the entry format.

## Verified

### LinkedIn's rules against automated tools put auto-apply bots at risk  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** LinkedIn's User Agreement prohibits automated tools and scraping, and LinkedIn has sued scrapers under that agreement and computer-fraud law.
- **How to use / why it matters:** Treat any agent that applies to jobs or messages people on LinkedIn for you as a risk to your account (restriction or termination).
- **Caveats:** The broader reading that it covers ordinary users of automation comes from a third-party analysis, not a legal ruling, and enforceability depends on jurisdiction.
- **Evidence:** [ConductAtlas analysis](https://conductatlas.com/platform/linkedin/linkedin-user-agreement/prohibition-on-scraping-and-automated-data-collection/), [TechCrunch on LinkedIn suing scrapers](https://techcrunch.com/2016/08/15/linkedin-sues-scrapers/)
- **Source note:** [notes/instagram/Dd1_GC-sJVz.md](../notes/instagram/Dd1_GC-sJVz.md)

### Grok Bot (SpaceXAI cloud agent)  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** A SpaceXAI product in beta since 11 August 2026: an AI agent that runs in the cloud, signs into software, inboxes and websites (including ones without an API) and keeps working after you close your laptop.
- **How to use / why it matters:** Available to SuperGrok Heavy, Cursor Ultra and Cursor Teams Premium subscribers on macOS, Windows, Linux and iOS (Android to follow); you create named agents with instructions and publish them.
- **Caveats:** Paid, not free; reported prices differ ($120 per team seat, $200 personal, $300 for SuperGrok Heavy). It is a beta, no official pricing page was found, and the reel is sponsored.
- **Evidence:** [Constellation Research](https://www.constellationr.com/insights/news/spacexai-launches-grok-bot-work-assistant), [Implicator](https://www.implicator.ai/spacexai-grok-bot-starts-at-120-a-seat/), [Korben](https://korben.info/en/grok-bot-launches-beta.html)
- **Source note:** [notes/instagram/Dd1_GC-sJVz.md](../notes/instagram/Dd1_GC-sJVz.md)

### FreeVideo: local MiniMax H3 (VDN-H3) video generation in ComfyUI  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** an open-source local inference engine from FlashML that generates video (and audio) with a modified MiniMax H3 model (OpenVDN's 8-step VDN-H3) on consumer GPUs, as a ComfyUI plugin plus Windows launcher and Linux CLI.
- **How to use / why it matters:** clone `FlashML-org/FreeVideo` into `ComfyUI/custom_nodes` (or use the Windows launcher / Linux `setup.sh`). Runs with as little as 8 GB VRAM and 16 GB RAM, no API key, so no per-video cost.
- **Caveats:** 8 GB / 16 GB is the minimum, so expect heavy offloading and slow generation; it is not the stock H3 model; code is Apache-2.0 but the weights fall under the MiniMax H3 Community License (territorial and acceptable-use limits); Windows and Mac builds are previews; model packs are large (about 23 GB).
- **Evidence:** [GitHub: FlashML-org/FreeVideo](https://github.com/FlashML-org/FreeVideo), [ComfyUI Wiki](https://comfyui-wiki.com/en/news/2026-10-04-freevideo-h3), [ZimaSpace on 8 GB limits](https://shop.zimaspace.com/blogs/tech-ai-hub/running-minimax-h3-locally-hardware-comfyui-and-a-self-hosted-ai-video-setup)
- **Source note:** [notes/instagram/DeSArmKIhid.md](../notes/instagram/DeSArmKIhid.md)

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

### Grok Bot agents swipe Tinder, win airline refunds and buy concert tickets  (2026-10-17)
- **Verdict:** unverified
- **What it is:** The reel's claims about what its example agents accomplish.
- **Why pending:** The screen shows only agent descriptions and a publish screen, never a completed swipe, refund or ticket purchase. The on-screen flight agent only hunts cheap fares and the event agent only flags nights. Tinder's terms on automation were not checked.
- **To resolve:** A screen recording of a finished run for each task, and Tinder's current terms on bots and automation.
- **Source note:** [notes/instagram/Dd1_GC-sJVz.md](../notes/instagram/Dd1_GC-sJVz.md)

### Arnold's best tricep exercise (PumpCrib short)  (2026-10-17)
- **Verdict:** unverified
- **What it is:** Short titled 'ARNOLD explains the BEST tricep exercise!'
- **Why pending:** Video and audio could not be fetched, so the named exercise was never read.
- **To resolve:** Paste the transcript or watch the source video at 6515s.
- **Source note:** [notes/youtube/R4yihx8sEO8.md](../notes/youtube/R4yihx8sEO8.md)

### FreeVideo gives 4K output with top speed and quality on 8 GB  (2026-10-17)
- **Verdict:** unverified
- **What it is:** the reel's "Free Unlimited 4K" banner and the claim that generation speed and quality are "number one" on 8 GB cards.
- **Why pending:** the README says it unlocks 2K and 4K, but no benchmark or sample quality evidence for 8 GB was found, and third-party guides say low-VRAM setups are slow and softer.
- **To resolve:** timings and output samples from an independent 8 GB user.
- **Source note:** [notes/instagram/DeSArmKIhid.md](../notes/instagram/DeSArmKIhid.md)

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
