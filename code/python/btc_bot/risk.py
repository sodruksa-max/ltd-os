"""
risk.py — Risk guardrails for BTC bot

Hard rules (enforced before every order):
  1. Max position    : 30% of NAV per trade
  2. Stop-loss       : exit if position loss > 3% of NAV
  3. Max drawdown    : halt all new longs if portfolio drawdown > 15% from peak

Output:
  check_entry(fraction, nav, current_price, peak_nav) -> dict
    approved    : bool
    fraction    : float (possibly reduced)
    dollar_size : float
    reason      : str

  check_stop(entry_price, current_price, nav, position_size_usd) -> dict
    stop_triggered : bool
    pnl_pct        : float
    reason         : str

  update_peak(nav, peak_nav) -> float  (returns new peak)
"""

MAX_POSITION_FRAC = 0.30   # 30% of NAV
STOP_LOSS_PCT     = -0.03  # -3% of NAV triggers stop
MAX_DRAWDOWN_PCT  = -0.15  # -15% from peak halts new longs


def check_entry(
    fraction: float,
    nav: float,
    peak_nav: float,
    label: str = "entry check",
) -> dict:
    """
    Validate and cap a proposed position size before entry.

    Parameters
    ----------
    fraction  : proposed fraction of NAV from sizer.get_size()
    nav       : current portfolio value in USD
    peak_nav  : highest NAV ever recorded (for drawdown calc)

    Returns
    -------
    dict with approved, fraction, dollar_size, drawdown_pct, reason
    """
    drawdown_pct = (nav - peak_nav) / peak_nav if peak_nav > 0 else 0.0

    # Drawdown circuit breaker
    if drawdown_pct <= MAX_DRAWDOWN_PCT:
        return {
            "approved":    False,
            "fraction":    0.0,
            "dollar_size": 0.0,
            "drawdown_pct": round(drawdown_pct, 4),
            "reason": (
                f"MAX DRAWDOWN HALT — portfolio down {drawdown_pct:.1%} from peak "
                f"(limit {MAX_DRAWDOWN_PCT:.0%})"
            ),
        }

    # Cap position at hard max
    capped = min(fraction, MAX_POSITION_FRAC)
    dollar_size = round(capped * nav, 2)

    reason = (
        f"OK — {capped:.1%} of NAV (${dollar_size:,.2f})"
        if capped == fraction
        else (
            f"CAPPED from {fraction:.1%} to {MAX_POSITION_FRAC:.0%} of NAV "
            f"(${dollar_size:,.2f})"
        )
    )

    return {
        "approved":    True,
        "fraction":    round(capped, 4),
        "dollar_size": dollar_size,
        "drawdown_pct": round(drawdown_pct, 4),
        "reason":      reason,
    }


def check_stop(
    entry_price: float,
    current_price: float,
    nav: float,
    position_size_usd: float,
) -> dict:
    """
    Evaluate whether the stop-loss has been triggered.

    Stop fires when: position PnL / NAV <= STOP_LOSS_PCT (-3%)
    This is NAV-relative (not position-relative) to bound tail loss.

    Parameters
    ----------
    entry_price       : price at which BTC position was opened
    current_price     : current BTC price
    nav               : current total NAV (including open position mark-to-market)
    position_size_usd : size of position in USD at entry

    Returns
    -------
    dict with stop_triggered, pnl_usd, pnl_nav_pct, reason
    """
    if entry_price <= 0:
        return {"stop_triggered": False, "pnl_usd": 0.0, "pnl_nav_pct": 0.0,
                "reason": "no open position"}

    price_return = (current_price - entry_price) / entry_price
    pnl_usd = position_size_usd * price_return
    pnl_nav_pct = pnl_usd / nav if nav > 0 else 0.0

    stop_triggered = pnl_nav_pct <= STOP_LOSS_PCT

    reason = (
        f"STOP TRIGGERED — position loss {pnl_nav_pct:.2%} of NAV "
        f"(${pnl_usd:,.2f}) exceeds {STOP_LOSS_PCT:.0%} limit"
        if stop_triggered
        else f"OK — position PnL {pnl_nav_pct:+.2%} of NAV (${pnl_usd:+,.2f})"
    )

    return {
        "stop_triggered": stop_triggered,
        "pnl_usd":        round(pnl_usd, 2),
        "pnl_nav_pct":    round(pnl_nav_pct, 4),
        "reason":         reason,
    }


def update_peak(nav: float, peak_nav: float) -> float:
    """Update and return the new peak NAV."""
    return max(nav, peak_nav)


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    nav      = 10_000.0
    peak_nav = 10_500.0   # down 4.8% from peak — within limit

    print("=== Risk Check: Entry ===")
    r = check_entry(fraction=0.30, nav=nav, peak_nav=peak_nav)
    print(f"  Approved   : {r['approved']}")
    print(f"  Fraction   : {r['fraction']:.1%}")
    print(f"  Dollar     : ${r['dollar_size']:,.2f}")
    print(f"  Drawdown   : {r['drawdown_pct']:.1%}")
    print(f"  Reason     : {r['reason']}")

    print("\n=== Risk Check: Drawdown halt ===")
    r2 = check_entry(fraction=0.30, nav=8_400.0, peak_nav=10_000.0)
    print(f"  Approved   : {r2['approved']}")
    print(f"  Reason     : {r2['reason']}")

    print("\n=== Risk Check: Stop-loss ===")
    s = check_stop(
        entry_price=80_000.0,
        current_price=77_200.0,   # -3.5% price drop
        nav=nav,
        position_size_usd=3_000.0,
    )
    print(f"  Stop triggered: {s['stop_triggered']}")
    print(f"  PnL ($)       : ${s['pnl_usd']:,.2f}")
    print(f"  PnL (% NAV)   : {s['pnl_nav_pct']:.2%}")
    print(f"  Reason        : {s['reason']}")
