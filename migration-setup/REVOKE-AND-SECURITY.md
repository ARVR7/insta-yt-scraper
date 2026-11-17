# REVOKE-AND-SECURITY: clean up the old accounts

Back to [README.md](README.md). Do this ONLY after [VERIFY.md](VERIFY.md) is all green on the new accounts. Time: about 15-20 minutes. No key value is written in this file.

## Checklist (in this order)

- [ ] 1. **Create the new Kaggle tokens FIRST** and put them in the new Claude environment (CLAUDE-ACCOUNT-SETUP.md section 3). Confirm `kaggle.py check` is `reachable: yes` for both accounts. Reason: step 2 kills the old tokens.
- [ ] 2. **Rotate and revoke every Kaggle token that was ever pasted anywhere** (kaggle.com > Settings > API > the token list > **Expire/Revoke** the old tokens, then Create New Token if needed). That means:
  - account 1's old token (it lived in the old environment and in the dataset `kagglegpu1`),
  - **account 2's key: it was displayed ONCE in the old session's tool output when its PDF (`kagglegpu2.pdf`) was read. ROTATE it unconditionally**,
  - any token you ever typed into a chat or a file.
- [ ] 3. **Hugging Face**: huggingface.co > Settings > Access Tokens > revoke the old `HF_Token` (it was also in `kagglegpu1`); create a new one for the new environment if you want it.
- [ ] 4. **Gemini key** (if one was made): aistudio.google.com > revoke it; the dataset `gemini-key` held it.
- [ ] 5. **Delete the key-vault datasets** on Kaggle after the keys are moved: `kagglegpu1` and `kagglegpu2` (kaggle.com > Datasets > the dataset > Settings > Delete). Also `gemini-key`. Verify no other dataset holds a key. Old test datasets `streamer-face`, `streamer-face-f`, `vlog-1vzlt3-src` can go too (they are not needed). Keep `clips-masters-*` only if you want those masters (KAGGLE.md).
- [ ] 6. **Remove the OLD Claude environment** (claude.ai/code > the old account > environment `Full access` > delete). Its variables disappear with it. Delete old sessions you no longer need.
- [ ] 7. **Uninstall the old GitHub App**: old GitHub account > Settings > Applications > Installed GitHub Apps > Claude > Uninstall (or "Configure" and remove the repo). Revoke authorised OAuth apps you no longer use (Settings > Applications > Authorized OAuth Apps).
- [ ] 8. **Old repo `ARVR7/VideoGeneration`**: either keep it **private** and archive it (Settings > General > Danger Zone > Archive this repository: read-only), or delete it (Danger Zone > Delete). **If the new repo is a FORK (option C), do NOT delete the old repo and do NOT remove the collaborator: GitHub deletes private forks then; re-create the new repo with a mirror first (GITHUB-MOVE.md, option A).** Never make it public. Remove the new account from its collaborators if you added it for copying (GITHUB-MOVE.md, path 2).
- [ ] 9. **Delete temporary personal access tokens** you made for the move (github.com > Settings > Developer settings > Personal access tokens > Delete) and the scratch folder `OLD.git` (it holds the full repo).
- [ ] 10. **Local files**: delete any `~/.kaggle/kaggle.json` on computers that no longer need access.
- [ ] 11. Run `git grep -lE "KGAT_[0-9A-Za-z]{16,}"` in the new repo: no output.

## Security notes

1. **The repo is PRIVATE and stays private.** It contains AI-generated reference images, clips cut from other people's streams, the pipeline settings and the names of key datasets. If it ever became public by mistake: make it private at once, assume every old commit was copied, and rotate every key.
2. **Never paste a key in chat.** Not in Claude, not in GitHub issues, not in a commit message. Keys live only in the Claude environment (variables or Network secrets) and in your password manager. If a session asks for a key in chat, refuse.
3. **The scripts mask tokens.** `kaggle.py` hides every token (known values and anything starting with the `KGAT_` prefix) in all output, passes the token only in the child process environment, and `kaggle.py raw` refuses to download the key dataset or any dataset that is not `<you>/clips-masters-*` or `clips-sources-*`.
4. **Agents never read keys.** Lessons `agents-never-see-kaggle-key` and `keys-never-in-chat`: no agent opens a key file, prints an environment variable value, or reads a PDF/dataset that holds a key. List names only: `env | cut -d= -f1`.
5. **The repo scans itself.** `autosave.sh`, `checkpoint.py` and `finalise.py` skip or refuse files that look like a key (token prefix, API key shapes, private keys) and any file over the size limit.
6. **The key vault datasets are plaintext.** They were a convenience; they are the weakest link (KAGGLE.md). Delete them after the move.
7. **Network**: an unrestricted environment can reach any host. If you do not need that, use the Limited host list in CLAUDE-ACCOUNT-SETUP.md.
8. **Rights**: clips from streams can carry copyright claims; the repo keeps `rights` in each `stream.json` and a warning in each `post.md`. Posting is your decision (lessons `youtube-reused-content-needs-commentary`, `rockstar-policy-non-commercial`).
9. **Two-factor authentication** on GitHub, Claude, Kaggle and Hugging Face accounts.

## After cleaning, you should see

- `kaggle.py check` works with the NEW tokens only; the old tokens return an authentication error (that is the proof they are revoked).
- The old repo is archived/deleted, the old App uninstalled, the old environment gone.
- No `kagglegpu1`, `kagglegpu2` or `gemini-key` dataset on any Kaggle account.

- The `history/` files (export of the whole session: your messages, the dialogue, agent briefs) were redacted automatically (tokens, keys, emails) but must be skimmed once by a person before the repo is ever made public, and the repo must stay private.
