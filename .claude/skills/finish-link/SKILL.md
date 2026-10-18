---
name: finish-link
description: Turn Claude's judgments about a link into the finished note, registry entries, library index, flow table and a git push, with one command and one small JSON file. Use after the research is done.
---

# finish-link

Write one small JSON file in the scratchpad containing only judgment, then run:

```bash
python3 scripts/finish_link.py "$SCRATCH/<id>/verdict.json" --push --trailer "<attribution line>" [--trailer "<second line>"]
```
Use the commit attribution lines from the session's instructions as `--trailer` values. The script prints a result summary and the issue comment text.

## verdict.json
```json
{
  "draft": "<scratch>/<id>/draft_note.md",
  "fill": {
    "title": "Plain name, max 50 chars, no parentheses",
    "category": "ai", "subcategory": "creative",
    "location": "india/delhi", "also": ["money/investing"],
    "tools": ["freevideo"],
    "usefulness": "helpful | mixed | misleading | noise",
    "verdict": "verified | partly-verified | hoax | sidequest | pending",
    "key_info": "What it is and the main caveat, 1-2 sentences.",
    "hook": "On-screen headline text", "cta": "What the creator asks viewers to do",
    "on_screen": "What the video shows", "summary": "2-4 sentences",
    "research": [["claim", "verdict", "evidence with [links](https://...)"]],
    "overall": "One sentence.",
    "instruction": "(only if the issue had one) the owner's instruction, verbatim",
    "instruction_result": "what you did and found for it",
    "caveats": ["...", "..."]
  },
  "entries": [
    {"section": "verified", "name": "Tool or fact", "verdict": "verified-with-caveats",
     "what": "...", "how": "...", "caveats": "...", "evidence": [["label", "https://..."]]},
    {"section": "pending", "name": "...", "verdict": "unverified", "what": "...", "why": "...", "resolve": "..."},
    {"section": "hoax", "name": "...", "verdict": "misleading", "what": "...", "why": "...", "evidence": [["label", "https://..."]]},
    {"section": "sidequest", "name": "...", "what": "one line"}
  ],
  "recipe": { "...": "required for food/recipes, see the recipe-card skill" },
  "decision": {"title": "...", "text": "..."}
}
```
- `location`, `also`, `entries` and `decision` are optional. `recipe` is mandatory for food/recipes notes: the script refuses the note without it and, when present, computes the macros, writes `recipes/<id>.json` and the Markdown card. Fields follow `categorize-link` and `write-link-note` (titles, usefulness scale). One registry entry per claim, not per video.
- Add a `decision` only for non-routine choices (a taxonomy addition, a workaround, a rule you applied for the first time). Routine filing needs none.

## What the script does
Validates the note and taxonomy before touching anything (a bad field changes nothing), writes `notes/<platform>/<id>.md` from the draft, adds the registry entries in the right files and format (skipping duplicates), appends the decision, rebuilds `data/` and `library/`, regenerates the "Current notes" table in `flow.md`, writes the issue comment, and with `--push` commits and pushes to `main` with fetch, rebase and retries. It refuses notes that still contain `TODO`, and it never overwrites an existing note unless `"overwrite": true`.

## After it runs
- Queue item: post the printed comment on the issue (GitHub MCP `add_issue_comment`), then set the labels to just `link` and close it (`issue_write`). If `git` says `PUSH FAILED`, fix that first and rerun; the script is safe to rerun.
- Chat link: reply with the verdict and the key point.
