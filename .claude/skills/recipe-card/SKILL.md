---
name: recipe-card
description: Turn a cooking video into a proper recipe card with calculated macros (calories, protein, carbs, fat, fibre) per serving, and check any macro claims the creator makes. Use for every link that teaches how to make food (category food, subcategory recipes).
---

# recipe-card

The numbers come from a script, never from guesswork: you list the ingredients with amounts, `scripts/recipe_card.py` converts them to grams, looks each up in `data/nutrition.json` (144 ingredients, USDA FoodData Central and IFCT based) and sums the macros. `finish_link.py` runs it for you when `verdict.json` contains a `recipe` object, writes `recipes/<platform>_<id>.json` (what the app's recipe card shows), and adds a Markdown card to the note.

## What to extract (from `brief.md`, the caption, OCR text and the contact sheet; always look at `sheet.jpg` for a recipe)
```json
"recipe": {
  "title": "Paneer tikka wrap", "servings": 2, "serving_note": "1 wrap each",
  "time": {"prep": 15, "cook": 12}, "cuisine": "Indian",
  "ingredients": [
    {"name": "paneer", "qty": 200, "unit": "g", "note": "cubed", "group": "Filling"},
    {"name": "onion", "qty": 1, "unit": "medium", "estimated": true},
    {"name": "salt", "qty": null, "unit": "to taste"},
    {"name": "mint chutney", "qty": 2, "unit": "tbsp",
     "per100g": {"kcal": 60, "protein": 2, "carbs": 8, "fat": 2.5, "fibre": 2}, "source": "label shown at 0:21"}
  ],
  "steps": ["Short imperative steps in order, at most about 12."],
  "tips": ["Only tips the creator gives."],
  "claimed": {"kcal": 450, "protein": 35}
}
```

## Rules
- **Do not invent.** Only ingredients that are shown, said or written. Amounts the video does not give: estimate a sensible amount, set `"estimated": true`, and the card will say so. Prefer weights (g, ml); the converter also knows tsp, tbsp, cup, piece, small/medium/large, clove, slice, scoop.
- **Servings:** use what the video says; if it does not, pick the number of portions the amounts plainly make, and say how in `serving_note`.
- **Claims:** if the video states calories or protein, put them in `claimed`. The card then shows "the video says X, calculated Y (+z%)" and flags a difference over 15%. A material difference is worth stating in `key_info` and the research rows.
- **Unknown ingredient:** the script stops and names it. Add it to `ROWS` in `scripts/build_nutrition.py` with values per 100 g from a reliable source (USDA FoodData Central or IFCT), run that script (it rejects rows whose calories disagree with the macros), and log the source in `decision.md`. For a packaged product, use `per100g` plus `source` inline only when the label is visible or quoted; never guess a brand's macros.
- **Cooking effects:** macros are for raw ingredient weights. Oil absorbed while frying, water lost and cooked-versus-raw amounts shift real values; the card says so. Where the video's oil quantity is vague, estimate it and flag it, since oil is the biggest hidden calorie source.
- **Usefulness:** `helpful` when the recipe is complete and the macro claims (if any) hold; `mixed` when a claim is materially off or most amounts are estimated. Fact-checking beyond the macro claim check is usually unnecessary for a recipe; skip web research.
- `fill.research` still needs rows for `finish_link.py`: use the macro claim check, for example `["Creator's macro claims", "protein consistent, calories +35%", "see the recipe card"]`, or `["Recipe", "n/a", "Amounts from the video; macros calculated"]`.

## Check before finishing
`python3 scripts/recipe_card.py <recipe.json> --markdown` prints the card without writing anything; sanity-check the per-serving calories against the ingredient list (oil and nuts dominate) before running `finish-link`.
