#!/usr/bin/env python3
"""Compare this checkout (the NEW repo, any checkout of main) with migration-setup/MANIFEST.json written by make_manifest.py in the OLD repo.
    python3 migration-setup/verify_manifest.py [--manifest PATH] [--no-preflight] [--kaggle] [--skip-env] [--quiet-files]
Prints a PASS/FAIL table and exits 1 if any row is FAIL. Never prints a secret: environment variables are checked by NAME only (os.environ keys);
Kaggle dataset names come from `kaggle.py raw datasets list --mine` (only the name column is kept).
Statuses: PASS ok | FAIL must be fixed | WARN worth a look, not blocking | NOTE explained difference | SKIP not checked (with the reason).
About sha values after the move: `git push --mirror`, a fork and a repository transfer keep EVERY commit and tree sha identical; a fresh copy of the files
(new `git init`, upload, zip) gets new shas. The file hashes (sha256) are the real test in both cases; the tree check says which case you are in.
  --no-preflight  do not run preflight.py (it contacts git origin, kaggle files and the job registry)
  --kaggle        also run `kaggle.py raw datasets list --mine` and compare the dataset names (needs Kaggle credentials; names only)
  --skip-env      do not check environment variable names (a plain checkout outside a session)"""
import argparse, json, os, re, subprocess as sp, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_manifest as mm

ROOT = mm.ROOT
KAGGLE_PY = os.path.join(ROOT, ".claude/skills/clips/scripts/download/kaggle.py")
rows = []   # (status, check, detail)


def add(status, check, detail=""):
    rows.append((status, check, detail))


def short(items, n=6):
    items = list(items)
    return ", ".join(items[:n]) + (f" ... (+{len(items) - n} more)" if len(items) > n else "")


def run(cmd, timeout=300, env=None):
    try:
        r = sp.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT, env=env)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 127, str(e)


def check_files(man, quiet):
    want = {e["path"]: e for e in man["files"]}
    have = set(p for p in mm.tracked() if p != mm.MANIFEST_REL)
    untracked = [p for p in mm.git("ls-files", "-o", "--exclude-standard", "-z").split("\0") if p and p != mm.MANIFEST_REL]
    present = {p for p in have if os.path.isfile(os.path.join(ROOT, p))}
    missing = sorted(p for p in want if p not in present)
    extra = sorted((have | set(untracked)) - set(want))
    changed = []
    for p in sorted(set(want) & present):
        e = want[p]
        if os.path.getsize(os.path.join(ROOT, p)) != e["size"] or mm.sha256_file(os.path.join(ROOT, p)) != e["sha256"]:
            changed.append(p)
    n = len(want)
    add("PASS" if not missing else "FAIL", "files missing", f"{len(missing)} of {n}" + (": " + short(missing) if missing else ""))
    add("PASS" if not changed else "FAIL", "files changed (sha256)", f"{len(changed)} of {n}" + (": " + short(changed) if changed else ""))
    add("PASS" if not extra else "WARN", "files extra", f"{len(extra)}" + (": " + short(extra) + " (new work since the move is fine; unknown files are not)" if extra else ""))
    if not quiet and (missing or changed or extra):
        for tag, lst in (("MISSING", missing), ("CHANGED", changed), ("EXTRA", extra)):
            for p in lst:
                print(f"  {tag}  {p}")
    return not missing and not changed


def check_history(man, files_ok):
    head = mm.git("rev-parse", "HEAD")
    try:
        twm = mm.tree_without_manifest()
    except SystemExit as e:
        twm = None
    shallow = mm.git("rev-parse", "--is-shallow-repository", check=False) == "true"
    same_commit = bool(mm.git("cat-file", "-t", man["commit"] + "^{commit}", check=False) == "commit")
    if twm == man["tree_without_manifest"]:
        add("PASS", "tree sha (without MANIFEST.json)", f"identical {twm[:12]}: the content is the same byte for byte")
    elif files_ok:
        add("NOTE", "tree sha (without MANIFEST.json)", f"differs ({(twm or '?')[:12]} vs {man['tree_without_manifest'][:12]}) but every file hash matches: extra files or modes only; explained by the EXTRA row")
    else:
        add("WARN", "tree sha (without MANIFEST.json)", f"differs ({(twm or '?')[:12]} vs {man['tree_without_manifest'][:12]}); see missing/changed rows")
    if same_commit:
        add("PASS", "old commit in history", f"{man['commit'][:12]} exists here: mirror / fork / transfer, all shas are identical")
    else:
        add("NOTE", "old commit in history", f"{man['commit'][:12]} not found: a fresh copy of the files (new shas are expected); the file hashes are the test" + (" [shallow clone: history cut]" if shallow else ""))
    n, old = int(mm.git("rev-list", "--count", "HEAD")), man["commit_count"]
    if shallow:
        add("SKIP", "commit count", f"shallow clone ({n} commits visible): run `git fetch --unshallow`")
    elif n == old:
        add("PASS", "commit count", f"{n}")
    elif n > old:
        add("NOTE", "commit count", f"{n} here vs {old} in the manifest: commits were added after it (the manifest and migration docs, new work)")
    elif same_commit:
        add("FAIL", "commit count", f"{n} here vs {old}: history lost commits although the old commit exists")
    else:
        add("NOTE", "commit count", f"{n} here vs {old} in the manifest: a fresh copy has its own history, nothing to compare")
    big, mx = mm.big_blobs(["--all"])
    allowed = {b["sha"] for b in man.get("blobs_over_30mb", [])}
    new_big = [b for b in big if b["sha"] not in allowed]
    mb = lambda x: f"{x / 1048576:.1f} MB"
    if mx >= 100 * 1048576:
        add("FAIL", "largest blob", f"{mb(mx)}: GitHub rejects pushes with a blob over 100 MB")
    elif new_big:
        add("FAIL", "largest blob", f"{len(new_big)} blob(s) over 30 MB that the old repo did not have: " + short(f"{b['path'] or b['sha'][:10]} {mb(b['size'])}" for b in new_big))
    else:
        old_mx = man["largest_blob_bytes"]["all_refs"]
        add("PASS", "largest blob", f"{mb(mx)} (old repo {mb(old_mx)}); {len(big)} blob(s) over 30 MB, all known from the manifest")


