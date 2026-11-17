#!/usr/bin/env python3
"""CHECKPOINT: save the work of a clip job to GitHub NOW, so a reclaimed container loses nothing. Safe to run any time, any number of times.
usage: python3 .claude/skills/clips/scripts/checkpoint.py [--stream STREAM_FOLDER] [-m WHAT] [--big-previews] [--no-push] [--dry-run]
  --stream   streams/<name> (or the name, or any path inside it); default: every folder under streams/
  -m WHAT    the end of the commit subject: `checkpoint: <stream> <WHAT>` (default: "<n> files")
  --big-previews   also commit a highlights preview.mp4 over 25 MB (the user opted in; it is gitignored, so this uses `git add -f`)
  --no-push  commit only      --dry-run  print what would be committed, change nothing
  --scan FILE...   print the files that look like they hold a key (exit 3 if any); autosave.sh uses it
What it stages (and ONLY this): in streams/<s>/: stream.json, docs/*, clips/<id>/{clip.json, post.md, edit-notes.md, commentary-script.md, poster*, versions/*, <output>.mp4 previews},
  highlights/<slug>/{highlights.json, post.md, render-report.json, commentary-script.md, poster*, versions/*, preview.mp4 (25 MB or less, or --big-previews)}, plus LATEST.md and streams/index.json.
Never: source/, masters/, work/, windows, *_upload.mp4, *.part.mp4, anything over 95 MB, a file that looks like it holds a key (KGAT token, API key, private key): that one is REFUSED, named, and left unstaged.
It commits only those paths (`git commit -- paths`: whatever else is staged is left alone), then pushes the CURRENT branch (`git push origin HEAD:refs/heads/<branch>`, the session branch ccr-*; never main, never force):
5 tries (waits 2, 4, 8, 16 s); on a rejection `git pull --no-rebase origin <branch>` (a conflict is aborted and reported, the repo is never left half-merged). It also pushes earlier commits that an old failed push left behind.
Prints ONE final line: `checkpoint: pushed <sha> (<n> files, <MB> MB)` | `checkpoint: nothing to save (<sha> is on origin/<branch>)` | `checkpoint: FAILED ...` (exit 2) ; refused files exit 3 (the rest is saved).
From other scripts: `import checkpoint; checkpoint.best_effort(stream_dir, "what")`: a failure prints WARNING NOT SAVED TO GITHUB and never raises. CLIPS_CHECKPOINT=off turns the hooks off (tests)."""
import fcntl, os, re, subprocess as sp, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
MB = 1_000_000
MAX_FILE = 95 * MB
BIG_PREVIEW = 25 * MB
# commit trailer: ONLY from the environment variable CLAUDE_COMMIT_TRAILER (the full text, e.g. "Co-Authored-By: ...\nClaude-Session: ..."; a literal \n becomes a newline). Unset or empty = NO trailer.
TRAILERS = [t for t in [os.environ.get("CLAUDE_COMMIT_TRAILER", "").replace("\\n", "\n").strip()] if t]
BACKOFF = [2, 4, 8, 16]

# ---- key-like content (patterns must stay valid POSIX ERE too: finalise.py hands them to `git grep -E`). Patterns are built from pieces so that this file (and every doc quoting it) never matches itself.
_P = [b"KGAT" + b"_[0-9a-f]{20,}", b"sk-" + b"ant-[A-Za-z0-9_-]{20,}", b"sk-" + b"[A-Za-z0-9]{32,}", b"gh" + b"[pousr]_[A-Za-z0-9]{30,}", b"github" + b"_pat_[A-Za-z0-9_]{30,}",
      b"AI" + b"za[0-9A-Za-z_-]{35}", b"AK" + b"IA[0-9A-Z]{16}", b"xo" + b"x[bap]-[0-9A-Za-z-]{10,}", b"-----BEGIN [A-Z ]*PRIVATE" + b" KEY-----",
      b"KAGGLE_(KEY|API_?TOKEN|APITOKEN)[A-Z0-9_]*[ ]*[=:][ ]*[\"']?[0-9A-Za-z_-]{16,}"]
