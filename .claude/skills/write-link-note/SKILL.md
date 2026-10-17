---
name: write-link-note
description: Write the markdown note for one shared link in notes/instagram/ or notes/youtube/ using the repo's note format. Use after fetch and analyze, before fact-checking.
---

# write-link-note

File: `notes/instagram/<shortcode>.md` or `notes/youtube/<video-id>.md`. One file per link; if it exists, update it instead of creating a duplicate.

Front matter, then sections in this order:

```markdown
---
url: <clean url, no tracking params>
platform: instagram | youtube
type: reel | post | video | short
author: <handle or channel>
posted: <ISO date>
duration_s: <n>
views: <n | not exposed>
likes: <n>
comments: <n>
language: <code>
fetch_status:
  metadata: ok | partial | failed (+ how)
  caption: ok | not returned
  video: downloaded | blocked (reason)
  transcript: ok (tool, auto-generated) | none
  on_screen_text: read from frames | n/a
verdict: verified | partly-verified | hoax | sidequest | pending
registry: <link to the entry in registry/*.md>
---
# <short title>
## Caption / hashtags
## Hook (on-screen text)
## Call to action
## Transcript (auto)
## What is shown on screen
## Summary
## Comments        <- filled by analyze-comments (omit if unavailable, say why)
## Research        <- filled by fact-check-claims: claim | verdict | evidence + links
## Notes / caveats
```

Rules:
- Record what could not be fetched in `fetch_status` and the caveats; never fill a gap with a guess.
- Quote the transcript lightly cleaned; mark guesses with `[?]`.
- Keep the author's claims separate from your verdicts: the note's top sections say what the video says, `## Research` says what is true.
- Do not put secrets, cookies or personal data of private individuals in notes.
