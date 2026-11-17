# KAGGLE: accounts, datasets, keys

Back to [README.md](README.md). Time: 10 minutes if you reuse the old Kaggle accounts, about 25 minutes with new ones (phone verification included).

**Key fact: Kaggle datasets and kernels live on the KAGGLE account, not on GitHub and not on Claude.** Moving GitHub and Claude does not touch them. The simplest move keeps the same Kaggle accounts: only the new Claude environment needs their key.

## What Kaggle is used for

Every YouTube download and every Whisper transcript runs in a Kaggle kernel, because YouTube blocks the Claude VM. Kernels are private, CPU for downloads (no quota), GPU (T4) only for Whisper when a video has no captions. Code: `.claude/skills/clips/scripts/download/kaggle.py`. You never run kernels by hand; the skill does.

## Checklist: reuse the same accounts (recommended)

- [ ] 1. kaggle.com > sign in as account 1 > Settings > API > **Create New Token** (new `KGAT_` access-token format). Copy it straight into the Claude environment as `KAGGLE_APITOKEN`; `KAGGLE_USERNAME` = the account 1 user name. Never paste it in chat.
- [ ] 2. Same for account 2 (the second account, default name `sovere`): `KAGGLE_APITOKEN2` and `KAGGLE_USERNAME2`.
- [ ] 3. In the first new session: `python3 .claude/skills/clips/scripts/download/kaggle.py check` shows both accounts `reachable: yes`.
- [ ] 4. Verify the key datasets are PRIVATE (section below), then follow REVOKE-AND-SECURITY.md to rotate keys and delete the vault datasets.

## Checklist: create NEW Kaggle accounts

- [ ] 1. kaggle.com > Register (use an email you control). 3 min.
- [ ] 2. **Phone verification**: profile > Settings > Phone verification > enter a number, type the SMS code. Without it Kaggle gives NO GPU and NO internet inside kernels, and the pipeline cannot download from YouTube. If Kaggle refuses a number for the second account, use a different number. 5 min.
- [ ] 3. Settings > API > **Create New Token** (copy it into the Claude environment, nowhere else).
- [ ] 4. Check quota: the quota is shown in a notebook's accelerator menu on kaggle.com (not checked here). Expect: **30 GPU hours per week per account**, resets weekly.
- [ ] 5. Repeat for the second account if you want the double quota (60 GPU h/week).
- [ ] 6. Set the variables (CLAUDE-ACCOUNT-SETUP.md section 3) and run `kaggle.py check`.
- [ ] 7. Copy the datasets you still need (next section); the old datasets stay on the old accounts.

## Two accounts: how the code decides