KEY_RE = re.compile(b"|".join(b"(?:" + p + b")" for p in _P))
BINARY_EXT = {".mp4", ".mov", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp3", ".wav", ".m4a", ".aac", ".npz", ".zip", ".pdf", ".ttf", ".otf", ".woff", ".woff2", ".webm", ".mkv", ".ico"}
TEXT_SCAN_MAX = 5 * MB


def key_hit(path):
    """a short reason (never the key itself) when the file holds key-like text, else None. Media files are skipped."""
    try:
        if os.path.splitext(path)[1].lower() in BINARY_EXT or os.path.getsize(path) > TEXT_SCAN_MAX:
            return None
        m = KEY_RE.search(open(path, "rb").read())
    except OSError:
        return None
    return f"looks like a secret ({m.group(0)[:4].decode('ascii', 'replace')}...)" if m else None


# ---- what may be committed
DENY = re.compile(r"(^|/)(source|masters|work|windows|cache)/|_upload\.mp4$|\.part\.mp4$|\.tmp$|(^|/)\.hyperframes/")
ALLOW = [re.compile(p) for p in (
    r"^streams/[^/]+/(stream\.json|docs/.+)$",
    r"^streams/[^/]+/clips/[^/]+/(clip\.json|post\.md|edit-notes\.md|commentary-script\.md|poster[^/]*\.(jpg|jpeg|png)|versions/.+|[^/]+\.mp4)$",
    r"^streams/[^/]+/highlights/[^/]+/(highlights\.json|post\.md|render-report\.json|commentary-script\.md|poster[^/]*\.(jpg|jpeg|png)|versions/.+|preview\.mp4)$",
    r"^(LATEST\.md|streams/index\.json)$")]
PREVIEW = re.compile(r"^streams/[^/]+/highlights/[^/]+/preview\.mp4$")


def run(*a, input=None, timeout=300, check=False):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_MERGE_AUTOEDIT="no", LC_ALL="C")
    try:
        r = sp.run(["git", "--literal-pathspecs", "-C", REPO, *a], input=input, capture_output=True, env=env, timeout=timeout)
    except sp.TimeoutExpired:
        r = sp.CompletedProcess(a, 124, b"", f"timed out after {timeout} s".encode())
    r.out, r.err = r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(a[:3])} failed: {r.err.strip()[:300]}")
    return r


def mask(s):
    return re.sub(r"(https?://)[^/@\s]+@", r"\1***@", s)


def stream_of(p):
    """streams/<name> for a stream folder, its name, or any path inside it; None for no argument"""
    if not p:
        return None
    ap = os.path.abspath(p if os.path.isabs(p) or os.path.exists(p) else os.path.join(REPO, p))
    rel = os.path.relpath(ap, REPO).replace(os.sep, "/")
    if rel.startswith("streams/") and len(rel.split("/")) >= 2:
        return "/".join(rel.split("/")[:2])
    if os.path.isdir(os.path.join(REPO, "streams", p)):
        return "streams/" + p.strip("/")
    raise SystemExit(f"checkpoint: FAILED: {p!r} is not a folder under streams/")


def candidates(scope):
    """repo-relative paths that differ from HEAD (modified, new, deleted, staged) inside scope, plus untracked-ignored highlights previews"""
    paths = set()
    spec = ["--", *scope]
    r = run("ls-files", "-z", "-m", "-o", "-d", "--exclude-standard", *spec, check=True)
    paths.update(x for x in r.out.split("\0") if x)
    r = run("diff", "--cached", "--name-only", "-z", *spec, check=True) if run("rev-parse", "-q", "--verify", "HEAD").returncode == 0 else None
    if r:
        paths.update(x for x in r.out.split("\0") if x)
    forced = set()
    for pv in sorted(sp.run(["git", "-C", REPO, "ls-files", "-z", "-o", "-i", "--exclude-standard", *spec], capture_output=True).stdout.decode().split("\0")):
        if pv and PREVIEW.match(pv):  # gitignored preview: a candidate only by name, and only when opted in or small enough
            forced.add(pv)
    return paths, forced


def human(n):
    return f"{n / MB:.1f}"


def lock():
    f = open(os.path.join(REPO, ".git", "clips-checkpoint.lock"), "a")
    t0 = time.time()
    while True:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB); return f
        except OSError:
            if time.time() - t0 > 180:
                raise SystemExit("checkpoint: FAILED: another checkpoint has held the lock for 3 minutes (.git/clips-checkpoint.lock)")
            time.sleep(1)


