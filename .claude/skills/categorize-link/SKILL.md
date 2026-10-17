---
name: categorize-link
description: Assign a category, subcategory, optional location and cross-listing to a link's note from the closed vocabulary in taxonomy.yml, so related videos always land together (one AI category, one Food category, and so on). Use when writing or re-filing any note.
---

# categorize-link

Source of truth: `taxonomy.yml`. Read it first, every time. Never invent a category, subcategory or city in a note; the build rejects them.

## Fields (in the note's front matter)
```yaml
category: ai                 # exactly one, required
subcategory: automation      # required when the category has subcategories
location: india/delhi        # optional: country, or country/city
also: [money/business]       # optional cross-listing, rarely needed
```

## How to choose
1. **Category = what the video is for.** Ask: what would the viewer do with this? Cook it, eat there, visit it, build with AI, invest in it. Pick the category of that main takeaway.
2. **One AI category.** Anything where AI is the point (tools, agents, AI side-hustles, AI creative work) is `ai` with a subcategory: `tools`, `automation`, `creative`, `ideas`. Do not use `money` or `tech` for these; `money` is for non-AI business and finance.
3. **Recipes get a recipe card.** `food/recipes` notes need macros and a card; follow the `recipe-card` skill.
3b. **Food vs Places.** A recipe is `food/recipes`. A restaurant or cafe is `food/eateries` with a `location`. A trip, stay or sight is `places/...` with a `location`.
4. **Location is separate from category** and only set when the caption, on-screen text or audio states it (a city, area or country). Map areas to their city (Cyber Hub -> `india/gurgaon`). Never infer a location from the creator's accent, profile or a guess; leave it blank.
5. **Aliases are accepted** (`ai-tools`, `Gurugram`) and rewritten by the build, but write the canonical key anyway.
6. **`also`** only when a second category would genuinely be where the viewer looks for it (an AI tool for investing: `category: ai`, `also: [money/investing]`). The primary decides counts.
7. **Entertainment** is for fun content, usually usefulness `noise`; it also goes in `registry/sidequests.md`.

## If nothing fits
1. Prefer a subcategory under the closest existing category; add it under that category in `taxonomy.yml` with 2-4 aliases.
2. A new city under a known country: add it under `locations`. A new country: add it with aliases.
3. A new top-level category only when at least two unrelated notes need it and no existing category's `about` covers it. Give it `label`, `icon` (one of: spark, fork, pin, heart, coin, code, book, play, dots), `colors`, `aliases`, `about`.
4. Use `other` only temporarily, then extend the taxonomy and recategorize.
5. Log every taxonomy addition in `decision.md` with the reason, then run `python3 scripts/build_index.py`.

## Keeping it tidy
- Check `library/by-category/` before adding anything to see how existing notes were filed, and follow them.
- Merge duplicates with `python3 scripts/taxonomy.py merge-sub|merge-cat|rename-city ...`, edit `taxonomy.yml`, rebuild, and log it in `decision.md`.
- `python3 scripts/taxonomy.py check` validates all notes.

## Worked examples
| Video | Category | Location |
|---|---|---|
| "Free AI studio runs a faceless YouTube channel" | `ai/automation` | none |
| "Katana makes motion graphics in Claude" | `ai/creative` | none |
| "5-minute paneer wrap" | `food/recipes` | none |
| "Best momos in Sarojini Nagar" | `food/eateries` | `india/delhi` |
| "Weekend trek near London" | `places/sights` | `uk` |
| "Claude prompts for stock research" | `ai/ideas`, also `money/investing` | none |
