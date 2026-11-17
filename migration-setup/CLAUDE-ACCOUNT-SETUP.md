# CLAUDE-ACCOUNT-SETUP: the new Claude account, step by step

Back to [README.md](README.md). Time: about 25 minutes. No key is written here; only variable NAMES and where each key is created.

## Checklist

- [ ] 1. Connect GitHub to the new Claude account (3 min)
- [ ] 2. Install the Claude GitHub App on the new private repo (3 min)
- [ ] 3. Create the keys you need (Kaggle, Hugging Face) (5-10 min)
- [ ] 4. Create the cloud environment, paste the one-line setup wrapper (10 min)
- [ ] 5. Put the keys into the environment (2 min)
- [ ] 6. Paste the response style (`i-have-adhd`) into Settings > Profile (2 min)
- [ ] 7. Optional: connectors and account skills (5 min)
- [ ] 8. Check permissions, model/advisor/auto mode and the autosave (5 min)

## 1. Connect GitHub (claude.ai/code)

1. Sign in to the NEW Claude account at https://claude.ai/code .
2. Open https://claude.ai/connect-github and authorise the NEW GitHub account.
3. If the repo is in an organization: authorise the organization too (the page shows an "Grant" button next to it).

## 2. Install the Claude GitHub App on the new repo

1. https://github.com/apps/claude/installations/select_target > pick the NEW account (or the organization).
2. "Only select repositories" > choose `VideoGeneration` (private). Save.
3. Back on claude.ai/code the repo shows up in the repository picker. If it does not: reload, or re-run step 1.

## 3. Create the keys (the values stay in the environment; never in chat)

