#!/usr/bin/env python3
"""Everything mechanical about one link, in one command.

Usage: prepare_link.py <url> <outdir> [--force] [--queued-via "GitHub issue #3"]

Does, with no model involved: normalise the URL, skip if a note already exists, fetch metadata
and media, extract frames/contact sheet, transcribe (translating non-English), OCR on-screen
text, pull candidate names/URLs/prices out of all the text, and look up facts for any GitHub
repos and PyPI packages found. Then writes, into <outdir>:

  brief.md        compact summary for Claude to read (instead of many tool outputs)
  draft_note.md   the note with everything mechanical filled in and TODO where judgment is needed
  sheet.jpg       contact sheet (only look at it when brief.md says needs_visual_review: yes)
  meta.json, transcript.txt, screen_text.txt, video.mp4 ...

Prints a short status. Exit codes: 0 ok, 3 already processed, 2 fetch blocked.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def classify(url):
    m = re.search(r"instagram\.com/(?:[\w.]+/)?(reel|reels|p|tv)/([\w-]+)", url)
    if m:
        return "instagram", m.group(2), "reel" if m.group(1) in ("reel", "reels") else "post"
    m = re.search(r"youtu\.be/([\w-]{6,})", url) or re.search(r"youtube\.com/(?:shorts|embed|live)/([\w-]{6,})", url) \
        or re.search(r"youtube\.com/watch\?(?:[^#]*&)?v=([\w-]{6,})", url)
    if m:
        return "youtube", m.group(1), "short" if "/shorts/" in url else "video"
    sys.exit(f"not an Instagram or YouTube link: {url}")


def run(cmd, log):
    r = subprocess.run(cmd, capture_output=True, text=True)
    Path(log).write_text((r.stdout or "") + "\n" + (r.stderr or ""))
    return r.returncode


def vtt_to_text(path):
    """Collapse a .vtt caption file into timestamped lines without the rolling duplicates."""
    out, last = [], ""
    t = ""
    for line in Path(path).read_text(encoding="utf8", errors="ignore").splitlines():
        m = re.match(r"(\d\d):(\d\d):(\d\d)\.\d+ -->", line)
        if m:
            t = f"{int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))}s"
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:")) or line == last:
            continue
        out.append(f"[{t}] {line}")
        last = line
    return "\n".join(out)


def readable_transcript(t):
    """The English text of a transcript file: the translation when there is one, no timestamps."""
    if not t:
        return ""
    if "## English translation" in t:
        t = t.split("## English translation", 1)[1].split("## Original", 1)[0]
    else:
        t = t.split("\n", 1)[-1]
    return re.sub(r"\s+", " ", re.sub(r"\[\d+s\]\s*", "", t)).strip()


def candidates(text):
    c = {}
    c["github"] = sorted({f"{o}/{r}".rstrip(".") for o, r in re.findall(r"github\.com/([\w.-]+)/([\w.-]+)", text, re.I)
                          if o.lower() not in ("sponsors", "orgs", "topics", "features", "login")})
    c["pypi"] = sorted(set(re.findall(r"pip3?\s+install\s+([\w.-]+)", text, re.I)))
    c["npm"] = sorted(set(re.findall(r"npm\s+(?:i|install)\s+(?:-g\s+)?(@?[\w./-]+)", text, re.I)))
    c["urls"] = sorted({u.rstrip(".,)") for u in re.findall(r"https?://[^\s<>\"']+", text) if "instagram.com" not in u})
    c["handles"] = sorted(set(re.findall(r"(?<![\w.])@([\w.]{3,30})", text)))
    c["prices"] = sorted(set(re.findall(r"[$₹€£]\s?\d[\d,.]*\s?[kKmM]?", text)))
    c["income_claims"] = sorted(set(m.strip() for m in re.findall(
        r"(?:\d[\d,.]*\s?(?:k|lakh|lakhs|lacs|crore|million)?\s?(?:rupees|usd|dollars|\$|₹)?\s?(?:per|/|a|every)\s?(?:day|week|month|year)|passive income|lakhs? every month|lacs? every month|make money|earn \$?\d[\d,.]*)",
        text, re.I)))
    return {k: v for k, v in c.items() if v}


def http_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "link-inbox", **(headers or {})})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def http_text(url, limit=200000):
    req = urllib.request.Request(url, headers={"User-Agent": "link-inbox"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read(limit).decode("utf8", "ignore")


def readme_hits(repo):
    """README lines that state requirements, licence, price or limits, for checking claims."""
    for name in ("README.md", "readme.md"):
        try:
            t = http_text(f"https://raw.githubusercontent.com/{repo}/HEAD/{name}", 40000)
            break
        except Exception:
            t = ""
    out, seen = [], set()
    for line in t.splitlines():
        line = re.sub(r"\s+", " ", re.sub(r"!\[.*?\]\(.*?\)|<[^>]+>|[#>*`|]", " ", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line))).strip()
        if len(line) > 25 and re.search(r"\bVRAM\b|\bGB\b|licen[cs]e|[$₹€£]\s?\d|pric(e|ing)|\bfree\b|requires?|API key|subscription|preview|beta|experimental", line, re.I) \
                and line.lower() not in seen:
            seen.add(line.lower())
            out.append(line[:200])
        if len(out) >= 8:
            break
    return out


def github_facts(repo):
    """Repo facts from the API when allowed, else from the public page and raw files.

    The anonymous API is rate-limited per shared IP (HTTP 403), so the fallback matters.
    """
    h = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    try:
        d = http_json(f"https://api.github.com/repos/{repo}", h)
        return {"repo": d["full_name"], "found": True, "url": d["html_url"], "description": d.get("description"),
                "license": (d.get("license") or {}).get("spdx_id"), "stars": d["stargazers_count"], "forks": d["forks_count"],
                "created": d["created_at"][:10], "pushed": d["pushed_at"][:10], "archived": d["archived"], "fork": d["fork"],
                "owner_type": d["owner"]["type"], "topics": d.get("topics", [])}
    except Exception as e:
        err = str(e)[:60]
    # API unavailable (403 on a shared IP or sandbox proxy): raw.githubusercontent.com still works
    try:
        readme = http_text(f"https://raw.githubusercontent.com/{repo}/HEAD/README.md", 6000)
    except Exception as e:
        try:
            readme = http_text(f"https://raw.githubusercontent.com/{repo}/HEAD/readme.md", 6000)
        except Exception:
            return {"repo": repo, "found": False, "error": f"API: {err}; no README at HEAD: {str(e)[:30]}"}
    f = {"repo": repo, "found": True, "url": f"https://github.com/{repo}", "via": "raw files (API unavailable; no stars or dates)"}
    f["readme_start"] = re.sub(r"\s+", " ", re.sub(r"[#>*`|\[\]]|!\[.*?\]\(.*?\)|<[^>]+>", " ", readme))[:400].strip()
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
        try:
            t = http_text(f"https://raw.githubusercontent.com/{repo}/HEAD/{name}", 4000)
            known = [k for k, pat in (("Apache-2.0", r"Apache License"), ("MIT", r"MIT License|Permission is hereby granted"),
                                      ("GPL", r"GNU GENERAL PUBLIC"), ("AGPL", r"GNU AFFERO"), ("BSD", r"BSD"), ("MPL", r"Mozilla Public"))
                     if re.search(pat, t, re.I)]
            f["license_file"] = known[0] if known else t.strip().splitlines()[0][:60]
            break
        except Exception:
            continue
    return f


def pypi_facts(pkg):
    try:
        d = http_json(f"https://pypi.org/pypi/{pkg}/json")["info"]
    except Exception as e:
        return {"package": pkg, "found": False, "error": str(e)[:80]}
    return {"package": pkg, "found": True, "url": f"https://pypi.org/project/{pkg}/", "version": d["version"],
            "summary": d.get("summary"), "license": d.get("license") or d.get("license_expression"),
            "home": (d.get("project_urls") or {}).get("Homepage") or d.get("home_page")}


def main():
    args = sys.argv[1:]
    force = "--force" in args
    qv = ""
    if "--queued-via" in args:
        i = args.index("--queued-via"); qv = args[i + 1]; del args[i:i + 2]
    args = [a for a in args if a != "--force"]
    if len(args) != 2:
        sys.exit(__doc__)
    url, outdir = args
    platform, vid, kind = classify(url)
    note = ROOT / "notes" / platform / f"{vid}.md"
    if note.exists() and not force:
        print(f"ALREADY_PROCESSED {note.relative_to(ROOT)}")
        sys.exit(3)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    # 1. fetch
    clean = f"https://www.instagram.com/{'reel' if kind == 'reel' else 'p'}/{vid}/" if platform == "instagram" else url
    fetcher = "fetch_instagram.py" if platform == "instagram" else "fetch_youtube.py"
    extra = ["--comments", "50"] if platform == "youtube" else []
    code = run([sys.executable, str(HERE / fetcher), clean, str(out), *extra], out / "fetch.log")
    meta = json.loads((out / "meta.json").read_text()) if (out / "meta.json").exists() else None
    if code != 0 or not meta:
        reason = (out / "fetch.log").read_text().strip().splitlines()[-1][:200] if (out / "fetch.log").exists() else "unknown"
        (out / "brief.md").write_text(f"# BLOCKED\n\nFetch failed for {url}: {reason}\n")
        print(f"BLOCKED fetch failed: {reason}")
        sys.exit(2)

    video = out / "video.mp4"
    gaps = []
    transcript = ""
    screen = []
    lang = "n/a"
    duration = meta.get("duration_s")
    if video.exists():
        try:
            d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True).stdout.strip()
            duration = round(float(d)) if d else duration
        except Exception:
            pass
        run([sys.executable, str(HERE / "analyze_video.py"), str(video), str(out), "--ocr"], out / "analyze.log")
        tp = out / "transcript.txt"
        transcript = tp.read_text() if tp.exists() else ""
        m = re.match(r"language: (\w+)", transcript)
        lang = m.group(1) if m else "n/a"
        sp = out / "screen_text.txt"
        screen = sp.read_text().splitlines() if sp.exists() else []
    else:
        caps = sorted(out.glob("captions*.vtt"))
        if caps:
            transcript = "language: n/a (YouTube captions)\n" + vtt_to_text(caps[0])
        gaps.append("video: " + (meta.get("video_error") or "not downloaded"))
        if not transcript:
            gaps.append("transcript: none (no video, no captions)")

    # 2. candidates and facts from all text
    caption = meta.get("caption") or meta.get("description") or ""
    blob = "\n".join([caption, transcript, "\n".join(screen), " ".join(meta.get("tags") or [])])
    cand = candidates(blob)
    facts = [github_facts(r) for r in cand.get("github", [])[:6]]
    found_names = {f["repo"].split("/")[-1].lower() for f in facts if f.get("found")}
    facts = [f for f in facts if f.get("found") or f["repo"].split("/")[-1].lower() not in found_names]  # OCR typos
    seen_repos, uniq = set(), []
    for f in facts:  # same repo seen with different casing
        k = f["repo"].lower()
        if k not in seen_repos:
            seen_repos.add(k); uniq.append(f)
    for f in uniq[:4]:
        if f.get("found"):
            f["readme_lines"] = readme_hits(f["repo"])
    facts = uniq[:4] + [pypi_facts(p) for p in cand.get("pypi", [])[:4]]

    # 3. visual review decision
    screen_chars = sum(len(x) for x in screen)
    talking_head = video.exists() and screen_chars < 120 and len(transcript) > 200
    needs_visual = video.exists() and not talking_head

    likes, comments = meta.get("likes"), meta.get("comments")
    ratio = f"{comments / likes:.2f}" if likes and comments is not None else "n/a"
    posted = meta.get("posted_utc") or meta.get("posted") or ""
    if re.fullmatch(r"\d{8}", str(posted)):
        posted = f"{posted[:4]}-{posted[4:6]}-{posted[6:]}"
    posted_iso = (str(posted).rstrip("Z") + ("" if len(str(posted)) == 10 else "Z")) if posted else ""
    author = meta.get("author") or ""

    # 4. brief for Claude
    b = [f"# Brief: {platform} {kind} {vid}", "",
         f"- url: {clean}", f"- author: {author}", f"- posted: {posted_iso}", f"- duration_s: {duration}",
         f"- likes: {likes}  comments: {comments}  comments/likes: {ratio}", f"- audio language: {lang}",
         f"- needs_visual_review: {'yes' if needs_visual else 'no'}" + (f"  (view {out / 'sheet.jpg'})" if needs_visual else "  (talking head, no readable screen text)" if talking_head else ""),
         f"- gaps: {'; '.join(gaps) if gaps else 'none'}", ""]
    if meta.get("title"):
        b += [f"## Title\n{meta['title']}", ""]
    b += ["## Caption / description", caption or "(none returned)", ""]
    if meta.get("hashtags"):
        b += ["Hashtags: " + " ".join("#" + h for h in meta["hashtags"]), ""]
    if meta.get("chapters"):
        b += ["## Chapters", *[f"- {int(c['start_time'])}s {c['title']}" for c in meta["chapters"]], ""]
    b += ["## Transcript", transcript.strip() or "(none)", ""]
    if screen:
        b += ["## On-screen text (OCR, noisy: words may run together)", *screen[:60], ""]
    if cand:
        b += ["## Candidates found in the text (not yet verified)", *[f"- {k}: {', '.join(v)}" for k, v in cand.items()], ""]
    if facts:
        b += ["## Looked up (primary sources, mechanical)"]
        for f in facts:
            if f.get("found"):
                b.append("- " + ", ".join(f"{k}={v}" for k, v in f.items() if k not in ("found", "readme_lines", "readme_start") and v not in (None, [], "")))
                if f.get("readme_start"):
                    b.append(f"  - README starts: {f['readme_start'][:200]}")
                for ln in f.get("readme_lines", []):
                    b.append(f"  - README: {ln}")
            else:
                b.append(f"- {f.get('repo') or f.get('package')}: NOT FOUND ({f['error']}); unverified, not proof of fakeness")
        b.append("")
    (out / "brief.md").write_text("\n".join(b))

    # 5. draft note with the mechanical parts filled in
    fs = ["  metadata: ok" + (" (instaloader, anonymous)" if platform == "instagram" else " (yt-dlp)"),
          f"  caption: {'ok' if caption else 'not returned'}",
          "  video: " + ("downloaded" if video.exists() else "blocked (" + (meta.get("video_error") or "not downloaded")[:80] + ")"),
          "  transcript: " + (("ok (faster-whisper" + (", translated" if lang not in ("en", "n/a") else "") + ", auto-generated, may contain errors)") if video.exists() and transcript else "YouTube captions" if transcript else "none"),
          "  on_screen_text: " + ("OCR + contact sheet" if screen else "contact sheet only" if video.exists() else "n/a"),
          "  comments: " + ("not fetched (Instagram requires login)" if platform == "instagram" else "see comments.json" if (out / "comments.json").exists() else "not fetched")]
    fm = ["---", f"url: {clean}", f"platform: {platform}", f"type: {kind}", f"author: {author}", f"posted: {posted_iso}",
          f"duration_s: {duration}", f"views: {meta.get('views') or 'not exposed'}", f"likes: {likes}", f"comments: {comments}",
          f"language: {lang}"]
    if qv:
        fm.append(f'queued_via: "{qv}"')
    fm += ["fetch_status:", *fs, "title: TODO", "category: TODO", "subcategory: TODO", "usefulness: TODO",
           "tools: []", 'key_info: "TODO"', "verdict: TODO", "registry: TODO", "---", ""]
    body = ["# TODO", "", "## Caption / hashtags", ("> " + caption.replace("\n", "\n> ")) if caption else "Not returned.", ""]
    if meta.get("hashtags"):
        body += ["Hashtags: " + " ".join("#" + h for h in meta["hashtags"]) + ".", ""]
    body += ["## Hook (on-screen text)", "TODO", "", "## Call to action", "TODO", "", "## Transcript (auto)",
             ("> " + readable_transcript(transcript)) if transcript else "None available.", "",
             "## What is shown on screen", "TODO", "", "## Summary", "TODO", ""]
    if platform == "instagram":
        cm = f"Not read: Instagram requires a login to list comments. The count is {comments} against {likes} likes"
        if likes:
            cm += f" (comments/likes {ratio}; a ratio near or above 1 usually means a prompt to comment, an inference)."
        else:
            cm += "."
        body += ["## Comments", cm, ""]
    body += ["## Research (checked " + datetime.now(timezone.utc).strftime("%Y-%m-%d") + ")", "",
             "| Claim | Verdict | Evidence |", "|---|---|---|", "| TODO | TODO | TODO |", "", "Overall: TODO", "",
             "## Notes / caveats", "- TODO"]
    (out / "draft_note.md").write_text("\n".join(fm + body) + "\n")

    print(f"OK {platform} {kind} {vid} | author {author} | {duration}s | lang {lang} | screen-text lines {len(screen)} | "
          f"candidates {sum(len(v) for v in cand.values())} | facts {sum(1 for f in facts if f.get('found'))}/{len(facts)}")
    print(f"needs_visual_review: {'yes' if needs_visual else 'no'}")
    print(f"read: {out / 'brief.md'}   edit: {out / 'draft_note.md'}")


if __name__ == "__main__":
    main()
