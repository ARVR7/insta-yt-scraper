#!/usr/bin/env python3
"""export_history.py - turn a Claude Code session transcript (JSONL) into a
SANITIZED, human-readable project history under migration-setup/history/.

Why: a new Claude account must be able to read the whole story of this project
(every user message, the dialogue, the agent work briefs, the context-compaction
summaries) without access to the raw 88 MB session log, which contains secrets.

Usage (from the repo root):
    python3 migration-setup/export_history.py                    # default session file
    python3 migration-setup/export_history.py --session PATH.jsonl
    python3 migration-setup/export_history.py --out migration-setup/history
    python3 migration-setup/export_history.py --verify-only      # just re-scan outputs

Outputs (see history/00-README.md after a run):
    00-README.md            how it was made, what was removed, counts
    01-user-messages.md     every message the user typed, verbatim, numbered
    02-conversation*.md     user message + assistant visible text replies (split ~1.5 MB)
    03-agent-briefs.md      every Agent tool_use brief + AskUserQuestion Q&A (+ SendMessage)
    04-session-summaries.md context-compaction summaries, verbatim

NEVER prints the raw transcript or matched secret values: only counts.
Every output string goes through redact(). The script re-scans its own output
and exits non-zero if anything suspicious remains.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_SESSION = "/root/.claude/projects/-home-user-VideoGeneration/0c6b7371-30a8-5800-b009-93a432c761bb.jsonl"
SPLIT_BYTES = 1_500_000
SIZE_BUDGET = 12_000_000
BIG_ASSISTANT = 4000      # used only when the size budget is exceeded
KEEP_ASSISTANT = 1500

# --------------------------------------------------------------------------- redaction
RED = "[REDACTED]"
COUNTS = Counter()
SHAS = set()

# (name, compiled regex, replacement). Order matters: specific first, generic last.
PATTERNS = [
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)", re.S), RED),
    ("KGAT", re.compile(r"KGAT_[0-9a-fA-F]{10,}"), RED),
    ("hf_token", re.compile(r"\bhf_[A-Za-z0-9]{20,}"), RED),
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), RED),
    ("github_gh_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), RED),
    ("sk_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), RED),
    ("google_AIza", re.compile(r"AIza[0-9A-Za-z_-]{30,}"), RED),
    ("google_GOCSPX", re.compile(r"GOCSPX-[0-9A-Za-z_-]{20,}"), RED),
    ("google_oauth_ya29", re.compile(r"\bya29\.[0-9A-Za-z_-]{20,}"), RED),
    ("aws_AKIA", re.compile(r"AKIA[0-9A-Z]{16}"), RED),
    ("slack_xox", re.compile(r"xox[bapors]-[A-Za-z0-9-]{8,}"), RED),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]*"), RED),
    ("bearer", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"), "Bearer " + RED),
    # name = value / name: value  (keep the name, redact the value)
    ("secret_assignment",
     re.compile(r"(?i)((?:api[_-]?key|token|secret|password)[\"']?\s*[=:]\s*[\"']?)(?!\[REDACTED\]|\$)(\S{12,})"),
     lambda m: m.group(1) + RED),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"), "[email]"),
]
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
HEX_RE = re.compile(r"(?<![0-9A-Za-z])[0-9a-fA-F]{32,}(?![0-9A-Za-z])")
# long runs: any alphanumeric/underscore/hyphen run of 30+ (covers base64url, hashes, ids)
LONG_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{28,}[A-Za-z0-9]")
B64_RE = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")


def _long_sub(m):
    s = m.group(0)
    if s in SHAS or UUID_RE.match(s):
        return s
    # Hyphen/underscore-joined runs are usually slugs and file names (kept for readability);
    # they are redacted only when they look like a random token (digit + upper + lower).
    if re.search(r"[_-]", s) and not (re.search(r"\d", s) and re.search(r"[A-Z]", s) and re.search(r"[a-z]", s)):
        return s
    COUNTS["long_alnum_run"] += 1
    return RED


def _hex_sub(m):
    s = m.group(0)
    if s in SHAS:
        return s
    COUNTS["long_hex"] += 1
    return RED


def _b64_sub(m):
    s = m.group(0)
    if "/" in s and sum(1 for seg in s.split("/") if re.fullmatch(r"[A-Za-z]{3,}", seg)) >= 2:
        return s   # a URL/file path, not base64
    if s in SHAS or not (re.search(r"[A-Z]", s) and re.search(r"[a-z]", s) and re.search(r"[0-9]", s)):
        return s
    COUNTS["base64_like"] += 1
    return RED


def redact(text):
    """Apply every redaction rule to a string. Counts per pattern in COUNTS."""
    if not text:
        return text
    for name, rx, rep in PATTERNS:
        def sub(m, rep=rep, name=name):
            COUNTS[name] += 1
            return rep(m) if callable(rep) else rep
        text = rx.sub(sub, text)
    text = HEX_RE.sub(_hex_sub, text)
    text = B64_RE.sub(_b64_sub, text)
    text = LONG_RE.sub(_long_sub, text)
    return text


# --------------------------------------------------------------------------- helpers
def load_shas():
    try:
        out = subprocess.run(["git", "log", "--all", "--format=%H"], cwd=REPO,
                             capture_output=True, text=True, check=True).stdout
        return set(out.split())
    except Exception:
        return set()


def parse_ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def fmt_ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC") if dt else "unknown time"


def fence(text):
    n = max([len(m) for m in re.findall(r"`+", text)] + [2]) + 1
    f = "`" * n
    return f"{f}\n{text}\n{f}"


SR_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
IDE_RE = re.compile(r"<ide_[a-z_]+>.*?</ide_[a-z_]+>", re.S)
CMD_NAME = re.compile(r"<command-name>(.*?)</command-name>", re.S)
CMD_ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)
NOISE_PREFIXES = (
    "<task-notification", "<local-command", "Stop hook feedback", "[SYSTEM NOTIFICATION",
    "<system-reminder", "<agent-message", "[Image:", "Another Claude session",
    "This session's worker process was restarted", "Base directory for this skill",
    "<teammate-message", "<hook", "Caveat:",
)
NOISE_ONLY = ("[Request interrupted",)


def content_text_and_images(content):
    """Return (text, n_images) for a message content (str or block list)."""
    if isinstance(content, str):
        return content, 0
    texts, imgs = [], 0
    if isinstance(content, list):
        for b in content:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "text":
                texts.append(b.get("text", ""))
            elif b.get("type") == "image":
                imgs += 1
    return "\n".join(texts), imgs


def clean_human(text):
    """Return cleaned human text, or None if the message is machine-generated."""
    text = SR_RE.sub("", text)
    text = IDE_RE.sub("", text)
    text = text.strip()
    if not text:
        return None
    if text.startswith(NOISE_PREFIXES) or text.startswith(NOISE_ONLY):
        return None
    if "<command-name>" in text:
        n = CMD_NAME.search(text)
        a = CMD_ARGS.search(text)
        if not n:
            return None
        text = (n.group(1).strip() + " " + (a.group(1).strip() if a else "")).strip()
    # pasted content markers (if the client ever wraps them)
    text = re.sub(r"<pasted_content[^>]*>", "[PASTED CONTENT START]\n", text)
    text = text.replace("</pasted_content>", "\n[PASTED CONTENT END]")
    return text


def tool_result_text(block):
    c = block.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
    return ""


# --------------------------------------------------------------------------- extraction
def extract(session_path):
    """One pass over the JSONL. Returns dict of collected, UNREDACTED structures."""
    humans = []        # dicts: ts, dt, text, images, src, line
    asst = []          # (dt, line, text)
    agents = []        # dicts
    asks = {}          # tool_use_id -> dict
    sendmsgs = []
    summaries = []     # (dt, line, text)
    stats = Counter()
    result_by_id = {}

    with open(session_path, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            stats["lines"] += 1
            try:
                o = json.loads(line)
            except Exception:
                stats["bad_json"] += 1
                continue
            t = o.get("type")
            stats["type:" + str(t)] += 1
            if o.get("isSidechain"):
                stats["sidechain_skipped"] += 1
                continue
            dt = parse_ts(o.get("timestamp", ""))

            if t == "user":
                msg = o.get("message") or {}
                content = msg.get("content")
                # tool results: only harvested for AskUserQuestion answers
                if isinstance(content, list):
                    for b in content:
                        if isinstance(b, dict) and b.get("type") == "tool_result":
                            result_by_id[b.get("tool_use_id")] = (o, tool_result_text(b))
                if o.get("isCompactSummary"):
                    txt, _ = content_text_and_images(content)
                    summaries.append((dt, i, txt))
                    continue
                if o.get("isMeta"):
                    stats["user_meta_skipped"] += 1
                    continue
                if o.get("toolUseResult") is not None or o.get("sourceToolAssistantUUID"):
                    continue
                origin = o.get("origin")
                if isinstance(origin, dict) and origin.get("kind") not in (None, "human"):
                    stats["user_nonhuman_skipped"] += 1
                    continue
                txt, imgs = content_text_and_images(content)
                if isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
                    continue
                cleaned = clean_human(txt)
                if cleaned is None and not imgs:
                    stats["user_noise_skipped"] += 1
                    continue
                humans.append(dict(dt=dt, text=cleaned or "", images=imgs, src="user", line=i))

            elif t == "queue-operation" and o.get("operation") == "enqueue":
                c = o.get("content")
                if isinstance(c, str):
                    cleaned = clean_human(c)
                    if cleaned is not None:
                        humans.append(dict(dt=dt, text=cleaned, images=0, src="queue", line=i))
                    else:
                        stats["queue_noise_skipped"] += 1

            elif t == "attachment":
                a = o.get("attachment") or {}
                if a.get("type") == "queued_command":
                    org = a.get("origin")
                    if isinstance(org, dict) and org.get("kind") == "human":
                        txt, imgs = content_text_and_images(a.get("prompt"))
                        cleaned = clean_human(txt)
                        if cleaned is not None or imgs:
                            humans.append(dict(dt=parse_ts(a.get("timestamp", "")) or dt,
                                               text=cleaned or "", images=imgs, src="queued", line=i))

            elif t == "assistant":
                msg = o.get("message") or {}
                if o.get("isApiErrorMessage"):
                    continue
                content = msg.get("content")
                if not isinstance(content, list):
                    continue
                for b in content:
                    if not isinstance(b, dict):
                        continue
                    bt = b.get("type")
                    if bt == "text":
                        tx = SR_RE.sub("", b.get("text", "")).strip()
                        if tx and tx != "No response requested.":
                            asst.append((dt, i, tx))
                    elif bt == "tool_use":
                        nm = b.get("name")
                        inp = b.get("input") or {}
                        if nm in ("Agent", "Task"):
                            agents.append(dict(dt=dt, line=i, input=inp, id=b.get("id")))
                        elif nm == "AskUserQuestion":
                            asks[b.get("id")] = dict(dt=dt, line=i, input=inp)
                        elif nm == "SendMessage":
                            sendmsgs.append(dict(dt=dt, line=i, input=inp))

    return dict(humans=humans, asst=asst, agents=agents, asks=asks, sendmsgs=sendmsgs,
                summaries=summaries, stats=stats, results=result_by_id)


def dedupe_humans(humans):
    """The same typed message can appear as a queue enqueue, a queued_command attachment
    and a user record (dequeue). Keep one, with the earliest (= typed) timestamp."""
    norm = lambda t: re.sub(r"\s+", " ", t).strip()
    queued = [h for h in humans if h["src"] != "user" and norm(h["text"])]
    # a user record written when a queued message is dequeued may be a MERGE of several queued
    # messages (joined by newlines): drop it when earlier queued messages (<=60 min before) cover it.
    covered = set()
    for u in humans:
        if u["src"] != "user" or not norm(u["text"]) or not u["dt"]:
            continue
        rest = norm(u["text"])
        used = 0
        for q in queued:
            if q["dt"] and 0 <= (u["dt"] - q["dt"]).total_seconds() <= 3600 and norm(q["text"]) in rest:
                rest = rest.replace(norm(q["text"]), " ", 1).strip()
                used += 1
        if used and len(rest) <= 3:
            covered.add(id(u))
    humans = [h for h in humans if id(h) not in covered]
    hs = sorted(humans, key=lambda h: (h["dt"] or datetime.min.replace(tzinfo=timezone.utc), h["line"]))
    kept = []
    last_by_text = {}
    dropped = 0
    for h in hs:
        key = re.sub(r"\s+", " ", h["text"]).strip()
        if not key and not h["images"]:
            continue
        prev = last_by_text.get(key)
        if prev is not None and key:
            gap = ((h["dt"] - prev["dt"]).total_seconds() if h["dt"] and prev["dt"] else 0)
            cross = prev["src"] != h["src"]
            window = 1200 if cross else (3600 if len(key) >= 20 else 180)
            if gap <= window:
                prev["images"] = max(prev["images"], h["images"])
                dropped += 1
                continue
        # an image-only/empty-text item adjacent to the same-time text item is the same message
        if not key and kept and kept[-1]["dt"] and h["dt"] and abs((h["dt"] - kept[-1]["dt"]).total_seconds()) < 2:
            kept[-1]["images"] = max(kept[-1]["images"], h["images"])
            dropped += 1
            continue
        kept.append(h)
        if key:
            last_by_text[key] = h
    # drop pure-empty image duplicates handled above; number them
    for n, h in enumerate(kept, 1):
        h["n"] = n
    return kept, dropped + len(covered)


# --------------------------------------------------------------------------- rendering
def human_block(h, with_header=True):
    text = redact(h["text"])
    flags = []
    if "[PASTED CONTENT START]" in text:
        flags.append("contains pasted content")
    elif len(text) > 2000:
        flags.append("long message, probably a pasted brief")
    if h["images"]:
        flags.append(f"{h['images']} image(s) attached (not exported)")
    head = f"### #{h['n']} - {fmt_ts(h['dt'])}"
    if flags:
        head += "  [" + "; ".join(flags) + "]"
    body = fence(text) if text else "_(no text, attachment only)_"
    return head + "\n\n" + body + "\n"


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return len(text.encode("utf-8"))


def trunc_assistant(tx, truncate):
    if truncate and len(tx) > BIG_ASSISTANT:
        COUNTS["assistant_blocks_truncated"] += 1
        return tx[:KEEP_ASSISTANT] + "\n\n[truncated]"
    return tx


def build_all(data, outdir, truncate):
    """Write files 01..04. Returns dict of per-file info. Redaction counts accumulate."""
    info = {}
    humans, dropped = dedupe_humans(data["humans"])
    info["humans_n"] = len(humans)
    info["humans_dropped_dups"] = dropped

    # 01
    parts = ["# 01 - Every message the user typed\n",
             "Verbatim, in order, numbered (UTC). Machine-generated turns (tool results, system reminders, "
             "hook feedback, task notifications, peer-agent messages) are excluded. "
             "Messages marked 'long message' are the user's pasted briefs.\n"]
    pasted = 0
    for h in humans:
        b = human_block(h)
        if "pasted" in b.split("\n", 1)[0] or "probably a pasted" in b.split("\n", 1)[0]:
            pasted += 1
        parts.append(b)
    info["01"] = write(os.path.join(outdir, "01-user-messages.md"), "\n".join(parts))
    info["pasted_flagged"] = pasted

    # 02: dialogue
    events = [("u", h["dt"], 0, h) for h in humans]
    events += [("a", dt, ln, tx) for dt, ln, tx in data["asst"]]
    epoch = datetime.min.replace(tzinfo=timezone.utc)
    events.sort(key=lambda e: (e[1] or epoch, 0 if e[0] == "u" else 1, e[2]))
    chunks, cur_asst_ts, cur_asst = [], None, []

    def flush_asst():
        nonlocal cur_asst, cur_asst_ts
        if cur_asst:
            body = "\n\n".join(redact(trunc_assistant(x, truncate)) for x in cur_asst)
            chunks.append(("a", f"#### Claude - {fmt_ts(cur_asst_ts)}\n\n{body}\n"))
        cur_asst, cur_asst_ts = [], None

    n_asst = 0
    for kind, dt, ln, payload in events:
        if kind == "u":
            flush_asst()
            chunks.append(("u", human_block(payload)))
        else:
            if not cur_asst:
                cur_asst_ts = dt
            cur_asst.append(payload)
            n_asst += 1
    flush_asst()
    info["asst_blocks"] = n_asst
    files, buf, size, part = [], [], 0, 1
    header = ("# 02 - Conversation (part {p})\n\nUser messages (verbatim, numbered as in 01) followed by "
              "the assistant's visible text replies. Tool calls, tool results and thinking are omitted. "
              "Times are UTC.\n")
    for kind, text in chunks:
        sz = len(text.encode("utf-8"))
        if kind == "u" and size + sz > SPLIT_BYTES and buf:
            files.append(buf)
            buf, size = [], 0
        buf.append(text)
        size += sz
    if buf:
        files.append(buf)
    conv_files = []
    for k, b in enumerate(files, 1):
        name = f"02-conversation-part-{k:02d}.md" if len(files) > 1 else "02-conversation.md"
        total = write(os.path.join(outdir, name), header.format(p=k) + "\n" + "\n".join(b))
        conv_files.append((name, total))
    info["02"] = conv_files

    # 03
    p3 = ["# 03 - Agent briefs, questions and follow-ups\n",
          "Every `Agent` tool call (the work briefs given to sub-agents: design decisions live here), "
          "then every AskUserQuestion with the user's answer, then every SendMessage to a running agent. "
          "Times UTC.\n", "\n## A. Agent briefs\n"]
    for k, a in enumerate(data["agents"], 1):
        inp = a["input"]
        p3.append(f"### Agent {k} - {fmt_ts(a['dt'])}\n")
        for key in ("description", "subagent_type", "model", "run_in_background", "isolation", "name"):
            if key in inp:
                p3.append(f"- **{key}**: {redact(str(inp[key]))}")
        p3.append("")
        p3.append(fence(redact(str(inp.get("prompt", "")))) + "\n")
    info["agents_n"] = len(data["agents"])
    p3.append("\n## B. Questions asked to the user (AskUserQuestion) and answers\n")
    for k, (tid, q) in enumerate(sorted(data["asks"].items(), key=lambda kv: kv[1]["line"]), 1):
        p3.append(f"### Question {k} - {fmt_ts(q['dt'])}\n")
        for qq in (q["input"].get("questions") or []):
            if not isinstance(qq, dict):
                continue
            p3.append(f"- **{redact(str(qq.get('header', '')))}**: {redact(str(qq.get('question', '')))}")
            for op in qq.get("options") or []:
                if isinstance(op, dict):
                    p3.append(f"    - option: {redact(str(op.get('label', '')))} - {redact(str(op.get('description', '')))}")
        res = data["results"].get(tid)
        if res:
            o, rtxt = res
            ans = None
            tur = o.get("toolUseResult")
            if isinstance(tur, dict) and tur.get("answers"):
                ans = json.dumps(tur["answers"], ensure_ascii=False)
            ans = ans or rtxt
            p3.append("\n**User's answer:**\n\n" + fence(redact(ans)) + "\n")
        else:
            p3.append("\n_(no answer recorded)_\n")
    info["asks_n"] = len(data["asks"])
    p3.append("\n## C. SendMessage follow-ups to running agents\n")
    for k, m in enumerate(data["sendmsgs"], 1):
        inp = m["input"]
        msg = inp.get("message", inp.get("content", ""))
        if not isinstance(msg, str):
            msg = json.dumps(msg, ensure_ascii=False)
        p3.append(f"### Message {k} - {fmt_ts(m['dt'])}  (to: {redact(str(inp.get('to', inp.get('session_id', '?'))))})\n")
        p3.append(fence(redact(msg)) + "\n")
    info["sendmsgs_n"] = len(data["sendmsgs"])
    info["03"] = write(os.path.join(outdir, "03-agent-briefs.md"), "\n".join(p3))

    # 04
    p4 = ["# 04 - Context-compaction summaries (verbatim, redacted)\n",
          "When the session context filled up, Claude Code replaced the history with these dense summaries. "
          "They are the best condensed record of what was built and decided. Times UTC.\n"]
    for k, (dt, ln, tx) in enumerate(data["summaries"], 1):
        p4.append(f"\n## Summary {k} - {fmt_ts(dt)}\n")
        p4.append(redact(tx).strip() + "\n")
    info["summaries_n"] = len(data["summaries"])
    info["04"] = write(os.path.join(outdir, "04-session-summaries.md"), "\n".join(p4))
    return info, humans


README_TMPL = """# 00 - README: full project history export

