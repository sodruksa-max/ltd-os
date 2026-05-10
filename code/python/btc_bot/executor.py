"""
executor.py — Order placement for BTC bot (Binance via ccxt)

Modes:
  dry_run=True  : log order details only, no real order sent (default until keys configured)
  dry_run=False : live order — requires BINANCE_API_KEY + BINANCE_SECRET_KEY in .secrets/.env

Supported order types:
  market_buy(usd_amount)  — buy BTC at market price
  market_sell(btc_amount) — sell BTC at market price

Safety checks (before every live order):
  - Minimum order size enforced (Binance minimum ~5 USDT)
  - Dry-run mode prints order details without touching Binance
  - Keys loaded from .secrets/.env only (never hardcoded)
"""

import os
from pathlib import Path

import ccxt

SYMBOL       = "BTC/USDT"
MIN_USD      = 6.0          # Binance min notional ~5 USDT, use 6 for safety
MIN_BTC_SELL = 0.000050     # ~$4 at $80k — Binance min base qty


def _load_env():
    env_file = Path(__file__).parent.parent.parent.parent / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def _get_exchange() -> ccxt.Exchange:
    _load_env()
    api_key    = os.environ.get("BINANCE_API_KEY")
    secret_key = os.environ.get("BINANCE_SECRET_KEY")
    if not api_key or not secret_key:
        raise EnvironmentError(
            "BINANCE_API_KEY and BINANCE_SECRET_KEY not set in .secrets/.env"
        )
    return ccxt.binance({
        "apiKey":        api_key,
        "secret":        secret_key,
        "enableRateLimit": True,
        "options":       {"defaultType": "spot"},
    })


def market_buy(usd_amount: float, dry_run: bool = True) -> dict:
    """
    Buy BTC with `usd_amount` USD at market price.

    Parameters
    ----------
    usd_amount : USD to spend (e.g. 3000.0)
    dry_run    : if True, log only — no real order sent

    Returns
    -------
    dict with status, symbol, side, usd_amount, order (or simulated)
    """
    if usd_amount < MIN_USD:
        return {
            "status":     "rejected",
            "reason":     f"usd_amount ${usd_amount:.2f} below minimum ${MIN_USD}",
            "usd_amount": usd_amount,
        }

    if dry_run:
        print(f"[DRY RUN] BUY {SYMBOL}  ${usd_amount:,.2f} USDT @ market")
        return {
            "status":     "dry_run",
            "symbol":     SYMBOL,
            "side":       "buy",
            "usd_amount": usd_amount,
            "order":      None,
        }

    ex = _get_exchange()
    # Binance market buy by quoteOrderQty (spend exact USD)
    order = ex.create_order(
        symbol    = SYMBOL,
        type      = "market",
        side      = "buy",
        amount    = None,
        params    = {"quoteOrderQty": usd_amount},
    )
    print(f"[LIVE] BUY {SYMBOL}  ${usd_amount:,.2f} USDT — order ID: {order['id']}")
    return {
        "status":     "filled",
        "symbol":     SYMBOL,
        "side":       "buy",
        "usd_amount": usd_amount,
        "order":      order,
    }


def market_sell(btc_amount: float, dry_run: bool = True) -> dict:
    """
    Sell `btc_amount` BTC at market price.

    Parameters
    ----------
    btc_amount : quantity of BTC to sell (e.g. 0.0375)
    dry_run    : if True, log only — no real order sent

    Returns
    -------
    dict with status, symbol, side, btc_amount, order (or simulated)
    """
    if btc_amount < MIN_BTC_SELL:
        return {
            "status":     "rejected",
            "reason":     f"btc_amount {btc_amount:.6f} below minimum {MIN_BTC_SELL}",
            "btc_amount": btc_amount,
        }

    if dry_run:
        print(f"[DRY RUN] SELL {SYMBOL}  {btc_amount:.6f} BTC @ market")
        return {
            "status":     "dry_run",
            "symbol":     SYMBOL,
            "side":       "sell",
            "btc_amount": btc_amount,
            "order":      None,
        }

    ex = _get_exchange()
    order = ex.create_order(
        symbol = SYMBOL,
        type   = "market",
        side   = "sell",
        amount = btc_amount,
    )
    print(f"[LIVE] SELL {SYMBOL}  {btc_amount:.6f} BTC — order ID: {order['id']}")
    return {
        "status":     "filled",
        "symbol":     SYMBOL,
        "side":       "sell",
        "btc_amount": btc_amount,
        "order":      order,
    }


# ---------------------------------------------------------------------------
# Quick test (dry-run only)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Executor test (dry-run mode) ===\n")

    print("Test 1: buy $3000 USDT of BTC")
    r = market_buy(3000.0, dry_run=True)
    print(f"  Status: {r['status']}\n")

    print("Test 2: sell 0.0375 BTC")
    r2 = market_sell(0.0375, dry_run=True)
    print(f"  Status: {r2['status']}\n")

    print("Test 3: reject tiny buy ($2)")
    r3 = market_buy(2.0, dry_run=True)
    print(f"  Status: {r3['status']} | {r3.get('reason', '')}")
