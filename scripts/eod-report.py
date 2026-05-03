#!/usr/bin/env python3
"""
End-of-day swing position report.

Usage:
    code/python/.venv/Scripts/python scripts/eod-report.py

Reads open positions from vault/20_investment/_journal/real-trades/
Fetches latest price from Alpaca, then shows per position:
  - Current price vs entry
  - Distance to stop loss (alert if within 3%)
  - Distance to target
  - Unrealized P&L

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRADES_DIR = ROOT / "vault/20_investment/_journal/real-trades"
STOP_ALERT_PCT = 3.0  # alert if price within this % of stop


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


def parse_frontmatter(filepath: Path) -> dict:
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if val in ("~", "", "null", "None"):
            val = None
        data[key] = val
    return data


def to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def get_prices(tickers: list[str]) -> dict[str, float]:
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("[warn] ALPACA keys not set -- prices unavailable")
        return {}
    try:
        from alpaca.data import StockHistoricalDataClient
        from alpaca.data.requests import StockLatestTradeRequest
        client = StockHistoricalDataClient(api_key, secret_key)
        resp = client.get_stock_latest_trade(
            StockLatestTradeRequest(symbol_or_symbols=tickers)
        )
        return {t: resp[t].price for t in tickers if t in resp}
    except Exception as e:
        print(f"[warn] Alpaca error: {e}")
        return {}


def pct(a, b):
    if a and b:
        return (a - b) / b * 100
    return None


def fmt(val, prefix="$"):
    if val is None:
        return "--"
    if prefix == "$":
        return f"${val:,.2f}"
    if prefix == "%":
        sign = "+" if val >= 0 else ""
        return f"{sign}{val:.1f}%"
    return str(val)


def main():
    load_env()

    if not TRADES_DIR.exists():
        print(f"No trades directory: {TRADES_DIR}")
        return

    open_trades = []
    for f in sorted(TRADES_DIR.glob("*.md")):
        data = parse_frontmatter(f)
        if not data or data.get("status") != "open":
            continue
        ticker  = data.get("ticker", "?")
        entry   = to_float(data.get("entry_usd"))
        shares  = to_float(data.get("shares"))
        stop    = to_float(data.get("stop_usd"))
        target  = to_float(data.get("target_usd"))
        direction = str(data.get("direction", "long")).lower()
        open_trades.append({
            "ticker": ticker, "entry": entry, "shares": shares,
            "stop": stop, "target": target, "direction": direction,
            "file": f.name,
        })

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"## EOD Report -- {today}")

    if not open_trades:
        print("No open positions.")
        return

    tickers = [t["ticker"] for t in open_trades if t["entry"] and t["shares"]]
    prices = get_prices(tickers) if tickers else {}

    alerts = []

    print("")
    print("| Ticker | Dir | Entry | Close | Stop | Target | vs Stop | vs Target | Unreal P&L | |")
    print("|--------|-----|-------|-------|------|--------|---------|-----------|------------|---|")

    for t in open_trades:
        ticker  = t["ticker"]
        entry   = t["entry"]
        shares  = t["shares"]
        stop    = t["stop"]
        target  = t["target"]
        direction = t["direction"]
        close   = prices.get(ticker)

        # vs stop: % price must move to hit stop (positive = safe, negative = already past stop)
        if close and stop:
            vs_stop = (close - stop) / close * 100 if direction == "long" \
                      else (stop - close) / close * 100
        else:
            vs_stop = None

        # vs target: % price must move to hit target
        if close and target:
            vs_target = (target - close) / close * 100 if direction == "long" \
                        else (close - target) / close * 100
        else:
            vs_target = None

        unreal = None
        if close and entry and shares:
            unreal = (close - entry) * shares if direction == "long" \
                     else (entry - close) * shares

        flag = ""
        if vs_stop is not None and vs_stop < STOP_ALERT_PCT:
            flag = "STOP NEAR"
            alerts.append(f"{ticker}: {vs_stop:.1f}% from stop")

        print(
            f"| **{ticker}** | {direction[0].upper()} "
            f"| {fmt(entry)} | {fmt(close)} | {fmt(stop)} | {fmt(target)} "
            f"| {fmt(vs_stop, '%')} | {fmt(vs_target, '%')} "
            f"| {fmt(unreal)} | {flag} |"
        )

    # Summary
    total_unreal = sum(
        (prices.get(t["ticker"], 0) - t["entry"]) * t["shares"]
        if t["direction"] == "long"
        else (t["entry"] - prices.get(t["ticker"], 0)) * t["shares"]
        for t in open_trades
        if t["entry"] and t["shares"] and prices.get(t["ticker"])
    )

    print(f"\n**Open positions:** {len(open_trades)} | "
          f"**Total unrealized:** {fmt(total_unreal if total_unreal else None)}")

    if alerts:
        print("\n**ALERTS:**")
        for a in alerts:
            print(f"  - {a}")


if __name__ == "__main__":
    main()
