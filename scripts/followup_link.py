#!/usr/bin/env python3
"""Answer a follow-up on a link that already has a note, without re-fetching or re-analysing the video.

Usage: followup_link.py <platform> <id> <question.txt> <answer.md> [--push] [--trailer "..."]...

Appends "## Follow-up: <question>" (the answer, with any sources) at the end of the existing note,
rebuilds the library and search index, and prints the issue comment. Claude writes only the answer.
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from finish_link import ROOT, push  # noqa: E402


def main():
    args = sys.argv[1:]
    trailers = []
    while "--trailer" in args:
        i = args.index("--trailer"); trailers.append(args[i + 1]); del args[i:i + 2]
    do_push = "--push" in args
    args = [a for a in args if a != "--push"]
    if len(args) != 4:
        sys.exit(__doc__)
    platform, vid, qf, af = args
    note = ROOT / "notes" / platform / f"{vid}.md"
    if not note.exists():
        sys.exit(f"{note} does not exist: process the link first")
    q = " ".join(Path(qf).read_text(encoding="utf8").split())
    a = Path(af).read_text(encoding="utf8").strip()
    if not q or not a or re.search(r"\bTODO\b", a):
        sys.exit("question and answer must be non-empty and free of TODO")
    text = note.read_text(encoding="utf8").rstrip() + f"\n\n## Follow-up: {q[:200]}\n\n_{date.today().isoformat()}_\n\n{a}\n"
    note.write_text(text, encoding="utf8")
    r = subprocess.run([sys.executable, str(HERE / "build_index.py")], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr.strip() or r.stdout.strip())
    if do_push:
        print(push(f"Follow-up on {platform} {vid}", trailers))
    print("--- issue comment ---\n" + a + f"\n\nSaved in the note: notes/{platform}/{vid}.md")


if __name__ == "__main__":
    main()
