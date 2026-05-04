#!/usr/bin/env python3
"""
Crypto momentum screener — ranks pairs by VP-MACD signal + cross-sectional momentum.

Implements:
  - VP-MACD        (arXiv:2604.26063): Volume-Price adjusted MACD
  - Cross-sectional momentum (Jegadeesh & Titman): RS vs BTC over 20d/3m/6m
  - LOB stress proxy (arXiv:2604.20949): spread drift + vol thinning from OHLCV
  - Macro calendar filter (arXiv:2604.01431): warn near FOMC/CPI dates

Usage:
    python scripts/crypto-screener.py                      # screen default pairs
    python scripts/crypto-screener.py --top 5              # top 5 only
    python scripts/crypto-screener.py --json               # JSON output (for auto-buy)
    python scripts/crypto-screener.py --timeframe 1h       # 1h candles (default: 1d)
    python scripts/crypto-screener.py BTC/USDT ETH/USDT    # specific pairs

No API keys required — uses Binance public data via ccxt.
"""

import json
import statistics
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent.parent

DEFAULT_PAIRS = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
    "AVAX/USDT", "DOGE/USDT", "ADA/USDT", "DOT/USDT", "LINK/USDT",
]
BENCHMARK = "BTC/USDT"
TIMEFRAME  = "1d"
HISTORY_LIMIT = 300       # candles (~10 months daily, covers 6m lookback)
LOOKBACK      = 20        # 20-day RS window
LOOKBACK_3M   = 63        # ~3 months
LOOKBACK_6M   = 126       # ~6 months
VP_N          = 20        # VP-MACD adjusted price window
VP_FAST       = 12
VP_SLOW       = 26
VP_SIGNAL     = 9
VP_LAMBDA     = 0.9       # sensitivity: buy threshold = lambda × signal line
STRESS_WINDOW = 20        # LOB proxy lookback


# ── FOMC / CPI calendar (2026) — static macro filter ──────────────────────────
# Source: Fed schedule + BLS release calendar
# Update this list at the start of each year
MACRO_EVENTS_2026 = [
    # (date, label)
    ("2026-01-29", "FOMC"), ("2026-03-19", "FOMC"), ("2026-05-07", "FOMC"),
    ("2026-06-18", "FOMC"), ("2026-07-30", "FOMC"), ("2026-09-17", "FOMC"),
    ("2026-10-29", "FOMC"), ("2026-12-10", "FOMC"),
    ("2026-01-14", "CPI"),  ("2026-02-11", "CPI"),  ("2026-03-11", "CPI"),
    ("2026-04-10", "CPI"),  ("2026-05-13", "CPI"),  ("2026-06-10", "CPI"),
    ("2026-07-15", "CPI"),  ("2026-08-12", "CPI"),  ("2026-09-09", "CPI"),
    ("2026-10-14", "CPI"),  ("2026-11-12", "CPI"),  ("2026-12-09", "CPI"),
]


def macro_event_within(days=2) -> tuple:
    """Returns (True, label) if a macro event is within N days."""
    today = date.today()
    for ds, label in MACRO_EVENTS_2026:
        ev = date.fromisoformat(ds)
        if abs((ev - today).days) <= days:
            return True, label
    return False, ""


def fetch_ohlcv(pairs: list, timeframe: str, limit: int) -> dict:
    import ccxt
    ex = ccxt.binance({"enableRateLimit": True})
    data = {}
    for pair in pairs:
        try:
            raw = ex.fetch_ohlcv(pair, timeframe, limit=limit)
            # raw = [[ts, open, high, low, close, volume], ...]
            data[pair] = raw
        except Exception as e:
            print(f"[warn] fetch {pair}: {e}", file=sys.stderr)
    return data


def _ema(values: list, span: int) -> list:
    """Exponential moving average via pandas-style ewm."""
    result = []
    k = 2.0 / (span + 1)
    for i, v in enumerate(values):
        if i == 0:
            result.append(v)
        else:
            result.append(v * k + result[-1] * (1 - k))
    return result


