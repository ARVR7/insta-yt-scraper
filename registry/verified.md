# Verified tools, hacks and facts

Items that checked out against primary sources. Newest first within each section. See `.claude/skills/update-registries/SKILL.md` for the entry format.

## Verified

### Understand Anything (Lum1104)  (2026-10-20)
- **Verdict:** verified-with-caveats
- **What it is:** Open-source plugin that builds an interactive knowledge graph of a codebase.
- **How to use / why it matters:** In Claude Code: /plugin marketplace add <owner>/Understand-Anything, /plugin install understand-anything, then /understand.
- **Caveats:** Repo is hosted under more than one owner; LLM cost on large repos is not stated.
- **Evidence:** [Understand Anything repo](https://github.com/Lum1104/Understand-Anything)
- **Source note:** [notes/instagram/Deqni2Tic2N.md](../notes/instagram/Deqni2Tic2N.md)

### RAG-Anything (HKUDS)  (2026-10-19)
- **Verdict:** verified-with-caveats
- **What it is:** Open-source multimodal document RAG framework built on LightRAG, using a multimodal knowledge graph.
- **How to use / why it matters:** pip install raganything; configure a parser and models.
- **Caveats:** Needs MinerU and LibreOffice for some formats; results are the authors' benchmarks.
- **Evidence:** [RAG-Anything paper](https://arxiv.org/html/2510.12323v1)
- **Source note:** [notes/instagram/DegUW7YG_O1.md](../notes/instagram/DegUW7YG_O1.md)

### Claude Code sub-agents for review pipelines  (2026-10-19)
- **Verdict:** verified-with-caveats
- **What it is:** Custom sub-agents with separate context and tool permissions, usable for reviewers like security and code quality.
- **How to use / why it matters:** Define agents as Markdown files in .claude/agents or via the /agents command.
- **Caveats:** The 'factory' orchestration shown is the creator's own build; sponsored demo.
- **Evidence:** [Claude Code sub-agent docs](https://code.claude.com/docs/en/sub-agents)
- **Source note:** [notes/instagram/Derra61CUhb.md](../notes/instagram/Derra61CUhb.md)

### ComfyUI local generation engine  (2026-10-19)
- **Verdict:** verified-with-caveats
- **What it is:** Open-source node-based engine for image, video and audio generation on local hardware.
- **How to use / why it matters:** Install ComfyUI from the Comfy-Org GitHub repository and load a model.
- **Caveats:** Needs a capable GPU; model licences vary.
- **Evidence:** [Wikipedia on ComfyUI](https://en.wikipedia.org/wiki/ComfyUI)
- **Source note:** [notes/instagram/Derp4yJoTmP.md](../notes/instagram/Derp4yJoTmP.md)

### n8n as a free Zapier alternative  (2026-10-19)
- **Verdict:** verified-with-caveats
- **What it is:** Workflow automation that is free to self-host.
- **How to use / why it matters:** Self-host n8n on a server or VPS.
- **Caveats:** Server costs and setup effort; fewer prebuilt integrations than Zapier.
- **Evidence:** [Hostinger comparison](https://www.hostinger.com/uk/tutorials/n8n-vs-zapier/)
- **Source note:** [notes/instagram/Dd4PDA1xYuc.md](../notes/instagram/Dd4PDA1xYuc.md)

### Cline as a free Cursor alternative  (2026-10-19)
- **Verdict:** verified-with-caveats
- **What it is:** Open-source VS Code extension for AI coding; bring your own model API key.
- **How to use / why it matters:** Install the Cline extension in VS Code and add an API key.
- **Caveats:** You pay for model usage; Cursor is more polished for inline completion.
- **Evidence:** [Fast.io on Cline](https://fast.io/resources/open-source-cursor-alternative/)
- **Source note:** [notes/instagram/Dd4PDA1xYuc.md](../notes/instagram/Dd4PDA1xYuc.md)

### Gemini Omni free video generation in Google Vids  (2026-10-18)
- **Verdict:** verified-with-caveats
- **What it is:** Free AI video generation with Gemini Omni for personal Google accounts via vids.new.
- **How to use / why it matters:** Go to vids.new and choose Create AI videos.
- **Caveats:** 1080p on the free tier is disputed (one test saw 720p); SynthID watermark; limits not stated.
- **Evidence:** [Android Authority](https://androidauthority.com/free-gemini-omni-videos-3695658), [Cryptopolitan](https://www.cryptopolitan.com/gemini-omni-paywall-google-vids-free-1080p/)
- **Source note:** [notes/instagram/Ddvk-Dxgc8z.md](../notes/instagram/Ddvk-Dxgc8z.md)

### HyperFrames (HTML to video for AI agents)  (2026-10-18)
- **Verdict:** verified-with-caveats
- **What it is:** Open-source renderer from HeyGen that turns HTML/CSS/GSAP compositions into video, driven by coding agents.
- **How to use / why it matters:** Add the skill with npx skills add heygen-com/hyperframes and let an agent build scenes as HTML.
- **Caveats:** Renders on a single machine; details from secondary sources.
- **Evidence:** [MindStudio explainer](https://www.mindstudio.ai/blog/what-is-hyperframes-html-video-renderer-ai-agents)
- **Source note:** [notes/instagram/DeGKrmWh89C.md](../notes/instagram/DeGKrmWh89C.md)

### Krea MCP connector for Claude  (2026-10-18)
- **Verdict:** verified-with-caveats
- **What it is:** Hosted MCP server for image and video generation inside Claude.
- **How to use / why it matters:** Claude Settings, Connectors, add custom connector, paste https://api.krea.ai/mcp, sign in to Krea.
- **Caveats:** Uses Krea compute allowance; sign-in required.
- **Evidence:** [Krea MCP docs](https://www.krea.ai/docs/developers/mcp.md)
- **Source note:** [notes/instagram/Dc36DK9zjdV.md](../notes/instagram/Dc36DK9zjdV.md)

### Oracle Cloud Always Free Ampere A1 instance  (2026-10-18)
- **Verdict:** verified-with-caveats
- **What it is:** Free VM.Standard.A1.Flex allowance equal to 4 OCPUs and 24 GB RAM, plus 200 GB block storage.
- **How to use / why it matters:** Sign up for Oracle Cloud and create an A1 Flex instance in the home region.
- **Caveats:** Idle instances can be reclaimed; capacity can be unavailable; a reported 2026 reduction to 2 OCPUs/12 GB is unconfirmed.
- **Evidence:** [Oracle Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/resourceref.htm)
- **Source note:** [notes/instagram/DemUJJRJjM1.md](../notes/instagram/DemUJJRJjM1.md)

### Ssemble AI clipping tool  (2026-10-18)
- **Verdict:** verified-with-caveats
- **What it is:** Web tool that cuts a long YouTube video into short clips.
- **How to use / why it matters:** Paste a YouTube link, pick clip length and captions, generate and schedule.
- **Caveats:** Free plan unconfirmed; paid from about $7.50 per month.
- **Evidence:** [Ssemble blog](https://www.ssemble.com/da/blog/best-ai-clipping-tools-2026)
- **Source note:** [notes/instagram/DenEaIdxmZk.md](../notes/instagram/DenEaIdxmZk.md)

### Free AI tool tiers (Gemini, FishAudio, ArtFlow)  (2026-10-18)
- **Verdict:** verified-with-caveats
- **What it is:** Free plans exist for all three tools shown in the reel.
- **How to use / why it matters:** Sign up on each vendor's site; free usage is credit-limited.
- **Caveats:** FishAudio free plan is personal use only per the vendor; limits change often.
- **Evidence:** [Fish Audio voice cloning](https://fish.audio/voice-clone), [ArtFlow listing](https://similarlabs.com/de/p/artflow-ai)
- **Source note:** [notes/instagram/DafrdobMFBG.md](../notes/instagram/DafrdobMFBG.md)

### Whop clipping: pay per 1,000 verified views  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** On Whop's Content Rewards, brands set a rate per 1,000 views and a total budget; clippers post short clips of the brand's or creator's content and are paid for verified views.
- **How to use / why it matters:** Join a campaign on Whop, read its rules, post clips to TikTok, Instagram or YouTube Shorts and submit them for verification.
- **Caveats:** Rates reported at $0.20-6 per 1,000 views with an average near $1; beginners typically earn $100-500 a month; budgets are finite, bot-inflated views get you banned, and figures come from clipping-tool vendors rather than Whop.
- **Evidence:** [Elev8or](https://www.elev8or.io/blog/whop-clipping), [OpenClip](https://openclip.app/guides/how-much-do-clippers-make), [Postiz](https://postiz.com/blog/whop-clipping-how-to-make-money-automate-it)
- **Source note:** [notes/instagram/DemnycCjEYg.md](../notes/instagram/DemnycCjEYg.md)

### OpenShorts (self-hosted AI video clipper)  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** An MIT-licensed tool that turns long videos into vertical 9:16 shorts with face-tracked cropping, captions and optional AI features; includes an MCP endpoint for agents.
- **How to use / why it matters:** Clone github.com/mutonby/openshorts and run it with Docker on a machine with 8 GB RAM or more; add your own Gemini, ElevenLabs and fal.ai API keys for the AI features.
- **Caveats:** Self-hosting is free but needs your own API keys (README: about $0.65 per video low-cost, about $2 premium); roughly 5 to 8 minutes per 8-minute video on CPU. The hosted version has a free plan with a watermark and 20 minutes a month, paid from $12 a month.
- **Evidence:** [GitHub: mutonby/openshorts](https://github.com/mutonby/openshorts)
- **Source note:** [notes/instagram/Demp5EUT6GV.md](../notes/instagram/Demp5EUT6GV.md)

### Google AI Pro includes premium Colab (A100 80GB)  (2026-10-17)
- **Verdict:** verified-with-caveats
- **What it is:** Google AI Pro plans now include premium Colab benefits with A100 80GB GPU access (Ultra adds H100s), announced by Google's Gemma account on 9-10 October 2026.
- **How to use / why it matters:** Subscribe to Google AI Pro (in India, claim the free 18 months through MyJio if you are an eligible Jio user), then pick the A100 runtime in Colab to run or fine-tune Gemma-class models.
- **Caveats:** Runs on Colab compute units (one source says 200 a month), hardware is not guaranteed, and the announcement is only confirmed through the Gemma post and secondary coverage, not an official page I read.
- **Evidence:** [AI Post Hub](https://www.aiposthub.com/google-ai-pro-colab-a100-80gb-gemma-experiments/), [Inside](https://www.inside.com.tw/article/42497-google-ai-pro-colab-200-compute-units-a100-cli), [Gulf News on Jio's 18 months](https://gulfnews.com/technology/companies/google-and-jio-launch-free-18-month-ai-pro-access-for-millions-in-india-1.500328266)
- **Source note:** [notes/instagram/DemHB0GhG_R.md](../notes/instagram/DemHB0GhG_R.md)

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

### Meta Muse will create 1000+ millionaires  (2026-10-20)
- **Verdict:** unverified
- **What it is:** A quoted prediction (attributed to Greg Isenberg) that Meta's Muse AI will make 1000+ millionaires, used to promote a free guide on earning with it.
- **Why pending:** The product exists, but a prediction is not evidence of earnings, and the guide is only available via comment-for-DM.
- **To resolve:** Independent reports of people earning from Meta Muse, or the guide's contents.
- **Evidence:** [Muse Spark launch coverage](https://pureai.com/articles/2026/04/09/meta-launches-muse-spark.aspx)
- **Source note:** [notes/instagram/DesCGsjTQcy.md](../notes/instagram/DesCGsjTQcy.md)

### Faceless channel on trending Netflix shows ($3,078 in a month)  (2026-10-20)
- **Verdict:** unverified
- **What it is:** Creator claims an unnamed small channel earned $3,078 in one month by posting faceless videos about a new Netflix show.
- **Why pending:** No channel is named or shown, so the earnings cannot be checked; the viewership of the show itself is roughly correct (about 12.2M views in three days).
- **To resolve:** A named channel with public view counts or an independent report of its earnings.
- **Evidence:** [TheWrap on the show's debut viewership](https://www.thewrap.com/monster-the-ed-gein-story-menendez-netflix-ratings/)
- **Source note:** [notes/instagram/DeuNjnMEVux.md](../notes/instagram/DeuNjnMEVux.md)

### 'Darkest uncensored ChatGPT' (hitansh.exee)  (2026-10-19)
- **Verdict:** unverified
- **What it is:** Unnamed uncensored chatbot pitched with a money-laundering example, link by DM.
- **Why pending:** No tool named, nothing demonstrated, link only by DM.
- **To resolve:** Ask for the tool's name and a public URL; do not follow DM links.
- **Source note:** [notes/instagram/DeqVUsUz1cT.md](../notes/instagram/DeqVUsUz1cT.md)

### 20 free sites list (anurag.builds)  (2026-10-19)
- **Verdict:** unverified
- **What it is:** Carousel promising 20 free sites for students and developers.
- **Why pending:** Slides not captured, so no site was read.
- **To resolve:** Provide slide screenshots or text, then check each site.
- **Source note:** [notes/instagram/Deo0IRdNC-S.md](../notes/instagram/Deo0IRdNC-S.md)

### AI tools carousel (power.ai)  (2026-10-19)
- **Verdict:** unverified
- **What it is:** Carousel of AI tools credited to Linus Ekenstam, links sent by DM.
- **Why pending:** Slides not captured.
- **To resolve:** Provide slide screenshots or text, then check each tool.
- **Source note:** [notes/instagram/DedHV-3lel2.md](../notes/instagram/DedHV-3lel2.md)

### Free tiers of MiniMax Hailuo and Tencent Hunyuan video  (2026-10-19)
- **Verdict:** unverified
- **What it is:** Reel claims three AI video generators are free.
- **Why pending:** Free limits conflict across third-party sources and official pages were not checked.
- **To resolve:** Check each vendor's current pricing and free-plan page.
- **Source note:** [notes/instagram/Deqmd98M2vB.md](../notes/instagram/Deqmd98M2vB.md)

### Other swaps in the 14-tool list  (2026-10-19)
- **Verdict:** unverified
- **What it is:** Eleven further paid-to-cheaper swaps listed in the caption.
- **Why pending:** Not checked, and post images were not captured.
- **To resolve:** Check each tool's current free plan and compare features.
- **Source note:** [notes/instagram/Dd4PDA1xYuc.md](../notes/instagram/Dd4PDA1xYuc.md)

### Animation Claude skills carousel (okaashish)  (2026-10-18)
- **Verdict:** unverified
- **What it is:** Carousel and caption promoting Claude skills for animation, links sent by DM.
- **Why pending:** Slides were not captured, so the listed skills were never read.
- **To resolve:** Provide slide screenshots or text, then check each skill and link.
- **Source note:** [notes/instagram/DeOxisYD6ap.md](../notes/instagram/DeOxisYD6ap.md)

### Content creation camp carousel claims  (2026-10-18)
- **Verdict:** unverified
- **What it is:** Carousel and caption promoting a 2026 content creation system with Reels and Trial Mode promotion tips.
- **Why pending:** Slides were not captured; caption claims are self-reported.
- **To resolve:** Provide slide screenshots or text, then check each item.
- **Source note:** [notes/instagram/DeMoCfwCHE8.md](../notes/instagram/DeMoCfwCHE8.md)

### 5 free AI video generators incl. a tool with Seedance, Veo 3.1 and Kling  (2026-10-18)
- **Verdict:** unverified
- **What it is:** Reel teases five free AI video generators, one said to give access to premium models.
- **Why pending:** Reel names no tools; the list is in a separate YouTube video.
- **To resolve:** Watch the linked YouTube video or paste its list, then check each tool's free limits.
- **Source note:** [notes/instagram/Db-83ucolWr.md](../notes/instagram/Db-83ucolWr.md)

### Ad cost drops from 2 lakh rupees to 1-2 hours with Claude  (2026-10-18)
- **Verdict:** unverified
- **What it is:** Creator's claim of a large cost and time saving on a 2.5-minute ad.
- **Why pending:** Self-reported, no finished video or invoices shown.
- **To resolve:** Request the finished ad and results, or reproduce the workflow on a small test.
- **Source note:** [notes/instagram/DeGKrmWh89C.md](../notes/instagram/DeGKrmWh89C.md)

### Rieseberg 'How to be more ambitious' article  (2026-10-18)
- **Verdict:** unverified
- **What it is:** Tutorial on speed, altitude, depth and range ambition with models, plus a four-part prompt.
- **Why pending:** Web search did not locate the original page; only the reel's on-screen capture was read.
- **To resolve:** Open felixrieseberg.com and confirm the article and prompt wording.
- **Source note:** [notes/instagram/Dek6wBjJgnA.md](../notes/instagram/Dek6wBjJgnA.md)

### September 2026 top-10 growing Claude Skills  (2026-10-18)
- **Verdict:** unverified
- **What it is:** Carousel ranking Claude Skills repos by stars gained in September 2026.
- **Why pending:** Slides not captured, so the repos were never read.
- **To resolve:** Paste the slide text or the linked list, then check each repo's star history.
- **Source note:** [notes/instagram/DeVyGbyJGcl.md](../notes/instagram/DeVyGbyJGcl.md)

### 46 free alternatives list  (2026-10-18)
- **Verdict:** unverified
- **What it is:** Creator promises 46 free alternatives to paid AI tools via comment.
- **Why pending:** Only sent after commenting; contents not seen.
- **To resolve:** Paste the list received, or check the creator's profile for it.
- **Source note:** [notes/instagram/DafrdobMFBG.md](../notes/instagram/DafrdobMFBG.md)

### chinaai.app gives free Seedance, Kling and Wan video generation  (2026-10-17)
- **Verdict:** unverified
- **What it is:** The reel says this site offers the best video models for free once free mode is on.
- **Why pending:** The page lists the models and 'no credit card required' but states no free allowance, sells credits, and names no operator; the free-mode setting is not shown.
- **To resolve:** The site's pricing and terms pages, or a screen recording of a free generation from sign-up to result.
- **Source note:** [notes/instagram/DeCH_lVqG-k.md](../notes/instagram/DeCH_lVqG-k.md)

### Meta Muse gives 1 billion free tokens through invite codes  (2026-10-17)
- **Verdict:** unverified
- **What it is:** Reported referral offer: redeem an invite code within 48 hours of signing up for 1 billion Muse tokens each.
- **Why pending:** Only third-party blogs report it, none tied to a Meta page, and the same reel says one billion in the audio and one million in the caption.
- **To resolve:** Meta's own Muse page or help centre confirming the offer, the regions and the expiry.
- **Source note:** [notes/instagram/DelxZzcvW49.md](../notes/instagram/DelxZzcvW49.md)

### Repo of 500+ viral AI motion design prompts  (2026-10-17)
- **Verdict:** unverified
- **What it is:** A GitHub repository, MIT licensed, of 500+ motion designs each with the exact AI prompt behind it, as shown in the reel.
- **Why pending:** The reel never shows the repo name and the link is only sent after you share the reel; searches found only similar collections.
- **To resolve:** The repo URL (ask the creator or find it by searching GitHub for the technologies named on screen), then check its README, licence and sample prompts.
- **Source note:** [notes/instagram/DeUK2NZS3Ig.md](../notes/instagram/DeUK2NZS3Ig.md)

### Jio's free Google AI Pro includes the Colab A100  (2026-10-17)
- **Verdict:** unverified
- **What it is:** Whether the 18-month Jio offer carries the new Colab benefits.
- **Why pending:** The Jio coverage lists Gemini Pro and developer limits but never mentions Colab.
- **To resolve:** Google's AI Pro plan page or a Jio user confirming Colab access.
- **Source note:** [notes/instagram/DemHB0GhG_R.md](../notes/instagram/DemHB0GhG_R.md)

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
