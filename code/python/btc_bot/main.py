"""
main.py — BTC/USDT trading bot orchestrator

Pipeline per 1h bar:
  data -> signals -> regime -> sizer -> risk -> executor

State tracked in-memory (no DB):
  position_btc   : BTC currently held
  entry_price    : price at which position was opened
  peak_nav       : highest portfolio NAV seen (for drawdown calc)

Usage:
  python btc_bot/main.py              # live dry-run (default)
  python btc_bot/main.py --live       # real orders (needs Binance keys)
  python btc_bot/main.py --once       # run once, print signal, exit

Config:
  NAV             : set initial portfolio size below
  DRY_RUN         : overridden by --live flag
  SCAN_INTERVAL_S : seconds between scans (3600 = 1h, aligned to bar close)
"""

import argparse
import time
from datetime import datetime, timezone

from btc_bot.data     import fetch_ohlcv, fetch_price
from btc_bot.signals  import get_signal
from btc_bot.regime   import get_regime
from btc_bot.sizer    import get_size
from btc_bot.risk     import check_entry, check_stop, update_peak
from btc_bot.executor import market_buy, market_sell

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

NAV_INITIAL     = 10_000.0    # initial portfolio USD (cash + BTC value)
SCAN_INTERVAL_S = 3_600       # 1h in seconds
DRY_RUN_DEFAULT = True        # override with --live


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class BotState:
    def __init__(self, nav: float):
        self.nav          = nav
        self.cash         = nav
        self.position_btc = 0.0
        self.entry_price  = 0.0
        self.peak_nav     = nav

    def update_nav(self, current_price: float):
        self.nav = self.cash + self.position_btc * current_price
        self.peak_nav = update_peak(self.nav, self.peak_nav)

    def open_position(self, usd_spent: float, price: float):
        btc_bought = usd_spent / price
        self.position_btc = btc_bought
        self.entry_price  = price
        self.cash        -= usd_spent

    def close_position(self, price: float):
        proceeds  = self.position_btc * price
        self.cash += proceeds
        self.position_btc = 0.0
        self.entry_price  = 0.0


# ---------------------------------------------------------------------------
# Single scan
# ---------------------------------------------------------------------------

def run_scan(state: BotState, dry_run: bool, verbose: bool = True) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 1. Fetch data
    df_1h = fetch_ohlcv("1h", limit=200)
    df_1d = fetch_ohlcv("1d", limit=200)
    price = fetch_price()

    state.update_nav(price)

    # 2. Signals
    sig    = get_signal(df_1h, df_1d)
    regime = get_regime(df_1d)
    size   = get_size(df_1h, df_1d, nav=state.nav)

    action = sig["action"]
    in_position = state.position_btc > 0

    log = {
        "time":      now,
        "price":     price,
        "nav":       round(state.nav, 2),
        "signal":    action,
        "regime":    regime["state"],
        "vol_fcast": size["forecast_vol"],
        "action_taken": "none",
    }

    # 3. Check stop-loss if holding
    if in_position:
        stop = check_stop(
            entry_price       = state.entry_price,
            current_price     = price,
            nav               = state.nav,
            position_size_usd = state.position_btc * state.entry_price,
        )
        if stop["stop_triggered"]:
            result = market_sell(state.position_btc, dry_run=dry_run)
            state.close_position(price)
            log["action_taken"] = f"STOP_LOSS_EXIT | {stop['reason']}"
            _print_scan(log, verbose)
            return log

    # 4. Regime check — override to exit if bear, skip entry if not bull
    if regime["state"] == "bear" and in_position:
        result = market_sell(state.position_btc, dry_run=dry_run)
        state.close_position(price)
        log["action_taken"] = "REGIME_EXIT | HMM state = BEAR"
        _print_scan(log, verbose)
        return log

    # 5. Signal-driven decisions
    if action == "exit" and in_position:
        result = market_sell(state.position_btc, dry_run=dry_run)
        state.close_position(price)
        log["action_taken"] = f"EXIT | {sig['reason']}"

    elif action == "long" and not in_position and regime["allow_long"]:
        risk = check_entry(
            fraction = size["fraction"],
            nav      = state.nav,
            peak_nav = state.peak_nav,
        )
        if risk["approved"]:
            result = market_buy(risk["dollar_size"], dry_run=dry_run)
            if result["status"] in ("dry_run", "filled"):
                state.open_position(risk["dollar_size"], price)
                log["action_taken"] = f"LONG | {risk['reason']}"
        else:
            log["action_taken"] = f"BLOCKED | {risk['reason']}"

    elif action == "long" and not in_position and not regime["allow_long"]:
        log["action_taken"] = f"SKIPPED | signal=long but regime={regime['state']}"

    else:
        log["action_taken"] = f"HOLD | {sig['reason']}"

    _print_scan(log, verbose)
    return log


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _print_scan(log: dict, verbose: bool):
    if not verbose:
        return
    bar = "=" * 60
    print(bar)
    print(f"  {log['time']}")
    print(f"  BTC/USDT   : ${log['price']:,.2f}")
    print(f"  NAV        : ${log['nav']:,.2f}")
    print(f"  Signal     : {log['signal'].upper()}")
    print(f"  Regime     : {log['regime'].upper()}")
    print(f"  Vol fcast  : {log['vol_fcast']:.1%}")
    print(f"  Action     : {log['action_taken']}")
    print(bar)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="BTC/USDT trading bot")
    parser.add_argument("--live", action="store_true", help="enable live orders")
    parser.add_argument("--once", action="store_true", help="run once and exit")
    args = parser.parse_args()

    dry_run = not args.live
    state   = BotState(nav=NAV_INITIAL)

    mode_str = "LIVE" if not dry_run else "DRY-RUN"
    print(f"\n=== BTC Bot starting ({mode_str}) | NAV=${NAV_INITIAL:,.0f} ===\n")

    if args.once:
        run_scan(state, dry_run=dry_run)
        return

    while True:
        try:
            run_scan(state, dry_run=dry_run)
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(SCAN_INTERVAL_S)


if __name__ == "__main__":
    main()
