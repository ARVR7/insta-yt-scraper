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
title: <plain name, max 6 words, e.g. "Higgsfield Katana in Claude">
category: ai                            # from taxonomy.yml, see categorize-link
subcategory: automation
location: india/delhi                   # optional, only if stated in the video
also: []                                # optional cross-listing, e.g. [money/investing]
tools: [named-tool-or-repo]             # optional
usefulness: helpful | mixed | misleading | noise   # see update-library
key_info: "<1-2 sentences: what it is and the most important caveat>"
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

## Titles
The title is the first thing the user scans, so keep it plain and uniform:
- Name **the thing the video is about** (the tool, recipe, place or idea), in 2-6 words and at most 50 characters: `Higgsfield Katana in Claude`, `Paneer tikka wrap`, `Hauz Khas fort at sunset`.
- No parentheses, no hype, no clickbait, no emoji, no question marks, and do not copy the creator's headline.
- Do not put the verdict, the platform or the creator in the title; the app shows those separately, and `key_info` carries what it does and the main caveat.
- The note's first heading (`# ...`) must be the same text as `title`.
- `scripts/build_index.py` rejects titles over 50 characters or containing parentheses.

Rules:
- Quote `key_info` and any front matter value containing `:` or `#` so the YAML stays valid.
- Fill `title`, `category`, `subcategory`, `usefulness` and `key_info` after the research is done; `scripts/build_index.py` refuses notes without them.
- Record what could not be fetched in `fetch_status` and the caveats; never fill a gap with a guess.
- Quote the transcript lightly cleaned; mark guesses with `[?]`.
- Keep the author's claims separate from your verdicts: the note's top sections say what the video says, `## Research` says what is true.
- Do not put secrets, cookies or personal data of private individuals in notes.
