# GITHUB-MOVE: get the repo into the new GitHub account

Back to [README.md](README.md). Pick ONE option. Default: **A (mirror)**. Time: 10-20 minutes.

## Rules for every option

1. The new repo MUST be **PRIVATE**. Why: it holds photo-real AI-generated reference images of the fictional streamer (`.claude/skills/clips/assets/facecam/reference/`), clips cut from streamers' videos (rights are not cleared, see `lessons/gotchas/rockstar-policy-non-commercial.md`), the full settings of the pipeline, and key-adjacent configuration (names of the key datasets, account names, the autosave script). A public repo would expose all of it, and every old commit stays public forever.
2. **No secret is in the repo** (the autosave and checkpoint scripts refuse key-like files). Still: never paste a key in chat or in a file.
3. **History was rewritten on 2026-11-15** (git-filter-repo removed every blob over 25 MB; see `archive/restructure-2026-11-15.md`). Any clone made before that date is dead: do NOT push it anywhere. Always clone fresh from the old repo.
4. **git-lfs is not used.** No `git lfs install` needed. GitHub's limit is 100 MB per file; the pipeline refuses files over 95 MB.
5. **`main` holds only the final, squashed clips** (made by `finalise.py`); the **session branch `ccr-*` holds the work** (every re-render, checkpoints, autosaves).
6. After the move, `origin` of the new session must be the NEW repo. Check with `git remote -v` (VERIFY.md).

Old repo: `https://github.com/ARVR7/VideoGeneration`. New repo: `https://github.com/NEW_USER/VideoGeneration` (replace `NEW_USER`).

## Which branches exist (checked 2026-11-16)

| Branch | Date | Keep? | Why |
|---|---|---|---|
| `main` | 2026-11-16 | **KEEP** | final clips + all non-stream files (autosave syncs docs here) |
| `ccr-4e94c80c-rpb12o` | 2026-11-16 | **KEEP** (newest `ccr-*`) | the old working branch; history only: the new session starts from `main` (same tree), do not check this branch out |
| `ccr-199080cc-gglwkg`, `ccr-80b0d582-9slqo7`, `ccr-da6f8e3a-s0vvrw` | 2026-10-17 | delete | old session branches, unrelated history from October (no common ancestor with `main`) |
| `feature/add-test-clips-arjun`, `feature/hf-space-scripts-arjun`, `feature/hf-wan22-aoti-arjun`, `feature/phantom-cpu-setup-arjun` | 2026-10-17 | delete | old experiments (October), unrelated history |
| `refs/pull/1`, `refs/pull/2` | | do not copy | GitHub's own pull-request refs; a mirror push to GitHub rejects them (see the fix in option A) |

Re-check the list any time: `git ls-remote --heads https://github.com/ARVR7/VideoGeneration.git` (the newest `ccr-*` is the one with the latest date in `git log -1 --format=%cd REF`).

Delete the rest AFTER the push, in the NEW repo only:
```
git push NEW --delete ccr-199080cc-gglwkg ccr-80b0d582-9slqo7 ccr-da6f8e3a-s0vvrw
git push NEW --delete feature/add-test-clips-arjun feature/hf-space-scripts-arjun feature/hf-wan22-aoti-arjun feature/phantom-cpu-setup-arjun
```
(`NEW` = `https://github.com/NEW_USER/VideoGeneration.git`, or a remote name you added with `git remote add NEW <that URL>`. Or click the trash icon on github.com/NEW_USER/VideoGeneration/branches.) Never delete `main` or the newest `ccr-*`.

Leaner alternative that skips the old branches from the start: replace `git push --mirror` below with
```
git push NEWURL main ccr-4e94c80c-rpb12o
```
(run inside the bare clone; it copies only these two branches with their full history; then `git push NEWURL --tags` only if you use tags: the repo has none today).

---

## What actually happened (2026-11-17): option B was used

The user already transferred the repo to the new GitHub account and renamed it: **`soverellp/clipper`** (not `NEW_USER/VideoGeneration`). The old account `ARVR7` stayed as a collaborator. Consequences:

- The old name `ARVR7/VideoGeneration` returns **403** for a session that still has it as origin (`git push` and `git fetch` fail; preflight `git-remote` FAILs). Do not keep retrying it: re-attach the transferred repo instead (below).
- A Claude session sees a repo only if the Claude GitHub App installation covers it. After a transfer the app must be installed on the NEW owner's account for that repo: https://github.com/apps/claude/installations/select_target (pick `soverellp`, select `clipper`), and the collaborator invite must be accepted by the account that connects Claude. Then attach the repo to a new session (or re-attach it to the running one).
- The repo name differs from the old one everywhere (`clipper`). `MANIFEST.json` and `verify_manifest.py` compare file trees and hashes, not names, so the manifest check still passes; docs that say `NEW_USER/VideoGeneration` mean "the new repo, whatever it is called".

