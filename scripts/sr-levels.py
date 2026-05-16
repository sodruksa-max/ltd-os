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

import io
import os
import sys
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


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


def get_ticker_data(ticker: str, bars, days: int) -> dict | None:
    """Return computed data dict for a ticker (used by both full and brief modes)."""
    if not bars or len(bars) < 2:
        return None
    prev = bars[-2]
    last = bars[-1]
    year_bars = bars[-252:] if len(bars) >= 252 else bars
    last_c = _get(last, "close")
    pivots = calc_pivots(_get(prev, "high"), _get(prev, "low"), _get(prev, "close"))
    swings = find_swings(bars, lookback=days)
    valid_bars = [b for b in year_bars if _get(b, "low") > last_c * 0.5 and _get(b, "high") < last_c * 2.0]
    week52_high = max(_get(b, "high") for b in valid_bars) if valid_bars else last_c
    week52_low = min(_get(b, "low") for b in valid_bars) if valid_bars else last_c
    atr = calc_atr(bars)
    prev_ts = _get(prev, "timestamp")
    return {
        "ticker": ticker,
        "last": last_c,
        "prev_date": prev_ts.strftime("%Y-%m-%d") if hasattr(prev_ts, "strftime") else str(prev_ts)[:10],
        "prev_ohlc": (_get(prev, "open"), _get(prev, "high"), _get(prev, "low"), _get(prev, "close")),
        "pivots": pivots,
        "swings": swings,
        "week52_high": week52_high,
        "week52_low": week52_low,
        "atr": atr,
        "atr_pct": round(atr / last_c * 100, 1) if atr else None,
    }


def print_ticker_full(d: dict, days: int):
    """Original full output — all pivots, swings, ATR."""
    ticker, last_close = d["ticker"], d["last"]
    o, h, l, c = d["prev_ohlc"]
    print(f"\n### {ticker}")
    print(f"*Prev day ({d['prev_date']}): O={fmt_price(o)} H={fmt_price(h)} L={fmt_price(l)} C={fmt_price(c)} | Last close: {fmt_price(last_close)}*")
    print(f"*52W: H={fmt_price(d['week52_high'])} / L={fmt_price(d['week52_low'])}*\n")

    print("**Pivot Points (Classic)**\n")
    print("| Level | Price | vs Last Close |")
    print("|---|---|---|")
    for label in ["R3", "R2", "R1", "PP", "S1", "S2", "S3"]:
        price = d["pivots"][label]
        pct = (price - last_close) / last_close * 100
        arrow = "+" if pct >= 0 else ""
        print(f"| **{label}** | {fmt_price(price)} | {arrow}{pct:.1f}% |")

    print(f"\n**Swing Highs/Lows (last {days} days)**\n")
    print("| Type | Price | Date | vs Last Close |")
    print("|---|---|---|---|")
    for s in d["swings"]:
        pct = (s["price"] - last_close) / last_close * 100
        arrow = "+" if pct >= 0 else ""
        print(f"| Swing {s['type']} | {fmt_price(s['price'])} | {s['date']} | {arrow}{pct:.1f}% |")

    if d["atr"] is not None:
        atr, last_c = d["atr"], d["last"]
        print(f"**ATR14 (volatility-adjusted stops)**\n")
        print(f"| | Value | Note |")
        print(f"|---|---|---|")
        print(f"| ATR14 | {fmt_price(atr)} ({d['atr_pct']:.1f}% of price) | avg daily range 14 days |")
        print(f"| Long stop (2×ATR below) | {fmt_price(round(last_c - 2*atr, 2))} | exit long if breaks here |")
        print(f"| Short stop (2×ATR above) | {fmt_price(round(last_c + 2*atr, 2))} | exit short if breaks here |")
        print()
    print()


def print_brief_table(data_list: list[dict]):
    """
    --brief mode: single compact table — S1/S2/R1/R2 + ATR% + distance from S1.
    ~600 words vs ~2500 in full mode. Use for pre-market brief embedding.
    """
    print("| Ticker | Last | S2 | S1 | R1 | R2 | ATR% | vs S1 | Zone |")
    print("|--------|------|----|----|----|----|------|-------|------|")
    for d in data_list:
        last = d["last"]
        p = d["pivots"]
        s1, s2 = p["S1"], p["S2"]
        r1, r2 = p["R1"], p["R2"]
        vs_s1 = (last - s1) / s1 * 100
        atr_str = f"{d['atr_pct']:.1f}%" if d["atr_pct"] else "?"
        if vs_s1 <= 5.0:
            zone = "NEAR★"
        elif vs_s1 <= 15.0:
            zone = "MID"
        else:
            zone = "EXTENDED"
        print(
            f"| {d['ticker']} | {fmt_price(last)} | {fmt_price(s2)} | {fmt_price(s1)} "
            f"| {fmt_price(r1)} | {fmt_price(r2)} | {atr_str} | +{vs_s1:.1f}% | {zone} |"
        )


def main():
    parser = argparse.ArgumentParser(description="S/R levels from Alpaca data")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols (e.g. AAPL SPY)")
    parser.add_argument("--days", type=int, default=30, help="Lookback days for swing levels (default: 30)")
    parser.add_argument("--brief", action="store_true", help="Compact single-table output (~75%% fewer tokens)")
    args = parser.parse_args()

    load_env()
    tickers = [t.upper() for t in args.tickers]

    fetched_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print(f"# S/R Levels — {date.today()}" + (" (brief)" if args.brief else ""))
    print(f"*Source: Alpaca | Pivots = prev day OHLC | Swings = last {args.days} days | fetched: {fetched_at}*\n")

    try:
        all_bars = get_bars(tickers, args.days)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    data_list = []
    for ticker in tickers:
        if ticker in all_bars:
            d = get_ticker_data(ticker, all_bars[ticker], args.days)
            if d:
                data_list.append(d)
            else:
                print(f"  [warn] {ticker}: insufficient data")
        else:
            print(f"  [warn] {ticker}: no data returned")

    if args.brief:
        print_brief_table(data_list)
        print(f"\n*NEAR★ = ≤5% above S1 (good entry zone) | MID = 5-15% | EXTENDED = >15%*")
    else:
        print("---")
        for d in data_list:
            print_ticker_full(d, args.days)


if __name__ == "__main__":
    main()
