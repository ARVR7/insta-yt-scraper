#!/usr/bin/env python3
"""Write migration-setup/MANIFEST.json: a fingerprint of this repo that verify_manifest.py checks in the NEW repo after the move.

Run it in the OLD repo, on the checkout that is about to become `main` of the new repo, with a clean working tree:
    python3 migration-setup/make_manifest.py            # writes migration-setup/MANIFEST.json, then commit that file
    python3 migration-setup/make_manifest.py --check    # print the summary only, write nothing

What it records (no secrets: environment variable NAMES only, never values; Kaggle dataset NAMES only):
  commit, tree, tree_without_manifest, branch, main_commit, commit_count, every tracked file (path, sha256, size; MANIFEST.json itself is skipped),
  counts (lessons active/superseded, incidents, scripts, destinations, streams, clips per stream, mp4 files), blobs over 30 MB (sha, size, path),
  env var names, Kaggle dataset names, skills folders, tool versions (ffmpeg, node, python, numpy, Pillow, kaggle).
`tree_without_manifest` is the git tree of the commit with MANIFEST.json removed: it does not change when this file is regenerated and committed,
so it is the value to compare after a mirror, fork or transfer. Exit 0 = written, 1 = refused (dirty tree) or error.
Needs: python3 and git only."""
import argparse, hashlib, json, os, re, shutil, subprocess as sp, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST_REL = "migration-setup/MANIFEST.json"
BIG = 30 * 1024 * 1024   # a blob over this size is listed; the new repo must not hold a bigger blob that is not listed here

ENV_NAMES = {  # names only. required_any = at least one name of each group must be set (or the file named in `or_file` must exist)
    "required_any": [
        {"purpose": "Kaggle account 1 username", "names": ["KAGGLE_USERNAME"], "or_file": "~/.kaggle/kaggle.json"},
        {"purpose": "Kaggle account 1 token", "names": ["KAGGLE_API_TOKEN", "KAGGLE_APITOKEN"], "or_file": "~/.kaggle/kaggle.json"},
    ],
    "optional": [
        {"purpose": "Kaggle account 2 username (default `sovere` if unset)", "names": ["KAGGLE_USERNAME2"]},
        {"purpose": "Kaggle account 2 token (if unset it is read in memory from the private dataset kagglegpu2 of account 1)", "names": ["KAGGLE_APITOKEN2", "KAGGLE_API_TOKEN2"]},
        {"purpose": "Gemini moment reviewer (only for --llm gemini)", "names": ["GEMINI_API_KEY"]},
    ],
}
KAGGLE_DATASETS = [  # owner of account 1 is the user; names only
    {"name": "gemini-key", "note": "plaintext key vault: optional transfer copy, delete after the key is in the new environment", "optional": True},
    {"name": "streamer-face", "note": "AI streamer reference images"},
    {"name": "streamer-face-f", "note": "AI streamer reference images (second set)"},
    {"name": "vlog-1vzlt3-src", "note": "source video of the first test job (156 MB)"},
    {"name": "kagglegpu1", "note": "plaintext key vault: optional transfer copy, delete after the keys are in the new environment", "optional": True},
    {"name": "kagglegpu2", "note": "plaintext key vault: optional transfer copy, delete after the keys are in the new environment (holds the account-2 token; read in memory by kaggle.py only when KAGGLE_APITOKEN2 is unset)", "optional": True},
]


def git(*a, check=True, env=None, inp=None):
    r = sp.run(["git", "-C", ROOT, *a], capture_output=True, text=True, env=env, input=inp)
    if check and r.returncode:
        raise SystemExit(f"git {' '.join(a)} failed: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def tracked():
    return [p for p in git("ls-files", "-z").split("\0") if p]


def tree_without_manifest(commit="HEAD"):
    """tree sha of `commit` with MANIFEST.json taken out, built in a throw-away index (the real index is untouched)"""
    with tempfile.TemporaryDirectory() as td:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(td, "idx"))
        git("read-tree", commit, env=env)
        git("update-index", "--force-remove", MANIFEST_REL, env=env)
        return git("write-tree", env=env)


