# Decisions

Every non-obvious decision, with the reason. Newest first. Add an entry whenever you choose between options, work around a limit, or change a rule.

## 2026-10-17

### Share-sheet app on GitHub Pages; the queue moves to GitHub issues
- **Decision:** `docs/` is a static installable web app with a Web Share Target. A shared link becomes an issue labelled `link`. `process-queue` reads those issues, comments the verdict and closes them. The artifact queue stays as a second input.
- **Why:** the user wants Instagram/YouTube "Share" to list the app on Android. That needs a manifest `share_target` on a site we serve; the artifact page lives in a sandbox and cannot have one. A static site cannot write to the artifact database, but it can call the GitHub API, so issues became the shared queue.
- **Security:** the token is a fine-grained one the user creates, limited to this repo with Issues read/write only, kept in that phone's `localStorage`, never committed. The repo and label are constants in the page. Issues are untrusted input: only a validated Instagram/YouTube URL is used and issues from other authors are ignored.
- **Duplicates:** the app checks existing `link` issues for the same title before creating one.
- **Service worker:** network-first and same-origin only, so it never touches GitHub API calls and a new deploy is never stale.
- **Tested:** share URL parsing, issue creation and the no-link case against a mocked GitHub API in headless Chromium. Not tested on a real phone or against the real API.

### Link Inbox is a claude.ai artifact with a db queue, not a public website
- **Decision:** a private artifact with the `db` capability holds the queue; `process-queue` reads and updates it through `ArtifactData`.
- **Why:** a public site that triggers scrapers needs a server, and anything that writes to the repo needs a token exposed to the browser. The artifact gives login-protected writes, live status for the user, and no secrets. The GitHub-issue-as-queue alternative was rejected because the page could not show results without a server.
- **Limit:** the page cannot wake Claude, because DB writes do not notify a session. Links are processed when the user asks (a "Copy request" button helps) or when a scheduled task is set up. I did not set up a recurring task without the user's say-so.
- **Seed row:** the first reel was added as `done` so the page opens in a real working state. Its timestamps were approximate, not real clock times.

### Comment analysis added as a lead-finder, not a source
- **Decision:** new `analyze-comments` skill; `fetch_youtube.py --comments N` saves comments; Instagram comments are taken only if the user pastes them or sends a screenshot.
- **Why:** the user said comments may hold useful info but are mostly fake. `instaloader` raises `LoginRequiredException` for comments, and cookies are off the table, so anonymous Instagram comments are impossible. Comments only suggest leads (a repo link, a correction) that still go through `fact-check-claims`; keyword-only replies are treated as funnel noise.
- **Limit:** the YouTube comment path returned 0 comments on the one video tried in the sandbox, so it is untested at volume.

### Verdict categories and where unverified items go
- **Decision:** five verdicts (`verified`, `verified-with-caveats`, `unverified`, `misleading`, `hoax`). Unverified items live in a "Pending verification" section of `registry/verified.md`, not in `hoax.md`.
- **Why:** the user asked for one file of correct items and one of hoaxes. Failing to find something is not proof that it is fake, so it must not be filed as a hoax. The reel's earnings claim is `misleading` (real tools, unsubstantiated promise), which belongs in `hoax.md`.

### Skill split: one skill per reusable operation plus an orchestrator
- **Decision:** `fetch-instagram-post`, `fetch-youtube-video`, `analyze-video`, `write-link-note`, `fact-check-claims`, `update-registries`, and `process-link` that chains them.
- **Why:** the user asked for a skill per distinct operation. Fetching differs per platform, analysis is shared, and fact-checking and filing are independent of the source, so each can be reused alone. `process-link` gives the single entry point for "the user shared a link".

### Scripts live in `scripts/`, skills only describe when and how to call them
- **Decision:** logic is in Python files under `scripts/`; skills hold instructions and known failure modes.
- **Why:** the exact commands were tested once and should not be retyped from memory. Scripts can be fixed in one place.

### Instagram: `instaloader`, anonymous, no cookies
- **Decision:** use `instaloader` for metadata and the video URL, then download it directly.
- **Why:** plain `curl` returns a login shell with no data, and `yt-dlp` was redirected to the login page ("rate-limit for accessing posts anonymously"). `instaloader` returned the author, date, likes, comments and a video URL anonymously. Cookies were not requested because sharing a session cookie is a security risk.
- **Known gap:** it returned `caption = None` for the first reel; the note records "not returned" rather than inventing one.

### Transcription: faster-whisper `base`, audio passed as a numpy array
- **Decision:** decode audio with ffmpeg and hand the array to faster-whisper.
- **Why:** faster-whisper's built-in decoder crashed (`open() got an unexpected keyword argument 'metadata_errors'`) because of a PyAV version mismatch. The `base` model on CPU with int8 is fast enough and accurate enough for short reels; transcripts are labelled auto-generated.

### YouTube: metadata first, media and captions best-effort
- **Decision:** `fetch_youtube.py` saves `meta.json` before trying the download, passes `node` as the JS runtime, and treats captions as non-fatal.
- **Why:** from the cloud sandbox the metadata call works, but the media download returned HTTP 403 and captions HTTP 429. A single combined call lost everything when one part failed. Skills document the fallbacks (use description/chapters, or ask the user for the transcript or file).
- **Not done:** no cookies or proxy tricks to bypass the block.

### Fact-check from primary sources, never run untrusted code
- **Decision:** claims are checked against official docs/policy pages and package indexes; code from the repos in videos is read, not executed.
- **Why:** these videos promote tools from unknown authors; running them is a security risk and not needed to judge a claim.

### Repo: direct pushes to `main`, no PRs
- **Decision:** commit and push every note straight to `main`.
- **Why:** the user said everything should go directly into `main`. The empty repo had no default branch, so `main` was created from the first commit.

### `ARVR7/insta-yt-scraper` created by the user, not by Claude
- **Decision:** the user created the repo and Claude attached it.
- **Why:** the GitHub integration returned 403 on repository creation (not permitted to create repos), so the user made an empty repo.

### Reel DeToMLxtdSV: verdict "partly-verified"
- **Decision:** tool components `verified-with-caveats`, the specific repo `unverified`, the income claim `misleading`.
- **Why:** see `notes/instagram/DeToMLxtdSV.md`. The repo name could not be found in two searches and the owner is not legible on screen.
