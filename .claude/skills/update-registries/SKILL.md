---
name: update-registries
description: File the verdicts from a fact-check into registry/verified.md, registry/hoax.md or registry/sidequests.md and keep the cross-links to the note. Use after fact-check-claims.
---

# update-registries

Three files under `registry/`:

| File | What goes in it |
|---|---|
| `verified.md` | Tools, hacks and facts that checked out (`verified`, `verified-with-caveats`). Also a **Pending verification** section for `unverified` items that may still turn out true. |
| `hoax.md` | Claims judged `hoax` or `misleading`, with the evidence. |
| `sidequests.md` | Videos with nothing checkable or no informative value (humour, motivation, news reaction), one line each. |

Entry format (newest first inside each section):

```markdown
### <Tool / claim name>  (<YYYY-MM-DD>)
- **Verdict:** verified | verified-with-caveats | unverified | misleading | hoax
- **What it is:** one sentence.
- **How to use / why it matters:** one or two lines (verified.md only).
- **Evidence:** [source](url), [source](url)
- **Source note:** [notes/instagram/<id>.md](../notes/instagram/<id>.md)
```

Rules:
- One entry per claim, not per video; a video can produce entries in both `verified.md` and `hoax.md`.
- If a claim is already registered, add the new note as an extra source instead of duplicating the entry.
- If a verdict changes later (a pending item is resolved), move the entry to the right file and say why in `decision.md`.
- Update the note's front matter (`verdict`, `registry`) to match.