def compute_vp_macd(ohlcv: list, N=VP_N, fast=VP_FAST, slow=VP_SLOW,
                    signal_period=VP_SIGNAL, lam=VP_LAMBDA) -> dict:
    """
    VP-MACD (arXiv:2604.26063).
    P* = Σ(close × volume × sigma × r) / Σ(volume)  over N-day window
    Signal: buy when VP-MACD crosses above lam×signal_line
    """
    if len(ohlcv) < slow + signal_period + N:
        return {"signal": "NEUTRAL", "vp_macd": 0.0, "signal_line": 0.0,
                "histogram": 0.0, "p_star": []}

    opens  = np.array([c[1] for c in ohlcv], dtype=float)
    highs  = np.array([c[2] for c in ohlcv], dtype=float)
    lows   = np.array([c[3] for c in ohlcv], dtype=float)
    closes = np.array([c[4] for c in ohlcv], dtype=float)
    vols   = np.array([c[5] for c in ohlcv], dtype=float)

    # Volatility component: σᵢ = std(high-low) over N days, normalized by close
    hl_range = highs - lows
    sigma = np.array([
        np.std(hl_range[max(0, i-N):i]) / closes[i]
        if closes[i] > 0 and i >= 2 else 0.0
        for i in range(len(closes))
    ])

    # Intraday conviction: rᵢ = |close-open| / (high-low)
    denom = np.where(hl_range > 0, hl_range, np.nan)
    r = np.abs(closes - opens) / denom
    r = np.nan_to_num(r, nan=0.0)

    # Adjusted price P*: rolling volume-weighted with sigma and r
    p_star = []
    for i in range(len(closes)):
        start = max(0, i - N + 1)
        w = vols[start:i+1] * sigma[start:i+1] * r[start:i+1]
        total_w = w.sum()
        if total_w > 0:
            p_star.append((closes[start:i+1] * w).sum() / total_w)
        else:
            p_star.append(closes[i])

    ema_fast_arr   = _ema(p_star, fast)
    ema_slow_arr   = _ema(p_star, slow)
    vp_macd_line   = [f - s for f, s in zip(ema_fast_arr, ema_slow_arr)]
    signal_line    = _ema(vp_macd_line, signal_period)

    cur  = vp_macd_line[-1]
    prev = vp_macd_line[-2]
    sig  = signal_line[-1]
    sig_prev = signal_line[-2]

    # Asymmetric entry/exit (Equation 13 from paper)
    if prev <= lam * sig_prev and cur > lam * sig:
        signal = "BUY"
    elif prev >= sig_prev and cur < sig:
        signal = "SELL"
    else:
        signal = "NEUTRAL"

    return {
        "signal": signal,
        "vp_macd": round(cur, 6),
        "signal_line": round(sig, 6),
        "vp_histogram": round(cur - sig, 6),
        "p_star": p_star,
    }


def compute_momentum(ohlcv: list, benchmark_ohlcv: list) -> dict:
    """Cross-sectional RS vs BTC over 20d / 3m / 6m (Jegadeesh & Titman)."""
    closes = [c[4] for c in ohlcv]
    vols   = [c[5] for c in ohlcv]
    bm     = [c[4] for c in benchmark_ohlcv] if benchmark_ohlcv else []

    def rs(n):
        if len(closes) < n + 1:
            return 0.0
        ret = (closes[-1] - closes[-n-1]) / closes[-n-1]
        if len(bm) >= n + 1:
            bm_ret = (bm[-1] - bm[-n-1]) / bm[-n-1]
            return ret - bm_ret
        return ret

    rs_20d = rs(LOOKBACK)
    rs_3m  = rs(LOOKBACK_3M)
    rs_6m  = rs(LOOKBACK_6M)

    if rs_3m == 0.0 and rs_6m == 0.0:
        composite = rs_20d
    elif rs_6m == 0.0:
        composite = 0.5 * rs_20d + 0.5 * rs_3m
    else:
        composite = 0.2 * rs_20d + 0.4 * rs_3m + 0.4 * rs_6m

    # Volume ratio (20d)
    vol_ratio = 0.0
    if len(vols) >= LOOKBACK + 1:
        avg_vol = sum(vols[-LOOKBACK-1:-1]) / LOOKBACK
        vol_ratio = vols[-1] / avg_vol if avg_vol > 0 else 0.0
    vol_weight = max(0.5, min(vol_ratio, 3.0))

    # Realized daily vol for vol-targeting
    if len(closes) >= 22:
        daily_rets = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(-20, 0)]
        realized_vol = statistics.stdev(daily_rets)
    else:
        realized_vol = 0.02

    return {
        "rs_20d_pct":   round(rs_20d * 100, 2),
        "rs_3m_pct":    round(rs_3m * 100, 2),
        "rs_6m_pct":    round(rs_6m * 100, 2),
        "composite_rs": round(composite * 100, 2),
        "vol_ratio":    round(vol_ratio, 2),
        "momentum_score": round(composite * vol_weight, 4),
        "realized_vol_20d": round(realized_vol, 5),
        "ret_20d_pct":  round((closes[-1] - closes[-LOOKBACK-1]) / closes[-LOOKBACK-1] * 100, 2)
                        if len(closes) >= LOOKBACK + 1 else 0.0,
    }


