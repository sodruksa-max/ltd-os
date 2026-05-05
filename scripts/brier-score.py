#!/usr/bin/env python3
"""
Rolling Brier Score tracker — reads OUTCOMES.md Trading Calibration Log,
calculates BS per day, rolling 10-day average, and over-confidence flag.

Usage:
    python scripts/brier-score.py [--window N]

Output: markdown table + rolling average + flag
"""

import re
import sys
from pathlib import Path
from datetime import datetime

OUTCOMES_PATH = Path(__file__).parent.parent / "vault" / "_memory" / "OUTCOMES.md"

CONF_MAP = {"low": 0.3, "medium": 0.5, "high": 0.7}
MATCH_MAP = {"yes": 1.0, "partial": 0.5, "no": 0.0}

# parse a confidence-level word like "medium" from "Predicted: Base (medium)"
_RE_CONF = re.compile(r"Predicted:\s*\w+\s*\((\w+)\)", re.IGNORECASE)
_RE_MATCH = re.compile(r"Match:\s*(Yes|Partial|No)", re.IGNORECASE)
_RE_BS = re.compile(r"BS:\s*([\d.]+)")
_RE_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s*—")


def parse_entries(text: str) -> list[dict]:
    entries = []
    in_section = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## Trading Calibration Log"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break  # next section
        if not in_section or not line:
            continue
        if line.startswith("[") or "[review-only]" in line:
            continue  # weekly-calibration summary lines or review-only

        date_m = _RE_DATE.match(line)
        if not date_m:
            continue
        date_str = date_m.group(1)

        # try to get stored BS first
        bs_m = _RE_BS.search(line)
        if bs_m:
            bs = float(bs_m.group(1))
            entries.append({"date": date_str, "bs": bs, "source": "stored"})
            continue

        conf_m = _RE_CONF.search(line)
        match_m = _RE_MATCH.search(line)
        if not conf_m or not match_m:
            continue

        conf_word = conf_m.group(1).lower()
        match_word = match_m.group(1).lower()
        conf = CONF_MAP.get(conf_word)
        outcome = MATCH_MAP.get(match_word)
        if conf is None or outcome is None:
            continue

        bs = round((conf - outcome) ** 2, 4)
        entries.append({"date": date_str, "bs": bs, "conf": conf_word, "match": match_word, "source": "calc"})

    return entries


def rolling_avg(values: list[float], window: int) -> list[float | None]:
    avgs = []
    for i, _ in enumerate(values):
        start = max(0, i - window + 1)
        window_vals = values[start : i + 1]
        avgs.append(round(sum(window_vals) / len(window_vals), 4))
    return avgs


def flag(avg: float | None) -> str:
    if avg is None:
        return ""
    if avg > 0.25:
        return "[!] OVER-CONFIDENT"
    if avg < 0.10:
        return "[ok] well-calibrated"
    return "[~] ok"


def main():
    window = 10
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--window" and i + 1 < len(sys.argv[1:]):
            window = int(sys.argv[i + 2])

    if not OUTCOMES_PATH.exists():
        print(f"ERROR: {OUTCOMES_PATH} not found")
        sys.exit(1)

    text = OUTCOMES_PATH.read_text(encoding="utf-8")
    entries = parse_entries(text)

    if not entries:
        print("No calibration entries found in Trading Calibration Log.")
        sys.exit(0)

    bss = [e["bs"] for e in entries]
    avgs = rolling_avg(bss, window)

    # header
    print(f"## Brier Score Tracker (window={window})")
    print(f"*Source: {OUTCOMES_PATH.relative_to(OUTCOMES_PATH.parent.parent.parent)} | BS = (confidence - outcome)^2*\n")
    print(f"*Confidence mapping: low=0.3 | medium=0.5 | high=0.7 | outcome: Yes=1 / Partial=0.5 / No=0*\n")
    print(f"| Date | BS | Rolling {window}d avg | Status |")
    print("|---|---|---|---|")

    for i, e in enumerate(entries):
        avg = avgs[i]
        status = flag(avg)
        source_note = "" if e["source"] == "stored" else " *(calc)*"
        print(f"| {e['date']} | {e['bs']:.4f}{source_note} | {avg:.4f} | {status} |")

    # summary
    overall = round(sum(bss) / len(bss), 4)
    latest_avg = avgs[-1]
    print(f"\n**Overall average BS ({len(entries)} days):** {overall:.4f} {flag(overall)}")
    print(f"**Latest rolling {window}d avg:** {latest_avg:.4f} {flag(latest_avg)}")

    # interpretation
    print("\n### Interpretation")
    print("- BS = 0.00 = perfect prediction (e.g. high confidence + correct)")
    print("- BS = 0.25 = medium confidence + wrong (baseline threshold)")
    print("- BS = 0.49 = high confidence + wrong (worst case)")
    print("- Rolling avg > 0.25 = systematically over-confident = reduce confidence levels")


if __name__ == "__main__":
    main()
