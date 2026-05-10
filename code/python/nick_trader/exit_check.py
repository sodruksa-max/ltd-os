"""
nick exit_check.py — daily exit checker for Nick paper positions.
Run every trading day at market open (9:30 AM ET).
Exits: stop -25% (full), target +50% (sell half, once only).
"""

import os
from datetime import date
from pathlib import Path
import json

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

REPO = Path(__file__).resolve().parents[3]
NICK_DIR = REPO / "vault/20_investment/nick"
TRADE_LOG = NICK_DIR / "trade-log.md"
STATE_FILE = NICK_DIR / "nick_state.json"

STOP_LOSS_PCT = -0.25
TARGET_PCT = 0.50


def load_state():
    return json.loads(STATE_FILE.read_text())


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def append_log(ticker, action, shares, price, pnl_pct, reason):
    with open(TRADE_LOG, "a", encoding="utf-8") as f:
        f.write(
            f"| {date.today()} | {ticker} | {action} | {shares} | ${price:.2f} | "
            f"- | - | - | - | - | {reason} (P&L: {pnl_pct:+.1f}%) |\n"
        )


def main():
    client = TradingClient(os.environ["ALPACA_API_KEY"], os.environ["ALPACA_SECRET_KEY"], paper=True)
    positions = client.get_all_positions()
    state = load_state()

    if not positions:
        print("No open positions.")
        return

    for pos in positions:
        ticker = pos.symbol
        qty = int(float(pos.qty))
        avg_cost = float(pos.avg_entry_price)
        current = float(pos.current_price)
        pnl_pct = (current - avg_cost) / avg_cost

        print(f"{ticker}: entry=${avg_cost:.2f}  current=${current:.2f}  P&L={pnl_pct:+.1%}  qty={qty}")

        if pnl_pct <= STOP_LOSS_PCT:
            client.submit_order(MarketOrderRequest(
                symbol=ticker, qty=qty, side=OrderSide.SELL, time_in_force=TimeInForce.DAY
            ))
            print(f"  STOP EXIT: {ticker} all {qty} shares")
            append_log(ticker, "STOP-EXIT", qty, current, pnl_pct * 100, "stop -25% triggered")
            state["positions"].pop(ticker, None)

        elif pnl_pct >= TARGET_PCT:
            pos_state = state["positions"].get(ticker, {})
            if pos_state.get("partial_taken"):
                print(f"  {ticker}: target already taken — trailing remainder")
                continue

            half = max(1, qty // 2)
            client.submit_order(MarketOrderRequest(
                symbol=ticker, qty=half, side=OrderSide.SELL, time_in_force=TimeInForce.DAY
            ))
            print(f"  TARGET PARTIAL: {ticker} sell {half}/{qty}")
            append_log(ticker, "TARGET-PARTIAL", half, current, pnl_pct * 100, "target +50% hit, sell half")
            state["positions"].setdefault(ticker, {})["partial_taken"] = True

    save_state(state)
    print("Exit check done.")


if __name__ == "__main__":
    main()