def compute_lob_stress(ohlcv: list) -> dict:
    """
    Simplified LOB stress proxy from OHLCV (arXiv:2604.20949).
    Uses spread proxy + volume thinning + conviction drop as regime signals.
    No HMM needed — OHLCV-based approximation.
    """
    if len(ohlcv) < STRESS_WINDOW + 2:
        return {"stress_score": 0.0, "stress_alert": False, "stress_detail": "insufficient data"}

    highs  = [c[2] for c in ohlcv]
    lows   = [c[3] for c in ohlcv]
    opens  = [c[1] for c in ohlcv]
    closes = [c[4] for c in ohlcv]
    vols   = [c[5] for c in ohlcv]

    # Spread proxy: (high - low) / close
    spreads = [(highs[i] - lows[i]) / closes[i] if closes[i] > 0 else 0
               for i in range(len(closes))]
    recent_spread = spreads[-1]
    avg_spread = sum(spreads[-STRESS_WINDOW-1:-1]) / STRESS_WINDOW
    std_spread = statistics.stdev(spreads[-STRESS_WINDOW-1:-1]) if STRESS_WINDOW > 1 else 1e-6
    spread_z = (recent_spread - avg_spread) / (std_spread + 1e-10)

    # Spread drift: is spread rising over last 5 bars?
    spread_drift = sum(1 for i in range(-5, 0) if spreads[i] > spreads[i-1]) / 5

    # Conviction (body / range): |close-open| / (high-low)
    convictions = [(abs(closes[i] - opens[i]) / (highs[i] - lows[i]))
                   if (highs[i] - lows[i]) > 0 else 0.5
                   for i in range(len(closes))]
    conv_drop = max(0, (sum(convictions[-STRESS_WINDOW-1:-1]) / STRESS_WINDOW) - convictions[-1])

    # Volume thinning: recent vol vs avg
    avg_vol = sum(vols[-STRESS_WINDOW-1:-1]) / STRESS_WINDOW
    vol_thin = max(0, 1 - vols[-1] / avg_vol) if avg_vol > 0 else 0

    # Composite stress: max of normalized signals (like paper)
    s_spread  = min(max(spread_z / 3.0, 0), 1)   # z-score normalized
    s_drift   = spread_drift                       # 0-1
    s_conv    = min(conv_drop * 3, 1)             # 0-1
    s_vol     = min(vol_thin, 1)                  # 0-1
    stress_score = max(s_spread, s_drift, s_conv, s_vol)

    alert = stress_score > 0.6
    details = []
    if s_spread > 0.5:  details.append(f"spread_spike(z={spread_z:.1f})")
    if s_drift > 0.6:   details.append("spread_rising")
    if s_conv > 0.5:    details.append("low_conviction")
    if s_vol > 0.5:     details.append("vol_thinning")

    return {
        "stress_score": round(stress_score, 3),
        "stress_alert": alert,
        "stress_detail": ", ".join(details) if details else "ok",
    }


def screen(ohlcv_data: dict) -> tuple:
    results = []
    fails   = []
    bm_data = ohlcv_data.get(BENCHMARK, [])

    pairs = [p for p in ohlcv_data if p != BENCHMARK]

    for pair in pairs:
        try:
            ohlcv = ohlcv_data[pair]
            if len(ohlcv) < VP_SLOW + VP_SIGNAL + VP_N + 5:
                fails.append((pair, f"only {len(ohlcv)} candles"))
                continue

            closes = [c[4] for c in ohlcv]
            price  = closes[-1]

            vp     = compute_vp_macd(ohlcv)
            mom    = compute_momentum(ohlcv, bm_data)
            stress = compute_lob_stress(ohlcv)

            # Combined score: momentum × VP-MACD conviction boost
            vp_boost = 1.3 if vp["signal"] == "BUY" else 0.7 if vp["signal"] == "SELL" else 1.0
            combined_score = mom["momentum_score"] * vp_boost * (1 - 0.3 * stress["stress_score"])

            results.append({
                "pair":           pair,
                "price":          round(price, 4),
                "ret_20d_pct":    mom["ret_20d_pct"],
                "rs_20d_pct":     mom["rs_20d_pct"],
                "rs_3m_pct":      mom["rs_3m_pct"],
                "rs_6m_pct":      mom["rs_6m_pct"],
                "composite_rs":   mom["composite_rs"],
                "vol_ratio":      mom["vol_ratio"],
                "momentum_score": mom["momentum_score"],
                "realized_vol_20d": mom["realized_vol_20d"],
                "vp_signal":      vp["signal"],
                "vp_macd":        vp["vp_macd"],
                "vp_histogram":   vp["vp_histogram"],
                "stress_score":   stress["stress_score"],
                "stress_alert":   stress["stress_alert"],
                "stress_detail":  stress["stress_detail"],
                "score":          round(combined_score, 4),
            })
        except Exception as e:
            fails.append((pair, str(e)))

    results.sort(key=lambda x: x["score"], reverse=True)
    return results, fails


