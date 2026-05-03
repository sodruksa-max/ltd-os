#!/usr/bin/env python3
"""
Momentum screener — ranks watchlist stocks by momentum score using Alpaca data.

Usage:
    python scripts/screener.py                   # screen all tickers in config/watchlist.txt
    python scripts/screener.py --top 5           # show top 5 only
    python scripts/screener.py --json            # output JSON (for auto-buy.py to consume)
    python scripts/screener.py --fundamentals    # add yfinance fundamental junk checks (slower)
    python scripts/screener.py NVDA AAPL         # screen specific tickers only

Criteria:
  1. RS vs SPY     — 20-day return vs benchmark (higher = outperforming)
  2. Volume        — today's volume vs 20-day average (>1.5x = breakout confirmation)
  3. Above MA50    — price trend filter
  4. Price         — $5-$1000 (exclude penny stocks)
  5. Junk filter   — pump detection, volatility, + optionally fundamentals (EPS, debt, OCF)

Score = RS_vs_SPY * clamp(VolRatio, 0.5, 3.0)
Junk: FAIL = excluded from auto-buy | WARN = flagged but still considered

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
WATCHLIST = ROOT / "config" / "watchlist.txt"
BENCHMARK = "SPY"
PRICE_MIN = 5.0
PRICE_MAX = 1000.0
LOOKBACK = 20      # 20-day return window
MA_PERIOD = 50
HISTORY_DAYS = 80  # calendar days to fetch (~56 trading days, enough for MA50)


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


def load_watchlist():
    if not WATCHLIST.exists():
        print(f"[warn] watchlist not found: {WATCHLIST}", file=sys.stderr)
        return []
    tickers = []
    for line in WATCHLIST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tickers.append(line.upper())
    return tickers


def fetch_bars(tickers):
    """Fetch daily bars for all tickers at once via Alpaca."""
    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA keys not set", file=sys.stderr)
        sys.exit(1)

    client = StockHistoricalDataClient(api_key, secret_key)
    start = datetime.combine(date.today() - timedelta(days=HISTORY_DAYS), datetime.min.time())

    resp = client.get_stock_bars(
        StockBarsRequest(symbol_or_symbols=tickers, timeframe=TimeFrame.Day, start=start)
    )
    return resp.data


def _bar_val(bar, field):
    return bar[field] if isinstance(bar, dict) else getattr(bar, field)


def screen(tickers, bars_data, fetch_fundamentals=False):
    import junk_filter

    results = []
    fails = []

    spy_bars = bars_data.get(BENCHMARK, [])
    spy_closes = [_bar_val(b, "close") for b in spy_bars]

    candidates = [t for t in tickers if t != BENCHMARK]
    total = len(candidates)

    for ticker in candidates:
        try:
            bars = bars_data.get(ticker, [])
            if len(bars) < LOOKBACK + 2:
                fails.append((ticker, f"only {len(bars)} bars"))
                continue

            closes = [_bar_val(b, "close") for b in bars]
            volumes = [_bar_val(b, "volume") for b in bars]

            current_price = closes[-1]
            if not (PRICE_MIN <= current_price <= PRICE_MAX):
                fails.append((ticker, f"price ${current_price:.2f} out of range"))
                continue

            ret_20d = (closes[-1] - closes[-LOOKBACK - 1]) / closes[-LOOKBACK - 1]

            if len(spy_closes) >= LOOKBACK + 1:
                spy_ret = (spy_closes[-1] - spy_closes[-LOOKBACK - 1]) / spy_closes[-LOOKBACK - 1]
                rs = ret_20d - spy_ret
            else:
                rs = ret_20d

            above_ma50 = False
            ma50_val = None
            if len(closes) >= MA_PERIOD:
                ma50_val = sum(closes[-MA_PERIOD:]) / MA_PERIOD
                above_ma50 = current_price > ma50_val

            vol_ratio = 0.0
            if len(volumes) >= LOOKBACK + 1:
                avg_vol = sum(volumes[-LOOKBACK - 1:-1]) / LOOKBACK
                vol_ratio = volumes[-1] / avg_vol if avg_vol > 0 else 0.0

            vol_weight = max(0.5, min(vol_ratio, 3.0))
            score = rs * vol_weight

            junk = junk_filter.evaluate(
                ticker, closes, volumes,
                ret_20d=ret_20d,
                fetch_fund=fetch_fundamentals,
            )

            results.append({
                "ticker": ticker,
                "price": round(current_price, 2),
                "return_20d_pct": round(ret_20d * 100, 2),
                "rs_vs_spy_pct": round(rs * 100, 2),
                "vol_ratio": round(vol_ratio, 2),
                "above_ma50": above_ma50,
                "ma50": round(ma50_val, 2) if ma50_val else None,
                "score": round(score, 4),
                "junk_level": junk["level"],
                "junk_summary": junk["summary"],
            })

        except Exception as e:
            fails.append((ticker, str(e)))

    results.sort(key=lambda x: x["score"], reverse=True)
    return results, fails


def print_table(results, top=None):
    rows = results[:top] if top else results
    if not rows:
        print("No results.")
        return

    print(f"{'#':<3} {'Ticker':<8} {'Price':>8} {'20d Ret':>8} {'RS/SPY':>8} {'VolRatio':>9} {'MA50':>5} {'Score':>8}  Filter")
    print("-" * 85)
    for i, r in enumerate(rows, 1):
        ma_flag = "Y" if r["above_ma50"] else "n"
        rs_sign = "+" if r["rs_vs_spy_pct"] >= 0 else ""
        ret_sign = "+" if r["return_20d_pct"] >= 0 else ""
        junk_level = r.get("junk_level", "PASS")
        junk_summary = r.get("junk_summary", "OK")
        junk_col = f"[{junk_level}] {junk_summary}" if junk_level != "PASS" else "[OK]"
        print(
            f"{i:<3} {r['ticker']:<8} ${r['price']:>7,.2f} "
            f"{ret_sign}{r['return_20d_pct']:>6.1f}% {rs_sign}{r['rs_vs_spy_pct']:>6.1f}% "
            f"{r['vol_ratio']:>8.2f}x {ma_flag:>5} {r['score']:>8.4f}  {junk_col}"
        )
    print()
    print("Score = RS_vs_SPY * clamp(VolRatio, 0.5, 3.0)")
    print("MA50 Y=above / n=below  |  Filter: [OK]=clean [WARN]=caution [FAIL]=excluded from auto-buy")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fundamentals", action="store_true",
                        help="Add yfinance fundamental junk checks (slower, ~30s extra)")
    parser.add_argument("tickers", nargs="*")
    args = parser.parse_args()

    load_env()
    # Add scripts/ to path so junk_filter.py can be imported
    sys.path.insert(0, str(ROOT / "scripts"))

    tickers = [t.upper() for t in args.tickers] if args.tickers else load_watchlist()
    if not tickers:
        print("No tickers to screen.")
        sys.exit(1)

    fetch_list = list(set(tickers + [BENCHMARK]))
    print(f"Fetching {len(fetch_list)} tickers from Alpaca...", file=sys.stderr)
    if args.fundamentals:
        print("Fundamental checks ON (yfinance — may take ~30s)...", file=sys.stderr)

    try:
        bars_data = fetch_bars(fetch_list)
    except Exception as e:
        print(f"ERROR fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    results, fails = screen(tickers, bars_data, fetch_fundamentals=args.fundamentals)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n## Momentum Screen -- {date.today()}\n")
    print_table(results, top=args.top)

    if fails:
        print(f"\n[skipped {len(fails)}]: " + ", ".join(f"{t}({r})" for t, r in fails[:8]))


if __name__ == "__main__":
    main()