| Variable NAME | Needed? | Where the key is created | Notes |
|---|---|---|---|
| `KAGGLE_USERNAME` | REQUIRED | the Kaggle user name (kaggle.com > your profile URL) | not secret, but keep it in the environment |
| `KAGGLE_APITOKEN` | REQUIRED | kaggle.com > Settings > API > **Create New Token** | the new access-token format (starts with `KGAT_`). `kaggle.py` also accepts `KAGGLE_API_TOKEN` or `~/.kaggle/kaggle.json` |
| `HF_Token` | optional | huggingface.co > Settings > Access Tokens > Create new token (type: Read) | no script in the repo reads it by name today; it only avoids Hugging Face rate limits when the Kokoro voice weights are downloaded. The old environment had it |
| `KAGGLE_USERNAME2` | optional | Kaggle user name of the second account (default if unset: `sovere`) | second GPU quota, see KAGGLE.md |
| `KAGGLE_APITOKEN2` | optional | the second account: Settings > API > Create New Token | if unset, `kaggle.py` tries to read it from the private dataset `<account 1>/kagglegpu2` (see KAGGLE.md, chicken-and-egg) |
| `CLAUDE_COMMIT_TRAILER` | optional (not a secret) | you write it: the full commit trailer text, a line break written as `\n` | `checkpoint.py`, `finalise.py` and `autosave.sh` add this text to every commit message and NOTHING else: unset = commits carry no `Co-Authored-By` / `Claude-Session` line. The old account's trailer is no longer hard-coded. Example: `Co-Authored-By: Claude <noreply@anthropic.com>\nClaude-Session: <the new session's URL>` (use the attribution lines the new session's system reminder gives). The session URL changes per session, so most people leave it unset |
| `GEMINI_API_KEY` | optional | aistudio.google.com > Get API key | only for the optional visual reviewer; without it a Sonnet/Haiku sub-agent does it. Free keys cannot generate images |

Nothing else is needed: no YouTube cookies, no proxy.

## 4. Create the cloud environment

Today's (old) environment, so you can copy it: name **Full access**, scope personal, network **unrestricted**, variables `KAGGLE_APITOKEN`, `KAGGLE_USERNAME` and the OPTIONAL `HF_Token` (no script reads it), no setup script, Repositories list empty.

1. claude.ai/code > the environment menu > **Add environment** (or Settings > Environments).
2. Name: `VideoGeneration` (personal).
3. **Network**: easiest = Unrestricted (as before). Safer = Limited with the host list below.
4. **Setup script**: the box takes at most 100 lines of 200 bytes, and `setup-environment.sh` is longer. The repo is already cloned when the setup script runs, so paste only this ONE-LINE wrapper (it runs the file from the repo; it finds the checkout by itself and never fails the session):
   ```
   for f in */migration-setup/setup-environment.sh; do [ -f "$f" ] && bash "$f"; done; true
   ```
   The wrapper only works when the repo is on the environment's Repositories list (step 5): add the repo first. The script starts one directory above the repo, runs as root after the clone, cannot read the environment's variables or secrets, is idempotent, and always exits 0 (a failing script would block the session). Optional extras, as a line BEFORE the wrapper: `export SETUP_KOKORO=1` (commentary voice, 1.7 GB, highlights videos only) and/or `export SETUP_HYPERFRAMES=1` (animations, 290 MB). Without them everything except highlights commentary and animated titles works. Tested on the old VM from the directory above the repo: it prints `[setup] ... done`.
5. **Repositories** list: add the new private repo (the old environment had this list empty and the repo was attached per session; with the list filled, every new session on this environment gets it).
6. Save, then start a new session on this environment.

### Allowed hosts for a Limited network (derived from the scripts)

| Host | Why | Source in the repo |
|---|---|---|
| `www.kaggle.com`, `api.kaggle.com`, `kaggle.com` | the kaggle CLI (kernels, datasets, API); the two `api.`/bare hosts are read from the installed CLI 2.2.5 (`kagglesdk`) | `kaggle.py`, QUICKSTART.md section 3, `grep` of the CLI |
| `storage.googleapis.com` | Kaggle serves kernel outputs and dataset files from Google storage; also the Chrome download for HyperFrames | inferred (not tested here): if `kaggle.py fetch` is blocked, the proxy message names the host |
| `pypi.org`, `files.pythonhosted.org` | `pip install kaggle numpy pillow`, Kokoro packages | QUICKSTART.md, `tts.py` |
| `registry.npmjs.org` | `npx hyperframes@0.9.52` (animations only) | `render_clip.py` |
| `huggingface.co` (and its CDN hosts if blocked, the proxy names them) | Kokoro-82M weights | `tts.py` |
| `download.pytorch.org` | CPU torch wheels for Kokoro | `tts.py` |
| `github.com` | git push/pull, spaCy `en_core_web_sm`, uv python download | `tts.py`, git |
| `objects.githubusercontent.com`, `raw.githubusercontent.com` | release downloads, HyperFrames registry (`hyperframes add`) | `assets/animations/*/hyperframes.json` |
| apt mirrors of the VM image (`archive.ubuntu.com`, `security.ubuntu.com`) | `apt-get install poppler-utils ffmpeg` | `setup-environment.sh` |

The VM never talks to YouTube: downloads happen inside Kaggle kernels (YouTube blocks the VM, lesson `youtube-blocks-vm`). Mark as UNVERIFIED anything in this table that is marked "inferred": the old environment was unrestricted, so the list was derived from the code, not tested.

## 5. Keys: Network secrets vs environment variables

- **Network secrets** (environment settings, where offered): the key is stored for ONE host and the proxy adds it to requests to that host, so the session never holds the value. Where a tool refuses to start without the variable, give the variable a DUMMY value in the expected format and let the proxy replace it. UNVERIFIED for the Kaggle CLI (the old setup never used it): if you try it, run `kaggle.py check` afterwards; if account 1 is not `reachable: yes`, fall back to plain variables.
- **Environment variables**: plain values stored in the environment; simplest, and what the old setup used (`KAGGLE_USERNAME`, `KAGGLE_APITOKEN`, and the OPTIONAL `HF_Token`). Enter them in the environment settings page. Plain text on the environment: keep the environment personal.
- NEVER paste a key in chat, in a file, in a commit, in the setup script or in `.claude/settings.json`. If a session asks you to paste a key, refuse and set it in the environment instead. The scripts mask tokens in every output; agents never read keys (`lessons/rules/agents-never-see-kaggle-key.md`).
- Variables apply from the next session start; a running session keeps the old values.
- Check without printing values: `env | cut -d= -f1 | grep -E 'KAGGLE|HF_'` (names only).

## 6. The response style (`i-have-adhd`)

ONE path: in the NEW claude.ai account open Settings > Profile (personal preferences) and paste the block from [CLAUDE-INSTRUCTIONS.md](CLAUDE-INSTRUCTIONS.md) section 1. `i-have-adhd` was the style's TITLE in the old account (it was also invoked there as `/i-have-adhd`); in the new account the pasted preference simply applies. A Claude Code terminal "output style" is a separate mechanism and optional (the repo carries no output style file; the repo `CLAUDE.md` holds the short form of the style for every session).

## 7. Connectors, plugins and account skills the old account had

Seen in the old account's sessions (2026-11-16). **None is required by the pipeline scripts** (a grep of the repo finds no script that calls a connector); they were used by agents for research or helpers.

| Item | Used for | Needed? | How to re-enable |
|---|---|---|---|
| HyperFrames skills (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `reverse-any-video`, `style-sampling`) | authoring new animation presets and HyperFrames videos; the committed presets in `assets/animations/` render without them | only to author NEW animations | claude.ai > Settings > Capabilities > Skills (they are account-level, synced) or the HeyGen HyperFrames plugin; rendering needs only `npx hyperframes@0.9.52` |
| `yt-*` skills (yt-audit, yt-chapters, yt-comment, yt-edit, yt-package, yt-plan, yt-retention, yt-script, yt-seo, yt-shorts, yt-viral) | titles, SEO, chapters, scripts | optional helpers; a copy also lives in the repo under `.claude/skills/yt-*` and `yt-templates` | nothing to do: the repo copy loads automatically |
| vidIQ connector | titles/SEO/trends; early test as a moment finder (lesson `vidiq`: 9 credits per clip-minute, not good for layout) | optional | claude.ai > Settings > Connectors > vidIQ > connect (needs a vidIQ account) |
| Higgsfield, OpusClip, EverygenAI connectors | early comparison tests (`lessons/tools/higgsfield.md`, `opusclip.md`); archived | no | Connectors page, only if you want to repeat the comparison |
| GitHub connector (`mcp__github__*`) | reading the repo from chat | optional; Claude Code uses git directly | Connectors page |
| Alpha Vantage, Bigdata.com | unrelated to this project | no | skip |

Account-skill rule: a skill in the REPO (`.claude/skills/`) always loads in a session with the repo. The clips and lessons skills are in the repo, so the new account needs no skill upload for the pipeline.

## 8. Permissions, model settings and the autosave hook

**Permissions.** The repo's `.claude/settings.json` allows these Bash patterns with no prompt (and nothing else):
```
Bash(python3 .claude/skills/clips/scripts/download/kaggle.py:*)
Bash(python3 /home/user/VideoGeneration/.claude/skills/clips/scripts/download/kaggle.py:*)
Bash(python3 scripts/download/kaggle.py:*)
```
`preflight.py` prints a WARN `settings-allow` listing 8 more scripts the job runs (long_run, jobs, checkpoint, finalise, journal, retro, edit_clip, add_lesson). Approve them in the session's permission prompt, or ask a human to add them to `permissions.allow`; agents never edit settings (lesson rule).

**Auto-mode classifier.** In auto mode a server-side classifier judges commands. Known limits (incident `agent-blocked-by-classifier`, count 2):
- It may DENY a Kaggle account-2 call, a GPU step or a delete: do not retry the same call; say what was blocked. The LEAD session runs account-2 and GPU steps itself, not a sub-agent.
- Sub-agents inherit stricter limits than the lead.
- It sometimes returns "no verdict (error)": the call did not run. Run it again once as is. After about 10 no-verdict responses in a row the turn stops: just re-run the agent or ask Claude to continue.

**Model, `advisorModel`, auto mode and plan.** What is known (2026-11-16, old account) and what you must check in the NEW account's settings; nothing here is invented:
- **`advisorModel`**: the old VM's `~/.claude/settings.json` held exactly one setting, `advisorModel: opus` (the `advisor` tool: a stronger reviewer that sees the whole conversation; project rule: Opus is only an advisor, see CLAUDE-INSTRUCTIONS.md rule 3). It is a per-user setting, so it does NOT travel with the repo. To get it back, set it in the new account (`/config` in Claude Code, or ask Claude to set `advisorModel` with the `update-config` skill; you approve). If the new account does not offer it, work without an advisor: nothing in the scripts needs it.
- **Which model for a session**: the pipeline scripts do not pick a model. By the project rules, the lead session runs Sonnet (`skill-runs-on-sonnet`); the old account's lead was Fable for planning and validation; ALL execution goes to Sonnet or Haiku sub-agents. Check in the new account which of Fable, Opus, Sonnet and Haiku are selectable; if Fable is missing, use Sonnet as lead and the best available model for the final validation step.
- **Auto mode**: the sessions ran with the platform's auto-mode classifier (limits above). Whether auto mode exists, and what it allows, depends on the new account's plan and settings: check Settings > Claude Code (or the session's permission menu) and, if it is off, expect a permission prompt for each command in the `settings-allow` WARN list.
- **Claude plan**: the old plan is not recorded anywhere in the repo or the logs, so it is UNKNOWN here. Needed: a plan that includes Claude Code cloud sessions with custom environments (check claude.ai/code opens and the Add environment button exists). A clip job with sub-agents is heavy; if you hit usage limits, the lead stops and tells you (rule `limits-retry-then-tell-user`) rather than lowering quality.

**The autosave hook: what is true (checked 2026-11-16).** The script is `.claude/scripts/autosave.sh` (in git). I searched every settings file I can read: the repo's `.claude/settings.json` (only `permissions`), the old VM's `~/.claude/settings.json` (only `advisorModel`) and `~/.claude.json` (no hooks). The only hook seen is the platform's own check (`~/.claude/launcher-settings.json`) that REMINDS you to commit and push when a turn ends; it does NOT call `autosave.sh`. In the old sessions the lead ran `bash .claude/scripts/autosave.sh` by hand when that reminder appeared (and, early on, a background loop every ~10 minutes, lesson `push-to-main-in-intervals`, superseded). `SKILL.md` and older docs say "Stop hook": read that as "run by hand at the Stop reminder". `checkpoint.py` already saves after every render step, so the new account works without a hook.

Exact way to do the same in the new account: when the reminder appears (and about every 10 minutes during a job), run this one line from the repo root, or tell Claude "run autosave":
```
bash .claude/scripts/autosave.sh
```
Optional, to automate it: ask Claude in the new account "add a Stop hook that runs .claude/scripts/autosave.sh" (it uses the `update-config` skill; you approve the change; an agent never edits settings on its own or on another agent's request). Or a HUMAN puts this in the repo's `.claude/settings.json`, merged with the existing `permissions` block, so it travels with git:
```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/scripts/autosave.sh\" 2>&1 | tail -2" } ] }
    ]
  }
}
```
(`$CLAUDE_PROJECT_DIR` makes the path independent of the hook's working directory. UNVERIFIED here: the snippet was not run as a hook; test it by ending a turn and checking `git log -1`.) The script is safe: no force push, skips files over 25 MB, broken `.py` files and key-like files, stops while `.autosave-pause` exists.

## Done when

`VERIFY.md` sections 1-3 are green. Next: [KAGGLE.md](KAGGLE.md).
