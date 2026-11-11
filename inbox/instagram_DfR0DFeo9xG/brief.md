# Brief: instagram reel DfR0DFeo9xG

- url: https://www.instagram.com/reel/DfR0DFeo9xG/
- author: arti.miller
- posted: 2026-11-03T11:50:34Z
- duration_s: 84
- likes: 10391  comments: 424  comments/likes: 0.04
- audio language: en
- needs_visual_review: yes  (view /home/runner/work/_temp/prep_instagram_DfR0DFeo9xG/sheet.jpg)
- recipe_hint: no
- gaps: none

## Caption / description
AI video editor in Claude Code: 3 prompts, from an empty folder to a finished reel.

SETUP (once)
1. Get the Claude app (claude.ai/download) and open the Code tab, not the browser.
2. Make a folder "AI Editor" with 3 folders inside: raw, references, done.
3. New chat in Code → Local → Select folder → AI Editor.
Needs a paid Claude plan.

PROMPT 1: TOOLS
You're my video editor. We work in this folder: raw, references, done. Install and verify 5 tools: FFmpeg with libass (on Mac: ffmpeg-full, full path), faster-whisper for word-level subtitles, yt-dlp for references, Remotion, HyperFrames (npm package hyperframes). Check what's installed first. Official installs only (Homebrew, winget, npm/pip), Node.js 22+. Python packages go in a .venv here, Python 3.14 or older: pip install faster-whisper "av<19". Test each for real: burn a subtitle into a test clip, transcribe 5 seconds of audio. Show a table: tool, version, works or not.

PROMPT 2: YOUR TASTE
Here are reels whose editing I like: [link 1] [link 2] [link 3]. My format: [talking to camera / voiceover]. Download them with yt-dlp into references (for study only). Study each one frame by frame and by ear: pacing, shot length, pause cuts, subtitles, colors, graphics, transitions, music, the first 3 seconds. Take inspiration, but don't copy: no shots, text, logos or brand elements. Write my own style to style.md with exact values. Show it and ask what to change.

PROMPT 3: EDIT
My new recording is in raw. Edit it using style.md:
1. Transcribe with Whisper, word timestamps. Ask me about doubtful words before burning subtitles.
2. Cut pauses, slips and bad takes, keep the last good take. Check cut points by audio level. Keep pauses that serve the meaning, breaths and word endings. Don't speed up my voice.
3. Word-by-word subtitles in my style.
4. If references/music.mp3 exists, put it quietly under the voice.
5. Graphics only where they help.
6. Export 1080×1920 to done as draft-v1.mp4 plus edit-notes.md.
Check the file yourself, then show me. I'll give edits in plain words; save each as draft-v2, draft-v3.

No code words. Follow for my own editing style, coming next.

## Transcript
language: en (1.00)
[0s] Everybody's editing their reels with Claude right now.
[2s] But the setup, they lock it behind paid courses.
[5s] Give me one minute, and I'll show you all of it.
[7s] Step one, download the Claude app and open Claude code
[10s] inside it, not in the browser.
[12s] Then, create a folder on your computer called AI Editor
[15s] and put three folders in it.
[17s] Raw, references, and done.
[19s] Open a new chat in Claude code, choose local
[22s] and point it at that folder.
[23s] Done.
[24s] Now, Claude can see your files and actually work with them.
[27s] Next, Claude needs editing tools, five of them.
[30s] Remotion and hyperframes build the video and the graphics.
[33s] FFMpeg cuts and exports.
[35s] Whisper takes care of the subtitles
[36s] and YTDLP downloads your references.
[39s] You don't install any of it yourself.
[41s] Just paste in the first prompt.
[43s] Now, Claude knows how to edit, but it doesn't know your taste.
[46s] Pick three to five reels in a style you like
[48s] and drop the links into the second prompt.
[50s] The most important line in there, take inspiration,
[52s] but don't copy.
[54s] That line is what keeps your videos
[55s] from looking like everyone else's.
[57s] Final step.
[58s] Shoot the way you always do.
[59s] Drop the recording into Raw and paste in the third prompt.
[62s] Claude cuts the pauses, adds subtitles,
[64s] lays music under it, and hands it all back for you to review.
[68s] Don't like something?
[69s] Just say it in plain words like make the hook bigger
[71s] and it'll fix it.
[72s] That's the whole process from an empty folder to a finished reel.
[76s] The tools handle the cutting, your taste handles the rest.
[79s] No code words, everything's in the description.
[81s] Follow, because next up I'm showing you my own editing style.

## On-screen text (OCR, noisy: words may run together)
[0s] 米Claude
[0s] 米Clau
[0s] reels with Claude right
[3s] CHECKOUT
[3s] PAID
[3s] Al Editing Masterciass
[3s] Claude setup revealed after payment
[3s] Payfor course→
[3s] paid courses.
[6s] 01.App
[6s] Claude
[6s] Desktop app
[6s] Chat
[6s] Cowork
[6s] Code
[6s] Step
[9s] Claude Code · new session
[9s] Ask Claude to work with your files.
[9s] inside it,
[12s] 02.Folder
[12s] Desktop
[12s] on your computer called
[15s] Al Editor
[15s] three folders in it:
[18s] 03·Local
[18s] Claude·Code
[18s] Newsession
[18s] Environment
[18s] Local
[18s] Remote
[18s] Folder
[18s] Select folder..
[18s] Open a new chat
[21s] ~/Desktop/AI Editor
[21s] it at that folder.
[24s] Claude can see
[24s] read
[24s] write
[24s] references
[24s] done
[24s] your files and actually
[27s] 04.Tools
[27s] editing tools
[27s] Remotion
[27s] vide
[27s] HyperFrames
[27s] graphic
[27s] FFmpeg
[27s] cuts& export
[27s] Whisper
[27s] subtitle
[27s] yt-dlp
[27s] downloads reference
[27s] tools.
[30s] video
[30s] graphics
[30s] build the video and
[33s] cuts& exports
[33s] FFmpeg cuts and exports.
[36s] subtitles

## Candidates found in the text (not yet verified)
- pypi: faster-whisper

## Looked up (primary sources, mechanical)
- package=faster-whisper, url=https://pypi.org/project/faster-whisper/, version=1.2.1, summary=Faster Whisper transcription with CTranslate2, license=MIT, home=https://github.com/SYSTRAN/faster-whisper