def check_counts(man):
    cur = mm.counts([p for p in mm.tracked() if p != mm.MANIFEST_REL])
    bad, more = [], []

    def cmp(label, nv, ov):
        if nv is None or nv < ov:
            bad.append(f"{label} {nv} vs {ov}")
        elif nv > ov:
            more.append(f"{label} {nv} vs {ov}")
    for k, v in man["counts"].items():
        if isinstance(v, dict):
            for s, ov in v.items():
                cmp(f"{k}[{s[:18]}]", cur[k].get(s, 0), ov)
        elif v is not None:
            cmp(k, cur.get(k), v)
    summary = (f"lessons {cur['lessons_active']} active + {cur['lessons_superseded']} superseded, incidents {cur['incidents']}, scripts {cur['scripts']}, "
               f"destinations {cur['destinations']}, streams {cur['streams']}, clips {list(cur['clips_per_stream'].values())}, mp4 {cur['mp4_total']}")
    if bad:
        add("FAIL", "counts", "fewer than the old repo: " + short(bad) + " | " + summary)
    elif more:
        add("NOTE", "counts", "more than the manifest (new work): " + short(more))
    else:
        add("PASS", "counts", summary)


def check_graph():
    gj, ix = os.path.join(ROOT, "lessons/graph.json"), os.path.join(ROOT, "lessons/INDEX.md")
    keep = {p: (open(p, "rb").read() if os.path.exists(p) else None) for p in (gj, ix)}
    rc, out = run([sys.executable, os.path.join(ROOT, ".claude/skills/lessons/scripts/build_graph.py")], 120)
    for p, b in keep.items():   # build_graph rewrites both files; put them back so the check leaves the checkout untouched
        if b is not None and open(p, "rb").read() != b:
            open(p, "wb").write(b)
    add("PASS" if rc == 0 else "FAIL", "lessons graph builds", (out.strip().splitlines() or ["no output"])[-1][:200])


def check_preflight():
    pf = os.path.join(ROOT, ".claude/skills/clips/scripts/preflight.py")
    if not os.path.exists(pf):
        return add("FAIL", "preflight.py", "missing")
    rc, out = run([sys.executable, pf], 240)
    lines = out.splitlines()
    n = lambda w: sum(1 for l in lines if l.startswith(w + " "))
    fails = [l.split()[1] for l in lines if l.startswith("FAIL ")]
    warns = [l.split()[1] for l in lines if l.startswith("WARN ")]
    last = next((l for l in reversed(lines) if l.startswith("PREFLIGHT")), "no PREFLIGHT line")
    st = "FAIL" if (rc != 0 or fails) else ("WARN" if warns else "PASS")
    add(st, "preflight.py", f"{n('PASS')} pass, {len(warns)} warn, {len(fails)} fail" + (f"; FAIL: {short(fails)}" if fails else "") + (f"; WARN: {short(warns)}" if warns else "") + f" | {last[:80]}")


def check_env(man):
    spec = man["env_var_names"]
    for g in spec["required_any"]:
        got = [x for x in g["names"] if x in os.environ]
        f = g.get("or_file") and os.path.exists(os.path.expanduser(g["or_file"]))
        add("PASS" if got or f else "FAIL", f"env: {g['purpose']}", ("present: " + ", ".join(got)) if got else (f"present as file {g['or_file']}" if f else "missing: " + " or ".join(g["names"])))
    for g in spec["optional"]:
        got = [x for x in g["names"] if x in os.environ]
        add("PASS" if got else "WARN", f"env (optional): {g['purpose'][:48]}", ("present: " + ", ".join(got)) if got else "missing: " + " or ".join(g["names"]))


