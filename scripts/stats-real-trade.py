#!/usr/bin/env python3
"""
Real money portfolio tracker with Alpaca real-time quotes.

Usage:
    code/python/.venv/Scripts/python scripts/stats-real-trade.py

Reads all .md files in vault/20_investment/_journal/real-trades/
- Open positions: fetches current price from Alpaca → unrealized P&L
- Closed positions: realized gain, R-multiple, broker fees
- Annual summary for tax (ภ.ง.ด. 90/91)
Updates vault/20_investment/portfolio-real.md
"""

import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRADES_DIR = ROOT / "vault/20_investment/_journal/real-trades"
PORTFOLIO_FILE = ROOT / "vault/20_investment/portfolio-real.md"


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


def to_float(val) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def get_current_prices(tickers: list[str]) -> dict[str, float]:
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        print("  [warn] ALPACA_API_KEY / ALPACA_SECRET_KEY not set — skipping real-time prices")
        return {}

    try:
        from alpaca.data import StockHistoricalDataClient
        from alpaca.data.requests import StockLatestTradeRequest

        client = StockHistoricalDataClient(api_key, secret_key)
        request = StockLatestTradeRequest(symbol_or_symbols=tickers)
        trades = client.get_stock_latest_trade(request)
        return {ticker: trades[ticker].price for ticker in tickers if ticker in trades}
    except Exception as e:
        print(f"  [warn] Alpaca API error: {e}")
        return {}


def calc_r(entry: float, stop: float, exit_price: float, direction: str) -> float:
    risk = abs(entry - stop)
    if risk == 0:
        return 0.0
    if direction == "long":
        return round((exit_price - entry) / risk, 2)
    return round((entry - exit_price) / risk, 2)


