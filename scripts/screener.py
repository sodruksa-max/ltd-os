#!/usr/bin/env python3
"""
Hedge-fund grade momentum screener — ranks watchlist stocks using multi-paper factor stack.

Usage:
    python scripts/screener.py                   # screen all tickers in config/watchlist.txt
    python scripts/screener.py --top 5           # show top 5 only
    python scripts/screener.py --json            # output JSON (for auto-buy.py to consume)
    python scripts/screener.py --fundamentals    # add yfinance fundamental checks (slower)
    python scripts/screener.py --reversal        # sort by reversal score (beginning-of-trend)
    python scripts/screener.py NVDA AAPL         # screen specific tickers only

Scoring (hedge-fund grade):
  Primary score = cross-sectional percentile rank of vol-scaled 12-1 momentum
    - 12-1 momentum    (Jegadeesh & Titman 1993; AQR 2014) : (close[-21] / close[-252]) - 1
    - Vol-scaled mom   (Barroso & Santa-Clara 2015)         : mom_12_1 / realized_vol_6m
    - CS rank          (Asness, Moskowitz & Pedersen 2013)  : percentile within screened universe
    - TS signal        (Moskowitz, Ooi & Pedersen 2012)     : mom_12_1 > 0 required

  Liquidity:
    - Amihud illiquidity (Amihud 2002)  : mean(|return| / dollar_volume) over 20d
    - Avg daily dollar volume            : flags stocks < $5M/day

  Trend & junk:
    - Above MA50, price $5-$1000
    - Junk filter: price-based + optional fundamentals (EPS, debt, OCF, gross profit, accruals)

  Sector neutrality (Asness, Moskowitz & Pedersen 2013):
    - Rank within GICS sector via yfinance, not across full universe
    - Single-ticker sectors get neutral rank 0.5
    - Prevents screener from returning all-Tech in bull markets

Backward-compat JSON fields (auto-buy.py): ticker, price, rs_vs_spy_pct, vol_ratio,
  return_5d_pct, reversal_score, score, junk_level, junk_summary, realized_vol_20d
New JSON fields: mom_12_1_pct, realized_vol_6m, vol_scaled_mom, ts_signal, amihud_illiq,
  avg_dollar_vol_m, cs_rank, sector

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import json
import os
import statistics
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT      = Path(__file__).parent.parent
WATCHLIST = ROOT / "config" / "watchlist.txt"
BENCHMARK = "SPY"

PRICE_MIN    = 5.0
PRICE_MAX    = 1000.0
LOOKBACK_12M = 252   # 12-month formation period (trading days)
SKIP_MONTH   = 21    # skip most-recent month to avoid short-term reversal
LOOKBACK_6M  = 126   # 6-month window for realized vol
LOOKBACK_3M  = 63
LOOKBACK_20D = 20
MA_PERIOD    = 50
HISTORY_DAYS = 500   # calendar days — comfortably covers 12m of trading days


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


def load_watchlist():
    if not WATCHLIST.exists():
        print(f"[warn] watchlist not found: {WATCHLIST}", file=sys.stderr)
        return []
    tickers = []
    for line in WATCHLIST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tickers.append(line.upper())
    return tickers


def fetch_bars(tickers):
    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    api_key    = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA keys not set", file=sys.stderr)
        sys.exit(1)

    client = StockHistoricalDataClient(api_key, secret_key)
    start  = datetime.combine(date.today() - timedelta(days=HISTORY_DAYS), datetime.min.time())
    resp   = client.get_stock_bars(
        StockBarsRequest(symbol_or_symbols=tickers, timeframe=TimeFrame.Day, start=start)
    )
    return resp.data


def _bar_val(bar, field):
    return bar[field] if isinstance(bar, dict) else getattr(bar, field)


SECTOR_ABBREV = {
    "Technology":             "Tech",
    "Communication Services": "Comm",
    "Consumer Cyclical":      "Cycl",
    "Consumer Defensive":     "Def ",
    "Healthcare":             "Hlth",
    "Financials":             "Fin ",
    "Financial Services":     "Fin ",
    "Industrials":            "Ind ",
    "Basic Materials":        "Mat ",
    "Energy":                 "Enrg",
    "Real Estate":            "RE  ",
    "Utilities":              "Util",
    "ETF":                    "ETF ",
    "Unknown":                "?   ",
}


def fetch_sectors(tickers: list) -> dict:
    """
    Fetch GICS sector for each ticker via yfinance (lightweight call).
    ETFs → 'ETF'. Any error → 'Unknown'. Takes ~3s for 25 tickers.
    """
    result = {}
    try:
        import time
        import yfinance as yf
        for t in tickers:
            try:
                info      = yf.Ticker(t).info
                qt        = info.get("quoteType", "")
                result[t] = info.get("sector") or qt or "Unknown"
            except Exception:
                result[t] = "Unknown"
            time.sleep(0.1)
    except ImportError:
        pass
    # Fill any missing tickers
    for t in tickers:
        result.setdefault(t, "Unknown")
    return result


# ---------------------------------------------------------------------------
# Pass 1 — per-ticker raw metrics
# ---------------------------------------------------------------------------

def _compute_raw(ticker, bars, spy_closes):
    """
    Returns raw metrics dict or None if ticker fails basic filters.
    All computations use daily OHLCV only (no external data needed here).
    """
    if not bars:
        return None

    closes  = [_bar_val(b, "close")  for b in bars]
    volumes = [_bar_val(b, "volume") for b in bars]

    if len(closes) < LOOKBACK_20D + 2:
        return None

    current_price = closes[-1]
    if not (PRICE_MIN <= current_price <= PRICE_MAX):
        return None

    # --- 12-1 momentum (Jegadeesh & Titman 1993; AQR 2014) ---
    # Formation window: 12 months ago → 1 month ago (skip most-recent month)
    if len(closes) >= LOOKBACK_12M + SKIP_MONTH:
        mom_12_1 = (closes[-SKIP_MONTH] - closes[-LOOKBACK_12M - 1]) / closes[-LOOKBACK_12M - 1]
    elif len(closes) >= LOOKBACK_6M + SKIP_MONTH:
        # 6-1 fallback when history < 12m
        mom_12_1 = (closes[-SKIP_MONTH] - closes[-LOOKBACK_6M - 1]) / closes[-LOOKBACK_6M - 1]
    else:
        # Short-history fallback: no skip (not enough bars)
        mom_12_1 = (closes[-1] - closes[-min(LOOKBACK_20D, len(closes) - 1) - 1]) / closes[-min(LOOKBACK_20D, len(closes) - 1) - 1]

    # Time-series signal (Moskowitz, Ooi & Pedersen 2012): trend must be positive
    ts_signal = 1 if mom_12_1 > 0 else -1

    # --- Realized volatility ---
    # 20d daily vol for auto-buy position sizing (backward compat)
    rets_20d = [(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(-LOOKBACK_20D, 0)]
    realized_vol_20d = statistics.stdev(rets_20d) if len(rets_20d) >= 2 else 0.02

    # 6m annualized vol for momentum scaling (Barroso & Santa-Clara 2015)
    n6m = min(LOOKBACK_6M, len(closes) - 1)
    rets_6m = [(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(-n6m, 0)]
    realized_vol_6m_ann = (statistics.stdev(rets_6m) * (252 ** 0.5)) if len(rets_6m) >= 10 else 0.30

    # Vol-scaled momentum — the Sharpe of momentum (Barroso & Santa-Clara 2015)
    vol_scaled_mom = mom_12_1 / max(realized_vol_6m_ann, 0.05)   # floor at 5% ann vol

    # --- Amihud illiquidity (Amihud 2002) ---
    # Lower = more liquid. High value = price moves a lot per dollar of volume traded.
    n_am = min(LOOKBACK_20D, len(closes) - 1)
    amihud_vals = []
    dv_vals = []
    for i in range(-n_am, 0):
        if closes[i - 1] > 0 and volumes[i] > 0:
            ret = abs((closes[i] - closes[i - 1]) / closes[i - 1])
            dv  = closes[i] * volumes[i]
            amihud_vals.append(ret / dv)
            dv_vals.append(dv)
    amihud         = statistics.mean(amihud_vals) if amihud_vals else 0.0
    avg_dollar_vol = statistics.mean(dv_vals)     if dv_vals     else 0.0

    # --- RS vs SPY (backward compat for display) ---
    ret_20d = (closes[-1] - closes[-LOOKBACK_20D - 1]) / closes[-LOOKBACK_20D - 1]
    rs_20d  = ret_20d
    if len(spy_closes) >= LOOKBACK_20D + 1:
        spy_ret = (spy_closes[-1] - spy_closes[-LOOKBACK_20D - 1]) / spy_closes[-LOOKBACK_20D - 1]
        rs_20d  = ret_20d - spy_ret

    rs_3m = 0.0; ret_3m_pct = 0.0
    if len(closes) >= LOOKBACK_3M + 1 and len(spy_closes) >= LOOKBACK_3M + 1:
        ret_3m     = (closes[-1] - closes[-LOOKBACK_3M - 1]) / closes[-LOOKBACK_3M - 1]
        spy_ret_3m = (spy_closes[-1] - spy_closes[-LOOKBACK_3M - 1]) / spy_closes[-LOOKBACK_3M - 1]
        rs_3m      = ret_3m - spy_ret_3m
        ret_3m_pct = ret_3m * 100

    rs_6m = 0.0; ret_6m_pct = 0.0
    if len(closes) >= LOOKBACK_6M + 1 and len(spy_closes) >= LOOKBACK_6M + 1:
        ret_6m     = (closes[-1] - closes[-LOOKBACK_6M - 1]) / closes[-LOOKBACK_6M - 1]
        spy_ret_6m = (spy_closes[-1] - spy_closes[-LOOKBACK_6M - 1]) / spy_closes[-LOOKBACK_6M - 1]
        rs_6m      = ret_6m - spy_ret_6m
        ret_6m_pct = ret_6m * 100

    # --- MA50 ---
    above_ma50 = False; ma50_val = None
    if len(closes) >= MA_PERIOD:
        ma50_val   = sum(closes[-MA_PERIOD:]) / MA_PERIOD
        above_ma50 = current_price > ma50_val

    # --- Volume ratio (backward compat) ---
    vol_ratio = 0.0
    if len(volumes) >= LOOKBACK_20D + 1:
        avg_vol   = sum(volumes[-LOOKBACK_20D - 1:-1]) / LOOKBACK_20D
        vol_ratio = volumes[-1] / avg_vol if avg_vol > 0 else 0.0

    # --- Reversal metrics ---
    ret_5d      = (closes[-1] - closes[-6]) / closes[-6] if len(closes) >= 6 else 0.0
    overextended = ret_20d > 0.70

    crossed_ma50 = False
    if ma50_val and len(closes) >= MA_PERIOD + 6:
        prev_ma50    = sum(closes[-MA_PERIOD - 5:-5]) / MA_PERIOD
        crossed_ma50 = closes[-6] < prev_ma50 and above_ma50

    vol_weight     = max(0.5, min(vol_ratio, 3.0))
    ma_bonus       = 2.0 if crossed_ma50 else 1.0
    reversal_score = max(0.0, ret_5d) * vol_weight * ma_bonus

    return {
        "closes":          closes,
        "volumes":         volumes,
        "price":           round(current_price, 2),
        "ret_20d":         ret_20d,
        "ret_20d_pct":     round(ret_20d * 100, 2),
        "ret_3m_pct":      round(ret_3m_pct, 2),
        "ret_6m_pct":      round(ret_6m_pct, 2),
        "ret_5d_pct":      round(ret_5d * 100, 2),
        "rs_20d_pct":      round(rs_20d * 100, 2),
        "rs_3m_pct":       round(rs_3m * 100, 2),
        "rs_6m_pct":       round(rs_6m * 100, 2),
        "vol_ratio":       round(vol_ratio, 2),
        "above_ma50":      above_ma50,
        "crossed_ma50":    crossed_ma50,
        "overextended":    overextended,
        "ma50":            round(ma50_val, 2) if ma50_val else None,
        "realized_vol_20d": round(realized_vol_20d, 5),
        "realized_vol_6m":  round(realized_vol_6m_ann, 4),
        "mom_12_1_pct":    round(mom_12_1 * 100, 2),
        "vol_scaled_mom":  round(vol_scaled_mom, 4),
        "ts_signal":       ts_signal,
        "amihud":          amihud,
        "avg_dollar_vol":  avg_dollar_vol,
        "reversal_score":  round(reversal_score, 4),
    }


# ---------------------------------------------------------------------------
# Pass 2 — cross-sectional rank + junk filter
# ---------------------------------------------------------------------------

def screen(tickers, bars_data, fetch_fundamentals=False):
    import junk_filter

    spy_bars    = bars_data.get(BENCHMARK, [])
    spy_closes  = [_bar_val(b, "close") for b in spy_bars]
    candidates  = [t for t in tickers if t != BENCHMARK]

    # Pass 1: compute raw metrics for every candidate
    raw_map = {}
    fails   = []
    for ticker in candidates:
        bars = bars_data.get(ticker, [])
        raw  = _compute_raw(ticker, bars, spy_closes)
        if raw is None:
            fails.append((ticker, "insufficient data or price out of range"))
        else:
            raw_map[ticker] = raw

    # Pass 2: sector-neutral cross-sectional percentile rank of vol_scaled_mom
    # (Asness, Moskowitz & Pedersen 2013) — rank within GICS sector, not full universe.
    # Prevents all picks coming from one dominant sector in bull markets.
    print("Fetching sector data (yfinance)...", file=sys.stderr)
    sector_map = fetch_sectors(list(raw_map.keys()))

    from collections import defaultdict
    sector_groups: dict = defaultdict(list)
    for t in raw_map:
        sector_groups[sector_map.get(t, "Unknown")].append(t)

    rank_map: dict = {}
    for sector_tickers in sector_groups.values():
        n = len(sector_tickers)
        if n == 1:
            rank_map[sector_tickers[0]] = 0.5   # single stock → neutral rank
        else:
            ordered = sorted(sector_tickers, key=lambda t: raw_map[t]["vol_scaled_mom"])
            for i, t in enumerate(ordered):
                rank_map[t] = i / (n - 1)

    results = []
    for ticker, raw in raw_map.items():
        cs_rank = rank_map.get(ticker, 0.0)

        junk = junk_filter.evaluate(
            ticker, raw["closes"], raw["volumes"],
            ret_20d=raw["ret_20d"],
            avg_dollar_vol=raw["avg_dollar_vol"],
            fetch_fund=fetch_fundamentals,
        )

        results.append({
            # --- Backward-compat fields (auto-buy.py reads these) ---
            "ticker":          ticker,
            "price":           raw["price"],
            "return_20d_pct":  raw["ret_20d_pct"],
            "return_3m_pct":   raw["ret_3m_pct"],
            "return_6m_pct":   raw["ret_6m_pct"],
            "return_5d_pct":   raw["ret_5d_pct"],
            "rs_vs_spy_pct":   raw["rs_20d_pct"],
            "rs_3m_pct":       raw["rs_3m_pct"],
            "rs_6m_pct":       raw["rs_6m_pct"],
            "vol_ratio":       raw["vol_ratio"],
            "above_ma50":      raw["above_ma50"],
            "crossed_ma50":    raw["crossed_ma50"],
            "overextended":    raw["overextended"],
            "ma50":            raw["ma50"],
            "realized_vol_20d": raw["realized_vol_20d"],
            "score":           round(cs_rank, 4),        # CS rank percentile (0=worst, 1=best)
            "reversal_score":  raw["reversal_score"],
            "junk_level":      junk["level"],
            "junk_summary":    junk["summary"],
            # --- New HF-grade fields ---
            "mom_12_1_pct":    raw["mom_12_1_pct"],
            "realized_vol_6m": raw["realized_vol_6m"],
            "vol_scaled_mom":  raw["vol_scaled_mom"],
            "ts_signal":       raw["ts_signal"],
            "amihud_illiq":    round(raw["amihud"] * 1e8, 4),
            "avg_dollar_vol_m": round(raw["avg_dollar_vol"] / 1e6, 2),
            "cs_rank":         round(cs_rank, 4),
            "sector":          sector_map.get(ticker, "Unknown"),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results, fails


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def print_table(results, top=None, reversal_mode=False):
    rows = results[:top] if top else results
    if not rows:
        print("No results.")
        return

    if reversal_mode:
        print(f"{'#':<3} {'Ticker':<8} {'Price':>8} {'5d Ret':>7} {'20d Ret':>8} {'MA50X':>5} "
              f"{'VolRatio':>9} {'R-Score':>8}  Filter")
        print("-" * 90)
        for i, r in enumerate(rows, 1):
            junk_col = f"[{r['junk_level']}] {r['junk_summary']}" if r["junk_level"] != "PASS" else "[OK]"
            over  = " OVER" if r.get("overextended") else ""
            cross = "X" if r.get("crossed_ma50") else "-"
            print(
                f"{i:<3} {r['ticker']:<8} ${r['price']:>7,.2f} "
                f"{r['return_5d_pct']:>+6.1f}% {r['return_20d_pct']:>+7.1f}% "
                f"{cross:>5} {r['vol_ratio']:>8.2f}x {r['reversal_score']:>8.4f}  {junk_col}{over}"
            )
        print()
        print("R-Score = 5d_return × clamp(VolRatio,0.5,3) × 2x_bonus_if_MA50_crossed")
        print("MA50X: X=just crossed above MA50 | - =already above or below")
    else:
        print(f"{'#':<3} {'Ticker':<8} {'Sector':<6} {'Price':>8} {'12-1Mom':>8} {'VolScaled':>10} "
              f"{'RVol6m':>7} {'AvgDV$M':>8} {'TS':>3} {'MA50':>5} {'CS-Rank':>8}  Filter")
        print("-" * 108)
        for i, r in enumerate(rows, 1):
            junk_col = f"[{r['junk_level']}] {r['junk_summary']}" if r["junk_level"] != "PASS" else "[OK]"
            ts_arrow = "↑" if r.get("ts_signal", 1) > 0 else "↓"
            ma_flag  = "Y" if r["above_ma50"] else "n"
            sec      = SECTOR_ABBREV.get(r.get("sector", "Unknown"), r.get("sector", "?")[:4])
            print(
                f"{i:<3} {r['ticker']:<8} {sec:<6} ${r['price']:>7,.2f} "
                f"{r['mom_12_1_pct']:>+7.1f}% {r['vol_scaled_mom']:>10.3f} "
                f"{r['realized_vol_6m']:>6.1%} {r['avg_dollar_vol_m']:>8.1f} "
                f"{ts_arrow:>3} {ma_flag:>5} {r['cs_rank']:>8.4f}  {junk_col}"
            )
        print()
        print("Score = sector-neutral CS rank of vol-scaled 12-1 momentum (0=worst in sector, 1=best)")
        print("12-1Mom = 12m return skipping last month  |  VolScaled = 12-1Mom / RealVol6m (ann.)")
        print("TS ↑ = time-series trend up (mom_12_1 > 0)  |  AvgDV$M = avg daily dollar volume ($M)")
        print("CS-Rank = percentile within GICS sector  |  MA50 Y=above / n=below")
        print("Filter: [OK]=clean [WARN]=caution [FAIL]=excluded from auto-buy")
        print()
        print("Papers: Jegadeesh&Titman 1993 | Barroso&Santa-Clara 2015 | Asness+Moskowitz+Pedersen 2013")
        print("        Moskowitz+Ooi+Pedersen 2012 | Amihud 2002 | Novy-Marx 2013 | Sloan 1996 (--fundamentals)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--top",          type=int, default=None)
    parser.add_argument("--json",         action="store_true")
    parser.add_argument("--fundamentals", action="store_true",
                        help="Add yfinance quality checks: gross profitability (Novy-Marx), "
                             "accruals (Sloan), EPS, debt, OCF — slower (~30s extra)")
    parser.add_argument("--reversal",     action="store_true",
                        help="Sort by reversal score (beginning-of-trend mode)")
    parser.add_argument("tickers",        nargs="*")
    args = parser.parse_args()

    load_env()
    sys.path.insert(0, str(ROOT / "scripts"))

    tickers = [t.upper() for t in args.tickers] if args.tickers else load_watchlist()
    if not tickers:
        print("No tickers to screen.")
        sys.exit(1)

    fetch_list = list(set(tickers + [BENCHMARK]))
    print(f"Fetching {len(fetch_list)} tickers ({HISTORY_DAYS}d history) from Alpaca...", file=sys.stderr)
    if args.fundamentals:
        print("Fundamental checks ON (yfinance — may take ~30s)...", file=sys.stderr)
    if args.reversal:
        print("Reversal mode ON — filtering overextended, sorting by reversal score...", file=sys.stderr)

    try:
        bars_data = fetch_bars(fetch_list)
    except Exception as e:
        print(f"ERROR fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    results, fails = screen(tickers, bars_data, fetch_fundamentals=args.fundamentals)

    if args.reversal:
        results = [r for r in results
                   if not r.get("overextended")
                   and r.get("reversal_score", 0) > 0
                   and r.get("return_5d_pct", 0) > 0]
        results.sort(key=lambda x: x["reversal_score"], reverse=True)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    mode_label = "Reversal (beginning-of-trend)" if args.reversal else "Momentum"
    print(f"\n## {mode_label} Screen — {date.today()}\n")
    print_table(results, top=args.top, reversal_mode=args.reversal)

    if fails:
        print(f"\n[skipped {len(fails)}]: " + ", ".join(f"{t}({r})" for t, r in fails[:8]))


if __name__ == "__main__":
    main()