def branch():
    r = run("symbolic-ref", "-q", "--short", "HEAD")
    return r.out.strip() if r.returncode == 0 else None


def remote_sha(b):
    r = run("ls-remote", "--heads", "origin", f"refs/heads/{b}", timeout=60)
    if r.returncode:
        return None, mask(r.err.strip()[:200])
    return (r.out.split()[0] if r.out.strip() else ""), None


def push_branch(b, scale=1.0):
    """push HEAD to origin/<b>: 5 tries, waits 2/4/8/16 s, a rejection is merged (never forced). Returns (ok, reason)"""
    last = "no attempt"
    for i in range(len(BACKOFF) + 1):
        r = run("push", "origin", f"HEAD:refs/heads/{b}", timeout=240)
        if r.returncode == 0:
            return True, ""
        lines = [l.strip() for l in (r.err or r.out).splitlines() if l.strip()]
        useful = [l for l in lines if re.search(r"fatal|remote:|denied|error|refus|could not|unable|timed out", l, re.I) and "failed to push some refs" not in l]
        last = mask((useful or lines or [f"git push exit {r.returncode}"])[0][:200])
        if re.search(r"rejected|non-fast-forward|fetch first|stale info", r.err):
            p = run("pull", "--no-rebase", "--no-edit", "origin", b, timeout=240)
            if p.returncode:
                run("merge", "--abort")
                return False, f"origin/{b} has commits that conflict with ours (merge aborted, nothing lost locally): {mask((p.err or p.out).strip()[-200:])}"
            continue  # merged: push again at once
        if i < len(BACKOFF):
            time.sleep(BACKOFF[i] * scale)
    return False, last


def checkpoint(stream=None, what=None, big=False, push=True, dry=False):
    """returns (exit code, final line)"""
    if os.path.exists(os.path.join(REPO, ".autosave-pause")):
        return 0, "checkpoint: paused (.autosave-pause exists: a history rewrite is running); nothing done"
    if os.path.exists(os.path.join(REPO, ".git", "MERGE_HEAD")):
        return 2, "checkpoint: FAILED: a merge is in progress in this repo; finish or abort it (git merge --abort), then run checkpoint again"
    b = branch()
    if not b:
        return 2, "checkpoint: FAILED: detached HEAD; `git checkout -b wip-<name>` first so the work has a branch to push"
    st = stream_of(stream)
    scope = [st] if st else ["streams"]
    scope += ["LATEST.md", "streams/index.json"]
    name = os.path.basename(st) if st else "all streams"
    cands, forced = candidates(scope)
    stage, forcedlist, refused, skipped, kept_local = [], [], [], [], []
    for p in sorted(cands | forced):
        ap = os.path.join(REPO, p)
        gone = not os.path.exists(ap)
        if DENY.search(p) or not any(r.match(p) for r in ALLOW):
            skipped.append(p); continue
        if gone:
            stage.append(p); continue  # a deletion of a tracked, allowed path
        size = os.path.getsize(ap)
        if PREVIEW.match(p) and size > BIG_PREVIEW and not big:
            kept_local.append(f"{p} ({human(size)} MB)"); continue
        if size > MAX_FILE:
            refused.append(f"{p}: {human(size)} MB is over the 95 MB limit (GitHub rejects 100 MB)"); continue
        why = key_hit(ap)
        if why:
            refused.append(f"{p}: {why}"); continue
        (forcedlist if p in forced else stage).append(p)
    for x in refused:
        print(f"checkpoint: REFUSED {x}", flush=True)
    if kept_local:
        print("checkpoint: kept local (not committed; send with SendUserFile, or --big-previews): " + ", ".join(kept_local), flush=True)
    if skipped:
        print(f"checkpoint: note: {len(skipped)} changed path(s) are not on the safe list and stay uncommitted, e.g. {skipped[0]}", flush=True)
    todo = stage + forcedlist
    code = 3 if refused else 0
    if dry:
        print("checkpoint: dry run, would commit: " + (", ".join(todo[:20]) + (" ..." if len(todo) > 20 else "") if todo else "nothing"))
        return code, f"checkpoint: dry run ({len(todo)} files)"
    sha_before = run("rev-parse", "HEAD").out.strip()
    committed = None
    if todo:
        msg = f"checkpoint: {name} {what or f'{len(todo)} files'}"
        for attempt in range(5):
            nul = lambda xs: "\0".join(xs) + "\0"
            if stage:
                r = run("add", "-A", "--pathspec-from-file=-", "--pathspec-file-nul", input=nul(stage).encode())
            if forcedlist and not (stage and r.returncode):
                r = run("add", "-f", "--pathspec-from-file=-", "--pathspec-file-nul", input=nul(forcedlist).encode())
            if r.returncode == 0:
                args = ["commit", "-q", "-m", msg[:200]] + sum((["-m", t] for t in TRAILERS), []) + ["--pathspec-from-file=-", "--pathspec-file-nul"]
                r = run(*args, input=nul(todo).encode())
                if r.returncode == 0:
                    committed = True; break
                if re.search(r"nothing (added )?to commit|no changes added", r.out + r.err):
                    break
            if "index.lock" in r.err or "Unable to create" in r.err or "did not match" in r.err:  # autosave is working: wait and try again
                time.sleep(1 + attempt); continue
            return 2, f"checkpoint: FAILED to commit: {mask(r.err.strip()[:300])}"
        else:
            return 2, "checkpoint: FAILED to commit after 5 tries (the git index stayed locked)"
    head = run("rev-parse", "HEAD").out.strip()
    short = run("rev-parse", "--short", "HEAD").out.strip()
    n = size = 0
    if committed:
        names = run("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", "HEAD").out.split("\0")
        for f in (x for x in names if x):
            n += 1
            try: size += os.path.getsize(os.path.join(REPO, f))
            except OSError: pass
    if not push:
        return code, f"checkpoint: committed {short} ({n} files, {human(size)} MB), not pushed (--no-push)"
    rs, err = remote_sha(b)
    if rs is None:
        return 2, f"checkpoint: FAILED: cannot reach origin ({err}); committed locally as {short} but NOT ON GITHUB"
    if rs == head:
        return code, f"checkpoint: nothing to save ({short} is on origin/{b})"
    ok, why = push_branch(b, float(os.environ.get("CHECKPOINT_BACKOFF_SCALE", "1")))
    if not ok:
        return 2, f"checkpoint: FAILED push of {b} after {len(BACKOFF) + 1} tries: {why}; committed locally as {short} but NOT ON GITHUB"
    short = run("rev-parse", "--short", "HEAD").out.strip()
    return code, f"checkpoint: pushed {short} ({n} files, {human(size)} MB)"


