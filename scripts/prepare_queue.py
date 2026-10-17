#!/usr/bin/env python3
"""Run prepare_link.py for queued links on a GitHub Actions runner and commit the results.

Environment (set by .github/workflows/prepare.yml):
  EVENT_NAME, ISSUE_NUMBER, INPUT_URL, INPUT_FORCE, GH_TOKEN, GITHUB_REPOSITORY,
  GITHUB_REPOSITORY_OWNER, YT_COOKIES (optional secret: Netscape cookie file for YouTube)

For each candidate link it writes inbox/<platform>_<id>/ (brief.md, draft_note.md, sheet.jpg,
transcript, screen text, meta; never the video) and labels the issue `prepared`. The model-side
check later reads inbox/ instead of scraping again. Failures are logged and left for the next run.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_link import classify  # noqa: E402

KEEP = ["brief.md", "draft_note.md", "sheet.jpg", "transcript.txt", "screen_text.txt", "meta.json", "comments.json"]
SKIP_LABELS = {"prepared", "needs-input", "processing"}


def gh(*args, check=True):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:300])
    return r.stdout


def candidates(owner, repo):
    ev, force = os.environ.get("EVENT_NAME", ""), os.environ.get("INPUT_FORCE") == "true"
    if ev == "issues":
        n = os.environ["ISSUE_NUMBER"]
        return [json.loads(gh("api", f"repos/{repo}/issues/{n}"))], force
    if os.environ.get("INPUT_URL"):
        return [{"number": None, "body": os.environ["INPUT_URL"], "labels": [], "user": {"login": owner}}], force
    out = json.loads(gh("api", f"repos/{repo}/issues?labels=link&state=open&per_page=50"))
    return [i for i in out if "pull_request" not in i and not SKIP_LABELS & {l["name"] for l in i["labels"]}], force


def main():
    repo, owner = os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_REPOSITORY_OWNER"]
    if os.environ.get("YT_COOKIES"):
        p = Path(os.environ["RUNNER_TEMP"]) / "yt_cookies.txt"
        p.write_text(os.environ["YT_COOKIES"])
        os.environ["YT_COOKIES_FILE"] = str(p)
        print("YouTube cookies: provided")
    items, force = candidates(owner, repo)
    done = 0
    for it in items:
        if it["user"]["login"].lower() != owner.lower():
            print(f"skip #{it['number']}: not authored by the owner")
            continue
        m = re.search(r"https?://[^\s<>\"']+", it.get("body") or "")
        if not m:
            continue
        try:
            platform, vid, _ = classify(m.group(0))
        except SystemExit:
            print(f"skip #{it['number']}: not an Instagram/YouTube link")
            continue
        dest = ROOT / "inbox" / f"{platform}_{vid}"
        if dest.exists() and not force:
            print(f"#{it['number']}: already prepared")
            continue
        out = Path(os.environ["RUNNER_TEMP"]) / f"prep_{platform}_{vid}"
        shutil.rmtree(out, ignore_errors=True)
        cmd = [sys.executable, str(ROOT / "scripts" / "prepare_link.py"), m.group(0), str(out)]
        if it["number"]:
            cmd += ["--queued-via", f"GitHub issue #{it['number']}"]
        if force:
            cmd.append("--force")
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(f"#{it['number']} {platform} {vid}: exit {r.returncode}: {(r.stdout or r.stderr).strip().splitlines()[0][:200] if (r.stdout or r.stderr).strip() else ''}")
        if r.returncode != 0:
            continue
        dest.mkdir(parents=True, exist_ok=True)
        for name in KEEP:
            if (out / name).exists():
                shutil.copy(out / name, dest / name)
        done += 1
        if it["number"]:
            try:
                gh("api", f"repos/{repo}/issues/{it['number']}/labels", "-f", "labels[]=prepared")
            except RuntimeError as e:
                print("label failed:", e)
    if done:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", "inbox"], check=True)
        subprocess.run(["git", "commit", "-q", "-m", f"Prepare {done} queued link(s)"], check=True)
        delay = 3
        for attempt in range(5):
            subprocess.run(["git", "pull", "-q", "--rebase", "origin", "main"], check=False)
            if subprocess.run(["git", "push", "origin", "HEAD:main"]).returncode == 0:
                break
            time.sleep(delay); delay *= 2
        else:
            sys.exit("push failed")
    print(f"prepared {done} link(s)")


if __name__ == "__main__":
    main()