def big_blobs(rev_args):
    """[(sha, size, path-or-empty)] of every blob over BIG reachable from rev_args (e.g. ['--all'] or ['HEAD']), and the largest size"""
    out = git("rev-list", "--objects", *rev_args)
    names = {}
    for line in out.splitlines():
        sha, _, path = line.partition(" ")
        names.setdefault(sha, path)
    r = sp.run(["git", "-C", ROOT, "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"], input="\n".join(names) + "\n", capture_output=True, text=True)
    big, mx = [], 0
    for line in r.stdout.splitlines():
        sha, typ, size = line.split()
        if typ == "blob":
            size = int(size)
            mx = max(mx, size)
            if size > BIG:
                big.append({"sha": sha, "size": size, "path": names.get(sha, "")})
    return sorted(big, key=lambda b: (-b["size"], b["sha"])), mx


def counts(files):
    """counts that verify_manifest.py compares; derived from tracked files and the generated lessons files"""
    c = {}
    try:
        nodes = json.load(open(os.path.join(ROOT, "lessons/graph.json")))["nodes"]
        c["lessons_active"] = sum(1 for n in nodes if n.get("status") == "active")
        c["lessons_superseded"] = sum(1 for n in nodes if n.get("status") == "superseded")
        c["lessons_total"] = len(nodes)
    except Exception:
        c["lessons_active"] = c["lessons_superseded"] = c["lessons_total"] = None
    try:
        inc = json.load(open(os.path.join(ROOT, "lessons/incidents.json")))["incidents"]
        c["incidents"] = len(inc)
    except Exception:
        c["incidents"] = None
    c["scripts"] = sum(1 for p in files if p.startswith(".claude/") and p.endswith((".py", ".sh", ".js")))
    c["destinations"] = sum(1 for p in files if re.fullmatch(r"\.claude/skills/clips/destinations/[^/]+\.json", p))
    streams = sorted({p.split("/")[1] for p in files if re.match(r"streams/[^/]+/stream\.json$", p)})
    c["streams"] = len(streams)
    c["clips_per_stream"] = {s: len({p.split("/")[3] for p in files if p.startswith(f"streams/{s}/clips/") and p.endswith("/clip.json")}) for s in streams}
    c["highlights_per_stream"] = {s: len({p.split("/")[3] for p in files if p.startswith(f"streams/{s}/highlights/") and p.endswith("/highlights.json")}) for s in streams}
    c["mp4_per_stream"] = {s: sum(1 for p in files if p.startswith(f"streams/{s}/") and p.endswith(".mp4")) for s in streams}
    c["mp4_total"] = sum(1 for p in files if p.endswith(".mp4"))
    return c


def tool_versions():
    """versions seen on this machine; a missing tool is recorded as null"""
    def run(cmd):
        try:
            r = sp.run(cmd, capture_output=True, text=True, timeout=30)
            return (r.stdout or r.stderr).strip().splitlines()[0]
        except Exception:
            return None
    v = {}
    f = run(["ffmpeg", "-version"])
    m = re.match(r"ffmpeg version (\S+)", f or "")
    v["ffmpeg"] = m.group(1) if m else None
    v["node"] = (run(["node", "-v"]) or "").lstrip("v") or None
    v["python"] = ".".join(map(str, sys.version_info[:3]))
    from importlib import metadata
    for key, dist in (("numpy", "numpy"), ("Pillow", "Pillow"), ("kaggle", "kaggle")):
        try:
            v[key] = metadata.version(dist)
        except Exception:
            v[key] = None
    if v["kaggle"] is None:  # the kaggle CLI often lives in its own venv (~/kvenv): ask the python next to the executable
        exe = shutil.which("kaggle") or os.path.expanduser("~/kvenv/bin/kaggle")
        py = os.path.join(os.path.dirname(exe), "python") if os.path.exists(exe) else None
        if py and os.path.exists(py):
            v["kaggle"] = run([py, "-c", "from importlib import metadata as m; print(m.version('kaggle'))"])
    return v


