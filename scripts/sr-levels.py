#!/usr/bin/env python3
"""
Support & Resistance levels calculator using Alpaca historical data.

Usage:
    code/python/.venv/Scripts/python scripts/sr-levels.py AAPL SPY QQQ
    code/python/.venv/Scripts/python scripts/sr-levels.py NVDA --days 60

Calculates per ticker:
  - Classic pivot points (PP, R1-R3, S1-S3) from previous trading day
  - Swing highs/lows (last --days bars, default 30)
  - 52-week high/low

Output: markdown table ready to paste into premarket brief.
Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import os
import sys
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path


def load_env():
    env_file = Path(__file__).parent.parent / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip())


def get_bars(tickers: list[str], days: int) -> dict:
    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA_API_KEY / ALPACA_SECRET_KEY not set in .secrets/.env")
        sys.exit(1)

    client = StockHistoricalDataClient(api_key, secret_key)
    # Fetch extra days to cover weekends/holidays; cap at ~1 year (400 calendar days)
    start = date.today() - timedelta(days=400)
    request = StockBarsRequest(
        symbol_or_symbols=tickers,
        timeframe=TimeFrame.Day,
        start=datetime.combine(start, datetime.min.time()),
    )
    bars_response = client.get_stock_bars(request)
    raw = bars_response.data  # dict: {ticker: [bar_dict, ...]}
    result = {}
    for ticker in tickers:
        if ticker in raw and raw[ticker]:
            result[ticker] = raw[ticker]
        else:
            print(f"  [warn] No data for {ticker}")
    return result


def calc_pivots(high: float, low: float, close: float) -> dict:
    pp = (high + low + close) / 3
    return {
        "R3": round(high + 2 * (pp - low), 2),
        "R2": round(pp + (high - low), 2),
        "R1": round(2 * pp - low, 2),
        "PP": round(pp, 2),
        "S1": round(2 * pp - high, 2),
        "S2": round(pp - (high - low), 2),
        "S3": round(low - 2 * (high - pp), 2),
    }


def _get(bar, field):
    """Access bar field whether bar is a dict or an object."""
    if isinstance(bar, dict):
        return bar[field]
    return getattr(bar, field)


def _bar_date(bar):
    ts = _get(bar, "timestamp")
    return ts.date() if hasattr(ts, "date") else ts


def find_swings(bars, lookback: int = 30, window: int = 3) -> list[dict]:
    """Find swing highs and lows using a rolling window."""
    recent = bars[-lookback:] if len(bars) > lookback else bars
    swings = []

    for i in range(window, len(recent) - window):
        bar = recent[i]
        neighbors_h = [_get(recent[j], "high") for j in range(i - window, i + window + 1) if j != i]
        neighbors_l = [_get(recent[j], "low") for j in range(i - window, i + window + 1) if j != i]
        h = _get(bar, "high")
        l = _get(bar, "low")

        if h >= max(neighbors_h):
            swings.append({"type": "High", "price": round(h, 2), "date": _bar_date(bar)})
        if l <= min(neighbors_l):
            swings.append({"type": "Low", "price": round(l, 2), "date": _bar_date(bar)})

    # Deduplicate nearby levels (within 0.5%)
    deduped = []
    for s in sorted(swings, key=lambda x: x["price"], reverse=True):
        if not any(abs(s["price"] - d["price"]) / s["price"] < 0.005 for d in deduped):
            deduped.append(s)

    return sorted(deduped, key=lambda x: x["price"], reverse=True)[:8]


def calc_atr(bars, period: int = 14) -> float | None:
    """Average True Range over `period` bars."""
    if len(bars) < period + 1:
        return None
    recent = bars[-(period + 1):]
    trs = []
    for i in range(1, len(recent)):
        h = _get(recent[i], "high")
        l = _get(recent[i], "low")
        pc = _get(recent[i - 1], "close")
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return round(sum(trs) / len(trs), 4)


def fmt_price(p: float) -> str:
    return f"${p:,.2f}"


def print_ticker(ticker: str, bars, days: int):
    if not bars or len(bars) < 2:
        print(f"\n### {ticker}\n  [warn] Insufficient data\n")
        return

    prev = bars[-2]      # previous trading day
    last = bars[-1]      # most recent bar
    year_bars = bars[-252:] if len(bars) >= 252 else bars

    pivots = calc_pivots(_get(prev, "high"), _get(prev, "low"), _get(prev, "close"))
    swings = find_swings(bars, lookback=days)
    last_c = _get(last, "close")
    # Filter out obvious bad data points (must be within 50% of last close)
    valid_bars = [b for b in year_bars if _get(b, "low") > last_c * 0.5 and _get(b, "high") < last_c * 2.0]
    week52_high = max(_get(b, "high") for b in valid_bars) if valid_bars else last_c
    week52_low = min(_get(b, "low") for b in valid_bars) if valid_bars else last_c

    prev_ts = _get(prev, "timestamp")
    prev_date = prev_ts.strftime("%Y-%m-%d") if hasattr(prev_ts, "strftime") else str(prev_ts)[:10]
    last_close = _get(last, "close")

    print(f"\n### {ticker}")
    print(f"*Prev day ({prev_date}): O={fmt_price(_get(prev,'open'))} H={fmt_price(_get(prev,'high'))} L={fmt_price(_get(prev,'low'))} C={fmt_price(_get(prev,'close'))} | Last close: {fmt_price(last_close)}*")
    print(f"*52W: H={fmt_price(week52_high)} / L={fmt_price(week52_low)}*\n")

    # Pivot table
    print("**Pivot Points (Classic)**\n")
    print("| Level | Price | vs Last Close |")
    print("|---|---|---|")
    for label in ["R3", "R2", "R1", "PP", "S1", "S2", "S3"]:
        price = pivots[label]
        diff = price - last_close
        pct = diff / last_close * 100
        arrow = "+" if diff >= 0 else ""
        print(f"| **{label}** | {fmt_price(price)} | {arrow}{pct:.1f}% |")

    # Swing levels
    print(f"\n**Swing Highs/Lows (last {days} days)**\n")
    print("| Type | Price | Date | vs Last Close |")
    print("|---|---|---|---|")
    for s in swings:
        diff = s["price"] - last_close
        pct = diff / last_close * 100
        arrow = "+" if diff >= 0 else ""
        print(f"| Swing {s['type']} | {fmt_price(s['price'])} | {s['date']} | {arrow}{pct:.1f}% |")

    # ATR section
    atr = calc_atr(bars)
    if atr is not None:
        atr_pct = atr / last_close * 100
        long_stop = round(last_close - 2 * atr, 2)
        short_stop = round(last_close + 2 * atr, 2)
        print(f"**ATR14 (volatility-adjusted stops)**\n")
        print(f"| | Value | Note |")
        print(f"|---|---|---|")
        print(f"| ATR14 | {fmt_price(atr)} ({atr_pct:.1f}% of price) | avg daily range 14 days |")
        print(f"| Long stop (2×ATR below) | {fmt_price(long_stop)} | exit long if breaks here |")
        print(f"| Short stop (2×ATR above) | {fmt_price(short_stop)} | exit short if breaks here |")
        print()

    print()


def main():
    parser = argparse.ArgumentParser(description="S/R levels from Alpaca data")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols (e.g. AAPL SPY)")
    parser.add_argument("--days", type=int, default=30, help="Lookback days for swing levels (default: 30)")
    args = parser.parse_args()

    load_env()
    tickers = [t.upper() for t in args.tickers]

    print(f"# S/R Levels - {date.today()}")
    print(f"*Pivot points = previous trading day OHLC | Swings = last {args.days} days | Source: Alpaca*\n")
    print("---")

    try:
        all_bars = get_bars(tickers, args.days)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    for ticker in tickers:
        if ticker in all_bars:
            print_ticker(ticker, all_bars[ticker], args.days)
        else:
            print(f"\n### {ticker}\n  [warn] No data returned\n")


if __name__ == "__main__":
    main()
