#!/usr/bin/env python3
"""
auto-trader: Daily screener bot — screens watchlist.json, ranks candidates,
and places one Alpaca paper order per day.

Flow: load watchlist → screen via universe-screen logic → filter EARLY+ALERT only
      → rank ALERT>EARLY, RS↑↑>RS↑>RS→ → skip held/full positions
      → buy top 1 candidate → log to trade-log.json

Usage:
    python scripts/auto-trader.py               # live paper mode
    python scripts/auto-trader.py --dry-run     # show plan, no orders
    python scripts/auto-trader.py --top 5       # consider top 5, buy 1 (default: 3)
"""

import os
import sys
import json
import argparse
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
WATCHLIST_PATH = Path(__file__).parent / "watchlist.json"
TRADE_LOG_PATH = Path(__file__).parent / "trade-log.json"

MAX_POSITIONS = 3       # max concurrent Alpaca paper positions before skipping
POSITION_SIZE_PCT = 0.10  # 10% of portfolio per trade
MAX_POSITION_USD = 500.0  # cap per trade at $500


# ---------------------------------------------------------------------------
# Env / secrets loading (same pattern as other scripts)
# ---------------------------------------------------------------------------

def load_env() -> None:
    """Read .secrets/.env key=value pairs into os.environ."""
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
# Watchlist loading
# ---------------------------------------------------------------------------

def load_watchlist() -> list[dict]:
    """Load all entries from watchlist.json. Returns empty list on failure."""
    if not WATCHLIST_PATH.exists():
        print("[warn] watchlist.json not found — nothing to screen")
        return []
    try:
        data = json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
        return data if data else []
    except Exception as e:
        print(f"[warn] watchlist.json parse error: {e}")
        return []


# ---------------------------------------------------------------------------
# Screening logic (imported from universe-screen.py)
# ---------------------------------------------------------------------------

# Add scripts/ to path so we can import universe-screen functions
sys.path.insert(0, str(Path(__file__).parent))

try:
    from universe_screen import (  # noqa: E402
        fetch_ohlcv, build_spy_map, analyze, rs_label,
        SECTOR_MAP, SECTOR_ETFS, calc_5d_momentum,
    )
    _SCREEN_IMPORT_OK = True
except ImportError:
    _SCREEN_IMPORT_OK = False