def build():
    files = [p for p in tracked() if p != MANIFEST_REL and os.path.isfile(os.path.join(ROOT, p))]
    entries = [{"path": p, "sha256": sha256_file(os.path.join(ROOT, p)), "size": os.path.getsize(os.path.join(ROOT, p))} for p in sorted(files)]
    main = next((r for r in ("origin/main", "main") if git("rev-parse", "--verify", "-q", r, check=False)), None)
    big_head, mx_head = big_blobs(["HEAD"])
    big_all, mx_all = big_blobs(["--all"])
    return {
        "format": 1,
        "about": "fingerprint of the old repo; verify with: python3 migration-setup/verify_manifest.py. No secret values inside: names only.",
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "commit": git("rev-parse", "HEAD"),
        "tree": git("rev-parse", "HEAD^{tree}"),
        "tree_without_manifest": tree_without_manifest(),
        "main_commit": git("rev-parse", main) if main else None,
        "main_ref": main,
        "commit_count": int(git("rev-list", "--count", "HEAD")),
        "files": entries,
        "file_count": len(entries),
        "counts": counts([e["path"] for e in entries]),
        "largest_blob_bytes": {"head_history": mx_head, "all_refs": mx_all},
        "blobs_over_30mb": big_all,
        "env_var_names": ENV_NAMES,
        "kaggle_datasets": KAGGLE_DATASETS,
        "kaggle_dataset_owner_note": "datasets live under the Kaggle account 1 of the user; verify with `kaggle.py raw datasets list --mine` (names only)",
        "skills": sorted(d for d in os.listdir(os.path.join(ROOT, ".claude/skills")) if os.path.isdir(os.path.join(ROOT, ".claude/skills", d))) if os.path.isdir(os.path.join(ROOT, ".claude/skills")) else [],
        "tools": tool_versions(),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="print the summary, write nothing")
    ap.add_argument("--allow-dirty", action="store_true", help="write even if tracked files differ from HEAD (the manifest then describes the working tree, not the commit)")
    a = ap.parse_args()
    dirty = [l for l in git("status", "--porcelain", "--untracked-files=no").splitlines() if l[3:] != MANIFEST_REL]
    if dirty and not a.allow_dirty:
        print("refused: tracked files differ from HEAD (commit them first, or use --allow-dirty):")
        print("\n".join("  " + l for l in dirty[:15]))
        return 1
    m = build()
    c = m["counts"]
    print(f"branch {m['branch']}  commit {m['commit'][:12]}  tree {m['tree'][:12]}  tree-without-manifest {m['tree_without_manifest'][:12]}  commits {m['commit_count']}")
    print(f"files {m['file_count']}  streams {c['streams']}  clips {c['clips_per_stream']}  mp4 {c['mp4_total']}")
    print(f"lessons active {c['lessons_active']} superseded {c['lessons_superseded']}  incidents {c['incidents']}  scripts {c['scripts']}  destinations {c['destinations']}")
    print(f"largest blob {m['largest_blob_bytes']['all_refs']} bytes; {len(m['blobs_over_30mb'])} blob(s) over 30 MB are listed (the new repo may hold these, no others)")
    print(f"skills {len(m['skills'])}  tools {m['tools']}")
    if a.check:
        return 0
    out = os.path.join(ROOT, MANIFEST_REL)
    with open(out, "w") as f:
        json.dump(m, f, indent=1, sort_keys=False)
        f.write("\n")
    print(f"wrote {MANIFEST_REL}: now `git add {MANIFEST_REL}` and commit it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
