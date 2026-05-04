#!/usr/bin/env python3
"""
Build config/sector-map.json from S&P 500 constituent list.
Uses the same GitHub CSV as update-universe.py — no extra API calls.

Usage:
    python scripts/update-sectors.py

Re-run monthly alongside update-universe.py to catch index changes.
"""

import csv
import io
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT  = ROOT / "config" / "sector-map.json"
URL  = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
UA   = "Mozilla/5.0"


def main():
    print("Fetching S&P 500 constituents with sector data...", file=sys.stderr)
    try:
        req  = urllib.request.Request(URL, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    sector_map = {}
    reader = csv.DictReader(io.StringIO(data))
    for row in reader:
        symbol = row.get("Symbol", "").replace(".", "-").strip()
        sector = row.get("GICS Sector", row.get("Sector", "")).strip()
        if symbol and sector:
            sector_map[symbol] = sector

    OUT.write_text(json.dumps(sector_map, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Saved {len(sector_map)} tickers → {OUT.name}", file=sys.stderr)

    # Print sector summary
    from collections import Counter
    counts = Counter(sector_map.values())
    for sector, n in sorted(counts.items()):
        print(f"  {sector:<35} {n} stocks")


if __name__ == "__main__":
    main()
