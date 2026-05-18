#!/usr/bin/env python3
"""
Parse vault/_memory/OUTCOMES.md → JSON index for fast filtered retrieval.

Parses decision entries (## YYYY-MM-DD — title blocks) with fields:
  decision, reasoning, outcome (ok/mixed/wrong), learned, tags, domain

Usage:
  python scripts/outcomes-index.py                       # rebuild + print summary
  python scripts/outcomes-index.py --query TEXT          # top-3 relevant entries
  python scripts/outcomes-index.py --query TEXT --top N  # top-N entries
  python scripts/outcomes-index.py --tag tooling         # filter by tag
  python scripts/outcomes-index.py --outcome ok          # filter: ok / mixed / wrong

Used by /council Phase 1 (CASE principle arXiv:2506.08607): query by topic keywords,
insert top-3 entries into brief as "Prior decisions context".
"""

from __future__ import annotations

import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Force UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO          = Path(__file__).resolve().parent.parent
OUTCOMES_PATH = REPO / "vault/_memory/OUTCOMES.md"
INDEX_PATH    = Path(__file__).parent / "outcomes-index.json"

OUTCOME_SYMBOLS = {"✅": "ok", "⚠️": "mixed", "❌": "wrong"}


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_outcomes(text: str) -> list[dict]:
    entries: list[dict] = []
    header_re = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — (.+)$", re.MULTILINE)
    matches = list(header_re.finditer(text))

    for i, m in enumerate(matches):
        date  = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body  = text[start:end]

        # Skip HTML comment example entries
        if "<!--" in body[:100]:
            continue

        entries.append({
            "date":      date,
            "title":     title,
            "type":      "decision",
            "decision":  _field(body, "Decision"),
            "reasoning": _field(body, "Reasoning at the time"),
            "outcome":   _parse_outcome(body),
            "learned":   _field(body, "What I learned"),
            "recommend": _field(body, "Would recommend"),
            "tags":      _parse_tags(body),
            "domain":    _infer_domain(title, _field(body, "Tags")),
        })

    return entries


def _field(body: str, label: str) -> str:
    m = re.search(
        rf"\*\*{re.escape(label)}\*\*[:\s]+(.+?)(?=\n\*\*|\Z)",
        body, re.S
    )
    return m.group(1).strip() if m else ""


def _parse_outcome(body: str) -> str:
    m = re.search(r"\*\*Outcome[^*]*\*\*[:\s]+(.+)", body)
    if not m:
        return "unknown"
    raw = m.group(1)
    for symbol, label in OUTCOME_SYMBOLS.items():
        if symbol in raw:
            return label
    return "unknown"


def _parse_tags(body: str) -> list[str]:
    m = re.search(r"\*\*Tags\*\*[:\s]+(.+)", body)
    if not m:
        return []
    return re.findall(r"#([\w-]+)", m.group(1))


def _infer_domain(title: str, tags_text: str) -> str:
    combined = (title + " " + tags_text).lower()
    if any(w in combined for w in ["trading", "investment", "nick", "portfolio", "stock", "market", "trade"]):
        return "trading"
    if any(w in combined for w in ["process", "workflow", "command", "tooling", "system", "pre-market", "command-design"]):
        return "process"
    if any(w in combined for w in ["content", "writing", "thread", "newsletter"]):
        return "content"
    return "general"


# ---------------------------------------------------------------------------
# Scoring (keyword overlap — domain/tag matches weighted 2×)
# ---------------------------------------------------------------------------

def _score(entry: dict, tokens: list[str]) -> int:
    haystack = " ".join([
        entry["title"], entry["decision"], entry["reasoning"],
        entry["learned"], " ".join(entry["tags"]), entry["domain"],
    ]).lower()
    counts = Counter(tokens)
    score  = 0
    for tok, n in counts.items():
        occ    = haystack.count(tok)
        weight = 2 if (tok in entry["domain"] or tok in " ".join(entry["tags"])) else 1
        score += occ * weight * n
    return score


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build(entries: list[dict]) -> None:
    INDEX_PATH.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _print_summary(entries: list[dict]) -> None:
    outcomes = Counter(e["outcome"] for e in entries)
    domains  = Counter(e["domain"]  for e in entries)
    top_tags = Counter(t for e in entries for t in e["tags"]).most_common(5)
    print(f"Indexed {len(entries)} decision entries -> {INDEX_PATH.name}")
    print(f"  Outcomes : ok={outcomes.get('ok',0)}  mixed={outcomes.get('mixed',0)}  wrong={outcomes.get('wrong',0)}  unknown={outcomes.get('unknown',0)}")
    print(f"  Domains  : {dict(domains)}")
    print(f"  Top tags : {top_tags}")


def _print_results(results: list[dict], query: str) -> None:
    icon_map = {"ok": "[ok]", "mixed": "[mixed]", "wrong": "[wrong]"}
    if not results:
        print("no relevant prior decisions")
        return
    print(f'Top {len(results)} for: "{query}"\n')
    for r in results:
        icon = icon_map.get(r["outcome"], "[?]")
        print(f'{icon} {r["date"]} -- {r["title"]}')
        if r["decision"]:
            print(f'   Decision : {r["decision"][:120]}')
        if r["learned"]:
            first_line = r["learned"].strip().splitlines()[0]
            print(f'   Learned  : {first_line[:120]}')
        if r["tags"]:
            print(f'   Tags     : {" ".join("#"+t for t in r["tags"])}')
        print()


def main() -> None:
    text    = OUTCOMES_PATH.read_text(encoding="utf-8")
    entries = parse_outcomes(text)
    _build(entries)

    args = sys.argv[1:]
    if not args:
        _print_summary(entries)
        return

    # Parse flags
    query      = ""
    top_n      = 3
    tag_filter = None
    out_filter = None
    i = 0
    while i < len(args):
        if args[i] == "--query" and i + 1 < len(args):
            query = args[i + 1]; i += 2
        elif args[i] == "--top" and i + 1 < len(args):
            top_n = int(args[i + 1]); i += 2
        elif args[i] == "--tag" and i + 1 < len(args):
            tag_filter = args[i + 1].lstrip("#"); i += 2
        elif args[i] == "--outcome" and i + 1 < len(args):
            out_filter = args[i + 1]; i += 2
        else:
            i += 1

    pool = entries
    if tag_filter:
        pool = [e for e in pool if tag_filter in e["tags"]]
    if out_filter:
        pool = [e for e in pool if e["outcome"] == out_filter]

    if query:
        tokens  = re.findall(r"\w+", query.lower())
        results = sorted(pool, key=lambda e: _score(e, tokens), reverse=True)[:top_n]
        _print_results(results, query)
    else:
        _print_summary(pool)


if __name__ == "__main__":
    main()
