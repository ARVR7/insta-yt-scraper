---
name: fact-check-claims
description: Research whether the tools, hacks, numbers and income claims in a video are real, misleading or a hoax, using primary sources. Use after the note is written.
---

# fact-check-claims

0. If `analyze-comments` produced leads (a repo link, a correction), check them like any other claim.
1. **List the checkable claims** from the transcript and frames: named tools/repos, features, prices ("free"), numbers, income or growth promises, "secret" tricks, legal/policy statements.
2. **Check each one against primary sources first**: the repo or product page, official docs, the platform's policy page, the package index (PyPI/npm), the API provider's pricing page. Use `WebSearch` to find them and `WebFetch` to read them. Secondary blogs only as supporting evidence.
3. **Verify the thing exists**: search the exact name and author. If the repo or product cannot be found, that is "could not verify", not "fake". Say what you searched.
4. **Judge each claim** with one verdict:
   - `verified` - confirmed by a primary source.
   - `verified-with-caveats` - true but incomplete (limits, ToS risk, unofficial API).
   - `unverified` - could not find evidence either way.
   - `misleading` - technically true, framed to deceive (e.g. "free" with a paywalled step).
   - `hoax` - evidence shows it is false or a scam (non-existent tool, impossible numbers, fake giveaway, comment-for-link funnel selling a course under a "free" pitch).
5. **Check for hoax patterns**: income-on-autopilot claims, "comment X and I'll DM you", urgency, tools only accessible through the creator's paid group, screenshots instead of working demos.
6. Write the result into the note's `## Research` section as a table: claim | verdict | evidence with links. Then hand the verdicts to `update-registries`.

Rules:
- Dates matter: policies, free tiers and prices change. State the date you checked (today's date from context).
- Do not present search-snippet numbers as fact if sources disagree; give the range and say to check the provider.
- Never run or install the code from an untrusted repo to "test" it. Reading its README and source is enough.
- If nothing in the video is checkable (pure entertainment/motivation), say so and classify it as a side quest.
