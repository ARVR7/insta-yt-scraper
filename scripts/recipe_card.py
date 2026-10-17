#!/usr/bin/env python3
"""Compute macros for a recipe and produce the recipe card (JSON for the app, Markdown for the note).

Usage:
  recipe_card.py <recipe_input.json> [--out recipes/<id>.json] [--markdown]
Library: from recipe_card import build, to_markdown

Input (what Claude writes; amounts as stated in the video, or estimated and flagged):
{
  "title": "Paneer tikka wrap", "servings": 2, "serving_note": "1 wrap each",
  "time": {"prep": 10, "cook": 15}, "cuisine": "Indian",
  "ingredients": [
    {"name": "paneer", "qty": 200, "unit": "g", "note": "cubed", "group": "Filling"},
    {"name": "onion", "qty": 1, "unit": "medium", "estimated": true},
    {"name": "salt", "qty": null, "unit": "to taste"},
    {"name": "mystery sauce", "qty": 2, "unit": "tbsp",
     "per100g": {"kcal": 120, "protein": 1, "carbs": 20, "fat": 4, "fibre": 1}, "source": "label"}
  ],
  "steps": ["..."], "tips": ["..."],
  "claimed": {"kcal": 450, "protein": 35}, "source": {"url": "...", "author": "..."}
}
Ingredient names are matched to data/nutrition.json (names and aliases). An unknown name stops with
an error listing it: add it to scripts/build_nutrition.py, or give per100g inline with a source.
Macros come from raw ingredient weights; actual values shift with cooking and oil absorption.
"""
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("kcal", "protein", "carbs", "fat", "fibre")
SIZE = {"small": 0.75, "medium": 1.0, "large": 1.25}
WEIGHT = {"g": 1, "gram": 1, "grams": 1, "kg": 1000, "oz": 28.35, "lb": 453.6}
VOLUME = {"ml": 1, "l": 1000, "litre": 1000, "liter": 1000}
COUNT = {"piece", "pieces", "pc", "pcs", "whole", "each", "nos", "medium", "large", "small"}
NONVEG, DAIRYISH = {"meat", "fish"}, {"dairy", "egg"}
DROP = {"fresh", "chopped", "diced", "sliced", "minced", "grated", "boiled", "cooked", "raw", "ripe", "large", "small", "medium",
        "finely", "roughly", "crushed", "ground", "powdered", "dried", "boneless", "skinless", "cubed", "thin", "thick", "whole", "of", "a"}


def load_db():
    items = json.loads((ROOT / "data" / "nutrition.json").read_text())["items"]
    names = {}
    for k, v in items.items():
        for n in [k] + v["aliases"]:
            names[re.sub(r"\s+", " ", n.lower().strip())] = k
    return items, names


def lookup(name, names):
    n = re.sub(r"\([^)]*\)", " ", name.lower())
    n = re.sub(r"[^a-z0-9 /&-]", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    cands = [n, re.sub(r"s$", "", n), re.sub(r"es$", "", n)]
    words = [w for w in n.split() if w not in DROP]
    cands += [" ".join(words), re.sub(r"s$", "", " ".join(words))]
    for c in cands:
        if c in names:
            return names[c]
    best = None  # longest known name that appears as whole words inside the given name
    for known in names:
        if re.search(rf"(?<![a-z]){re.escape(known)}(?![a-z])", n) and (best is None or len(known) > len(best)):
            best = known
    return names[best] if best else None


def number(q):
    if q is None or q == "":
        return None
    if isinstance(q, (int, float)):
        return float(q)
    q = str(q).strip().replace("½", " 1/2").replace("¼", " 1/4").replace("¾", " 3/4")
    try:
        return float(sum(Fraction(p) for p in q.split()))
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"cannot read quantity '{q}'")


