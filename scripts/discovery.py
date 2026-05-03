#!/usr/bin/env python3
"""
Discovery screener — finds new stocks from Alpaca market movers.

Instead of a fixed watchlist, pulls today's most-active + top gainers from Alpaca
then runs the same momentum/reversal screening logic.

Usage:
    python scripts/discovery.py                 # momentum mode
    python scripts/discovery.py --reversal      # reversal mode (beginning-of-trend)
    python scripts/discovery.py --top 10        # show top 10
    python scripts/discovery.py --json          # JSON output for bot/dashboard

Sources:
  - Alpaca Most Actives by volume (top 50) — liquid, high-interest stocks
  - Alpaca Top Gainers (top 20, price $5-$350) — stocks moving today

Scoring reuses screener.py logic (RS vs SPY, vol ratio, MA50, reversal signals).
"""

import json
import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

BENCHMARK   = "SPY"
PRICE_MIN   = 5.0
PRICE_MAX   = 1000.0
TOP_ACTIVES = 50
TOP_GAINERS = 20


def load_env():
    env_file = ROOT / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def fetch_universe():
    """Pull dynamic ticker list from Alpaca ScreenerClient."""
    from alpaca.data import (
        ScreenerClient, MostActivesRequest, MostActivesBy, MarketMoversRequest,
    )
    api_key    = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA keys not set", file=sys.stderr)
        sys.exit(1)

    client  = ScreenerClient(api_key, secret_key)
    symbols = set()

    try:
        actives = client.get_most_actives(
            MostActivesRequest(by=MostActivesBy.VOLUME, top=TOP_ACTIVES)
        )
        for item in actives.most_actives:
            symbols.add(item.symbol)
        print(f"Most actives: {len(actives.most_actives)} tickers", file=sys.stderr)
    except Exception as e:
        print(f"[warn] most_actives failed: {e}", file=sys.stderr)

    try:
        movers = client.get_market_movers(MarketMoversRequest(top=TOP_GAINERS))
        added = 0
        for g in movers.gainers:
            if PRICE_MIN <= g.price <= PRICE_MAX:
                symbols.add(g.symbol)
                added += 1
        print(f"Top gainers (price-filtered): {added} tickers", file=sys.stderr)
    except Exception as e:
        print(f"[warn] market_movers failed: {e}", file=sys.stderr)

    return sorted(symbols)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--top",      type=int, default=None)
    parser.add_argument("--json",     action="store_true")
    parser.add_argument("--reversal", action="store_true",
                        help="Sort by reversal score, filter overextended")
    args = parser.parse_args()

    load_env()

    # Import reusable functions from screener.py
    import screener as sc

    print("Fetching universe from Alpaca market data...", file=sys.stderr)
    universe = fetch_universe()
    if not universe:
        print("ERROR: no tickers fetched", file=sys.stderr)
        sys.exit(1)

    fetch_list = list(set(universe + [BENCHMARK]))
    print(f"Universe: {len(universe)} tickers -- fetching bar history...", file=sys.stderr)

    try:
        bars_data = sc.fetch_bars(fetch_list)
    except Exception as e:
        print(f"ERROR fetching bars: {e}", file=sys.stderr)
        sys.exit(1)

    results, fails = sc.screen(universe, bars_data, fetch_fundamentals=False)

    if args.reversal:
        results = [r for r in results if not r.get("overextended")]
        results.sort(key=lambda x: x["reversal_score"], reverse=True)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    mode = "Discovery Reversal" if args.reversal else "Discovery Momentum"
    print(f"\n## {mode} Screen -- {date.today()}")
    print(f"Universe: {len(universe)} tickers from Alpaca most-actives + gainers\n")
    sc.print_table(results, top=args.top, reversal_mode=args.reversal)

    if fails:
        shown = fails[:6]
        print(f"\n[skipped {len(fails)}]: " + ", ".join(f"{t}({r[:20]})" for t, r in shown))


if __name__ == "__main__":
    main()
