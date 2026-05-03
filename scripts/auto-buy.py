#!/usr/bin/env python3
"""
Auto-buy — screens watchlist and places Alpaca paper orders for top picks.

Usage:
    python scripts/auto-buy.py              # screen + buy (dry-run OFF = places real paper orders)
    python scripts/auto-buy.py --dry-run    # show what WOULD be bought, no orders placed
    python scripts/auto-buy.py --top 3      # consider top 3 screener picks (default: 2)
    python scripts/auto-buy.py --size 0.05  # position size as fraction of portfolio (default: 5%)

Rules applied (from PREFERENCES.md):
  1. Max 4 concurrent positions — skip if already at limit
  2. Skip tickers already held in portfolio
  3. Position size = size_pct * portfolio_value (round down to whole shares)
  4. Skip if buying power < position_size
  5. Place market order (fills at next tick)
  6. Log every decision with reason

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
Paper account must be funded (see: alpaca-paper.py account)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
MAX_POSITIONS = 4
DEFAULT_SIZE_PCT = 0.05   # 5% of portfolio per trade
DEFAULT_TOP_N = 2          # consider top N screener picks per run


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


def get_trading_client():
    from alpaca.trading.client import TradingClient
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA keys not set in .secrets/.env")
        sys.exit(1)
    return TradingClient(api_key, secret_key, paper=True)


def get_account_state(client):
    """Returns (portfolio_value, buying_power, held_tickers, open_count)."""
    acct = client.get_account()
    positions = client.get_all_positions()
    held = {p.symbol for p in positions}
    portfolio_value = float(acct.portfolio_value or 0)
    buying_power = float(acct.buying_power or 0)
    return portfolio_value, buying_power, held, len(positions)


def run_screener(top_n):
    """Run screener.py and return top N results as list of dicts."""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "screener.py"), "--json"],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode != 0:
        print(f"[warn] screener failed: {result.stderr.strip()}")
        return []
    import json
    try:
        all_results = json.loads(result.stdout)
        return all_results[:top_n]
    except Exception as e:
        print(f"[warn] screener output parse error: {e}")
        return []


def place_order(client, ticker, shares, dry_run):
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
    if dry_run:
        print(f"  [DRY RUN] would BUY {shares} x {ticker} (market)")
        return None
    req = MarketOrderRequest(
        symbol=ticker, qty=shares,
        side=OrderSide.BUY, time_in_force=TimeInForce.DAY,
    )
    order = client.submit_order(req)
    return order


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Auto-buy paper trades")
    parser.add_argument("--dry-run", action="store_true", help="Show plan, do not place orders")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP_N, help="Top N screener picks to consider")
    parser.add_argument("--size", type=float, default=DEFAULT_SIZE_PCT, help="Position size as fraction of portfolio (0.05 = 5%%)")
    args = parser.parse_args()

    load_env()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    mode = "DRY RUN" if args.dry_run else "LIVE PAPER"
    print(f"## Auto-Buy Run -- {now} [{mode}]")
    print(f"Config: top={args.top}, size={args.size*100:.0f}% per trade, max_positions={MAX_POSITIONS}")
    print()

    # --- Account state ---
    try:
        client = get_trading_client()
        portfolio_value, buying_power, held, open_count = get_account_state(client)
    except Exception as e:
        print(f"ERROR: Alpaca connection failed: {e}")
        sys.exit(1)

    print(f"Account: portfolio=${portfolio_value:,.2f} | buying_power=${buying_power:,.2f} | open_positions={open_count}/{MAX_POSITIONS}")

    if portfolio_value == 0:
        print()
        print("ERROR: Paper account has $0 — fund it first:")
        print("  alpaca.markets -> Paper Trading -> Reset Account")
        sys.exit(1)

    slots_available = MAX_POSITIONS - open_count
    if slots_available <= 0:
        print(f"\nNo slots available (already at {MAX_POSITIONS} positions). Nothing to buy.")
        sys.exit(0)

    print(f"Slots available: {slots_available}")
    print()

    # --- Run screener ---
    print(f"Running screener (top {args.top} picks)...")
    candidates = run_screener(args.top)
    if not candidates:
        print("Screener returned no candidates.")
        sys.exit(0)

    print(f"Screener top {len(candidates)}:")
    for i, c in enumerate(candidates, 1):
        rs_sign = "+" if c["rs_vs_spy_pct"] >= 0 else ""
        print(f"  {i}. {c['ticker']:<8} ${c['price']:,.2f}  RS={rs_sign}{c['rs_vs_spy_pct']:.1f}%  vol={c['vol_ratio']:.1f}x  score={c['score']:.4f}")
    print()

    # --- Decision loop ---
    bought = 0
    position_size_usd = portfolio_value * args.size

    print("Decisions:")
    for c in candidates:
        ticker = c["ticker"]
        price = c["price"]

        if bought >= slots_available:
            print(f"  SKIP {ticker} — no more slots this run")
            continue

        if ticker in held:
            print(f"  SKIP {ticker} — already holding")
            continue

        shares = int(position_size_usd / price)
        if shares < 1:
            print(f"  SKIP {ticker} — position size ${position_size_usd:,.0f} buys <1 share at ${price:,.2f}")
            continue

        cost = shares * price
        if cost > buying_power:
            print(f"  SKIP {ticker} — cost ${cost:,.0f} exceeds buying power ${buying_power:,.0f}")
            continue

        if not c["above_ma50"]:
            print(f"  SKIP {ticker} — below 50-day MA (trend filter)")
            continue

        # Place order
        try:
            order = place_order(client, ticker, shares, args.dry_run)
            if order:
                print(f"  BUY  {ticker} — {shares} shares @ ~${price:,.2f} (${cost:,.0f}) | order_id={str(order.id)[:8]} status={order.status.value}")
                buying_power -= cost
                held.add(ticker)
            bought += 1
        except Exception as e:
            print(f"  ERROR {ticker} — order failed: {e}")

    print()
    if bought == 0:
        print("No orders placed this run.")
    else:
        action = "would place" if args.dry_run else "placed"
        print(f"Done: {action} {bought} order(s).")
    print("Run /eod to see updated positions.")


if __name__ == "__main__":
    main()