def best_effort(stream, what, big=False, timeout=600):
    """for the render scripts: checkpoint in a child process; never raises, never stops the caller; True when saved"""
    if os.environ.get("CLIPS_CHECKPOINT", "").lower() == "off":
        return True
    try:
        cmd = [sys.executable, os.path.abspath(__file__), "-m", what] + (["--stream", str(stream)] if stream else []) + (["--big-previews"] if big or os.environ.get("CHECKPOINT_BIG_PREVIEWS") == "1" else [])
        r = sp.run(cmd, timeout=timeout, stdin=sp.DEVNULL)
        if r.returncode == 0:
            return True
        why = f"exit {r.returncode}" + (": some files were refused (see the REFUSED lines above)" if r.returncode == 3 else "")
    except Exception as e:  # timeout, no git, anything
        why = str(e)[:200]
    print(f"WARNING NOT SAVED TO GITHUB: checkpoint of {stream or 'all streams'} failed ({why}). The files exist on this machine only until you run: python3 .claude/skills/clips/scripts/checkpoint.py"
          + (f" --stream {stream}" if stream else ""), file=sys.stderr, flush=True)
    return False


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__); return 0
    if argv[:1] == ["--scan"]:  # used by autosave.sh: print every given file that looks like it holds a key; exit 3 when there is one
        hits = [f for f in argv[1:] if os.path.isfile(f) and key_hit(f)]
        print("\n".join(hits)); return 3 if hits else 0
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv and argv.index(k) + 1 < len(argv) else d
    lk = lock()
    try:
        code, line = checkpoint(opt("--stream"), opt("-m"), "--big-previews" in argv, "--no-push" not in argv, "--dry-run" in argv)
    finally:
        lk.close()
    print(line, flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
