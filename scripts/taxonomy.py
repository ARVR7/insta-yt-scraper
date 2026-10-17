#!/usr/bin/env python3
"""Shared taxonomy helpers and the rename/merge command.

Library use:   from taxonomy import load, resolve_category, resolve_location
CLI:
  taxonomy.py check                       validate every note against taxonomy.yml
  taxonomy.py merge-sub  <cat> <from> <to>    move notes from one subcategory to another
  taxonomy.py merge-cat  <from> <to>          move notes (and subs, if names match) between categories
  taxonomy.py rename-city <country> <from> <to>   rename a city key in all notes
The CLI edits note front matter only; edit taxonomy.yml yourself, then run build_index.py.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def load():
    return yaml.safe_load((ROOT / "taxonomy.yml").read_text(encoding="utf8"))


def _lookup(table, value):
    """Resolve a key or alias in {key: {aliases: []}} to the canonical key."""
    v = slug(value)
    for key, spec in table.items():
        if v == key or v in [slug(a) for a in (spec or {}).get("aliases", [])]:
            return key
    return None


def resolve_category(tax, cat, sub=None):
    """Return (cat_key, sub_key or None) or raise ValueError with a helpful message."""
    ck = _lookup(tax["categories"], cat)
    if not ck:
        raise ValueError(f"unknown category '{cat}'. Known: {', '.join(tax['categories'])}")
    if not sub:
        return ck, None
    subs = tax["categories"][ck].get("subcategories") or {}
    sk = _lookup(subs, sub)
    if not sk:
        raise ValueError(f"unknown subcategory '{sub}' under '{ck}'. Known: {', '.join(subs) or 'none'}. Add it to taxonomy.yml if it is genuinely new")
    return ck, sk


def resolve_location(tax, loc):
    """'india/delhi' or 'Delhi' or 'india' -> ('india', 'delhi'|None)."""
    parts = [p for p in str(loc).split("/") if p.strip()]
    if len(parts) == 1:
        # a bare city name or alias: search the cities
        for ck, c in tax["locations"].items():
            if _lookup({ck: c}, parts[0]):
                return ck, None
            city = _lookup(c.get("cities") or {}, parts[0])
            if city:
                return ck, city
        raise ValueError(f"unknown location '{loc}'. Add the country/city to taxonomy.yml")
    country = _lookup(tax["locations"], parts[0])
    if not country:
        raise ValueError(f"unknown country '{parts[0]}'. Known: {', '.join(tax['locations'])}")
    cities = tax["locations"][country].get("cities") or {}
    city = _lookup(cities, parts[1])
    if not city:
        raise ValueError(f"unknown city '{parts[1]}' in '{country}'. Known: {', '.join(cities) or 'none'}. Add it to taxonomy.yml")
    return country, city


FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def notes():
    return sorted((ROOT / "notes").glob("*/*.md"))


def set_fields(path, updates):
    """Replace or append top-level front matter keys textually, preserving the rest."""
    text = path.read_text(encoding="utf8")
    m = FM.match(text)
    fm = m.group(1)
    for k, v in updates.items():
        line = f"{k}: {v}"
        if re.search(rf"^{k}:.*$", fm, re.M):
            fm = re.sub(rf"^{k}:.*$", line, fm, flags=re.M)
        else:
            fm += "\n" + line
    path.write_text("---\n" + fm + "\n---\n" + text[m.end():], encoding="utf8")


def get_meta(path):
    return yaml.safe_load(FM.match(path.read_text(encoding="utf8")).group(1)) or {}


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cmd, args = argv[0], argv[1:]
    tax = load()
    if cmd == "check":
        bad = 0
        for p in notes():
            m = get_meta(p)
            try:
                resolve_category(tax, m.get("category", ""), m.get("subcategory"))
                if m.get("location"):
                    resolve_location(tax, m["location"])
            except ValueError as e:
                bad += 1
                print(f"{p.relative_to(ROOT)}: {e}")
        sys.exit(1 if bad else 0)
    if cmd == "merge-sub" and len(args) == 3:
        cat, a, b = args
        n = 0
        for p in notes():
            m = get_meta(p)
            if slug(m.get("category", "")) == cat and slug(m.get("subcategory", "")) == a:
                set_fields(p, {"subcategory": b}); n += 1
        print(f"{n} notes moved {cat}/{a} -> {cat}/{b}. Now remove '{a}' from taxonomy.yml, then run build_index.py")
        return
    if cmd == "merge-cat" and len(args) == 2:
        a, b = args
        n = 0
        for p in notes():
            m = get_meta(p)
            if slug(m.get("category", "")) == a:
                set_fields(p, {"category": b}); n += 1
        print(f"{n} notes moved {a} -> {b}. Fix any subcategories, remove '{a}' from taxonomy.yml, run build_index.py")
        return
    if cmd == "rename-city" and len(args) == 3:
        country, a, b = args
        n = 0
        for p in notes():
            m = get_meta(p)
            if str(m.get("location", "")).lower() == f"{country}/{a}":
                set_fields(p, {"location": f"{country}/{b}"}); n += 1
        print(f"{n} notes updated. Rename the city key in taxonomy.yml, run build_index.py")
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
