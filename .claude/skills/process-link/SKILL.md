---
name: process-link
description: Full pipeline for a shared Instagram reel/post or YouTube video/short - mechanical prepare, read the brief, research the claims, write the verdicts, finish and push. Use whenever the user shares an instagram.com or youtube.com/youtu.be link.
---

# process-link

Everything that does not need judgment is a script, so the model only reads one brief, researches, and writes one small JSON file.

1. **Prepare (mechanical)** - `prepare-link`: `python3 scripts/prepare_link.py "<url>" "$SCRATCH/<id>" [--queued-via "GitHub issue #N"]`. Exit 3 means the note already exists (say so and stop); exit 2 means the fetch is blocked (tell the user or mark `needs-input`).
2. **Read** `$SCRATCH/<id>/brief.md` and nothing else. Look at `sheet.jpg` only if the brief says `needs_visual_review: yes`. For YouTube, read `comments.json` only if it is non-empty, with `analyze-comments`.
3. **Research** - `fact-check-claims`, starting from the brief's "Looked up" section (already primary-source facts) and its candidate list. Search the web only for claims those do not cover, and stop when every claim has a source or is marked unverified. Skip research for entertainment videos (side quest).
3b. **Recipes** - if the video teaches how to make food, follow `recipe-card`: extract ingredients and amounts, include a `recipe` object in `verdict.json`, and skip web research. Always look at `sheet.jpg` for recipes.
4. **Judge** - choose title, `categorize-link` fields, usefulness and verdicts using `write-link-note` (titles) and the usefulness scale in `update-library`; draft the registry entries.
5. **Finish (mechanical)** - write `verdict.json` and run `finish-link`: `python3 scripts/finish_link.py "$SCRATCH/<id>/verdict.json" --push --trailer "<attribution>"`. It writes the note from the draft, files the registry entries, rebuilds the library and `flow.md`, and pushes to `main`.
6. **Report** - queue item: post the printed comment on the issue and close it. Chat: tell the user what it is, the verdicts, what could not be fetched, and anything needed from them.

Rules:
- Never claim a verdict the research did not support; "could not verify" goes in the pending section, not in hoax.
- Log non-obvious choices through the `decision` field of `verdict.json`, never in chat only.
- Several links at once: process them one at a time; one commit per link.
- Never ask for cookies; keep media out of the repo.

The older single-step skills (`fetch-instagram-post`, `fetch-youtube-video`, `analyze-video`, `write-link-note`, `update-registries`, `update-library`) stay as reference and manual fallbacks; the scripts above call the same code.
