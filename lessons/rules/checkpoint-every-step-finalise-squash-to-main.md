---
id: checkpoint-every-step-finalise-squash-to-main
type: rule
stage: publish
topic: push-cadence
status: active
supersedes: push-to-main-in-intervals
date: 2026-11-16
source: user: "Find out ways in which you never lose the clips, maybe push things directly on GitHub branch and to main once finalised. Otherwise our time would be wasted."
evidence: .claude/skills/clips/scripts/checkpoint.py
---
# Checkpoint every step to the session branch; squash to main only when finalised
**Rule:** Every render step saves to GitHub at once: checkpoint.py (called by make_clips after each clip, edit_clip --render, render_highlights, long_run after every step) commits only safe files and pushes the CURRENT session branch ccr-*; autosave.sh also pushes that branch when the lead runs it (bash .claude/scripts/autosave.sh when the platform reminder appears and about every 10 minutes; the platform reminder hook does not call it by itself). Stream content reaches main ONLY through finalise.py --stream S --yes: one squashed commit (tree of the branch, parent origin/main, message 'clips: <stream>, <n> clips (final)'), so WIP re-render blobs never enter main. Non-stream files (.claude, lessons, README) go to main via finalise.py --sync-docs from autosave. Never force-push, never push HEAD:main for stream files.
**Why:** The container is ephemeral; on 2026-11-16 a plain background job died while idle and 1.5 h were lost, and pushing every WIP re-render (80-100 MB masters, 5-25 MB clips) straight to main would bloat main forever. The user asked to never lose the clips: push to the branch directly and to main once finalised.
**How to apply:** Nothing to remember for the branch: the scripts do it and print WARNING NOT SAVED TO GITHUB on failure (then run checkpoint.py --stream streams/<s> by hand and tell the user). Run bash .claude/scripts/autosave.sh by hand at the end of a turn and about every 10 minutes. When the user keeps the clips: finalise.py --stream streams/<s> (dry run), then --yes. If finalise says main was changed from another branch, do not force: ask the user. Container gone: git checkout the ccr- branch, jobs.py check, fetch-windows or backup_sources.py restore.

**Related:**
- [long-jobs-detach-and-register](../gotchas/long-jobs-detach-and-register.md)
- [output-preview-in-git-master-on-keep](../preferences/output-preview-in-git-master-on-keep.md)
- [repo-keeps-only-current-work](../rules/repo-keeps-only-current-work.md)
- replaces: [push-to-main-in-intervals](../rules/push-to-main-in-intervals.md)