- Account 1 is the default (`KAGGLE_USERNAME` + `KAGGLE_APITOKEN`; `KAGGLE_API_TOKEN` and `~/.kaggle/kaggle.json` also work). All CPU jobs (downloads, prepare) stay on account 1.
- Account 2 (`KAGGLE_USERNAME2`, default name `sovere`, hard-coded as `ACCOUNT2_USER` in `kaggle.py`; `KAGGLE_APITOKEN2`) takes over a GPU job when the kernel stays **QUEUED for more than 20 minutes** or the push/run hits a **quota error**. `long_run.py` does it for the whole windows+whisper chain; `kaggle.py push` does it when it has no `--kernel-source` and no dataset of account 1.
- A chain must stay on ONE account (a kernel cannot read another account's private kernel). `--account 1|2` (or env `KAGGLE_ACCOUNT=2`) forces an account. `wait`, `status`, `fetch` remember the account per kernel NAME in `~/.cache/clips/kaggle_accounts.json` (no secret in it).
- Agents never see a key. Any Kaggle CLI call for either account goes through `python3 .claude/skills/clips/scripts/download/kaggle.py [--account 2] raw <kaggle args>`; the token only travels in the child process environment and the output is masked. `raw datasets download` is refused for anything except `<active user>/clips-masters-*` and `clips-sources-*`.

## Datasets in the old accounts (private)

| Dataset (account 1 unless noted) | Holds | Read by the code? | Needed after the move? |
|---|---|---|---|
| `gemini-key` | a Gemini API key as a text file | only `run.py --gemini-key-file` if you ask for it | no: a plaintext key vault, optional transfer copy; use `GEMINI_API_KEY` env and delete the dataset |
| `streamer-face`, `streamer-face-f` | face/reference images of the fictional streamer | old tests only | no, the facecam library is in git (`assets/facecam/`) |
| `vlog-1vzlt3-src` | an old source video | old test only | no |
| `kagglegpu1` (NEW) | plaintext lines `HF_Token=...`, `KAGGLE_APITOKEN=...`, `KAGGLE_USERNAME=...` of account 1 (a key vault) | **no, nothing in the repo reads it** | no: optional transfer copy, delete after the keys are in the new environment |
| `kagglegpu2` | account 2's API key as a PDF (`kagglegpu2.pdf`) | **yes**: `kaggle.py` `_token_from_dataset()` reads it (in memory only, with `pdftotext`) when `KAGGLE_APITOKEN2` is not set | no, if you set `KAGGLE_USERNAME2` + `KAGGLE_APITOKEN2` |
| `clips-masters-<stream>` | the 60 fps upload masters of one stream (~100 MB each) | `SKILL.md` step 7/8, `kaggle.py raw` | only if you still want those masters |
| `clips-sources-<stream>` | optional backup of source windows (`backup_sources.py`) | `backup_sources.py restore` | only on request |

(I checked the code: `kaggle.py` reads ONLY `kagglegpu2`; `kagglegpu1` is documented here because it exists, not because a script uses it.)

### Honest security note about the key datasets

`kagglegpu1`, `kagglegpu2` (and `gemini-key`, which holds a Gemini key) are **plaintext key vaults** stored as Kaggle datasets: an optional transfer copy, to delete after the keys are in the new environment. A missing vault dataset is fine (`verify_manifest.py --kaggle` and the carry-over check do not FAIL on it); `streamer-face`, `streamer-face-f` and `vlog-1vzlt3-src` are normal datasets to keep. They are only as safe as their visibility:
1. **The user must check that BOTH are Private**: kaggle.com > Datasets (or `kaggle.com/<user>/datasets`) > open the dataset > Settings (gear) > Sharing > must say **Private**. A public key dataset leaks the keys to the world. (Visibility is not shown by the CLI list; use the web page.)
2. **Chicken and egg:** to read `kagglegpu1` or `kagglegpu2` at all, the new environment needs account 1's `KAGGLE_USERNAME` + `KAGGLE_APITOKEN` as environment variables. So the vault cannot bootstrap anything; it is only a transfer/backup copy.
3. **Recommendation:** put every key straight into the new environment (variables or Network secrets), then **delete both datasets** and **rotate the keys** (REVOKE-AND-SECURITY.md). The account-2 key was displayed once in an old session's tool output when its PDF was read, so ROTATE it regardless.
4. Do not copy these two datasets to the new Kaggle account. Create fresh tokens instead.

## What breaks if the Kaggle username changes

`kaggle.py` builds every owner name from `KAGGLE_USERNAME` (account 1) and `KAGGLE_USERNAME2` (account 2, default `sovere`):
- kernel ids `<user>/<NAME>` (so old kernels and their outputs are not visible: just start new jobs),
- dataset names `<user>/clips-masters-<stream>` (old masters are under the OLD user; `raw datasets download` accepts only the ACTIVE user's `clips-masters-*`, so the old masters cannot be fetched with the new account: copy them, below),
- `kagglegpu2` is looked up in `<account 1 user>/kagglegpu2`: a NEW account 1 does not have it. Fix: set `KAGGLE_USERNAME2` + `KAGGLE_APITOKEN2` in the environment (then the dataset is never touched),
- the hard-coded default `sovere` only applies when `KAGGLE_USERNAME2` is unset.
Old docs and archived runs mention the old user name in example commands: they are history, not config.

## How to copy a dataset to another account

Only masters and source backups are worth copying. Run these in YOUR terminal logged in as the right account (do not hand a key to a chat or an agent):

```
# 1. download from the OLD account (uses the old token in env, KAGGLE_USERNAME / KAGGLE_APITOKEN)
kaggle datasets download OLD_USER/clips-masters-<stream> -p ./copy --unzip

# 2. create the folder metadata for the NEW account
kaggle datasets init -p ./copy
#    edit ./copy/dataset-metadata.json: "id": "NEW_USER/clips-masters-<stream>", "title": "clips-masters-<stream>", licenses other

# 3. upload as a PRIVATE dataset (create makes it private unless you add --public)
kaggle datasets create -p ./copy
# later versions:  kaggle datasets version -p ./copy -m "update"
```
(`kaggle datasets download --help`, `datasets create --help` and `datasets init --help` were checked with CLI 2.2.5.) Then check Sharing = Private in the web page. The same recipe is written in `SKILL.md` (masters upload, the `clips-masters-<stream>` block).

## Weekly routine

- GPU is needed only for videos WITHOUT captions (Whisper). Most jobs use no GPU hours at all.
- If a job says `LIMIT REACHED` / `QUOTA`: wait for the weekly reset or run with `--account 2`.
- `kaggle.py check` any time: it prints user names and reachability, never a token.
