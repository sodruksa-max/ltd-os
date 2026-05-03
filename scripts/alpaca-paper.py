#!/usr/bin/env python3
"""
Alpaca Paper Trading — place and manage paper trades via Alpaca API.

Usage:
    python scripts/alpaca-paper.py account
    python scripts/alpaca-paper.py positions
    python scripts/alpaca-paper.py orders
    python scripts/alpaca-paper.py buy  TICKER SHARES [--limit PRICE] [--stop PRICE]
    python scripts/alpaca-paper.py sell TICKER SHARES [--limit PRICE]
    python scripts/alpaca-paper.py cancel ORDER_ID

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
Uses Alpaca paper trading endpoint (paper=True) — no real money involved.
"""

import os
import sys
from pathlib import Path


def load_env():
    env_file = Path(__file__).parent.parent / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def get_client():
    from alpaca.trading.client import TradingClient
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA_API_KEY / ALPACA_SECRET_KEY not set in .secrets/.env")
        sys.exit(1)
    return TradingClient(api_key, secret_key, paper=True)


def cmd_account(client):
    acct = client.get_account()
    portfolio = float(acct.portfolio_value or 0)
    cash = float(acct.cash or 0)
    buying_power = float(acct.buying_power or 0)
    equity = float(acct.equity or 0)
    last_equity = float(acct.last_equity or 0)
    long_val = float(acct.long_market_value or 0)
    today_pl = equity - last_equity

    print("## Alpaca Paper Account")
    print(f"  Portfolio value : ${portfolio:>12,.2f}")
    print(f"  Cash            : ${cash:>12,.2f}")
    print(f"  Buying power    : ${buying_power:>12,.2f}")
    print(f"  Long mkt value  : ${long_val:>12,.2f}")
    print(f"  Today P&L       : ${today_pl:>+12,.2f}")

    if portfolio == 0 and cash == 0:
        print()
        print("  [!] Paper account has $0 — fund it at alpaca.markets:")
        print("      Dashboard -> Paper Trading -> Reset -> set starting balance (e.g. $100,000)")


def cmd_positions(client):
    positions = client.get_all_positions()
    if not positions:
        print("No open paper positions.")
        return
    print("## Paper Positions (Alpaca)")
    print(f"{'Ticker':<8} {'Qty':>6} {'Entry':>10} {'Current':>10} {'Unreal P&L':>12} {'%':>8}")
    print("-" * 58)
    total = 0.0
    for p in positions:
        qty = float(p.qty)
        entry = float(p.avg_entry_price)
        current = float(p.current_price)
        unreal = float(p.unrealized_pl)
        pct = float(p.unrealized_plpc) * 100
        total += unreal
        sign = "+" if unreal >= 0 else ""
        print(f"{p.symbol:<8} {qty:>6.0f} ${entry:>9,.2f} ${current:>9,.2f} {sign}${unreal:>10,.2f} {sign}{pct:>6.1f}%")
    print("-" * 58)
    sign = "+" if total >= 0 else ""
    print(f"{'Total':>38} {sign}${total:>10,.2f}")


def cmd_orders(client):
    from alpaca.trading.requests import GetOrdersRequest
    from alpaca.trading.enums import QueryOrderStatus
    orders = client.get_orders(GetOrdersRequest(status=QueryOrderStatus.ALL, limit=20))
    if not orders:
        print("No recent orders.")
        return
    print("## Recent Orders (Alpaca Paper)")
    print(f"{'ID':>10}  {'Symbol':<7} {'Side':<5} {'Qty':>6}  {'Type':<10} {'Status':<12} {'Fill':>10}")
    print("-" * 68)
    for o in orders:
        filled = f"${float(o.filled_avg_price):,.2f}" if o.filled_avg_price else "--"
        print(
            f"{str(o.id)[:10]:>10}  {o.symbol:<7} {o.side.value:<5} "
            f"{float(o.qty):>6.0f}  {o.order_type.value:<10} {o.status.value:<12} {filled:>10}"
        )


def cmd_buy(client, ticker, shares, limit=None, stop=None):
    from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopLimitOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce

    ticker = ticker.upper()
    qty = float(shares)

    if stop and limit:
        req = StopLimitOrderRequest(
            symbol=ticker, qty=qty,
            side=OrderSide.BUY, time_in_force=TimeInForce.DAY,
            limit_price=float(limit), stop_price=float(stop),
        )
        desc = f"stop-limit (stop ${float(stop):.2f} / limit ${float(limit):.2f})"
    elif limit:
        req = LimitOrderRequest(
            symbol=ticker, qty=qty,
            side=OrderSide.BUY, time_in_force=TimeInForce.DAY,
            limit_price=float(limit),
        )
        desc = f"limit @ ${float(limit):.2f}"
    else:
        req = MarketOrderRequest(
            symbol=ticker, qty=qty,
            side=OrderSide.BUY, time_in_force=TimeInForce.DAY,
        )
        desc = "market"

    order = client.submit_order(req)
    print(f"BUY order submitted: {qty:.0f} x {ticker} ({desc})")
    print(f"  Order ID : {order.id}")
    print(f"  Status   : {order.status.value}")


def cmd_sell(client, ticker, shares, limit=None):
    from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce

    ticker = ticker.upper()
    qty = float(shares)

    if limit:
        req = LimitOrderRequest(
            symbol=ticker, qty=qty,
            side=OrderSide.SELL, time_in_force=TimeInForce.DAY,
            limit_price=float(limit),
        )
        desc = f"limit @ ${float(limit):.2f}"
    else:
        req = MarketOrderRequest(
            symbol=ticker, qty=qty,
            side=OrderSide.SELL, time_in_force=TimeInForce.DAY,
        )
        desc = "market"

    order = client.submit_order(req)
    print(f"SELL order submitted: {qty:.0f} x {ticker} ({desc})")
    print(f"  Order ID : {order.id}")
    print(f"  Status   : {order.status.value}")


def cmd_cancel(client, order_id):
    client.cancel_order_by_id(order_id)
    print(f"Order {order_id} cancelled.")


def parse_flags(args):
    flags = {}
    i = 0
    while i < len(args):
        if args[i] in ("--limit", "--stop") and i + 1 < len(args):
            flags[args[i].lstrip("-")] = args[i + 1]
            i += 2
        else:
            i += 1
    return flags


def main():
    load_env()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()

    try:
        client = get_client()
    except Exception as e:
        print(f"ERROR connecting to Alpaca paper API: {e}")
        sys.exit(1)

    try:
        if cmd == "account":
            cmd_account(client)
        elif cmd == "positions":
            cmd_positions(client)
        elif cmd == "orders":
            cmd_orders(client)
        elif cmd == "buy":
            if len(sys.argv) < 4:
                print("Usage: buy TICKER SHARES [--limit PRICE] [--stop PRICE]")
                sys.exit(1)
            flags = parse_flags(sys.argv[4:])
            cmd_buy(client, sys.argv[2], sys.argv[3],
                    limit=flags.get("limit"), stop=flags.get("stop"))
        elif cmd == "sell":
            if len(sys.argv) < 4:
                print("Usage: sell TICKER SHARES [--limit PRICE]")
                sys.exit(1)
            flags = parse_flags(sys.argv[4:])
            cmd_sell(client, sys.argv[2], sys.argv[3], limit=flags.get("limit"))
        elif cmd == "cancel":
            if len(sys.argv) < 3:
                print("Usage: cancel ORDER_ID")
                sys.exit(1)
            cmd_cancel(client, sys.argv[2])
        else:
            print(f"Unknown command: {cmd}")
            print(__doc__)
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
