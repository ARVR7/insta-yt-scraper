---
id: keys-never-in-chat
type: rule
stage: infra
topic: secrets
status: active
supersedes: 
date: 2026-11-16
source: user: "put in place without looking at it"; move to a new account 2026-11-16: keys only in the environment
evidence: .claude/skills/clips/scripts/transcript/run.py
---
# Keys never appear in chat or logs
**Rule:** Keep API keys only in environment variables or Network secrets of the Claude environment; never print, paste, log, commit or ask for them in chat. A private Kaggle dataset is only a transfer copy: delete it once the keys are in the environment.
**Why:** User privacy rule (put in place without looking at it). A Kaggle dataset is a plaintext vault and the old vault datasets are deleted on purpose in the account move (2026-11-16).
**How to apply:** Set keys in the environment settings; use scripts/download/kaggle.py (masks output); grep the log for the key pattern = 0 matches; delete kagglegpu1, kagglegpu2 and gemini-key after the keys are moved.

**Related:**
- [kaggle](../tools/kaggle.md)