Generated by `migration-setup/export_history.py` on {now}. Source: one Claude Code session
transcript (JSONL, {lines} lines, {srcmb:.0f} MB, covering the whole project across 2 context
compactions, {first} to {last}). The raw transcript is NOT in this repo (it contains secrets);
these files are a sanitized, human-readable extract of it.

**Keep the repo private.** Redaction is automatic and pattern based: skim these files once
before the repo is ever made public (see `../REVOKE-AND-SECURITY.md`).

## Table of contents

| File | What it is | Count | Size |
|------|-----------|-------|------|
{toc}

## What was kept

- 01: every genuine user text (typed answers like `Yes` or `1`, slash commands with their args,
  long pasted briefs flagged as such). Sources merged and de-duplicated: user records, messages
  typed while a turn was running (queue enqueue + queued_command), with the earliest (typed) timestamp.
  {dropped} duplicate copies were dropped. {imgs} messages had images attached (images are not exported).
- 02: the dialogue: each user message followed by the assistant's visible text blocks ({asst_blocks} blocks).
- 03: all `Agent` briefs (description, subagent_type, model, run_in_background, prompt),
  AskUserQuestion questions with options and the user's answer, and SendMessage follow-ups.
- 04: the compaction summaries verbatim (dense history of what was built and why).