## Option A (recommended): mirror to a new repo owned by the new account

Full history, all branches, same commit ids. Needs `git` on a computer (or any Claude session that has both accounts' access; a person can run it on their own laptop).

1. On github.com (new account) > New repository: name `VideoGeneration`, **Private**, **do not** add README, .gitignore or license (it must be EMPTY). Copy its URL.
2. Clone the OLD repo as a mirror (a fresh clone, never an old one):
   ```
   git clone --mirror https://github.com/ARVR7/VideoGeneration.git OLD.git
   ```
   (Private old repo: Git asks for the old account's login in its credential prompt; use a fine-grained token with Contents: Read on that repo, entered in the prompt, never in chat.)
3. Remove GitHub's hidden pull-request refs, otherwise the push is partly rejected with `deny updating a hidden ref`:
   ```
   cd OLD.git
   git for-each-ref --format='delete %(refname)' refs/pull | git update-ref --stdin
   ```
4. Push everything to the new repo (the credential prompt asks for the NEW account; use a fine-grained token with Contents: Write on the new repo only, entered in the prompt):
   ```
   git push --mirror https://github.com/NEW_USER/VideoGeneration.git
   ```
   Expected last lines: ` * [new branch]      main -> main` and so on. Time: 1-3 minutes (about 200 MB packed).
5. Clean the branches (table above), then check:
   ```
   git ls-remote https://github.com/NEW_USER/VideoGeneration.git
   ```
   `refs/heads/main` has the same sha as `git ls-remote https://github.com/ARVR7/VideoGeneration.git refs/heads/main`.
6. Make the new repo the origin of your working copy (a Claude session on the new account attaches the repo itself, then this is already right):
   ```
   git clone https://github.com/NEW_USER/VideoGeneration.git
   ```
7. Delete the two scratch items: `OLD.git` folder (it is a full copy of the repo) and the tokens you used (REVOKE-AND-SECURITY.md).
8. **The old remote**: if you keep working in an old clone, repoint or delete it:
   ```
   git remote set-url origin https://github.com/NEW_USER/VideoGeneration.git
   git remote -v
   ```
   After VERIFY.md is green, either archive the old repo (Settings > General > Danger Zone > Archive: read-only, stays private) or delete it. See REVOKE-AND-SECURITY.md.

## After using GitHub "Import repository": how to copy later commits

GitHub also has a web importer: github.com/new/import (paste the old repo URL, pick the new owner and name, choose Private, give the old account's login when asked). That is a **snapshot of the moment you pressed Import**. Everything that happens on the old repo afterwards is NOT copied: the `migration-setup/` folder if it was still being written, new final clips, the autosave commits of the old session. The import keeps the same commit ids, so catching up later is a plain fast-forward.

First check whether you are behind (two commands, same sha = in sync):
```
git ls-remote https://github.com/ARVR7/VideoGeneration.git refs/heads/main
git ls-remote https://github.com/NEW_USER/VideoGeneration.git refs/heads/main
```
Do the same with `refs/heads/ccr-4e94c80c-rpb12o`. Different sha: pick a path.

**Path 1 (simplest, recommended): wait until the old repo is final, then re-import fresh.** Wait until `migration-setup/` is complete and nothing runs on the old session. Then: new repo > Settings > General > Danger Zone > Delete this repository; go to github.com/new/import and import again. The commit ids stay identical to the old repo. Do this BEFORE you create the Claude environment, the GitHub App install and the first session on the new repo (deleting the repo drops those links). If you already did, reinstall the app on the re-created repo (https://github.com/apps/claude/installations/select_target) and re-attach it in the environment's Repositories list.

**Path 2 (inside the Claude app, no local computer): fast-forward from the old repo.** Use this when the new repo is already in use.
1. Old account > old repo > Settings > Collaborators > Add people > the NEW GitHub account with **Read** access. The new account accepts the invitation (email or github.com/notifications).
2. Open a Claude session on the new account with the NEW repo attached. In that session ask Claude to add the OLD repo as a second repository (the session tool is `add_repo`, access: read; it gives you a clone command and a path). Then:
   ```
   git remote add old <clone path of the old repo from add_repo>
   git fetch old
   git push origin old/main:main old/ccr-4e94c80c-rpb12o:ccr-4e94c80c-rpb12o
   ```
   These pushes are fast-forwards because the import kept the commit ids; there is no force, so if one is rejected something else was added on the new repo: stop and read TROUBLESHOOTING.md ("push rejected").
3. Check with the two `git ls-remote` commands above: same sha.
4. Remove the collaborator again: old repo > Settings > Collaborators > remove the new account. (Only when the new repo is an import, mirror or transfer. If it is a FORK, do NOT remove access: GitHub deletes private forks when access is removed.)

**Path 3 (from a computer): clone the old repo, push everything to the new one.**
```
git clone https://github.com/ARVR7/VideoGeneration.git
cd VideoGeneration
git remote add new https://github.com/NEW_USER/VideoGeneration.git
git push new --all
git push new --tags
```
Use a fine-grained personal access token of the NEW account with **Contents: Read and write on the NEW repo only**. Git asks for it in its own credential prompt: type or paste it THERE, never in a chat, never in a file, never in the URL. When done, revoke the token (github.com > Settings > Developer settings > Personal access tokens > Delete). `--all` pushes branches only; `--tags` pushes tags (there are none today, the command is harmless).

---

## Option B: transfer ownership

Moves the SAME repo (stars, issues, settings, the Claude GitHub App link) to the new account. The old account loses it.

1. Old account > repo > Settings > General > Danger Zone > **Transfer** > type the repo name > enter the NEW username.
2. The new account gets an email; it must **accept within 1 day** (github.com/NEW_USER notification, or the link in the email).
3. The old URL may redirect for a while, but a Claude session that still uses the old name gets 403 (seen on 2026-11-17); do not rely on it; use the new URL (`git remote set-url origin https://github.com/NEW_USER/VideoGeneration.git`) or let the platform re-attach the repo.
4. Visibility stays **Private** (check it). GitHub Apps installed on the old account are NOT carried over: reinstall the Claude GitHub App on the new account: https://github.com/apps/claude/installations/select_target .
5. Collaborators and webhooks stay; Actions secrets stay (this repo has none).

Trade-off: fastest and keeps everything, but the old account has no copy afterwards (take a backup mirror first with steps 2-3 of option A if you want one).

## Option C: fork

Fork the old repo from the new account (needs read access to the old repo: add the new account as a collaborator with Read, as in Path 2).

Limits: a fork of a private repo stays private and can only be owned by an account that has access; you cannot make a private fork public; forks copy only the branches you select (default branch only unless you untick "Copy the main branch only"), and the link to the parent means later pushes can diverge. Admin rights are on the fork (you own it), not on the parent. Pull-request refs are not copied. **Data-loss warning:** if the old account removes the new account's access to a private repo, or deletes that private repo, GitHub deletes the forks of it. So with option C NEVER remove the collaborator and NEVER delete the old repo afterwards, and do not use option C together with Path 2 below. Use a fork only if you want to keep contributing back to the old repo; for a clean break use A or B.

## Option D: FULL ADMIN POWER for the new account

GitHub fact: a repo owned by a **personal account** has exactly one owner and cannot give another user the Admin role; collaborators on a personal repo get **write** at most (they cannot change visibility, delete the repo or manage collaborators). To give the new account full admin power, choose one:

**D1. Make the new account the owner:** use option B (transfer) or option A (the new account creates the repo itself).

**D2. Use a GitHub Organization (then people can be real Admins/Owners):**
1. From the old account: github.com/settings/organizations > New organization > Free plan > name it (for example `video-generation-org`) > the old account is the first Owner.
2. Invite the new account: Org > People > Invite member > new username > role **Owner**; the new account accepts by email. Owners control everything in the org.
3. Move the repo into the org: repo > Settings > General > Danger Zone > Transfer > the org name. (Private repos stay private.)
4. Reinstall the Claude GitHub App on the organization (https://github.com/apps/claude/installations/select_target > pick the org).
5. Optional: later transfer the repo from the org to the new account, or remove the old account from the org.

**Add collaborators later:** repo > Settings > Collaborators > Add people > username > role (Read, Write; in an org also Triage, Maintain, Admin).

**Branch protection to AVOID (it breaks autosave and finalise):** `autosave.sh`, `checkpoint.py` and `finalise.py` push straight to `main` and to the `ccr-*` branch as **fast-forward pushes, never forced**. So do NOT turn on any of these for `main` or `ccr-*`: "Require a pull request before merging", "Require status checks", "Require signed commits", "Restrict who can push". "Do not allow force pushes" is fine (the tools never force). If you must protect `main`, allow the account/app that pushes to bypass the rule, and expect `finalise.py` to stop with an error when it cannot push.

## After any option: tell Claude

1. [CLAUDE-ACCOUNT-SETUP.md](CLAUDE-ACCOUNT-SETUP.md): connect GitHub, install the app on the new repo, add it to the environment.
2. [VERIFY.md](VERIFY.md): `git remote -v` shows the NEW private repo, `git log origin/main -1` shows the latest final commit.
