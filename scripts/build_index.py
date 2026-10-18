#!/usr/bin/env python3
"""Rebuild the library index from the notes, validated against taxonomy.yml.

Usage: build_index.py
Reads front matter of notes/*/*.md and writes:
  data/library.json               machine index (the web app reads this)
  data/taxonomy.json              categories, subcategories, locations for the app
  data/search.json                full text of each note (summary, caption, transcript, screen text, research, recipe) for search
  library/README.md               every link, newest first
  library/by-category/<cat>.md    grouped by subcategory
  library/by-location/<loc>.md    one file per country or country-city
  library/by-usefulness/<u>.md    helpful / mixed / misleading / noise
All files under library/ and data/ are generated: edit the notes, then rerun this.
"""
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import taxonomy as tx  # noqa: E402

ROOT = tx.ROOT
USEFULNESS = ["helpful", "mixed", "misleading", "noise"]
BLURB = {
    "helpful": "Verified, actionable tools, hacks or facts.",
    "mixed": "A real tool or fact, but with misleading framing or unproven claims.",
    "misleading": "Mostly hoax, hype or unsupported claims.",
    "noise": "Nothing informative (side quests).",
}
REQUIRED = ["url", "platform", "title", "usefulness", "verdict", "key_info", "category"]


def fail(path, msg):
    sys.exit(f"{path.relative_to(ROOT)}: {msg}")


def read_note(path, tax):
    if re.search(r"\bTODO\b", path.read_text(encoding="utf8")):
        fail(path, "still contains TODO placeholders from the draft")
    meta = tx.get_meta(path)
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        fail(path, f"front matter lacks {', '.join(missing)}")
    title = str(meta["title"])
    if len(title) > 50 or "(" in title or ")" in title:
        fail(path, f"title '{title}' must be a plain name of at most 50 characters with no parentheses")
    if meta["usefulness"] not in USEFULNESS:
        fail(path, f"usefulness must be one of {USEFULNESS}")
    cats = tax["categories"]
    try:
        ck, sk = tx.resolve_category(tax, meta["category"], meta.get("subcategory"))
        if cats[ck].get("subcategories") and not sk:
            fail(path, f"category '{ck}' needs a subcategory: {', '.join(cats[ck]['subcategories'])}")
        country = city = None
        if meta.get("location"):
            country, city = tx.resolve_location(tax, meta["location"])
        also = []
        for a in meta.get("also") or []:
            c, _, s = str(a).partition("/")
            ac, asub = tx.resolve_category(tax, c, s or None)
            if (ac, asub) != (ck, sk):
                also.append(ac + (f"/{asub}" if asub else ""))
    except ValueError as e:
        fail(path, str(e))
    loc = None
    if country:
        loc = country + (f"/{city}" if city else "")
    locs = tax["locations"]
    loc_label = None
    if country:
        loc_label = locs[country]["label"] if not city else f"{locs[country]['cities'][city]['label']}, {locs[country]['label']}"
    recipe = None
    if meta.get("recipe"):
        rp = ROOT / meta["recipe"]
        if not rp.exists():
            fail(path, f"recipe file {meta['recipe']} is missing")
        card = json.loads(rp.read_text(encoding="utf8"))
        ps = card["macros"]["per_serving"]
        recipe = {"path": meta["recipe"], "servings": card["servings"], "kcal": ps["kcal"], "protein": ps["protein"],
                  "carbs": ps["carbs"], "fat": ps["fat"], "diet": card["diet"]}
    return {
        "id": path.stem,
        "platform": meta["platform"],
        "url": meta["url"],
        "title": meta["title"],
        "author": meta.get("author") or "",
        "posted": str(meta.get("posted") or ""),
        "type": meta.get("type") or "",
        "category": ck,
        "category_label": cats[ck]["label"],
        "subcategory": sk,
        "subcategory_label": cats[ck]["subcategories"][sk]["label"] if sk else None,
        "location": loc,
        "location_label": loc_label,
        "also": also,
        "recipe": recipe,
        "tools": meta.get("tools") or [],
        "usefulness": meta["usefulness"],
        "verdict": meta["verdict"],
        "key_info": " ".join(str(meta["key_info"]).split()),
        "note_path": str(path.relative_to(ROOT)),
    }


SEARCH_FIELDS = {  # note heading -> search field
    "Summary": "summary", "Caption / hashtags": "caption", "Transcript (auto)": "transcript",
    "What is shown on screen": "screen", "Hook (on-screen text)": "hook", "Call to action": "cta",
    "Recipe card": "recipe", "Your instruction": "instruction", "Notes / caveats": "caveats",
}