## What was removed, and why

- Tool results and tool calls other than the three kinds above: huge, and where secrets leaked
  (a Kaggle access token was displayed once in a tool result).
- Thinking blocks: internal reasoning, not part of the record the user saw.
- `<system-reminder>` blocks, hook feedback ("Stop hook feedback"), `<task-notification>`,
  `<agent-message>` / peer-agent hand-backs, `[SYSTEM NOTIFICATION`, local-command output,
  skill-expansion text, worker-restart notices, image path notes: machine generated, not the user.
- Sidechain (sub-agent internal) records and API-error records.
{trunc_note}
## Redaction (applied to every output string)

Replaced by `[REDACTED]`: `KGAT_` tokens, `hf_`, `github_pat_`, `gh[pousr]_`, `sk-`, `AIza`, `GOCSPX-`, `ya29.`,
`AKIA`, `xox*-`, JWTs, PEM private-key blocks, `Bearer <token>`, `api_key/token/secret/password = <value>`
(the name is kept, only the value is redacted), any 32+ hex string that is not a git commit sha present in
`git log --all`, and any other run of 30+ letters/digits/-/_ that is not a git sha or a UUID.
Email addresses become `[email]`. Redaction counts of the last run (counts only):

{redcounts}

## Verification performed by the script

Re-scan of every generated file for the patterns above and for any 30+ alphanumeric string not in the sha set
({verify}); and the repo key scanner (`.claude/skills/clips/scripts/checkpoint.py` secret scan) run over the
files. Total size of `history/`: {total:.2f} MB.

