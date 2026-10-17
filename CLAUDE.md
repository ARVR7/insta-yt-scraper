# insta-yt-scraper

When the user shares an instagram.com or youtube.com / youtu.be link, use the `process-link` skill (`.claude/skills/process-link/SKILL.md`) and follow it to the end: fetch, analyze, note, fact-check, registries, docs, push.

- Work on `main` and push directly; the user asked for no branches or PRs.
- Keep downloaded media out of the repo; use the scratchpad.
- Log non-obvious choices in `decision.md` and structural changes in `flow.md`.
- Never claim something is fake just because it could not be found; use "unverified".
- Do not ask for or use the user's Instagram/YouTube cookies.

- Links can also arrive through the Link Inbox artifact (https://claude.ai/artifact/FLi1JREBRUV493gipCS5AG). When the user says to process the queue, use the `process-queue` skill.
- Categories come only from `taxonomy.yml` (see the `categorize-link` skill). Never add free-form tags; extend the taxonomy instead and log it in `decision.md`.
