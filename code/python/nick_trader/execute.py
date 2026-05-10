"""
nick execute.py — read latest Nick weekly rec, place Alpaca paper orders.
Run manually after /nick-weekly, or on a schedule.
Rules: EARLY-only new entries, conviction sizing, regime tags logged every trade.
"""

import os
import re
import json
from datetime import date
from pathlib import Path

import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

REPO = Path(__file__).resolve().parents[3]
NICK_DIR = REPO / "vault/20_investment/nick"
WEEKLY_DIR = NICK_DIR / "weekly"
TRADE_LOG = NICK_DIR / "trade-log.md"
NAV_LOG = NICK_DIR / "performance/nav_log.md"
STATE_FILE = NICK_DIR / "nick_state.json"

CONVICTION_SIZE = {"high": 0.15, "med": 0.08, "low": 0.03}
STOP_LOSS_PCT = -0.25
TARGET_PCT = 0.50
MIN_CASH_PCT = 0.10
MAX_POSITION_PCT = 0.30


def load_state():
    return json.loads(STATE_FILE.read_text())


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_nav(client: TradingClient) -> float:
    try:
        account = client.get_account()
        return round(float(account.portfolio_value), 2)
    except Exception:
        return 10000.0


def append_nav_log(nav: float, note: str = ""):
    row = f"| {date.today()} | ${nav:,.2f} | - | - | {note} |\n"
    with open(NAV_LOG, "a", encoding="utf-8") as f:
        f.write(row)


def get_regime():
    data = {}
    for name, sym in {"VIX": "^VIX", "TNX": "^TNX", "SOXX": "SOXX", "QQQM": "QQQM"}.items():
        try:
            hist = yf.Ticker(sym).history(period="60d")["Close"]
            price = hist.iloc[-1]
            ma50 = hist.rolling(50).mean().iloc[-1]
            data[name] = {"value": round(float(price), 2), "above_50ma": bool(price > ma50)}
        except Exception:
            data[name] = {"value": None, "above_50ma": None}

    vix = data.get("VIX", {}).get("value") or 25
    data["tier"] = "EARLY" if vix < 20 else ("EXTENDED" if vix < 28 else "DANGER")
    return data


def get_latest_rec():
    files = sorted(WEEKLY_DIR.glob("*_weekly-rec.md"), reverse=True)
    if not files:
        return None, []
    rec_file = files[0]
    content = rec_file.read_text(encoding="utf-8")
    m = re.search(r"## ORDERS.*?```json\s*\n(\[.*?\])\s*\n```", content, re.DOTALL)
    if not m:
        print(f"No ORDERS block in {rec_file.name} — run /nick-weekly first")
        return rec_file, []
    return rec_file, json.loads(m.group(1))


def get_price(ticker):
    try:
        return float(yf.Ticker(ticker).fast_info["lastPrice"])
    except Exception:
        return None


def append_log(row):
    with open(TRADE_LOG, "a", encoding="utf-8") as f:
        f.write(
            "| {date} | {ticker} | {action} | {shares} | ${price:.2f} | "
            "{nav_pct} | {conviction} | {vix} | {tnx} | {soxx} | {reason} |\n".format(**row)
        )


def main():
    state = load_state()
    rec_file, orders = get_latest_rec()
    if not orders:
        return

    rec_name = rec_file.name
    if state.get("last_executed_rec") == rec_name:
        print(f"Already executed {rec_name} — skipping to avoid double-orders")
        return

    regime = get_regime()
    tier = regime["tier"]
    vix = regime.get("VIX", {}).get("value", "?")
    tnx = regime.get("TNX", {}).get("value", "?")
    soxx = "above50ma" if regime.get("SOXX", {}).get("above_50ma") else "below50ma"

    client = TradingClient(os.environ["ALPACA_API_KEY"], os.environ["ALPACA_SECRET_KEY"], paper=True)
    positions = {p.symbol: p for p in client.get_all_positions()}
    account = client.get_account()
    nav = get_nav(client)
    cash = float(account.cash)

    print(f"NAV: ${nav:,.0f}  |  Tier: {tier}  |  VIX: {vix}  |  10Y: {tnx}  |  SOXX: {soxx}")

    for order in orders:
        action = order.get("action", "").upper()
        ticker = order.get("ticker", "").upper()
        conviction = order.get("conviction", "med").lower()
        reason = order.get("reason", "")
        base_row = dict(date=date.today(), ticker=ticker, conviction=conviction,
                        vix=vix, tnx=tnx, soxx=soxx, reason=reason, price=0, shares=0, nav_pct="-")

        if action == "BUY":
            if tier == "DANGER":
                print(f"  SKIP {ticker}: tier=DANGER (VIX≥28 — no new entries)")
                append_log({**base_row, "action": "SKIP-DANGER", "reason": "blocked: VIX≥28"})
                continue
            if tier == "EXTENDED" and conviction != "high":
                print(f"  SKIP {ticker}: tier=EXTENDED, conviction={conviction} (high-only in EXTENDED)")
                append_log({**base_row, "action": "SKIP-EXTENDED", "reason": f"blocked: EXTENDED requires high conviction, got {conviction}"})
                continue

            if ticker in positions:
                print(f"  SKIP {ticker}: already have position")
                continue

            price = get_price(ticker)
            if not price:
                print(f"  SKIP {ticker}: cannot get price")
                continue

            size_pct = CONVICTION_SIZE.get(conviction, 0.03)
            target_value = min(nav * size_pct, nav * MAX_POSITION_PCT)

            if cash * (1 - MIN_CASH_PCT) < target_value:
                print(f"  SKIP {ticker}: cash too low (${cash:.0f})")
                continue

            shares = int(target_value / price)
            if shares < 1:
                continue

            client.submit_order(MarketOrderRequest(
                symbol=ticker, qty=shares, side=OrderSide.BUY, time_in_force=TimeInForce.DAY
            ))
            print(f"  BUY {shares} {ticker} @ ~${price:.2f}  ({size_pct*100:.0f}% NAV)")
            append_log({**base_row, "action": "BUY", "shares": shares, "price": price,
                        "nav_pct": f"{size_pct*100:.0f}%"})
            state["positions"][ticker] = {"partial_taken": False, "entry_date": str(date.today())}
            cash -= shares * price

        elif action in ("SELL", "TRIM"):
            if ticker not in positions:
                print(f"  SKIP {action} {ticker}: no position")
                continue
            pos = positions[ticker]
            qty = int(float(pos.qty))
            sell_qty = max(1, qty // 2) if action == "TRIM" else qty

            client.submit_order(MarketOrderRequest(
                symbol=ticker, qty=sell_qty, side=OrderSide.SELL, time_in_force=TimeInForce.DAY
            ))
            price = float(pos.current_price)
            print(f"  {action} {sell_qty} {ticker} @ ~${price:.2f}")
            append_log({**base_row, "action": action, "shares": sell_qty, "price": price})
            if action == "SELL":
                state["positions"].pop(ticker, None)

    state["last_executed_rec"] = rec_name
    save_state(state)

    # Update NAV log with post-trade portfolio value
    nav_after = get_nav(client)
    orders_executed = [o for o in orders if o.get("action", "").upper() in ("BUY", "SELL", "TRIM")]
    note = f"post-execute: {len(orders_executed)} orders from {rec_name}"
    append_nav_log(nav_after, note)
    print(f"NAV log updated: ${nav_after:,.2f}")
    print("Done.")


if __name__ == "__main__":
    main()
