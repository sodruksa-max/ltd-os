#!/usr/bin/env python3
"""
End-of-day swing position report.

Usage:
    code/python/.venv/Scripts/python scripts/eod-report.py

Two sections:
  1. Paper positions from Alpaca paper trading account (live, auto-tracked)
  2. Real positions from vault/20_investment/_journal/real-trades/*.md (manual, Dime broker)

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRADES_DIR = ROOT / "vault/20_investment/_journal/real-trades"
STOP_ALERT_PCT = 3.0


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


# ---------------------------------------------------------------------------
# Section 1 — Alpaca paper positions
# ---------------------------------------------------------------------------

def fetch_paper_positions():
    """Pull open positions from Alpaca paper trading account."""
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        return None, "ALPACA keys not set"
    try:
        from alpaca.trading.client import TradingClient
        client = TradingClient(api_key, secret_key, paper=True)
        positions = client.get_all_positions()
        acct = client.get_account()
        return positions, acct, None
    except Exception as e:
        return None, None, str(e)


def print_paper_section():
    result = fetch_paper_positions()
    if len(result) == 3:
        positions, acct, error = result
    else:
        positions, error = result
        acct = None

    print("### Paper Positions (Alpaca)")

    if error:
        print(f"[unavailable: {error}]")
        print()
        return

    if not positions:
        portfolio = float(acct.portfolio_value or 0) if acct else 0
        if portfolio == 0:
            print("[Paper account balance is $0]")
            print("Fund at: alpaca.markets -> Paper Trading -> Reset")
        else:
            print("No open paper positions.")
        print()
        return

    alerts = []
    print("| Ticker | Qty | Entry | Current | Unreal P&L | % | |")
    print("|--------|-----|-------|---------|------------|---|---|")

    total = 0.0
    for p in positions:
        qty = float(p.qty)
        entry = float(p.avg_entry_price)
        current = float(p.current_price)
        unreal = float(p.unrealized_pl)
        pct = float(p.unrealized_plpc) * 100
        total += unreal
        sign = "+" if unreal >= 0 else ""
        flag = ""
        # No stop/target info from Alpaca — show placeholder
        print(
            f"| **{p.symbol}** | {qty:.0f} | ${entry:,.2f} | ${current:,.2f} "
            f"| {sign}${unreal:,.2f} | {sign}{pct:.1f}% | {flag} |"
        )

    sign = "+" if total >= 0 else ""
    if acct:
        today_pl = float(acct.equity or 0) - float(acct.last_equity or 0)
        print(f"\n**Paper total unrealized:** {sign}${total:,.2f} | **Today P&L:** ${today_pl:+,.2f}")
    else:
        print(f"\n**Paper total unrealized:** {sign}${total:,.2f}")
    print()


# ---------------------------------------------------------------------------
# Section 2 — Real trades from markdown (Dime broker)
# ---------------------------------------------------------------------------

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
        print(f"[warn] Alpaca data error: {e}")
        return {}


def fmt(val, prefix="$"):
    if val is None:
        return "--"
    if prefix == "$":
        return f"${val:,.2f}"
    if prefix == "%":
        sign = "+" if val >= 0 else ""
        return f"{sign}{val:.1f}%"
    return str(val)


def print_real_section():
    print("### Real Positions (Dime broker — manual)")

    if not TRADES_DIR.exists():
        print("No trades directory found.")
        print()
        return

    open_trades = []
    for f in sorted(TRADES_DIR.glob("*.md")):
        data = parse_frontmatter(f)
        # Skip paper trades (tracked by Alpaca) and non-open trades
        if not data or data.get("status") != "open":
            continue
        if data.get("type") == "paper":
            continue
        ticker = data.get("ticker", "?")
        entry = to_float(data.get("entry_usd"))
        shares = to_float(data.get("shares"))
        stop = to_float(data.get("stop_usd"))
        target = to_float(data.get("target_usd"))
        direction = str(data.get("direction", "long")).lower()
        open_trades.append({
            "ticker": ticker, "entry": entry, "shares": shares,
            "stop": stop, "target": target, "direction": direction,
            "file": f.name,
        })

    if not open_trades:
        print("No open real positions.")
        print()
        return

    tickers = [t["ticker"] for t in open_trades if t["entry"] and t["shares"]]
    prices = get_prices(tickers) if tickers else {}
    alerts = []

    print("| Ticker | Dir | Entry | Close | Stop | Target | vs Stop | vs Target | Unreal P&L | |")
    print("|--------|-----|-------|-------|------|--------|---------|-----------|------------|---|")

    for t in open_trades:
        ticker = t["ticker"]
        entry = t["entry"]
        shares = t["shares"]
        stop = t["stop"]
        target = t["target"]
        direction = t["direction"]
        close = prices.get(ticker)

        if close and stop:
            vs_stop = (close - stop) / close * 100 if direction == "long" \
                      else (stop - close) / close * 100
        else:
            vs_stop = None

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

    total_unreal = sum(
        (prices.get(t["ticker"], 0) - t["entry"]) * t["shares"]
        if t["direction"] == "long"
        else (t["entry"] - prices.get(t["ticker"], 0)) * t["shares"]
        for t in open_trades
        if t["entry"] and t["shares"] and prices.get(t["ticker"])
    )
    print(f"\n**Real open positions:** {len(open_trades)} | **Total unrealized:** {fmt(total_unreal or None)}")

    if alerts:
        print("\n**ALERTS:**")
        for a in alerts:
            print(f"  - {a}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_env()
    now = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")
    fetched_at = now.strftime("%Y-%m-%d %H:%M UTC")
    print(f"## EOD Report -- {today}")
    print(f"*Source: Alpaca paper positions + real-trades/ | fetched: {fetched_at}*\n")

    print_paper_section()
    print_real_section()


if __name__ == "__main__":
    main()