def grams_for(ing, spec):
    """Return (grams, how). grams None means not countable (to taste)."""
    if ing.get("grams") is not None:
        return float(ing["grams"]), "stated grams"
    qty, unit = number(ing.get("qty")), str(ing.get("unit") or "").lower().strip().rstrip(".")
    if qty is None or qty == 0 or unit in ("to taste", "as needed", "pinch to taste", "for frying", "for serving", "as required"):
        return None, "to taste"
    units = spec["units"] if spec else {}
    dens = (spec or {}).get("units", {}).get("density", 1.0)
    unit = {"gms": "g", "gm": "g", "tablespoon": "tbsp", "tablespoons": "tbsp", "tbs": "tbsp", "teaspoon": "tsp", "teaspoons": "tsp",
            "cups": "cup", "cloves": "clove", "slices": "slice", "pods": "pod", "cans": "can", "scoops": "scoop", "pinches": "pinch",
            "millilitre": "ml", "milliliter": "ml", "mls": "ml"}.get(unit, unit)
    if unit in WEIGHT:
        return qty * WEIGHT[unit], "weight"
    if unit in VOLUME:
        return qty * VOLUME[unit] * dens, f"volume x density {dens}"
    if unit in COUNT or unit == "":
        base = units.get("piece")
        if base is None:
            raise ValueError(f"'{ing['name']}' has no piece weight; give grams or use g/ml/tsp/tbsp/cup")
        return qty * base * SIZE.get(unit, 1.0), f"{qty:g} x {base:g} g piece"
    if unit in units:
        return qty * units[unit], f"{qty:g} x {units[unit]:g} g {unit}"
    raise ValueError(f"cannot convert '{ing['name']}' {qty:g} {unit} to grams; give grams")


def build(inp, id_=None):
    items, names = load_db()
    servings = number(inp.get("servings")) or 1
    rows, unknown, errors = [], [], []
    for ing in inp["ingredients"]:
        spec, key = None, None
        if ing.get("per100g"):
            per = {f: float(ing["per100g"].get(f, 0)) for f in FIELDS}
            if not ing.get("source"):
                errors.append(f"'{ing['name']}': per100g needs a source")
            cat = "other"
            spec = {"units": {"piece": ing.get("piece_g")} if ing.get("piece_g") else {}}
            spec["units"].update({"tsp": 5, "tbsp": 15, "cup": 240})
        else:
            key = lookup(ing["name"], names)
            if not key:
                unknown.append(ing["name"])
                continue
            spec = items[key]
            per, cat = {f: spec[f] for f in FIELDS}, spec["category"]
        try:
            g, how = grams_for(ing, spec)
        except ValueError as e:
            errors.append(str(e))
            continue
        macros = {f: round(per[f] * g / 100, 1) for f in FIELDS} if g else None
        rows.append({"name": ing["name"], "matched": key or "inline per100g", "qty": ing.get("qty"), "unit": ing.get("unit"),
                     "grams": round(g, 1) if g else None, "how": how, "note": ing.get("note"), "group": ing.get("group"),
                     "estimated": bool(ing.get("estimated")), "category": cat, "macros": macros})
    if unknown or errors:
        msg = []
        if unknown:
            msg.append("unknown ingredients (add to scripts/build_nutrition.py or give per100g + source): " + ", ".join(unknown))
        msg += errors
        raise SystemExit("recipe_card: " + "; ".join(msg))

    counted = [r for r in rows if r["macros"]]
    total = {f: round(sum(r["macros"][f] for r in counted), 1) for f in FIELDS}
    grams_total = sum(r["grams"] for r in counted)
    per_serving = {f: round(total[f] / servings, 1) for f in FIELDS}
    per_100 = {f: round(total[f] * 100 / grams_total, 1) for f in FIELDS} if grams_total else {}
    kc = per_serving["protein"] * 4 + per_serving["carbs"] * 4 + per_serving["fat"] * 9
    split = {"protein": round(100 * per_serving["protein"] * 4 / kc), "carbs": round(100 * per_serving["carbs"] * 4 / kc),
             "fat": round(100 * per_serving["fat"] * 9 / kc)} if kc else {}
    cats = {r["category"] for r in rows}
    keys = {r["matched"] for r in rows}
    diet = "non-vegetarian" if cats & NONVEG else "eggetarian" if "egg" in cats else "vegetarian"
    vegan = not (cats & (NONVEG | DAIRYISH)) and "honey" not in keys
    notes = ["Calculated from raw ingredient weights with data/nutrition.json (USDA FoodData Central and IFCT based); accurate to about 10%. Cooking, water loss and oil absorption change the real values."]
    est = [r["name"] for r in rows if r["estimated"]]
    if est:
        notes.append("Amounts were not all stated in the video; estimated: " + ", ".join(est) + ".")
    skipped = [r["name"] for r in rows if not r["macros"]]
    if skipped:
        notes.append("Not counted (to taste): " + ", ".join(skipped) + ".")
    claim_check = []
    for field, label in (("kcal", "calories"), ("protein", "protein g")):
        claimed = (inp.get("claimed") or {}).get(field)
        if claimed:
            calc = per_serving[field]
            diff = round(100 * (calc - claimed) / claimed)
            verdict = "consistent" if abs(diff) <= 15 else "differs"
            claim_check.append({"field": field, "claimed": claimed, "calculated": calc, "diff_pct": diff, "verdict": verdict})
    card = {
        "id": id_ or inp.get("id"), "title": inp["title"], "servings": servings, "serving_note": inp.get("serving_note"),
        "time": inp.get("time") or {}, "cuisine": inp.get("cuisine"), "diet": diet, "vegan": vegan,
        "ingredients": rows, "steps": inp.get("steps") or [], "tips": inp.get("tips") or [],
        "macros": {"per_serving": per_serving, "total": total, "per_100g": per_100, "energy_split_pct": split,
                   "basis_grams": round(grams_total), "coverage_pct": 100 if not rows else round(100 * len(counted) / len(rows))},
        "claim_check": claim_check, "notes": notes, "source": inp.get("source") or {},
    }
    return card


