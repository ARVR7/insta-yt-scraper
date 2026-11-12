# Brief: instagram reel DfpU3LeNFh_

- url: https://www.instagram.com/reel/DfpU3LeNFh_/
- author: kem_glitch
- posted: 2026-11-12T15:00:47Z
- duration_s: 168
- likes: 124  comments: 29  comments/likes: 0.23
- audio language: en
- needs_visual_review: yes  (view /home/runner/work/_temp/prep_instagram_DfpU3LeNFh_/sheet.jpg)
- recipe_hint: no
- gaps: none

## Caption / description
Does the harness improve outputs? Well, yes ..kinda when it’s raining on a Tuesday! 
#ai #artificialintelligence #openai @nous_research @openai @anthropicai

Hashtags: #ai #artificialintelligence #openai

## Transcript
language: en (0.99)
[0s] Hi friends I'm sure a lot of you have heard that the harness matters more than the model that you're
[6s] using. I think that conversation conflates a couple of things. There's building a harness from scratch
[12s] which is what some teams do when they run agents through the API and there's what most of us do which
[17s] is scripting on top of the harness we already use. I call that a meta harness. So what we need to know
[23s] is when those numbers matter and where the practical signal is for getting better outputs.
[28s] So today I'm putting one model opus 5.5 inside three harnesses which are Claude code codex
[34s] and Hermes and I'm going to challenge an idea from hugging face. They took lfm 2.5 which is a small
[41s] 2.6 bill parameter model from liquid AI and ran it inside different harnesses. Same weights and it
[47s] sold 62% of its tasks inside one and 33% inside Claude code. So before we begin let's talk about
[55s] what a harness is. It's everything wrapped around the model. That's the system prompt which is
[59s] just a set of instructions you never see. The tools it's allowed to use the loop that the program
[64s] itself runs till the job is done and the checks it runs before it tells you it's finished. For my test
[70s] I used opus in all three each in its own bucket container fully scripted. I give them the same
[76s] six real bugs from sweet bench three times each and the project's own test decide what's
[82s] a pass. Before I typed a single word Claude code had already sent the model about 11,000 tokens
[88s] of instructions and tools and opus works completely differently in each one. Claude code gave it
[94s] 26 tools and it used one which was the command line. In Hermes it used the tools it was given to
[100s] search, read and edit the code and in codex it took the fewest steps and finish fastest. So what
[106s] happened? Well even though they worked so differently the results were the same across the board.
[111s] All three solved 16 of the 18 tasks but what did change was the speed and the bill where
[117s] codex was the fastest and Hermes surprisingly was the cheapest. But one thing really did stand out
[123s] is 72 runs opus reproduced the bug before changing the code twice. That's because none of the three
[130s] harnesses told it to do so. So I wrote one page of extra instructions telling it how to work
[136s] once more script that won't let it finish until those checks pass and on that one bug they kept
[141s] getting wrong opus more than doubled its pass rate and that's the lesson. If you're building a harness
[147s] from scratch to run your own agents it still really matters but for the rest of us with a model
[152s] this good inside any of the leading harnesses what makes the difference in my test was the layer on top
[158s] your skills your scripts and your checks that's the meta harness and it's really just files and
[163s] folders. So let's keep leveling up friends chemicalist care club signing out.

## On-screen text (OCR, noisy: words may run together)
[0s] GLITCH_CAT
[0s] File Harness Layer
[0s] 14:00
[0s] THEHARNESS
[0s] DOES THE HARNESS
[0s] MATTER MORE
[0s] THAN THE MODEL?
[0s] CLAUDE CODE
[0s] CODEX
[0s] HERMES
[0s] I'm sure a lot of
[0s] you have heard
[3s] thattheharness
[3s] mattersmore
[6s] ITER MORE
[6s] AN THE MODEL?
[6s] CODEK
[6s] Ithinkthat
[6s] conversation
[9s] STHEHARNESS
[9s] There'sbuildinga
[9s] harness from
[12s] FROM SCRATCH
[12s] MODEL
[12s] teams do when they
[12s] run agents
[15s] through the API
[15s] most of us do, which
[15s] is scripting
[18s] ON TOP
[18s] YOUR HARNESS
[21s] META HARNESS
[21s] So what we need to
[21s] know is when
[24s] the practical signal
[24s] is for getting
[30s] 01 TODAY
[30s] OPUS
[30s] Opus 5.5 inside
[30s] three harnesses,
[33s] whichareClaude
[33s] code, Codex and
[36s] Huggingface.
[39s] 01HUGGING FACE
[39s] LFM2.5 - 2.6B - LIQUID AI
[39s] They took LFM 2.5,
[39s] which is a
[42s] from Liquid Al and
[42s] ran it inside
[45s] same weights
[45s] MINI-SWE-AGENT
[45s] Same weights, and it
[45s] solved 62%
[48s] of its tasks inside
[48s] one and 33%
[51s] inside Claude code.
[54s] 02WHATISAHARNESS?
[54s] WHAT IS
[54s] A HARNESS?
[54s] aboutwhataharness

## Candidates found in the text (not yet verified)
- handles: anthropicai, nous_research, openai
