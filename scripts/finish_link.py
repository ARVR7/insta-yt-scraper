#!/usr/bin/env python3
"""Everything mechanical after the judgment is done.

Usage: finish_link.py <verdict.json> [--push] [--trailer "Co-Authored-By: ..."]...

verdict.json (written by Claude; short):
{
  "draft": "<scratch>/draft_note.md",           # from prepare_link.py; the script writes the note from it
  "fill": {                                       # only the judgment: the mechanical parts stay untouched
    "title": "Plain name, max 50 chars", "category": "ai", "subcategory": "creative",
    "location": "india/delhi",                    # optional
    "also": ["money/investing"],                  # optional
    "tools": ["name"], "usefulness": "helpful", "verdict": "verified",
    "key_info": "What it is and the main caveat.", "hook": "...", "cta": "...", "on_screen": "...",
    "summary": "...", "research": [["claim", "verdict", "evidence with [links](https://...)"]],
    "overall": "...", "caveats": ["...", "..."]
  },
  "recipe": {                                     # REQUIRED for food/recipes: input for scripts/recipe_card.py
    "title": "...", "servings": 2, "time": {"prep": 10, "cook": 15},
    "ingredients": [{"name": "paneer", "qty": 200, "unit": "g"}], "steps": ["..."], "tips": [],
    "claimed": {"kcal": 450, "protein": 35}                # only if the video states macros
  },
  "overwrite": false,                             # true only to redo an existing note
  # (or give "note": "notes/instagram/<id>.md" for a note you already wrote by hand)
  "entries": [                                    # claim-level registry entries
    {"section": "verified|pending|hoax|sidequest", "name": "...", "verdict": "verified-with-caveats",
     "what": "...", "how": "...", "caveats": "...", "why": "...", "resolve": "...",
     "evidence": [["label", "https://..."]]}
  ],
  "decision": {"title": "...", "text": "..."}     # optional, only for non-routine choices
}

Does: add the registry entries in the right files and format (skipping duplicates), validate the
taxonomy, rebuild data/ and library/, regenerate the "Current notes" table in flow.md, write the
issue comment to <note>.comment.md (and print it), and with --push commit and push to main with
retries. Refuses to run if the note still contains TODO.
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import taxonomy as tx  # noqa: E402

ROOT = tx.ROOT
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
FILES = {"verified": "registry/verified.md", "pending": "registry/verified.md", "hoax": "registry/hoax.md", "sidequest": "registry/sidequests.md"}


def fail(msg):
    sys.exit(f"finish_link: {msg}")


def entry_md(e, note_rel):
    ev = ", ".join(f"[{l}]({u})" for l, u in e.get("evidence", []))
    lines = [f"### {e['name']}  ({TODAY})", f"- **Verdict:** {e['verdict']}"]
    if e.get("what"):
        lines.append(f"- **What it is:** {e['what']}")
    if e["section"] == "verified" and e.get("how"):
        lines.append(f"- **How to use / why it matters:** {e['how']}")
    if e.get("caveats"):
        lines.append(f"- **Caveats:** {e['caveats']}")
    if e.get("why"):
        lines.append(f"- **{'Why pending' if e['section'] == 'pending' else 'Why it is ' + e['verdict']}:** {e['why']}")
    if e["section"] == "pending" and e.get("resolve"):
        lines.append(f"- **To resolve:** {e['resolve']}")
    if ev:
        lines.append(f"- **Evidence:** {ev}")
    lines.append(f"- **Source note:** [{note_rel}](../{note_rel})")
    return "\n".join(lines) + "\n\n"


def add_entries(entries, note_rel):
    done, skipped = [], []
    for e in entries:
        path = ROOT / FILES[e["section"]]
        text = path.read_text(encoding="utf8")
        if re.search(rf"^### {re.escape(e['name'])}\b", text, re.M) or (e["section"] == "sidequest" and f"- {e['name']} (" in text):
            skipped.append(e["name"])
            continue
        md = entry_md(e, note_rel) if e["section"] != "sidequest" else ""
        if e["section"] == "pending":
            anchor = "## Pending verification\n\n"
            text = text.replace(anchor, anchor + md, 1) if anchor in text else text + "\n" + anchor + md
        elif e["section"] == "verified":
            anchor = "## Verified\n\n"
            text = text.replace(anchor, anchor + md, 1)
        elif e["section"] == "hoax":
            first = re.search(r"\n### ", text)
            text = text[:first.start() + 1] + md + text[first.start() + 1:] if first else text.rstrip() + "\n\n" + md
        else:  # side quest: one line each
            line = f"- {e['name']} ({TODAY}): {e.get('what', '')} [{note_rel}](../{note_rel})\n"
            text = text.replace("_(none yet)_\n", "").rstrip() + "\n" + line
        path.write_text(text, encoding="utf8")
        done.append(e["name"])
    return done, skipped


def add_decision(d):
    p = ROOT / "decision.md"
    text = p.read_text(encoding="utf8")
    block = f"### {d['title']}\n{d['text'].strip()}\n\n"
    m = re.search(r"^## (\d{4}-\d{2}-\d{2})\n", text, re.M)
    if m and m.group(1) == TODAY:
        i = m.end()
        text = text[:i] + "\n" + block + text[i:].lstrip("\n")
    else:
        i = m.start() if m else len(text)
        text = text[:i] + f"## {TODAY}\n\n" + block + text[i:]
    p.write_text(text, encoding="utf8")


def refresh_flow(items):
    p = ROOT / "flow.md"
    text = p.read_text(encoding="utf8")
    rows = "\n".join(f"| [{i['note_path']}]({i['note_path']}) | {i['category_label']} · {i['usefulness']} · {i['verdict']} |" for i in items)
    section = "## Current notes\n| Note | Category · usefulness · verdict |\n|---|---|\n" + rows + "\n"
    text = re.sub(r"## Current notes\n.*\Z", section, text, flags=re.S) if "## Current notes" in text else text.rstrip() + "\n\n" + section
    p.write_text(text, encoding="utf8")


def comment_text(item, note_path):
    meta = tx.get_meta(ROOT / note_path)
    gaps = [f"{k}: {v}" for k, v in (meta.get("fetch_status") or {}).items() if re.search(r"not |blocked|none", str(v), re.I)]
    c = f"**Verdict: {item['verdict']} ({item['usefulness']}).**\n\n{item['key_info']}\n"
    if gaps:
        c += "\nNot fetched or limited: " + "; ".join(gaps) + ".\n"
    c += f"\nNote: [{note_path}](https://github.com/ARVR7/insta-yt-scraper/blob/main/{note_path})\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_\n"
    return c


def git(*args, check=True):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=check)


def push(msg, trailers):
    git("add", "-A")
    if not git("status", "--porcelain").stdout.strip():
        return "nothing to commit"
    body = msg + ("\n\n" + "\n".join(trailers) if trailers else "")
    git("commit", "-q", "-m", body)
    delay = 2
    for attempt in range(5):
        git("fetch", "-q", "origin", "main", check=False)
        git("rebase", "-q", "origin/main", check=False)
        r = git("push", "origin", "main", check=False)
        if r.returncode == 0:
            return "pushed " + git("rev-parse", "--short", "HEAD").stdout.strip()
        if attempt < 4:
            time.sleep(delay); delay *= 2
    return "PUSH FAILED: " + (r.stderr or r.stdout).strip()[-200:]


def write_note(v):
    """Create notes/<platform>/<id>.md from the draft by filling its TODO placeholders."""
    draft = Path(v["draft"]).read_text(encoding="utf8")
    f = v["fill"]
    for k in ("title", "category", "subcategory", "usefulness", "verdict", "key_info", "summary", "research"):
        if not f.get(k) and not (k == "subcategory" and f.get("category") == "other"):
            fail(f"fill.{k} is required")
    meta = tx.get_meta(Path(v["draft"]))
    sys.path.insert(0, str(HERE))
    from prepare_link import classify  # noqa: E402
    platform, vid, _ = classify(meta["url"])
    rel = f"notes/{platform}/{vid}.md"
    if (ROOT / rel).exists() and not v.get("overwrite"):
        fail(f"{rel} already exists (set overwrite: true to redo it)")
    secs = sorted({e["section"] for e in v.get("entries", [])})
    reg = ", ".join(sorted({FILES[x] for x in secs})) or f.get("registry") or "none"
    q = json.dumps
    recipe_md = ""
    if f.get("category") == "food" and f.get("subcategory") == "recipes" and not v.get("recipe"):
        fail("food/recipes notes need a \"recipe\" object (ingredients with amounts, steps) so macros and the recipe card can be built")
    fm_extra = ""
    if v.get("recipe"):
        import recipe_card
        card = recipe_card.build(v["recipe"], id_=f"{platform}_{vid}")
        card["source"] = card.get("source") or {"url": meta["url"], "author": meta.get("author")}
        rp = ROOT / "recipes" / f"{platform}_{vid}.json"
        rp.parent.mkdir(exist_ok=True)
        rp.write_text(json.dumps(card, indent=1, ensure_ascii=False) + "\n", encoding="utf8")
        recipe_md = recipe_card.to_markdown(card)
        fm_extra += f"recipe: {q(str(rp.relative_to(ROOT)))}\n"
    if f.get("location"):
        fm_extra += f"location: {q(f['location'])}\n"
    if f.get("also"):
        fm_extra += f"also: {q(f['also'])}\n"
    rep = {
        r"^title: TODO$": f"title: {q(f['title'])}", r"^category: TODO$": f"category: {f['category']}",
        r"^subcategory: TODO$": f"subcategory: {f.get('subcategory') or 'null'}\n{fm_extra}".rstrip("\n"),
        r"^usefulness: TODO$": f"usefulness: {f['usefulness']}", r"^tools: \[\]$": f"tools: {q(f.get('tools') or [])}",
        r'^key_info: "TODO"$': f"key_info: {q(f['key_info'])}", r"^verdict: TODO$": f"verdict: {f['verdict']}",
        r"^registry: TODO$": f"registry: {reg}", r"^# TODO$": f"# {f['title']}",
        r"^Overall: TODO$": f"Overall: {f.get('overall', '')}",
    }
    out = draft
    for pat, val in rep.items():
        out = re.sub(pat, lambda m, val=val: val, out, count=1, flags=re.M)
    for head, key in (("## Hook (on-screen text)", "hook"), ("## Call to action", "cta"), ("## What is shown on screen", "on_screen"), ("## Summary", "summary")):
        out = out.replace(f"{head}\nTODO", f"{head}\n{f.get(key) or 'None.'}", 1)
    if recipe_md:
        out = out.replace("## Research (checked", recipe_md + "\n## Research (checked", 1)
    rows = "\n".join("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in f["research"])
    out = out.replace("| TODO | TODO | TODO |", rows, 1)
    out = out.replace("- TODO", "\n".join(f"- {c}" for c in (f.get("caveats") or ["None."])), 1)
    if re.search(r"\bTODO\b", out):
        fail("draft still has unfilled TODO placeholders after filling: " + ", ".join(sorted(set(re.findall(r".*\bTODO\b.*", out)))[:3]))
    (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / rel).write_text(out, encoding="utf8")
    return rel


def main():
    args = sys.argv[1:]
    trailers = []
    while "--trailer" in args:
        i = args.index("--trailer"); trailers.append(args[i + 1]); del args[i:i + 2]
    do_push = "--push" in args
    args = [a for a in args if a != "--push"]
    if len(args) != 1:
        sys.exit(__doc__)
    v = json.loads(Path(args[0]).read_text())
    note_rel = write_note(v) if v.get("draft") else v["note"]
    note = ROOT / note_rel
    if not note.exists():
        fail(f"{note_rel} does not exist (move the filled-in draft there first)")
    if re.search(r"\bTODO\b", note.read_text(encoding="utf8")):
        fail(f"{note_rel} still contains TODO placeholders")
    r = subprocess.run([sys.executable, str(HERE / "build_index.py")], capture_output=True, text=True)
    if r.returncode != 0:  # validate the note before touching anything else
        fail(r.stderr.strip() or r.stdout.strip())
    done, skipped = add_entries(v.get("entries", []), note_rel)
    if v.get("decision"):
        add_decision(v["decision"])
    if v.get("draft"):  # a draft prepared by GitHub Actions lives in inbox/; it has served its purpose
        d = Path(v["draft"]).resolve().parent
        if d.parent == (ROOT / "inbox").resolve():
            import shutil
            shutil.rmtree(d, ignore_errors=True)
    items = json.loads((ROOT / "data" / "library.json").read_text())
    refresh_flow(items)
    me = next((i for i in items if i["note_path"] == note_rel), None)
    if not me:
        fail("note was not indexed")
    comment = comment_text(me, note_rel)
    cpath = Path(args[0]).with_suffix(".comment.md")  # beside the verdict file (scratch), never in notes/
    cpath.write_text(comment)
    out = {"registry_added": done, "registry_skipped_duplicates": skipped, "index": r.stdout.strip()}
    if do_push:
        out["git"] = push(v.get("commit") or f"Add note for {me['platform']} {me['id']}", trailers)
    print(json.dumps(out, indent=2))
    print("--- issue comment ---")
    print(comment)


if __name__ == "__main__":
    main()