def main():
    if not TRADES_DIR.exists():
        print(f"Trades directory not found: {TRADES_DIR}")
        return

    open_trades = []
    closed_trades = []

    for f in sorted(TRADES_DIR.glob("*.md")):
        data = parse_frontmatter(f)
        if not data:
            continue

        status = data.get("status", "open")
        ticker = data.get("ticker", "?")
        direction = str(data.get("direction", "long")).lower()
        entry = to_float(data.get("entry_usd"))
        shares = to_float(data.get("shares"))
        fees = to_float(data.get("fees_usd")) or 0.0
        exit_fees = to_float(data.get("exit_fees_usd")) or 0.0
        stop = to_float(data.get("stop_usd"))
        exit_p = to_float(data.get("exit_usd"))

        trade = {
            "ticker": ticker,
            "direction": direction,
            "date_open": str(data.get("date_open", "?")),
            "date_close": str(data.get("date_close", "?")),
            "entry": entry,
            "shares": shares,
            "fees": fees,
            "exit_fees": exit_fees,
            "stop": stop,
        }

        if status == "closed" and entry and shares and exit_p:
            if direction == "long":
                realized = (exit_p - entry) * shares - fees - exit_fees
            else:
                realized = (entry - exit_p) * shares - fees - exit_fees

            r = calc_r(entry, stop, exit_p, direction) if stop else None
            result = "win" if realized > 0 else ("loss" if realized < 0 else "breakeven")

            trade.update({
                "cost_basis": entry * shares + fees,
                "exit": exit_p,
                "realized_gain": round(realized, 2),
                "r_multiple": r,
                "result": result,
                "year": str(data.get("date_close", ""))[:4],
            })
            closed_trades.append(trade)
        else:
            open_trades.append(trade)

    # Fetch real-time prices for open positions
    open_tickers = [t["ticker"] for t in open_trades if t["entry"] and t["shares"]]
    prices = get_current_prices(open_tickers) if open_tickers else {}

    total_unrealized = 0.0
    for t in open_trades:
        current = prices.get(t["ticker"])
        if t["entry"] and t["shares"] and current:
            pnl = (current - t["entry"]) if t["direction"] == "long" else (t["entry"] - current)
            t["unrealized"] = round(pnl * t["shares"] - t["fees"], 2)
            t["current_price"] = current
            total_unrealized += t["unrealized"]
        else:
            t["unrealized"] = None
            t["current_price"] = None

    # Aggregate stats
    total_realized = sum(t["realized_gain"] for t in closed_trades)
    total_fees = sum(t["fees"] + t["exit_fees"] for t in closed_trades)
    wins = sum(1 for t in closed_trades if t["result"] == "win")
    losses = sum(1 for t in closed_trades if t["result"] == "loss")
    win_rate = round(wins / len(closed_trades) * 100, 1) if closed_trades else 0.0
    r_values = [t["r_multiple"] for t in closed_trades if t["r_multiple"] is not None]
    avg_r = round(sum(r_values) / len(r_values), 2) if r_values else 0.0

    annual_gain: dict[str, float] = defaultdict(float)
    annual_fees_map: dict[str, float] = defaultdict(float)
    for t in closed_trades:
        year = t.get("year", "?")
        annual_gain[year] += t["realized_gain"]
        annual_fees_map[year] += t["fees"] + t["exit_fees"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    unrealized_line = f"${total_unrealized:+,.2f}" if open_tickers and prices else "— (no API or no open position)"

    # Open positions table
    open_rows = []
    for t in open_trades:
        cp = f"${t['current_price']:.2f}" if t["current_price"] else "—"
        unreal = f"${t['unrealized']:+,.2f}" if t["unrealized"] is not None else "—"
        entry_str = f"${t['entry']:.2f}" if t["entry"] else "—"
        shares_str = str(int(t["shares"])) if t["shares"] else "—"
        open_rows.append(f"| {t['date_open']} | {t['ticker']} | {t['direction']} | {entry_str} | {cp} | {shares_str} | {unreal} |")
    open_table = "\n".join(open_rows) if open_rows else "| — | — | — | — | — | — | — |"

    # Closed trades table
    closed_rows = []
    for t in closed_trades:
        r_str = f"{t['r_multiple']:+.2f}R" if t["r_multiple"] is not None else "—"
        wl = {"win": "W", "loss": "L", "breakeven": "B"}.get(t["result"], "?")
        gain_str = f"${t['realized_gain']:+,.2f}"
        entry_str = f"${t['entry']:.2f}" if t["entry"] else "—"
        exit_str = f"${t['exit']:.2f}" if t["exit"] else "—"
        shares_str = str(int(t["shares"])) if t["shares"] else "—"
        closed_rows.append(
            f"| {t['date_close']} | {t['ticker']} | {t['direction']} "
            f"| {entry_str} | {exit_str} | {shares_str} | {gain_str} | {r_str} | {wl} |"
        )
    closed_table = "\n".join(closed_rows) if closed_rows else "| — | — | — | — | — | — | — | — | — |"

    # Annual tax table
    tax_rows = []
    for year in sorted(annual_gain.keys()):
        net = annual_gain[year]
        fees_total = annual_fees_map[year]
        tax_rows.append(f"| {year} | ${net:+,.2f} | ${fees_total:,.2f} | ${net:+,.2f} |")
    tax_table = "\n".join(tax_rows) if tax_rows else "| — | — | — | — |"

    content = f"""# Real Money Portfolio — Dashboard
*Updated: {now} | คำนวณอัตโนมัติจาก `scripts/stats-real-trade.py` | ราคาจาก Alpaca*

---

## Overview

| Metric | Value |
|---|---|
| **Open positions** | {len(open_trades)} |
| **Unrealized P&L** | {unrealized_line} |
| **Closed trades** | {len(closed_trades)} |
| **Realized P&L (net fees)** | ${total_realized:+,.2f} |
| **Total fees paid** | ${total_fees:,.2f} |
| **Win rate** | {win_rate}% ({wins}W / {losses}L) |
| **Avg R-multiple** | {avg_r:+.2f}R |

---

## Open Positions

| Date | Ticker | Dir | Entry | Current | Shares | Unrealized P&L |
|---|---|---|---|---|---|---|
{open_table}

*ราคา current จาก Alpaca (อาจ delay 15 นาที สำหรับ free tier)*

---

## Closed Trades

| Date closed | Ticker | Dir | Entry | Exit | Shares | Net P&L | R | W/L |
|---|---|---|---|---|---|---|---|---|
{closed_table}

---

## Annual Summary (สรุปภาษีรายปี)

| ปี | Realized Gain (USD) | ค่าธรรมเนียมรวม | กำไรสุทธิ |
|---|---|---|---|
{tax_table}

*สำหรับ ภ.ง.ด. 90/91: แปลง USD → THB ที่อัตราวันที่ทำการค้า (ดูที่ BOT หรือ Dime statement)*

---

## วิธีใช้

1. Copy `vault/_templates/real-trade-template.md`
   → บันทึกเป็น `vault/20_investment/_journal/real-trades/YYYY-MM-DD-TICKER.md`
2. กรอก frontmatter: ticker, direction, entry_usd, shares, fees_usd, stop_usd, date_open
3. ตอนปิด trade: กรอก exit_usd, exit_fees_usd, date_close → เปลี่ยน status → closed
4. รัน: `code/python/.venv/Scripts/python scripts/stats-real-trade.py`
"""

    PORTFOLIO_FILE.write_text(content, encoding="utf-8")
    print(f"Portfolio updated -> {PORTFOLIO_FILE.relative_to(ROOT)}")
    print(f"  Open: {len(open_trades)} | Closed: {len(closed_trades)} | Realized: ${total_realized:+,.2f} | Unrealized: {unrealized_line}")


if __name__ == "__main__":
    main()
