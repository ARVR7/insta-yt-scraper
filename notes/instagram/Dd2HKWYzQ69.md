---
url: https://www.instagram.com/reel/Dd2HKWYzQ69/
platform: instagram
type: reel
author: aiwithdivyam
posted: 2026-09-28T21:08:58Z
duration_s: 61
views: not exposed
likes: 1762
comments: 305
language: hi
queued_via: "GitHub issue #58"
fetch_status:
  metadata: "ok (instaloader/yt-dlp, anonymous)"
  caption: "not returned"
  video: "downloaded"
  transcript: "ok (faster-whisper, translated, auto-generated, may contain errors)"
  on_screen_text: "OCR + contact sheet"
  comments: "not fetched (Instagram requires login)"
title: "NVIDIA Nemotron 3 Diarization explained"
category: ai
subcategory: tools
usefulness: helpful
tools: ["nemotron-3-diarization", "nvidia-nemo", "hugging-face"]
key_info: "NVIDIA's Nemotron 3 Diarization is real: a roughly 100M-parameter open-weight speaker diarization model (who spoke when) that tracks up to 8 speakers with overlapping voices, released in September 2026 under the OpenMDW licence on Hugging Face. The 'commercial use allowed' claim needs a check: one report says the preview checkpoint on Hugging Face is limited to evaluation, so read the model card licence for the version you use. It needs an NVIDIA GPU stack (NeMo on Linux)."
verdict: partly-verified
registry: registry/verified.md
---

# NVIDIA Nemotron 3 Diarization explained

## Caption / hashtags
Not returned.

## Hook (on-screen text)
NVIDIA released a 100-million-parameter model that tells you who spoke when, even with overlapping voices

## Call to action
Comment to get the post and video links by DM

## Transcript (auto)
> 5-6 days ago, I have open sourced a model of small to 100 million parameters. Its name is Nemotron 3 Diorization. The name is very heavy, but the work is very simple and effective. So basically, the previous speech-to-text models were given words, transcripts. But if 5-6 people are speaking together with overlapping voices, then ASR, which is an automatic speech recognition, will tell the words. But it won't be able to tell which speaker spoke at that time. And I am not talking about the teams, everyone has their accounts and audio streams. So there is no need to do any recognition. I am talking about an example. Suppose, 6 people are sitting in the podcast and 3 speakers are speaking together. Their voice is overlapping. And I need different transcripts of those 3, user-wise. And even this should happen, suppose that speaker is quiet for a while, like a speaker 2. Later, he started speaking, so I need to mix his transcript with someone else. When he is speaking in front of the same transcript, it should be added. Basically, speaker-attributed transcript is needed, which can be done through this model. Because it doesn't just rely on ASR. It combines the time interval of the speaker to be active. And it is also permitting its commercial use. If you want to know the rest in more detail, then this is the link of the post of the end video. And this is the link of the video of YouTube. I will do a DM, comment something.

## What is shown on screen
Screenshots of an article dated September 23, 2026 on 'NVIDIA releases Nemotron 3 Diarization': open-weight speaker diarization, 100M parameters, up to 8 speakers, one checkpoint for offline and streaming, OpenMDW licence permitting commercial use, runs on Linux via NVIDIA NeMo on Ampere, Hopper or Blackwell GPUs.

## Summary
In Hindi, the creator explains that ASR tells you the words but not who said them, and that NVIDIA's new small Nemotron 3 Diarization model produces speaker-attributed transcripts by combining ASR output with time intervals when each speaker is active, even with overlapping voices, and that its licence allows commercial use.

## Comments
Not read: Instagram requires a login to list comments. The count is 305 against 1762 likes (comments/likes 0.17; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-10-22)

| Claim | Verdict | Evidence |
|---|---|---|
| NVIDIA released Nemotron 3 Diarization, a ~100M-parameter open-weight speaker diarization model | verified | Reported by [Unite.AI](https://www.unite.ai/nvidia-releases-nemotron-3-diarization-open-weight-speaker-model/) and several other outlets, listed on Hugging Face as nvidia/Nemotron-3-Diarization. |
| Tracks up to 8 speakers including overlapping voices, offline and streaming | verified | Matches the coverage and the article shown on screen. |
| Diarization gives who-spoke-when intervals, to be combined with ASR for speaker-attributed transcripts | verified | The model outputs time intervals and anonymous speaker labels, not words; combining it with an ASR model is the intended use. |
| Commercial use is permitted | partly verified | Coverage names the OpenMDW 1.1 licence and says it permits commercial use, but one report says the Hugging Face preview checkpoint is restricted to internal evaluation; check the model card for the version you use. |
| Runs on a typical machine | unverified | It runs on Linux via NVIDIA NeMo on Ampere, Hopper or Blackwell GPUs; consumer hardware needs were not checked. |

Overall: Accurate description of a real model; confirm the licence on the exact checkpoint before commercial use.

## Notes / caveats
- Benchmarks quoted in coverage come from NVIDIA or a leaderboard and vary by source.
- Diarization labels speakers anonymously; it does not identify who they are.
- The post's links were sent only by DM; the model was found via the on-screen article and web coverage.
