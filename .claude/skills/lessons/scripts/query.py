#!/usr/bin/env python3
"""Print the ACTIVE lessons for what you are about to do, one line each (keep Step 0 output short).
usage: python3 query.py --stage captions,zoom [--type preference,rule,gotcha] [--topic T] [--about ID [--depth 1]] [--why] [--all] [--retros N] [-h|--help]
stages: plan,download,moments,render,layout,captions,zoom,facecam,publish,infra (start of a job: pass ALL of them to print every active lesson). No arguments: prints every active lesson. -h/--help: print this text and exit.
--about walks the graph links both ways; --all includes superseded notes; --why adds the reason.
--retros N  also print the OPEN findings (disposition PENDING or backlog) of the newest N streams/*/docs/retro.md, and the open incidents (lessons/incidents.json: enforced_by none, or count >= 2); prints nothing for either when there are none. Alone (no --stage/--type/--topic/--about) it prints only that part."""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lessons_lib as L
a = sys.argv[1:]
if "-h" in a or "--help" in a:
    print(__doc__.strip()); sys.exit(0)
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
notes = L.load_all(); by = {n["id"]: n for n in notes}
pid = {os.path.normpath(n["_path"]): n["id"] for n in notes}
retros_n = int(opt("--retros", "0") or 0)
if retros_n and not any(opt(k) for k in ("--stage", "--type", "--topic", "--about")):
    a = a + ["--no-lessons"]
sel = notes
if opt("--stage"):
    st = opt("--stage").split(","); sel = [n for n in sel if n.get("stage") in st]
if opt("--type"):
    ty = opt("--type").split(","); sel = [n for n in sel if n.get("type") in ty]
if opt("--topic"):
    sel = [n for n in sel if n.get("topic") == opt("--topic")]
if opt("--about"):
    seen, front = {opt("--about")}, {opt("--about")}
    for _ in range(int(opt("--depth", "1"))):
        nxt = set()
        for i in front:
            nxt |= {pid[l] for l in by[i]["_links"] if l in pid}
            nxt |= {n["id"] for n in notes if i in [pid.get(l) for l in n["_links"]]}
        front = nxt - seen; seen |= nxt
    sel = [n for n in sel if n["id"] in seen]
if "--all" not in a:
    sel = [n for n in sel if n.get("status") == "active"]
if "--no-lessons" not in a:
    print(f"LESSONS ({len(sel)}) " + ("(all)" if "--all" in a else "(active only)"))
    for n in sel:
        print(f"[{n.get('stage')}] {n['id']} ({n['type']}): {n['_rule']}" + (f"  WHY: {n['_why']}" if "--why" in a else ""))

if retros_n:
    repo = os.path.abspath(os.path.join(L.ROOT, ".."))
    FINDING = re.compile(r"^- (F\d+) \[([\w-]+)\] (.*) \| disposition: (.*?)(?: <!--k:.*?-->)?\s*$")
    files = sorted(glob.glob(os.path.join(repo, "streams", "*", "docs", "retro.md")), key=os.path.getmtime, reverse=True)[:retros_n]
    for f in files:
        rows = [m.groups() for m in (FINDING.match(l.rstrip("\n")) for l in open(f, encoding="utf-8")) if m]
        open_ = [r for r in rows if r[3].strip().upper().startswith("PENDING") or r[3].strip().lower().startswith("backlog")]
        if open_:
            print(f"OPEN RETRO FINDINGS ({os.path.basename(os.path.dirname(os.path.dirname(f)))}, {len(open_)} of {len(rows)}):")
            for fid, kind, text, disp in open_:
                print(f"  {fid} [{kind}] {text[:140]} -> {disp[:60]}")
    try:
        import json
        inc = [i for i in json.load(open(os.path.join(L.ROOT, "incidents.json"), encoding="utf-8")).get("incidents", [])
               if str(i.get("enforced_by", "none")).strip().lower() in ("none", "") or int(i.get("count", 0)) >= 2]
    except (OSError, ValueError):
        inc = []
    if inc:
        print(f"OPEN INCIDENTS ({len(inc)}):")
        for i in inc:
            print(f"  {i['id']}: count {i.get('count', 0)}, enforced_by {i.get('enforced_by', 'none')}" + (" -> MUST BECOME A CHECK before the next job" if int(i.get("count", 0)) >= 2 and str(i.get("enforced_by", "none")) == "none" else ""))