def _import_screen_funcs():
    """Fallback: import from universe-screen.py by loading the file directly."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "universe_screen",
        Path(__file__).parent / "universe-screen.py",
    )
    mod = importlib.util.load_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def screen_tickers(watchlist: list[dict]) -> list[dict]:
    """
    Run universe-screen analysis on all watchlist tickers.
    Returns list of analysis dicts enriched with watchlist metadata.
    Only EARLY and ALERT tiers are returned.
    """
    # Dynamic import to handle the hyphen in filename
    import importlib.util
    screen_path = Path(__file__).parent / "universe-screen.py"
    spec = importlib.util.spec_from_file_location("universe_screen", screen_path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore

    fetch_ohlcv_fn = mod.fetch_ohlcv
    build_spy_map_fn = mod.build_spy_map
    analyze_fn = mod.analyze
    calc_5d_mom_fn = mod.calc_5d_momentum
    sector_map = mod.SECTOR_MAP
    sector_etfs = mod.SECTOR_ETFS

    # Fetch SPY benchmark
    spy_bars = fetch_ohlcv_fn("SPY")
    spy_map = build_spy_map_fn(spy_bars) if spy_bars else {}

    # Fetch sector ETF momentum
    sector_5d: dict[str, float | None] = {}
    for etf in sector_etfs:
        etf_bars = fetch_ohlcv_fn(etf)
        sector_5d[etf] = calc_5d_mom_fn(etf_bars) if etf_bars else None

    results = []
    for entry in watchlist:
        ticker = entry["ticker"]
        bars = fetch_ohlcv_fn(ticker)
        if bars is None:
            continue

        etf_key = sector_map.get(ticker)
        sec_mom = sector_5d.get(etf_key) if etf_key else None
        r = analyze_fn(ticker, bars, spy_map, sector_momentum=sec_mom)

        # Only keep actionable tiers
        if r["tier"] not in ("EARLY", "ALERT"):
            continue

        # Enrich with watchlist metadata
        r["sector"] = entry.get("sector", etf_key or "?")
        r["tags"] = entry.get("tags", [])
        r["name"] = entry.get("name", ticker)
        results.append(r)

    return results


# ---------------------------------------------------------------------------
# Ranking
# ---------------------------------------------------------------------------

_TIER_RANK = {"ALERT": 0, "EARLY": 1}  # ALERT first (momentum confirmed)
_RS_RANK = {"RS↑↑": 0, "RS↑": 1, "RS→": 2, "RS↓": 3, "RS?": 4}


def rank_candidates(results: list[dict]) -> list[dict]:
    """Sort by: ALERT > EARLY, then RS↑↑ > RS↑ > RS→ > RS↓."""
    def sort_key(r):
        rs = r.get("rs_10d")
        rs_lbl = (
            "RS↑↑" if rs is not None and rs > 3.0 else
            "RS↑"  if rs is not None and rs > 1.0 else
            "RS→"  if rs is not None and rs > -1.0 else
            "RS↓"  if rs is not None else "RS?"
        )
        return (_TIER_RANK.get(r["tier"], 9), _RS_RANK.get(rs_lbl, 4))

    return sorted(results, key=sort_key)


# ---------------------------------------------------------------------------
# Alpaca account state
# ---------------------------------------------------------------------------

def get_trading_client():
    """Return Alpaca paper trading client. Exits if keys missing."""
    from alpaca.trading.client import TradingClient
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA_API_KEY / ALPACA_SECRET_KEY not set in .secrets/.env")
        sys.exit(1)
    return TradingClient(api_key, secret_key, paper=True)


def get_account_state(client) -> tuple[float, float, set[str], int]:
    """Returns (portfolio_value, buying_power, held_tickers_set, open_position_count)."""
    acct = client.get_account()
    positions = client.get_all_positions()
    held = {p.symbol for p in positions}
    portfolio_value = float(acct.portfolio_value or 0)
    buying_power = float(acct.buying_power or 0)
    return portfolio_value, buying_power, held, len(positions)


# ---------------------------------------------------------------------------
# Trade log
# ---------------------------------------------------------------------------

def load_trade_log() -> list[dict]:
    """Read trade-log.json. Returns empty list if file missing or empty."""
    if not TRADE_LOG_PATH.exists():
        return []
    try:
        text = TRADE_LOG_PATH.read_text(encoding="utf-8").strip()
        return json.loads(text) if text else []
    except Exception:
        return []


def append_trade_log(entry: dict) -> None:
    """Append one trade entry to trade-log.json."""
    log = load_trade_log()
    log.append(entry)
    TRADE_LOG_PATH.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# Order placement
# ---------------------------------------------------------------------------

def place_market_order(client, ticker: str, shares: int, dry_run: bool):
    """Place a market buy order. Prints action. Returns order or None."""
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce

    if dry_run:
        print(f"  [DRY RUN] would BUY {shares} x {ticker} (market order)")
        return None

    req = MarketOrderRequest(
        symbol=ticker,
        qty=shares,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )
    return client.submit_order(req)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Auto-trader: screen watchlist and place one paper order/day")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be bought, do not place orders")
    parser.add_argument("--top", type=int, default=3,
                        help="Consider top N candidates, always buy at most 1 (default: 3)")
    args = parser.parse_args()

    load_env()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    mode = "DRY RUN" if args.dry_run else "LIVE PAPER"
    print(f"## Auto-Trader -- {now} [{mode}]")
    print(f"Config: consider top {args.top}, buy 1, size=10% of portfolio (max ${MAX_POSITION_USD:.0f}), max_positions={MAX_POSITIONS}")
    print()

    # --- Load watchlist ---
    watchlist = load_watchlist()
    if not watchlist:
        print("No tickers in watchlist — nothing to screen. Run watchlist-manager.py --list to check.")
        sys.exit(0)
    print(f"Watchlist: {len(watchlist)} tickers loaded from watchlist.json")

    # --- Screen tickers ---
    print("Screening tickers (this may take 60-120 seconds)...")
    try:
        candidates = screen_tickers(watchlist)
    except Exception as e:
        print(f"ERROR: screening failed: {e}")
        sys.exit(1)

    print(f"Found {len(candidates)} actionable tickers (EARLY or ALERT tier)")
    if not candidates:
        print("No EARLY or ALERT setups today. Nothing to buy.")
        sys.exit(0)

    # --- Rank ---
    ranked = rank_candidates(candidates)
    top_n = ranked[:args.top]

    print()
    print(f"Top {len(top_n)} candidates (ranked ALERT>EARLY, RS↑↑>RS↑>RS→):")
    for i, r in enumerate(top_n, 1):
        rs_val = r.get("rs_10d")
        rs_str = (
            "RS↑↑" if rs_val is not None and rs_val > 3.0 else
            "RS↑"  if rs_val is not None and rs_val > 1.0 else
            "RS→"  if rs_val is not None and rs_val > -1.0 else
            "RS↓"  if rs_val is not None else "RS?"
        )
        print(f"  {i}. {r['ticker']:<7} [{r['tier']}] {rs_str} | RSI={r['rsi']} | "
              f"${r['price']:,.2f} | vs MA20={r['pct_vs_ma']:+.1f}%")
    print()

    # --- Alpaca account state ---
    try:
        client = get_trading_client()
        portfolio_value, buying_power, held, open_count = get_account_state(client)
    except Exception as e:
        print(f"ERROR: Alpaca connection failed: {e}")
        sys.exit(1)

    print(f"Account: portfolio=${portfolio_value:,.2f} | buying_power=${buying_power:,.2f} | "
          f"open_positions={open_count}/{MAX_POSITIONS}")

    if portfolio_value == 0:
        print()
        print("ERROR: Paper account has $0 — fund it at alpaca.markets > Paper Trading > Reset Account")
        sys.exit(1)

    if open_count >= MAX_POSITIONS:
        print(f"\nSkipping: already at max positions ({MAX_POSITIONS}). Nothing to buy today.")
        sys.exit(0)

    # --- Decision loop: find the first valid candidate and buy it ---
    print("Decisions:")
    bought = False
    for r in top_n:
        ticker = r["ticker"]
        price = r["price"]

        if ticker in held:
            print(f"  SKIP {ticker} — already holding")
            continue

        # Position sizing: 10% of portfolio, capped at MAX_POSITION_USD
        raw_size_usd = portfolio_value * POSITION_SIZE_PCT
        position_usd = min(raw_size_usd, MAX_POSITION_USD)
        shares = int(position_usd / price)  # whole shares only

        if shares < 1:
            print(f"  SKIP {ticker} — position ${position_usd:.0f} buys <1 share at ${price:,.2f}")
            continue

        cost = shares * price
        if cost > buying_power:
            print(f"  SKIP {ticker} — cost ${cost:,.0f} exceeds buying power ${buying_power:,.0f}")
            continue

        # Build RS label for log
        rs_val = r.get("rs_10d")
        rs_label_str = (
            "RS↑↑" if rs_val is not None and rs_val > 3.0 else
            "RS↑"  if rs_val is not None and rs_val > 1.0 else
            "RS→"  if rs_val is not None and rs_val > -1.0 else
            "RS↓"  if rs_val is not None else "RS?"
        )
        reason_str = f"universe-screen {r['tier']} {rs_label_str}"

        # Place order
        try:
            order = place_market_order(client, ticker, shares, args.dry_run)

            if args.dry_run or order:
                print(f"  BUY  {ticker} — {shares} sh @ ~${price:,.2f} (${cost:,.0f}) "
                      f"[{r['tier']} | {rs_label_str}]")
                if order:
                    print(f"       order_id={str(order.id)[:8]} status={order.status.value}")

                # Log the trade
                log_entry = {
                    "date": str(date.today()),
                    "ticker": ticker,
                    "action": "BUY",
                    "shares": shares,
                    "price": round(price, 2),
                    "tier": r["tier"],
                    "rs": rs_label_str,
                    "reason": reason_str,
                    "portfolio_value": round(portfolio_value, 2),
                    "dry_run": args.dry_run,
                }
                append_trade_log(log_entry)
                print(f"       Logged to trade-log.json")

                bought = True
                break  # buy exactly 1 per day

        except Exception as e:
            print(f"  ERROR {ticker} — order failed: {e}")
            continue

    print()
    if not bought:
        print("No order placed today (all candidates were skipped).")
    else:
        action = "Would buy" if args.dry_run else "Bought"
        print(f"Done: {action} 1 position.")
    print("Run /eod to see updated positions.")


if __name__ == "__main__":
    main()