def print_table(results: list, top=None):
    rows = results[:top] if top else results
    if not rows:
        print("No results.")
        return

    # Check macro calendar
    macro_near, macro_label = macro_event_within(days=2)
    if macro_near:
        print(f"  [MACRO WARNING] {macro_label} within 2 days -- elevated vol risk\n")

    header = f"{'#':<3} {'Pair':<12} {'Price':>10} {'20d Ret':>8} {'RS/BTC':>8} {'VolRatio':>9} {'VP-SIG':>7} {'Stress':>7} {'Score':>8}  Detail"
    print(header)
    print("-" * 100)

    for i, r in enumerate(rows, 1):
        vp_col = {"BUY": "BUY ^", "SELL": "SELL v", "NEUTRAL": "  ---"}.get(r["vp_signal"], "  ---")
        stress_col = f"{'⚠' if r['stress_alert'] else ' '}{r['stress_score']:.2f}"
        ret_sign = "+" if r["ret_20d_pct"] >= 0 else ""
        rs_sign  = "+" if r["composite_rs"] >= 0 else ""
        print(
            f"{i:<3} {r['pair']:<12} ${r['price']:>9,.4f} "
            f"{ret_sign}{r['ret_20d_pct']:>5.1f}% "
            f"{rs_sign}{r['composite_rs']:>5.1f}% "
            f"{r['vol_ratio']:>8.2f}x "
            f"{vp_col:>7} "
            f"{stress_col:>7} "
            f"{r['score']:>8.4f}  "
            f"{r['stress_detail'] if r['stress_alert'] else ''}"
        )

    print()
    print("Score = composite_RS(20d/3m/6m vs BTC) * vol_ratio * VP-MACD_boost * (1 - stress)")
    print("VP-MACD (arXiv:2604.26063): lambda-adjusted buy | symmetric sell | LOB stress proxy (arXiv:2604.20949)")
    print("composite_RS = 0.2*RS_20d + 0.4*RS_3m + 0.4*RS_6m | VP boost: BUY*1.3 SELL*0.7")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--timeframe", default=TIMEFRAME,
                        help="Candle timeframe: 1d (default), 4h, 1h, 15m")
    parser.add_argument("pairs", nargs="*")
    args = parser.parse_args()

    pairs = [p.upper().replace("-", "/") for p in args.pairs] if args.pairs else DEFAULT_PAIRS

    # Ensure benchmark is in fetch list
    fetch_list = list(dict.fromkeys([BENCHMARK] + pairs))
    # Remove benchmark from display list if not explicitly requested
    display_pairs = pairs if args.pairs else [p for p in pairs if p != BENCHMARK]

    print(f"Fetching {len(fetch_list)} pairs from Binance ({args.timeframe})...", file=sys.stderr)

    ohlcv_data = fetch_ohlcv(fetch_list, args.timeframe, HISTORY_LIMIT)

    missing = [p for p in display_pairs if p not in ohlcv_data]
    if missing:
        print(f"[warn] no data for: {', '.join(missing)}", file=sys.stderr)

    # Filter to display pairs only (keep benchmark in data for RS calculation)
    screen_data = {p: ohlcv_data[p] for p in ohlcv_data if p in display_pairs or p == BENCHMARK}

    results, fails = screen(screen_data)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n## Crypto Screen — {args.timeframe} — {date.today()}\n")
    print_table(results, top=args.top)

    if fails:
        print(f"\n[skipped {len(fails)}]: " + ", ".join(f"{p}({r})" for p, r in fails[:6]))


if __name__ == "__main__":
    main()
