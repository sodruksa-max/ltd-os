#!/usr/bin/env python3
"""
outcomes-index.py — Build structured index from OUTCOMES.md for fast retrieval.

Parses OUTCOMES.md trade entries → outputs JSON index with fields:
  date, ticker, action, outcome (win/loss/break-even), pnl_pct, pattern_tags, notes

Usage:
  python scripts/outcomes-index.py              # print summary
  python scripts/outcomes-index.py --json       # dump full index as JSON
  python scripts/outcomes-index.py --ticker NVDA  # filter by ticker
  python scripts/outcomes-index.py --tag macro/ai-capex  # filter by theme tag
"""

import json
import re
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTCOMES_PATH = ROOT / "vault" / "_memory" / "OUTCOMES.md"
INDEX_PATH = ROOT / "vault" / "_memory" / "outcomes-index.json"


def parse_outcomes(text: str) -> list[dict]:
    entries = []
    # Match markdown table rows: | date | ticker | action | pnl | tags | notes |
    # Also match freeform entry blocks with frontmatter-style fields
    block_pattern = re.compile(
        r"##\s+(?P<date>\d{4}-\d{2}-\d{2})[^\n]*\n(?P<body>(?:(?!##).)+)",
        re.DOTALL,
    )
    field_pattern = re.compile(r"\*\*(?P<key>[^*]+)\*\*[:\s]+(?P<val>[^\n]+)")

    for match in block_pattern.finditer(text):
        date = match.group("date")
        body = match.group("body")
        fields: dict = {"date": date}

        for f in field_pattern.finditer(body):
            key = f.group("key").strip().lower().replace(" ", "_")
            val = f.group("val").strip()
            fields[key] = val

        # Normalize common field names
        ticker = fields.get("ticker") or fields.get("stock") or fields.get("symbol", "")
        action = fields.get("action") or fields.get("trade", "")
        outcome = fields.get("outcome") or fields.get("result", "")
        pnl_raw = fields.get("pnl") or fields.get("p&l") or fields.get("return", "")
        notes = fields.get("notes") or fields.get("lesson") or fields.get("note", "")
        tags_raw = fields.get("theme_cluster") or fields.get("tags") or fields.get("pattern", "")

        # Parse pnl percentage
        pnl_pct = None
        m = re.search(r"([+-]?\d+\.?\d*)%", pnl_raw)
        if m:
            pnl_pct = float(m.group(1))

        # Derive win/loss/break-even
        if outcome.lower() in ("win", "profit", "✅"):
            outcome_class = "win"
        elif outcome.lower() in ("loss", "stop", "❌"):
            outcome_class = "loss"
        elif pnl_pct is not None:
            outcome_class = "win" if pnl_pct > 0 else ("loss" if pnl_pct < 0 else "break-even")
        else:
            outcome_class = outcome or "unknown"

        pattern_tags = [t.strip() for t in re.split(r"[,|;]", tags_raw) if t.strip()]

        if ticker or action:
            entries.append({
                "date": date,
                "ticker": ticker.upper() if ticker else "",
                "action": action,
                "outcome": outcome_class,
                "pnl_pct": pnl_pct,
                "pattern_tags": pattern_tags,
                "notes": notes,
            })

    return entries


def print_summary(entries: list[dict]) -> None:
    if not entries:
        print("No entries found in OUTCOMES.md")
        print("File may be empty or not yet populated with trade records.")
        return

    wins = sum(1 for e in entries if e["outcome"] == "win")
    losses = sum(1 for e in entries if e["outcome"] == "loss")
    tickers = sorted({e["ticker"] for e in entries if e["ticker"]})
    tags = {}
    for e in entries:
        for t in e["pattern_tags"]:
            tags[t] = tags.get(t, 0) + 1

    print(f"OUTCOMES index — {len(entries)} entries")
    print(f"Win: {wins}  Loss: {losses}  Other: {len(entries)-wins-losses}")
    print(f"Tickers: {', '.join(tickers) if tickers else 'none'}")
    if tags:
        top = sorted(tags.items(), key=lambda x: -x[1])[:5]
        print(f"Top tags: {', '.join(f'{t}({n})' for t,n in top)}")


def main():
    args = sys.argv[1:]

    if not OUTCOMES_PATH.exists():
        print(f"OUTCOMES.md not found at {OUTCOMES_PATH}")
        sys.exit(1)

    text = OUTCOMES_PATH.read_text(encoding="utf-8")
    entries = parse_outcomes(text)

    # Filter flags
    if "--ticker" in args:
        idx = args.index("--ticker")
        ticker = args[idx + 1].upper()
        entries = [e for e in entries if e["ticker"] == ticker]

    if "--tag" in args:
        idx = args.index("--tag")
        tag = args[idx + 1]
        entries = [e for e in entries if tag in e["pattern_tags"]]

    if "--json" in args:
        print(json.dumps(entries, indent=2, ensure_ascii=False))
    else:
        print_summary(entries)

    # Always write index file
    INDEX_PATH.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
