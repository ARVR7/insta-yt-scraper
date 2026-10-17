---
name: update-library
description: Rebuild the library index (data/library.json and the library/ lists by usefulness and topic) from the notes. Use after every new or edited note, before committing.
---

# update-library

```bash
python3 scripts/build_index.py
```

Reads the front matter of every `notes/*/*.md` and regenerates:

| Output | Used by |
|---|---|
| `data/library.json` | the web app (Library, Overview, Queue tabs) |
| `library/README.md` | every link, newest first, with key info |
| `library/by-usefulness/{helpful,mixed,misleading,noise}.md` | lists grouped by how useful the link is |
| `library/by-topic/<topic>.md` | one list per topic |

All of these are generated: never edit them by hand, and always commit them together with the note.

The script exits with an error naming the note if front matter lacks `url`, `platform`, `title`, `usefulness`, `verdict` or `key_info`, or if `usefulness` is not one of `helpful | mixed | misleading | noise`. Fix the note and rerun.

## Choosing `usefulness`
| Value | Meaning |
|---|---|
| `helpful` | At least one verified, actionable tool, hack or fact, and no major deception. |
| `mixed` | A real tool or fact, but misleading framing, a paywall behind "free", or unproven headline claims. |
| `misleading` | Mostly hoax, hype or unsupported claims. |
| `noise` | Nothing informative (also listed in `registry/sidequests.md`). |

`topics` are short lowercase tags (`ai-tools`, `video-generation`, `devops`). Reuse an existing tag when one fits (check `library/by-topic/`) so lists stay consolidated; add a new one only when none fits. `key_info` is one or two sentences: what the thing is and the single most important caveat.
