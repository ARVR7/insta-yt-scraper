# MIGRATION-AUDIT (read-only audit, 2026-11-16)

Audited at `8e014d0` (`ccr-4e94c80c-rpb12o`); `origin/main` (`084a832`) has the identical tree (603 files). Nothing was fixed, committed or rendered; no key, env value or dataset content was read.

## Verdict: GO, with 8 P1 fixes first (about 20 minutes, Sonnet)

No P0. A new Claude can follow `README.md` to a working pipeline. It is not "100%": a fresh machine and the web click paths cannot be proven from the old VM.

## Result per area

| # | Area | Result | Evidence |
|---|---|---|---|
| 1 | Coverage | PASS | 104/104 active and 22/22 superseded lessons, 7/7 incidents, 5/5 destinations, all 29 report/research docs in KNOWLEDGE-BASE.md or PIPELINE.md. Scripts 52/60 by name; the 8 `trials/*.py` only as a group. File map matches `git ls-files` |
| 2 | Truth | PASS with 6 errors | about 150 claims checked (110 flags/subcommands, 20 defaults, 12 versions, 12 counts). Errors: P1-2, P1-3, P2-1..4 |
| 3 | Setup from zero | PASS with gaps | 0 dead links; all linked files are on `main`. The reader must guess at P1-1, P1-4, P1-5, P1-6, P2-5 |
| 4 | Consistency | FAIL (minor) | contradictions P1-5, P1-6, P1-7, P2-2, P2-6, P2-7 |
| 5 | Safety | PASS | `checkpoint.py --scan` on all tracked files: 0 hits. Token regex (KGAT, hf_, AIza, gh*_, 30+ char high-entropy): 0 in the tree, 0 in the 324 commits of all refs. Repo is private (`gh api`). Account-2 key rotation: REVOKE-AND-SECURITY.md:10, KAGGLE.md:54. No instruction makes an agent read a key |
| 6 | Missing knowledge | PASS with gaps | preferences, how the user talks, model roles, session conventions, licences, dataset names, unproven list and open items are written. Missing: P1-4, P1-8, P2-9, P2-10 |

## Gaps, ranked

### P1 (works, but the new Claude is misled or degraded)

| ID | Where | Problem | One-line fix |
|---|---|---|---|
| P1-1 | CLAUDE-ACCOUNT-SETUP.md:82, CLAUDE-INSTRUCTIONS.md:15-19, README.md:78 | The style is described three ways: a Claude Code "output style", a claude.ai Profile preference, and a skill header ("Invoke with /i-have-adhd") | Name ONE path (Settings > Profile preferences); mark the others unverified |
| P1-2 | FABLE-CARRYOVER-CHECK.md:15 | `query.py --stage plan` prints 15 lessons, not 104: a false FAIL | Use `query.py` with no arguments (prints `LESSONS (104)`) |
| P1-3 | KNOWLEDGE-BASE.md:6, CLAUDE-INSTRUCTIONS.md:12, PIPELINE.md:29 | The stage list has no `infra`: it prints 90 of 104 lessons, not "every active lesson"; skipped: `agents-never-see-kaggle-key`, `tick-first-during-jobs` and 12 more | Add `,infra` to the `--stage` list (also SKILL.md:49) |
| P1-4 | `.claude/skills/clips/scripts/checkpoint.py:23`, `.claude/scripts/autosave.sh:22` (not mentioned in any migration file) | Both hard-code the OLD account's `Claude-Session:` URL and "Claude Sonnet 5.5" as commit trailers | Add a VERIFY.md step: replace both trailers with the new session's attribution |
| P1-5 | FABLE-CARRYOVER-CHECK.md:14 and `verify_manifest.py --kaggle` vs REVOKE-AND-SECURITY.md:14, KAGGLE.md:55 | The check says the datasets "must include" `kagglegpu1`, `kagglegpu2`, `gemini-key`; the other files say delete them, never copy them. New Kaggle accounts give a false FAIL | Reword: "a missing vault dataset is fine (deleted on purpose)" |
| P1-6 | CLAUDE-INSTRUCTIONS.md:75 vs CLAUDE-ACCOUNT-SETUP.md:114 | One says the Stop hook ran autosave every turn, the other that no such hook was configured. The platform's own Stop hook (`~/.claude/launcher-settings.json`) does not call `autosave.sh` | Line 75: "autosave was run by hand; no hook called it" |
| P1-7 | `lessons/rules/keys-never-in-chat.md:13` (active; KNOWLEDGE-BASE.md:216) | Rule text: "Keep API keys in the private Kaggle dataset", the opposite of the move (keys only in the environment, vaults deleted) | With `add_lesson.py`, supersede it: "keys live only in the Claude environment" |
| P1-8 | repo root | No `CLAUDE.md`: after the first session nothing loads CLAUDE-INSTRUCTIONS.md by itself | With the user's OK, add a short `CLAUDE.md` pointing to `migration-setup/CLAUDE-INSTRUCTIONS.md` |

