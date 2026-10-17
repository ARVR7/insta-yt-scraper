---
name: update-library
description: Rebuild the library index (data/library.json and the library/ lists by category, location and usefulness) from the notes. Use after every new or edited note, before committing.
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
| `library/by-category/<category>.md` | one list per category, grouped by subcategory |
| `library/by-location/<country[-city]>.md` | one list per place |
| `data/taxonomy.json` | categories, icons, colours and locations for the app |

All of these are generated: never edit them by hand, and always commit them together with the note.

The script exits with an error naming the note if front matter lacks `url`, `platform`, `title`, `usefulness`, `verdict`, `key_info` or `category`, or if the category, subcategory or location is not in `taxonomy.yml`, or if `usefulness` is not one of `helpful | mixed | misleading | noise`. Fix the note and rerun.

## Choosing `usefulness`
| Value | Meaning |
|---|---|
| `helpful` | At least one verified, actionable tool, hack or fact, and no major deception. |
| `mixed` | A real tool or fact, but misleading framing, a paywall behind "free", or unproven headline claims. |
| `misleading` | Mostly hoax, hype or unsupported claims. |
| `noise` | Nothing informative (also listed in `registry/sidequests.md`). |

`category`, `subcategory` and `location` come from `taxonomy.yml` (see `categorize-link`); the build rejects anything not in it and rewrites aliases. `key_info` is one or two sentences: what the thing is and the single most important caveat.
