#!/usr/bin/env bash
# Commit and push everything to the CURRENT BRANCH (the session branch ccr-*) once. The platform reminder hook does not call it: the lead runs `bash .claude/scripts/autosave.sh` when the reminder appears and about every 10 minutes.
# WHERE THINGS GO (rule of 2026-11-16, lesson checkpoint-every-step-finalise-squash-to-main):
#   * EVERYTHING changed is committed and pushed to the current branch: that is the safety net. checkpoint.py does the same after every render step, so a reclaimed container loses at most the step in flight.
#   * STREAM content (streams/, LATEST.md) reaches main ONLY through `finalise.py --stream S --yes` (one squashed commit of final files, no WIP re-render blobs). This script never pushes stream files to main.
#   * NON-STREAM files (.claude/, lessons/, README ... everything outside streams/ and LATEST.md) are also put on main by `finalise.py --sync-docs`: one small commit on top of origin/main, fast-forward only, skipped with one line if main was changed from elsewhere.
# Safe rules: never force-push; skip while .autosave-pause exists (history rewrites); skip files over 25 MB; skip a changed .py file that does not compile; skip a file that looks like it holds a key.
# Highlights preview.mp4 files are gitignored (80 MB per render, delivered with SendUserFile) and are never deleted; the one preview committed earlier stays as it is and a re-render of it is left unstaged here.
cd "$(dirname "$0")/../.." || exit 1
[ -e .autosave-pause ] && { echo "paused"; exit 0; }
b=$(git rev-parse --abbrev-ref HEAD)
sync_main() { [ "$b" = main ] || timeout 300 python3 .claude/skills/clips/scripts/finalise.py --sync-docs 2>&1 | tail -1; }
git add -A
git reset -q -- 'streams/*/highlights/*/preview.mp4' 2>/dev/null   # unstage a re-rendered tracked preview; the file itself is untouched
for f in $(git diff --cached --name-only); do
  [ -f "$f" ] && [ "$(stat -c %s "$f")" -gt 26214400 ] && { git reset -q -- "$f"; echo "skipped big file $f"; }
  case "$f" in *.py) [ -f "$f" ] && ! python3 -m py_compile "$f" 2>/dev/null && { git reset -q -- "$f"; echo "skipped broken $f"; };; esac
done
for f in $(git diff --cached --name-only | xargs -r python3 .claude/skills/clips/scripts/checkpoint.py --scan); do git reset -q -- "$f"; echo "skipped key-like file $f"; done
find . -name __pycache__ -prune -not -path "./.git/*" -exec rm -rf {} \; 2>/dev/null
git diff --cached --quiet && { echo "nothing to save"; sync_main; exit 0; }
tr=${CLAUDE_COMMIT_TRAILER-}; tr=${tr//\\n/$'\n'}   # trailer ONLY from the env var CLAUDE_COMMIT_TRAILER (full text, \n allowed); unset = no trailer
set -- -m "autosave $(date -u +%Y-%m-%d\ %H:%M) UTC"; [ -n "$tr" ] && set -- "$@" -m "$tr"
git commit -q "$@" || exit 1
[ "$b" = HEAD ] && { echo "detached HEAD: committed here, not pushed"; exit 1; }
for try in 1 2; do
  git push -q origin "HEAD:refs/heads/$b" 2>/dev/null && { echo "pushed $b $(git rev-parse --short HEAD)"; sync_main; exit 0; }
  git pull -q --no-rebase --no-edit origin "$b" 2>/dev/null || { git merge --abort 2>/dev/null; break; }
done
echo "push failed: will retry next round"; exit 1