### P2 (cosmetic or small)

| ID | Where | Problem | Fix |
|---|---|---|---|
| P2-1 | VERIFY.md:76, TROUBLESHOOTING.md:75 | `query.py --help` prints all lessons, not usage (no `--help` exists) | Use `query.py --stage plan \| head -3` |
| P2-2 | CLAUDE-INSTRUCTIONS.md:73 | "the `gh` CLI is not available": false. `gh api repos/...` works; only `gh repo view` (GraphQL) fails | Copy the wording of FABLE-CARRYOVER-CHECK.md:10 |
| P2-3 | HISTORY-AND-REQUIREMENTS.md:82 | "pass 1 took 574 s": `prepare_report.json` says 544.7 s (PIPELINE.md:62 is right) | 574 -> 545 |
| P2-4 | HISTORY-AND-REQUIREMENTS.md:84; README.md:17,102 | "Clip files 20-42 MB": real range 7-43 MB. "12 checks": preflight has 14 (12 PASS + 2 WARN) | Correct both numbers |
| P2-5 | setup-environment.sh:2, README.md:151 | "paste this file into the Setup script box": 116 lines, the box takes 100. CLAUDE-ACCOUNT-SETUP.md:48-52 (wrapper) is right | Header and table row: "run by the one-line wrapper" |
| P2-6 | VM-SETUP-LOG.md:79, GITHUB-MOVE.md:21 | "`git checkout ccr-4e94c80c-rpb12o` to continue": `main` has the same tree; a cloud session stays on its own branch | "Start from `main`; the old `ccr-*` branch is history only" |
| P2-7 | `.claude/skills/clips/PLAN.md:23,26,31` | Current plan still says: validation "fixes in progress"; "a real 5-6 h link" is backlog (done); Whisper turbo with a superseded lesson. PIPELINE.md:192 names two other stale items only | Add these three to the stale list in PIPELINE.md section 13 |
| P2-8 | README.md:106 vs :77 | The smoke test demands account 2 `reachable: yes`, but account 2 is optional (VERIFY.md:22 allows it missing) | Add "(account 2 only if you use one)" |
| P2-9 | CLAUDE-ACCOUNT-SETUP.md | Not written: the old setting `advisorModel: opus`; auto mode; which model to pick for a session; which Claude plan | Add 3 lines to section 8 |
| P2-10 | KNOWLEDGE-BASE.md:34, :303, :319; HISTORY-AND-REQUIREMENTS.md:47 | Source/licence of the `yt-*` skills, yt-dlp, numpy, Pillow "not recorded"; `docs/destination-rules.md` lacks the `.claude/skills/clips/` prefix | Record them; fix the path |

## Commands run (all passed unless listed above)

`preflight.py` (12 PASS, 2 WARN), `kaggle.py check` (both accounts reachable), both `edit_clip` dry runs (saved as v8), `check_layout.py` (3 clips 12 PASS each; 15 GamerFleet clips exit 0), `jobs.py check`, `build_graph.py` (126 notes, 297 edges), `verify_manifest.py --no-preflight` (14 pass, 0 FAIL), `bash -n`, `py_compile`, `git grep` KGAT, `git ls-tree origin/main` (30 GamerFleet mp4, 15 folders, 52 mp4), `ffprobe` (54.0 s), `gh api` (private: true), all tool versions.

## Not verified, and why

1. `setup-environment.sh` and the one-line wrapper were not executed: the permission classifier refused it. Only `bash -n` and a line count (116 lines, none over 200 bytes).
2. A fresh machine: every tool is cached on this VM.
3. All web click paths and URLs (claude.ai/connect-github, environment page, github.com/new/import, Kaggle pages): no browser.
4. The Stop-hook JSON snippet and Network secrets with the Kaggle CLI: still untested.
5. The Limited-network host list: this environment is unrestricted (only the two Kaggle hosts were confirmed in the CLI).
6. Kaggle dataset names and their Private setting: out of scope here.
7. "769 s for 15 windows" and the dated incident details: no source file found.
8. `MANIFEST.json` is one commit behind (`bde1b96`, main `7a814c8`): regenerate it after the last doc commit, as FABLE-CARRYOVER-CHECK.md:3 says.

