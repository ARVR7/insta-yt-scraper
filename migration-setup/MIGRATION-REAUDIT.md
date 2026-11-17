# MIGRATION-REAUDIT (read-only re-check, 2026-11-17)

Audited at `4e89a2d` (`ccr-4e94c80c-rpb12o`). Nothing fixed or pushed; no key, env value or key dataset read.

## Verdict: NO-GO today, GO after one sync (about 5 minutes)

The fixes are good, but they are only on the session branch. `origin/main` (`7bc2637`) lacks all of them, and every doc tells the new Claude to start from `main`.

## The 18 gaps

| ID | Result | Evidence |
|---|---|---|
| P1-1 | FIXED | one path, Settings > Profile: CLAUDE-INSTRUCTIONS.md:16, CLAUDE-ACCOUNT-SETUP.md:83, README.md:79 |
| P1-2 | FIXED | FABLE-CARRYOVER-CHECK.md:15; all-stage query prints `LESSONS (104)` |
| P1-3 | FIXED | no stage list without `infra` left in any `.md` |
| P1-4 | FIXED | `autosave.sh:22-23`, `checkpoint.py:24,204`, `finalise.py:82`. Scratch clone with a local bare origin: unset = no trailer, set = 2 lines, 27 MB file skipped, no force, finalise dry run ok |
| P1-5 | FIXED | `verify_manifest.py:204-210`, `make_manifest.py:34-39`, KAGGLE.md:51 |
| P1-6 | PARTIAL | migration docs fixed; "at every Stop" stays in root `README.md:13`, `autosave.sh:2`, PLAN.md:38 and the ACTIVE lesson `lessons/rules/checkpoint-every-step-finalise-squash-to-main.md:13` |
| P1-7 | FIXED | `lessons/rules/keys-never-in-chat.md:13`; KNOWLEDGE-BASE.md:216 |
| P1-8 | FIXED | `CLAUDE.md`, 43 lines, 12 rules match CLAUDE-INSTRUCTIONS.md section 2, all paths exist, 0 secrets |
| P2-1 | FIXED | `query.py --help` prints usage |
| P2-2 | FIXED | CLAUDE-INSTRUCTIONS.md:74 |
| P2-3 | FIXED | HISTORY-AND-REQUIREMENTS.md:82 |
| P2-4 | FIXED | HISTORY-AND-REQUIREMENTS.md:84; README.md:17,103 |
| P2-5 | FIXED | `setup-environment.sh:2-3`; README.md:153 |
| P2-6 | FIXED | GITHUB-MOVE.md:21; VERIFY.md:58 |
| P2-7 | FIXED | the three stale lines are gone from PLAN.md; PIPELINE.md:192 |
| P2-8 | FIXED | README.md:107 |
| P2-9 | FIXED | CLAUDE-ACCOUNT-SETUP.md:115-119 (plan honestly UNKNOWN) |
| P2-10 | PARTIAL | KNOWLEDGE-BASE.md:303,319 recorded; Node 22 still "not recorded" (:320) |

## New gaps

| ID | Where | Problem | Fix |
|---|---|---|---|
| P0-1 | `origin/main` (`7bc2637`) | 27 files differ from the fixed branch: no `CLAUDE.md`, old hard-coded trailer in `checkpoint.py`/`autosave.sh`, old docs, old MANIFEST | `bash .claude/scripts/autosave.sh` (sync-docs to main), then check `git diff --stat origin/main HEAD` is empty |
| P1-9 | local commit `1a19b76` | An autosave at 05:50 UTC committed this report's draft (not made by this audit's commands in the real repo, cause not proven; not pushed, origin answers 403). MANIFEST.json is now stale: `verify_manifest.py` shows 1 extra file (WARN, still PASS) | decide keep or drop this file, then `make_manifest.py` and commit last |
| P1-10 | this VM, `git fetch`/`ls-remote` | origin returns 403 since the session resumed; preflight `git-remote` FAILs, nothing can be pushed | re-attach the repo or start a fresh session, then P0-1 |
| P2-11 | README.md:91-93 vs :166-170 | bootstrap prompt says "every file it links": `history/` is 0.94 MB (02 is 532 KB) and can fill the context | add: "history: read 04 and 01 only, the rest on demand" |
| P2-12 | README.md:63-84, VERIFY.md | no step runs `verify_manifest.py` or the carry-over check; only the table of contents names them | add them to step 11 |
| P2-13 | root `README.md` | no `CLAUDE.md`, `migration-setup/`, `docs/` in the tree | add 3 lines |
| P2-14 | CLAUDE-INSTRUCTIONS.md:3 | says sessions began 2026-11-10; history starts 2026-10-24 | correct the date |
| P2-15 | FABLE-CARRYOVER-CHECK.md:15 | `query.py ... \| head -1` prints a BrokenPipe traceback | add `2>/dev/null` |

## Commands run

`verify_manifest.py --no-preflight` at `4e89a2d`: 14 pass, 0 FAIL, tree identical. `preflight.py`: 11 PASS, 2 WARN, 1 FAIL (`git-remote`, the 403). `build_graph.py`: 126 notes, 297 edges. `bash -n` ok; `py_compile` 67 files ok. `check_layout.py`: 4 clips, 12 PASS each. Smoke step 3: `saved as v8`.
History scan (counts only): KGAT, `hf_`, `sk-`, AIza with a value 0; emails 0; 37 runs of 30+ characters, all hyphenated file names. `checkpoint.py --scan` and `export_history.py --verify-only`: 0 findings.

## Not verified

1. The live state of GitHub `main` (403 now): P0-1 rests on the fetch at the start of this audit.
2. `setup-environment.sh` and the wrapper on a fresh machine; all web click paths; the Stop-hook snippet; Network secrets with Kaggle; the Limited-network host list.
3. `kaggle.py check` and `--kaggle`: not run in this re-check.
4. `history/02` and `03` were pattern-scanned and sampled, not read in full.