def search_doc(path, item):
    """Plain-text fields of one note for the app's full-text search (capped so the index stays small)."""
    body = re.sub(r"\A---\n.*?\n---\n", "", path.read_text(encoding="utf8"), flags=re.S)
    fields = {}
    for part in re.split(r"^## ", body, flags=re.M)[1:]:
        head, _, text = part.partition("\n")
        key = "research" if head.startswith("Research") else "followup" if head.startswith("Follow-up") else SEARCH_FIELDS.get(head.strip())
        if key:
            text = re.sub(r"[#>*`|]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or " ", text)
            fields[key] = (fields.get(key, "") + " " + re.sub(r"\s+", " ", text).strip())[:4000].strip()
    return {
        "id": item["id"], "platform": item["platform"], "title": item["title"], "author": item["author"],
        "key_info": item["key_info"], "tools": " ".join(item["tools"]),
        "where": " ".join(filter(None, [item["category_label"], item["subcategory_label"], item["location_label"]])),
        "fields": fields,
    }


def row(i, up):
    t = i["title"].replace("|", "/")
    k = i["key_info"].replace("|", "/")
    where = f" · {i['location_label']}" if i["location_label"] else ""
    return f"| [{t}]({i['url']}) | {i['usefulness']} | {i['category_label']}{' › ' + i['subcategory_label'] if i['subcategory_label'] else ''}{where} | {k} | [note]({up}/{i['note_path']}) |"


def table(items, up="."):
    head = "| Link | Usefulness | Category | Key info | Note |\n|---|---|---|---|---|\n"
    return head + "\n".join(row(i, up) for i in items) + "\n"


def taxonomy_json(tax):
    return {
        "categories": [
            {"key": k, "label": c["label"], "icon": c.get("icon", "dots"), "colors": c.get("colors", ["#a3a8b3", "#7d828f"]),
             "subcategories": [{"key": sk, "label": s["label"]} for sk, s in (c.get("subcategories") or {}).items()]}
            for k, c in tax["categories"].items()
        ],
        "locations": [
            {"key": k, "label": c["label"], "cities": [{"key": ck, "label": cc["label"]} for ck, cc in (c.get("cities") or {}).items()]}
            for k, c in tax["locations"].items()
        ],
    }


def main():
    tax = tx.load()
    items = [read_note(p, tax) for p in tx.notes()]
    items.sort(key=lambda i: i["posted"], reverse=True)

    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "library.json").write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n")
    docs = [search_doc(ROOT / i["note_path"], i) for i in items]
    (ROOT / "data" / "search.json").write_text(json.dumps(docs, ensure_ascii=False, separators=(",", ":")) + "\n")
    (ROOT / "data" / "taxonomy.json").write_text(json.dumps(taxonomy_json(tax), indent=2, ensure_ascii=False) + "\n")

    lib = ROOT / "library"
    shutil.rmtree(lib / "by-topic", ignore_errors=True)  # replaced by by-category
    for sub in ("by-usefulness", "by-category", "by-location"):
        d = lib / sub
        d.mkdir(parents=True, exist_ok=True)
        for f in d.glob("*.md"):
            f.unlink()
    note = "_Generated by `scripts/build_index.py`. Edit the notes, not this file._\n\n"

    counts = {u: sum(1 for i in items if i["usefulness"] == u) for u in USEFULNESS}
    summary = " · ".join(f"{u}: {n}" for u, n in counts.items())
    (lib / "README.md").write_text(f"# Library\n\n{note}{len(items)} links. {summary}\n\n" + table(items))

    for u in USEFULNESS:
        sel = [i for i in items if i["usefulness"] == u]
        (lib / "by-usefulness" / f"{u}.md").write_text(
            f"# {u.capitalize()}\n\n{note}{BLURB[u]}\n\n" + (table(sel, "../..") if sel else "_None yet._\n"))

    for ck, c in tax["categories"].items():
        sel = [i for i in items if i["category"] == ck or any(a.split("/")[0] == ck for a in i["also"])]
        if not sel:
            continue
        body = f"# {c['label']}\n\n{note}{c.get('about', '')}\n\n{len(sel)} links.\n\n"
        groups = defaultdict(list)
        for i in sel:
            groups[(i["subcategory_label"] if i["category"] == ck else "Also listed here") or "General"].append(i)
        for g in sorted(groups, key=lambda g: (g == "Also listed here", g)):
            body += f"## {g}\n\n" + table(groups[g], "../..") + "\n"
        (lib / "by-category" / f"{ck}.md").write_text(body)

    byloc = defaultdict(list)
    for i in items:
        if i["location"]:
            byloc[i["location"]].append(i)
            if "/" in i["location"]:
                byloc[i["location"].split("/")[0]].append(i)
    for loc, sel in sorted(byloc.items()):
        label = sel[0]["location_label"] if "/" in loc else tax["locations"][loc]["label"]
        (lib / "by-location" / f"{loc.replace('/', '-')}.md").write_text(f"# {label}\n\n{note}{len(sel)} links.\n\n" + table(sel, "../.."))

    print(f"{len(items)} notes; usefulness: {summary}; categories used: {len({i['category'] for i in items})}; locations used: {len(byloc)}")


if __name__ == "__main__":
    main()
