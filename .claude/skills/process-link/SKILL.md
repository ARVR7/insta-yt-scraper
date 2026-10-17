---
name: process-link
description: Full pipeline for a shared Instagram reel/post or YouTube video/short - fetch, analyze, write the note, fact-check the claims, update the registries and docs, then push to main. Use whenever the user shares an instagram.com or youtube.com/youtu.be link.
---

# process-link

Run these steps in order. Each step is its own skill; read it before running it.

1. **Fetch** - `fetch-instagram-post` for instagram.com links, `fetch-youtube-video` for youtube.com / youtu.be links. Output goes to a scratch directory, never into the repo.
2. **Analyze** - `analyze-video` on the downloaded video (frames, contact sheet, transcript). Look at `sheet.jpg` to read on-screen text.
3. **Write the note** - `write-link-note` creates `notes/<platform>/<id>.md`.
4. **Fact-check** - `fact-check-claims` researches every checkable claim in the video and returns verdicts.
5. **Registries** - `update-registries` files each verdict in `registry/verified.md`, `registry/hoax.md` or `registry/sidequests.md`, and links back to the note.
6. **Docs** - append a dated entry to `decision.md` for every non-obvious choice made in this run (including workarounds for blocked fetches). Update `flow.md` if a script, skill or folder was added or changed.
7. **Ship** - commit and push straight to `main` (the user's standing instruction). Commit message: `Add note for <platform> <id>`.

Finish by telling the user: what the post is, the verdicts, what could not be fetched, and anything you need from them.

Rules:
- Never claim a verdict the research did not support. "Could not verify" is a valid result; put it in the Pending section of `registry/verified.md`, not in hoax.
- If the video is not informative (entertainment, no checkable claim or tool), skip fact-checking and add it to `registry/sidequests.md` instead.
- If several links arrive at once, process them one by one; do not batch commits across links.