## Fix status (2026-11-16, after the audit)

All 8 P1 and all 10 P2 gaps were handled; nothing is skipped except what is named below. The numbers `P1-n` / `P2-n` are the IDs above.

| ID | Status | What was done |
|---|---|---|
| P1-1 | fixed | One path everywhere: paste the block into claude.ai Settings > Profile; `i-have-adhd` was the style's title in the old account (also `/i-have-adhd` there); a Claude Code output style is a separate, optional mechanism (CLAUDE-INSTRUCTIONS.md section 1, CLAUDE-ACCOUNT-SETUP.md section 6, README.md, VERIFY.md) |
| P1-2 | fixed | FABLE-CARRYOVER-CHECK.md step 8 counts active notes from `lessons/INDEX.md` / the all-stage query and compares with `counts.lessons_active` of MANIFEST.json (104 at the move) |
| P1-3 | fixed | `infra` added to the stage list in KNOWLEDGE-BASE.md, CLAUDE-INSTRUCTIONS.md, PIPELINE.md, SKILL.md and docs/openshorts-skill.md; `query.py` already supports it (104 lessons printed) |
| P1-4 | fixed | `checkpoint.py` and `autosave.sh` no longer hard-code a trailer: only `CLAUDE_COMMIT_TRAILER` (`\n` allowed) or none. Tested in a scratch clone with a local bare origin (no trailer, trailer, 27 MB file skipped, no force). Documented in QUICKSTART.md, CLAUDE-ACCOUNT-SETUP.md, CLAUDE-INSTRUCTIONS.md |
| P1-5 | fixed | `make_manifest.py` marks `gemini-key`, `kagglegpu1`, `kagglegpu2` optional (plaintext key vaults, transfer copy); `verify_manifest.py --kaggle` PASSes when they are absent and WARNs when present; FABLE-CARRYOVER-CHECK.md step 7 and KAGGLE.md say the same |
| P1-6 | fixed | The truth in CLAUDE-INSTRUCTIONS.md, CLAUDE-ACCOUNT-SETUP.md section 8, VM-SETUP-LOG.md, README.md, KNOWLEDGE-BASE.md, SKILL.md, TROUBLESHOOTING.md and the carry-over check: only the platform's commit reminder exists, it does not call `autosave.sh`; run `bash .claude/scripts/autosave.sh` by hand; optionally ask Claude to add a Stop hook (update-config skill, user approves) |
| P1-7 | fixed | `keys-never-in-chat` rewritten with `add_lesson.py` (same id): keys only in the environment, a Kaggle dataset is a transfer copy to delete; graph valid; KNOWLEDGE-BASE.md row updated |
| P1-8 | fixed | Root `CLAUDE.md` (43 lines): first commands, the 12 rules, ADHD format, key safety, branch/main rule, pointers |
| P2-1 | fixed | `query.py --help` / `-h` now prints usage (no existing flag changed) |
| P2-2 | fixed | `gh api` works, `gh repo view` fails (GraphQL): CLAUDE-INSTRUCTIONS.md section 4 |
| P2-3 | fixed | 574 s -> 544.7 s (HISTORY-AND-REQUIREMENTS.md) |
| P2-4 | fixed | 20-42 MB -> 7-43 MB; 12 checks -> 14 (README.md; 12 PASS + 2 WARN) |
| P2-5 | fixed | `setup-environment.sh` header and README.md table row: run by the one-line wrapper, not pasted (over 100 lines) |
| P2-6 | fixed | VM-SETUP-LOG.md, GITHUB-MOVE.md, VERIFY.md: start from `main`; the old `ccr-*` branch is history only |
| P2-7 | fixed | The three stale lines of `.claude/skills/clips/PLAN.md` corrected; PIPELINE.md section 13 notes it |
| P2-8 | fixed | README.md smoke test: account 2 only if used |
| P2-9 | fixed | CLAUDE-ACCOUNT-SETUP.md section 8: `advisorModel` (old value `opus`), model choice, auto mode, plan. The old plan is NOT recorded anywhere: marked UNKNOWN, to be checked in the new account |
| P2-10 | partly fixed | Path fixed (`.claude/skills/clips/docs/...`); the `yt-*` source and licence taken from git history (commit `be9d31a`: MIT, Jake Schincariol); yt-dlp, numpy and Pillow licences read from the installed package metadata (`importlib.metadata`). Node 22 licence left "not recorded" |