def fmt_qty(r):
    q, u = r.get("qty"), (r.get("unit") or "").strip()
    if q in (None, "", 0):
        return u or ""
    q = number(q)
    s = f"{q:g}"
    return f"{'~' if r['estimated'] else ''}{s} {u}".strip()


def to_markdown(c):
    ps, m = c["macros"]["per_serving"], c["macros"]
    t = c["time"]
    bits = [f"serves {c['servings']:g}" + (f" ({c['serving_note']})" if c.get("serving_note") else "")]
    if t.get("prep"):
        bits.append(f"{t['prep']} min prep")
    if t.get("cook"):
        bits.append(f"{t['cook']} min cook")
    bits.append(c["diet"] + (", vegan" if c["vegan"] else ""))
    out = [f"## Recipe card", "", f"**{c['title']}** · " + " · ".join(bits), "",
           "| Per serving | kcal | Protein | Carbs | Fat | Fibre |", "|---|---|---|---|---|---|",
           f"| 1 serving | {ps['kcal']:g} | {ps['protein']:g} g | {ps['carbs']:g} g | {ps['fat']:g} g | {ps['fibre']:g} g |",
           f"| whole recipe | {m['total']['kcal']:g} | {m['total']['protein']:g} g | {m['total']['carbs']:g} g | {m['total']['fat']:g} g | {m['total']['fibre']:g} g |"]
    if m["per_100g"]:
        p = m["per_100g"]
        out.append(f"| per 100 g | {p['kcal']:g} | {p['protein']:g} g | {p['carbs']:g} g | {p['fat']:g} g | {p['fibre']:g} g |")
    out.append("")
    if m["energy_split_pct"]:
        s = m["energy_split_pct"]
        out += [f"Calories from protein {s['protein']}% · carbs {s['carbs']}% · fat {s['fat']}%.", ""]
    for cc in c["claim_check"]:
        out.append(f"Claim check: the video says {cc['claimed']:g} {'kcal' if cc['field'] == 'kcal' else 'g protein'} per serving; calculated {cc['calculated']:g} ({cc['diff_pct']:+d}%), {cc['verdict']}.")
    if c["claim_check"]:
        out.append("")
    out += ["### Ingredients", ""]
    group = object()
    for r in c["ingredients"]:
        if r.get("group") != group:
            group = r.get("group")
            if group:
                out += (["" ] if out[-1] != "" else []) + [f"**{group}**", ""]
        qty = fmt_qty(r)
        tt = qty.lower() in ("to taste", "as needed", "for frying", "for serving", "as required")
        line = (f"- {r['name']}, {qty}" if tt else f"- {qty} {r['name']}").replace("  ", " ")
        if r.get("note"):
            line += f", {r['note']}"
        if r["grams"] and (r.get("unit") or "").lower() not in ("g", "gram", "grams"):
            line += f" ({r['grams']:g} g)"
        out.append(line)
    out += ["", "### Method", ""]
    out += [f"{i}. {s}" for i, s in enumerate(c["steps"], 1)] or ["_Steps were not stated in the video._"]
    if c["tips"]:
        out += ["", "### Tips", ""] + [f"- {x}" for x in c["tips"]]
    out += ["", *[f"> {n}" for n in c["notes"]], ""]
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    out = None
    if "--out" in args:
        i = args.index("--out"); out = Path(args[i + 1]); del args[i:i + 2]
    md = "--markdown" in args
    args = [a for a in args if a != "--markdown"]
    if len(args) != 1:
        sys.exit(__doc__)
    inp = json.loads(Path(args[0]).read_text())
    card = build(inp)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(card, indent=1, ensure_ascii=False) + "\n")
    print(to_markdown(card) if md else json.dumps(card["macros"], indent=1))


if __name__ == "__main__":
    main()