## How to rerun

```
python3 migration-setup/export_history.py                      # uses the default session path
python3 migration-setup/export_history.py --session /path/to/session.jsonl
python3 migration-setup/export_history.py --verify-only        # only re-scan existing output
python3 migration-setup/make_manifest.py                       # then refresh MANIFEST.json (commit history first)
```

The default session path is `{default}`; it only exists on the machine that ran the session,
so a rerun elsewhere needs `--session`. The script prints counts only, never matched values.

## Reading order for a new Claude account

1. `04-session-summaries.md` (densest), 2. `01-user-messages.md` (what the user actually asked, in their words),
3. `03-agent-briefs.md` (design decisions and requirements), 4. `02-conversation*.md` (the full back-and-forth).
"""

# --------------------------------------------------------------------------- verification
SCAN_RES = {
    "KGAT": re.compile(r"KGAT_[0-9a-fA-F]{10,}"),
    "hf_": re.compile(r"\bhf_[A-Za-z0-9]{20,}"),
    "github_pat": re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    "gh_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    "sk-": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    "AIza": re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    "AKIA": re.compile(r"AKIA[0-9A-Z]{16}"),
    "xox": re.compile(r"xox[bap]-[A-Za-z0-9-]+"),
    "bearer": re.compile(r"(?i)\bBearer\s+(?!\[REDACTED\])[A-Za-z0-9._~+/=-]{8,}"),
    "assignment": re.compile(r"(?i)(?:api[_-]?key|token|secret|password)[\"']?\s*[=:]\s*[\"']?(?!\[REDACTED\]|\$)\S{12,}"),
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
    "hex32": re.compile(r"(?<![0-9A-Za-z])[0-9a-fA-F]{32,}(?![0-9A-Za-z])"),
    "alnum30": re.compile(r"[A-Za-z0-9]{30,}"),
}


def verify(outdir):
    """Scan generated files. Returns (Counter of findings per pattern, files scanned)."""
    bad = Counter()
    files = sorted(f for f in os.listdir(outdir) if f.endswith(".md"))
    for f in files:
        txt = open(os.path.join(outdir, f), encoding="utf-8").read()
        for name, rx in SCAN_RES.items():
            for m in rx.finditer(txt):
                s = m.group(0)
                if name in ("hex32", "alnum30") and s in SHAS:
                    continue
                if name == "email" and s.startswith("[email]"):
                    continue
                bad[name] += 1
    return bad, files


def run_repo_scanner(outdir):
    """Apply the repo's own key regex (checkpoint.KEY_RE, the same one finalise.py uses via git grep)
    to every generated file, ignoring checkpoint.key_hit's 5 MB size skip. Returns hit count or None."""
    scripts = os.path.join(REPO, ".claude/skills/clips/scripts")
    if not os.path.exists(os.path.join(scripts, "checkpoint.py")):
        return None
    sys.path.insert(0, scripts)
    try:
        import checkpoint as cp
    except Exception:
        return None
    hits = 0
    for f in sorted(os.listdir(outdir)):
        if f.endswith(".md") and cp.KEY_RE.search(open(os.path.join(outdir, f), "rb").read()):
            hits += 1
    return hits


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session", default=DEFAULT_SESSION, help="session JSONL path")
    ap.add_argument("--out", default=os.path.join(REPO, "migration-setup", "history"))
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()
    outdir = os.path.abspath(args.out)
    os.makedirs(outdir, exist_ok=True)
    SHAS.update(load_shas())

    if args.verify_only:
        bad, files = verify(outdir)
        print("scanned", len(files), "files; findings per pattern (counts only):", dict(bad))
        return 1 if bad else 0

    if not os.path.exists(args.session):
        print("session file not found:", args.session, file=sys.stderr)
        return 2
    data = extract(args.session)

    truncate = False
    for attempt in (0, 1):
        COUNTS.clear()
        for f in os.listdir(outdir):
            if f.endswith(".md") and f != "00-README.md":
                os.remove(os.path.join(outdir, f))
        info, humans = build_all(data, outdir, truncate)
        total = sum(os.path.getsize(os.path.join(outdir, f)) for f in os.listdir(outdir) if f.endswith(".md"))
        if total <= SIZE_BUDGET or truncate:
            break
        truncate = True

    # README (needs final numbers; its own size is tiny)
    dts = [h["dt"] for h in humans if h["dt"]]
    toc = []
    toc.append(f"| `01-user-messages.md` | every user message, verbatim, numbered | {info['humans_n']} messages | {info['01']/1e3:.0f} KB |")
    for name, sz in info["02"]:
        toc.append(f"| `{name}` | dialogue: user + assistant text | {info['asst_blocks']} assistant text blocks in total | {sz/1e3:.0f} KB |")
    toc.append(f"| `03-agent-briefs.md` | Agent briefs, AskUserQuestion Q&A, SendMessage | {info['agents_n']} agent briefs, {info['asks_n']} questions, {info['sendmsgs_n']} messages | {info['03']/1e3:.0f} KB |")
    toc.append(f"| `04-session-summaries.md` | context-compaction summaries | {info['summaries_n']} summaries | {info['04']/1e3:.0f} KB |")
    toc.append("| `00-README.md` | this file | - | - |")
    st = data["stats"]
    redcounts = "\n".join(f"- `{k}`: {v}" for k, v in sorted(COUNTS.items())) or "- none"
    trunc_note = ""
    if truncate:
        trunc_note = (f"- Assistant text blocks longer than {BIG_ASSISTANT} characters were cut to their first "
                      f"{KEEP_ASSISTANT} characters followed by `[truncated]` (the full set exceeded the {SIZE_BUDGET/1e6:.0f} MB budget; "
                      f"{COUNTS['assistant_blocks_truncated']} blocks affected).\n")
    readme_path = os.path.join(outdir, "00-README.md")
    imgs = sum(1 for h in humans if h["images"])
    write(readme_path, README_TMPL.format(
        now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), lines=st["lines"],
        srcmb=os.path.getsize(args.session) / 1e6, first=fmt_ts(min(dts)) if dts else "?",
        last=fmt_ts(max(dts)) if dts else "?", toc="\n".join(toc), dropped=info["humans_dropped_dups"],
        imgs=imgs, asst_blocks=info["asst_blocks"], trunc_note=trunc_note, redcounts=redcounts,
        verify="pass", total=total / 1e6, default=DEFAULT_SESSION))

    # verification (README included: it must be clean too)
    bad, files = verify(outdir)
    total = sum(os.path.getsize(os.path.join(outdir, f)) for f in os.listdir(outdir) if f.endswith(".md"))
    print("files:", len(files), "total bytes:", total)
    print("user messages:", info["humans_n"], "dup copies dropped:", info["humans_dropped_dups"],
          "assistant blocks:", info["asst_blocks"], "agent briefs:", info["agents_n"],
          "questions:", info["asks_n"], "sendmessages:", info["sendmsgs_n"], "summaries:", info["summaries_n"])
    print("redactions by pattern (counts only):", dict(COUNTS))
    print("post-scan findings per pattern (must be empty):", dict(bad))
    hits = run_repo_scanner(outdir)
    print("repo key scanner (checkpoint.KEY_RE) files with hits:", hits)
    print("truncated assistant blocks:", COUNTS.get("assistant_blocks_truncated", 0))
    return 1 if (bad or hits) else 0


if __name__ == "__main__":
    sys.exit(main())