def check_skills(man):
    d = os.path.join(ROOT, ".claude/skills")
    have = {x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))} if os.path.isdir(d) else set()
    miss = sorted(set(man["skills"]) - have)
    ok_files = all(os.path.exists(os.path.join(d, s, "SKILL.md")) for s in ("clips", "lessons"))
    add("PASS" if not miss and ok_files else "FAIL", "skills folders", f"{len(have)} present" + (f"; missing {short(miss)}" if miss else "") + ("" if ok_files else "; clips or lessons has no SKILL.md"))


def check_tools(man):
    cur = mm.tool_versions()
    miss = [k for k in ("ffmpeg", "python") if not cur.get(k)]
    diff = [f"{k} {cur.get(k)} (was {v})" for k, v in man["tools"].items() if v and cur.get(k) != v]
    absent = [k for k, v in man["tools"].items() if v and not cur.get(k) and k not in miss]
    if miss:
        add("FAIL", "tool versions", "missing: " + ", ".join(miss))
    elif absent or diff:
        add("NOTE", "tool versions", "differ from the old machine (a newer version is normally fine; rerun a render to be sure): " + short(diff + [f"{a} not installed" for a in absent]))
    else:
        add("PASS", "tool versions", ", ".join(f"{k} {v}" for k, v in cur.items()))


def check_keys():
    files = [p for p in mm.tracked() if os.path.isfile(os.path.join(ROOT, p))]
    scan = os.path.join(ROOT, ".claude/skills/clips/scripts/checkpoint.py")
    if not os.path.exists(scan):
        return add("SKIP", "key-like strings in tracked files", "checkpoint.py --scan not found")
    hits = []
    for i in range(0, len(files), 200):
        rc, out = run([sys.executable, scan, "--scan", *files[i:i + 200]], 120)
        if rc == 3:
            hits += [l.strip() for l in out.splitlines() if l.strip()]
    add("PASS" if not hits else "FAIL", "key-like strings in tracked files", "none" if not hits else "files (names only): " + short(hits))


def check_kaggle(man):
    rc, out = run([sys.executable, KAGGLE_PY, "raw", "datasets", "list", "--mine"], 120)
    if rc != 0:
        return add("FAIL", "kaggle datasets", "could not list (credentials?): " + (out.strip().splitlines() or ["?"])[-1][:100])
    have = {l.split()[0].split("/")[-1].lower() for l in out.splitlines()[2:] if l.strip() and "/" in l.split()[0]}
    req = [d for d in man["kaggle_datasets"] if not d.get("optional")]
    vault = [d for d in man["kaggle_datasets"] if d.get("optional")]
    miss = [d["name"] for d in req if d["name"].lower() not in have]
    add("PASS" if not miss else "FAIL", "kaggle datasets", "all %d normal datasets present" % len(req) if not miss else "missing: " + ", ".join(miss))
    # key vaults are an optional transfer copy: absent = fine (deleted on purpose); present = reminder to delete them once the keys are in the new environment
    left = [d["name"] for d in vault if d["name"].lower() in have]
    add("PASS" if not left else "WARN", "kaggle key vaults", "none present (good: deleted or never copied)" if not left else "still present (optional transfer copy, delete after the keys are in the new environment): " + ", ".join(left))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", default=os.path.join(ROOT, mm.MANIFEST_REL))
    ap.add_argument("--no-preflight", action="store_true")
    ap.add_argument("--kaggle", action="store_true")
    ap.add_argument("--skip-env", action="store_true")
    ap.add_argument("--quiet-files", action="store_true", help="do not list every missing/changed/extra path")
    a = ap.parse_args()
    try:
        man = json.load(open(a.manifest))
    except Exception as e:
        print(f"FAIL  cannot read {a.manifest}: {e}")
        return 1
    add("PASS", "manifest loaded", f"{man['file_count']} files, commit {man['commit'][:12]} on {man['branch']}")
    ok = check_files(man, a.quiet_files)
    check_history(man, ok)
    check_counts(man)
    check_graph()
    check_skills(man)
    check_tools(man)
    check_keys()
    if a.no_preflight:
        add("SKIP", "preflight.py", "--no-preflight")
    else:
        check_preflight()
    if a.skip_env:
        add("SKIP", "env var names", "--skip-env")
    else:
        check_env(man)
    if a.kaggle:
        check_kaggle(man)
    else:
        add("SKIP", "kaggle datasets", "run with --kaggle (names only), or see FABLE-CARRYOVER-CHECK.md step 7")
    w = max(len(r[1]) for r in rows)
    print(f"\n{'STATUS':<6}  {'CHECK':<{w}}  DETAIL")
    for st, ck, d in rows:
        print(f"{st:<6}  {ck:<{w}}  {d}")
    c = {s: sum(1 for r in rows if r[0] == s) for s in ("PASS", "FAIL", "WARN", "NOTE", "SKIP")}
    print(f"\n{c['PASS']} pass, {c['FAIL']} FAIL, {c['WARN']} warn, {c['NOTE']} note, {c['SKIP']} skip  =>  {'FAIL' if c['FAIL'] else 'PASS'}")
    return 1 if c["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
