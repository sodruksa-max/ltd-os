"""
sizer.py — Vol-targeted position sizing for BTC bot

Source:
  Hung et al. (2020), North American J. Econ. Finance
  "Realized GARCH + Tri-Power Variation for BTC vol forecasting"

Method:
  1. Tri-power variation (TPV) — jump-robust realized vol from 1h returns
  2. GARCH(1,1) on daily log returns with TPV as realized measure
  3. Vol-targeting: size = target_vol / forecast_vol (capped at max_position)

Output:
  get_size(df_1h, df_1d, nav) -> dict
    fraction    : float  (0.0–max_position, fraction of NAV to deploy)
    dollar_size : float  (dollar amount to deploy)
    forecast_vol: float  (annualized 1-day-ahead vol forecast)
    tpv         : float  (tri-power variation, annualized)
"""

import math
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# 1. Tri-Power Variation (jump-robust realized vol)
# ---------------------------------------------------------------------------

def tri_power_variation(df_1h: pd.DataFrame, lookback: int = 24) -> float:
    """
    TPV = scaling * sum(|r_t|^(2/3) * |r_{t-1}|^(2/3) * |r_{t-2}|^(2/3))
    over the last `lookback` 1h bars.

    Returns annualized vol (multiply by sqrt(8760) for 1h data = 8760 hrs/year).
    TPV is robust to price jumps — standard RV overestimates vol during jumps.
    """
    log_ret = np.log(df_1h["close"] / df_1h["close"].shift(1)).dropna()
    r = log_ret.values[-lookback:]

    if len(r) < 3:
        return float("nan")

    # mu_1 = E[|Z|^(2/3)] for Z ~ N(0,1)
    mu1 = 2 ** (1/3) * (math.gamma(7/6) / math.gamma(1/2))

    abs_r = np.abs(r)
    tpv_sum = np.sum(abs_r[2:] ** (2/3) * abs_r[1:-1] ** (2/3) * abs_r[:-2] ** (2/3))
    tpv_daily = tpv_sum / (mu1 ** 3)          # realized variance estimate

    # annualize: 24 hrs/day → scale to daily first, then sqrt for vol
    # 1h bars: realized variance per 24h window = sum of 24 squared returns
    # annualized vol = sqrt(tpv_daily * 365)
    tpv_vol_annual = float(np.sqrt(max(tpv_daily, 0) * 365))
    return tpv_vol_annual


# ---------------------------------------------------------------------------
# 2. GARCH(1,1) vol forecast (daily)
# ---------------------------------------------------------------------------

def garch_vol_forecast(df_1d: pd.DataFrame, min_bars: int = 60) -> float:
    """
    Fit GARCH(1,1) on daily log returns, return 1-step-ahead annualized vol.
    Falls back to rolling std if arch library unavailable or fit fails.
    """
    log_ret = (np.log(df_1d["close"] / df_1d["close"].shift(1)).dropna() * 100)

    if len(log_ret) < min_bars:
        # fallback: 30d rolling std annualized
        return float(log_ret.std() * np.sqrt(365) / 100)

    try:
        from arch import arch_model
        am = arch_model(log_ret, vol="Garch", p=1, q=1, dist="normal", rescale=False)
        res = am.fit(disp="off", show_warning=False)
        fc = res.forecast(horizon=1, reindex=False)
        var_forecast = float(fc.variance.iloc[-1, 0])
        vol_daily_pct = np.sqrt(var_forecast)
        vol_annual = vol_daily_pct * np.sqrt(365) / 100
        return vol_annual
    except Exception:
        # fallback: 30d rolling std
        return float(log_ret.tail(30).std() * np.sqrt(365) / 100)


# ---------------------------------------------------------------------------
# 3. Combined vol estimate + position sizing
# ---------------------------------------------------------------------------

def get_size(
    df_1h: pd.DataFrame,
    df_1d: pd.DataFrame,
    nav: float,
    target_vol: float = 0.25,       # target 25% annualized vol
    max_position: float = 0.30,     # max 30% of NAV per trade (risk.py enforces this too)
    tpv_weight: float = 0.5,        # blend weight for TPV vs GARCH
) -> dict:
    """
    Blend TPV (jump-robust) and GARCH(1,1) vol forecasts.
    Position size = target_vol / blended_vol, capped at max_position.

    Parameters
    ----------
    df_1h        : 1h OHLCV DataFrame (for TPV intraday vol)
    df_1d        : daily OHLCV DataFrame (for GARCH daily vol)
    nav          : total portfolio NAV in USD
    target_vol   : annualized vol target (default 25%)
    max_position : hard cap on fraction of NAV (default 30%)
    tpv_weight   : blend weight for TPV (1 - tpv_weight goes to GARCH)

    Returns
    -------
    dict with fraction, dollar_size, forecast_vol, tpv_vol, garch_vol
    """
    tpv_vol   = tri_power_variation(df_1h)
    garch_vol = garch_vol_forecast(df_1d)

    # Blend: use TPV heavily (jump-robust for BTC) + GARCH for trend
    if np.isnan(tpv_vol):
        blended_vol = garch_vol
    else:
        blended_vol = tpv_weight * tpv_vol + (1 - tpv_weight) * garch_vol

    blended_vol = max(blended_vol, 0.01)    # floor at 1% to avoid div-by-zero

    raw_fraction = target_vol / blended_vol
    fraction = min(raw_fraction, max_position)

    return {
        "fraction":     round(fraction, 4),
        "dollar_size":  round(fraction * nav, 2),
        "forecast_vol": round(blended_vol, 4),
        "tpv_vol":      round(tpv_vol, 4) if not np.isnan(tpv_vol) else None,
        "garch_vol":    round(garch_vol, 4),
        "nav":          nav,
    }


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from btc_bot.data import fetch_ohlcv

    print("Fetching data...")
    df_1h = fetch_ohlcv("1h", limit=200)
    df_1d = fetch_ohlcv("1d", limit=150)
    print(f"  1h bars: {len(df_1h)} | 1d bars: {len(df_1d)}\n")

    nav = 10_000.0   # example $10,000 portfolio
    size = get_size(df_1h, df_1d, nav=nav)

    print("=== Position Sizer (vol-targeted) ===")
    print(f"  TPV vol    (annualized): {size['tpv_vol']:.1%}" if size["tpv_vol"] else "  TPV vol: N/A")
    print(f"  GARCH vol  (annualized): {size['garch_vol']:.1%}")
    print(f"  Blended vol (forecast) : {size['forecast_vol']:.1%}")
    print(f"  Position fraction      : {size['fraction']:.1%} of NAV")
    print(f"  Dollar size ($10k NAV) : ${size['dollar_size']:,.2f}")
