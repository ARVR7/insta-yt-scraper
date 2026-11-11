---
url: https://www.instagram.com/reel/DfR0DFeo9xG/
platform: instagram
type: reel
author: arti.miller
posted: 2026-11-03T11:50:34Z
duration_s: 84
views: not exposed
likes: 10391
comments: 424
language: en
queued_via: "GitHub issue #152"
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
> AI video editor in Claude Code: 3 prompts, from an empty folder to a finished reel.
> 
> SETUP (once)
> 1. Get the Claude app (claude.ai/download) and open the Code tab, not the browser.
> 2. Make a folder "AI Editor" with 3 folders inside: raw, references, done.
> 3. New chat in Code → Local → Select folder → AI Editor.
> Needs a paid Claude plan.
> 
> PROMPT 1: TOOLS
> You're my video editor. We work in this folder: raw, references, done. Install and verify 5 tools: FFmpeg with libass (on Mac: ffmpeg-full, full path), faster-whisper for word-level subtitles, yt-dlp for references, Remotion, HyperFrames (npm package hyperframes). Check what's installed first. Official installs only (Homebrew, winget, npm/pip), Node.js 22+. Python packages go in a .venv here, Python 3.14 or older: pip install faster-whisper "av<19". Test each for real: burn a subtitle into a test clip, transcribe 5 seconds of audio. Show a table: tool, version, works or not.
> 
> PROMPT 2: YOUR TASTE
> Here are reels whose editing I like: [link 1] [link 2] [link 3]. My format: [talking to camera / voiceover]. Download them with yt-dlp into references (for study only). Study each one frame by frame and by ear: pacing, shot length, pause cuts, subtitles, colors, graphics, transitions, music, the first 3 seconds. Take inspiration, but don't copy: no shots, text, logos or brand elements. Write my own style to style.md with exact values. Show it and ask what to change.
> 
> PROMPT 3: EDIT
> My new recording is in raw. Edit it using style.md:
> 1. Transcribe with Whisper, word timestamps. Ask me about doubtful words before burning subtitles.
> 2. Cut pauses, slips and bad takes, keep the last good take. Check cut points by audio level. Keep pauses that serve the meaning, breaths and word endings. Don't speed up my voice.
> 3. Word-by-word subtitles in my style.
> 4. If references/music.mp3 exists, put it quietly under the voice.
> 5. Graphics only where they help.
> 6. Export 1080×1920 to done as draft-v1.mp4 plus edit-notes.md.
> Check the file yourself, then show me. I'll give edits in plain words; save each as draft-v2, draft-v3.
> 
> No code words. Follow for my own editing style, coming next.

## Hook (on-screen text)
TODO

## Call to action
TODO

## Transcript (auto)
> Everybody's editing their reels with Claude right now. But the setup, they lock it behind paid courses. Give me one minute, and I'll show you all of it. Step one, download the Claude app and open Claude code inside it, not in the browser. Then, create a folder on your computer called AI Editor and put three folders in it. Raw, references, and done. Open a new chat in Claude code, choose local and point it at that folder. Done. Now, Claude can see your files and actually work with them. Next, Claude needs editing tools, five of them. Remotion and hyperframes build the video and the graphics. FFMpeg cuts and exports. Whisper takes care of the subtitles and YTDLP downloads your references. You don't install any of it yourself. Just paste in the first prompt. Now, Claude knows how to edit, but it doesn't know your taste. Pick three to five reels in a style you like and drop the links into the second prompt. The most important line in there, take inspiration, but don't copy. That line is what keeps your videos from looking like everyone else's. Final step. Shoot the way you always do. Drop the recording into Raw and paste in the third prompt. Claude cuts the pauses, adds subtitles, lays music under it, and hands it all back for you to review. Don't like something? Just say it in plain words like make the hook bigger and it'll fix it. That's the whole process from an empty folder to a finished reel. The tools handle the cutting, your taste handles the rest. No code words, everything's in the description. Follow, because next up I'm showing you my own editing style.

## What is shown on screen
TODO

## Summary
TODO

## Comments
Not read: Instagram requires a login to list comments. The count is 424 against 10391 likes (comments/likes 0.04; a ratio near or above 1 usually means a prompt to comment, an inference).

## Research (checked 2026-11-11)

| Claim | Verdict | Evidence |
|---|---|---|
| TODO | TODO | TODO |

Overall: TODO

## Notes / caveats
- TODO
