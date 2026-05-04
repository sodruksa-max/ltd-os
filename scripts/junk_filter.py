"""
Junk stock filter — detects financially weak, manipulated, or delisting-risk stocks.

Imported by screener.py and auto-buy.py.

Filter levels:
  PASS — no issues
  WARN — caution flag (auto-buy proceeds but shows warning)
  FAIL — hard disqualification (auto-buy skips this ticker)

Price-based checks (uses existing Alpaca bar data — no extra API call):
  1. Extreme runup      : 20d return > 100%               → WARN (possible pump-and-dump)
  2. High volatility    : daily std > 8%                  → WARN (erratic price action)
  3. Near 52w low       : price < 115% of period low      → WARN (weak price structure)
  4. Low liquidity      : avg daily dollar vol < $5M      → WARN  (Amihud 2002)

Fundamental checks (yfinance — optional, pass fetch_fund=True):
  5. Micro-cap          : market cap < $50M               → FAIL (delisting risk)
  6. Negative EPS       : trailing AND forward < 0        → FAIL (loss-making, no recovery)
  7. Extreme debt       : D/E > 500%                      → FAIL (overleveraged)
  8. Negative OCF       : operating cash flow < 0         → WARN (burning cash)
  9. Revenue shrink     : revenue growth < -30% YoY       → WARN (declining business)
  10. Low gross profit  : gross_profit/assets < 0         → WARN  (Novy-Marx 2013)
  11. High accruals     : (net_income - OCF) / assets > 0.10 → WARN  (Sloan 1996)
  12. Pump signal       : 20d return >150% + bad fund     → FAIL (cross-check)

ETFs are exempt from fundamental checks (quoteType=ETF).
"""

import time
from statistics import stdev


# ---------------------------------------------------------------------------
# Price-based checks (fast, no extra API)
# ---------------------------------------------------------------------------

def check_price_based(ticker: str, closes: list, volumes: list,
                      lookback: int = 20, avg_dollar_vol: float = 0.0) -> list:
    """Returns list of (level, code, detail) tuples."""
    issues = []
    if len(closes) < lookback + 2:
        return issues

    current = closes[-1]
    past    = closes[-lookback - 1]
    ret_20d = (current - past) / past if past > 0 else 0

    # 1. Overextended
    if 0.70 < ret_20d <= 1.0:
        issues.append(("WARN", "OVEREXT", f"+{ret_20d*100:.0f}% in 20d"))

    # Extreme runup — possible pump
    if ret_20d > 1.0:
        issues.append(("WARN", "PUMP?", f"+{ret_20d*100:.0f}% in 20d"))

    # 2. Daily return volatility
    daily_rets = [
        (closes[i] - closes[i - 1]) / closes[i - 1]
        for i in range(max(1, len(closes) - lookback), len(closes))
        if closes[i - 1] > 0
    ]
    if len(daily_rets) >= 5:
        vol = stdev(daily_rets)
        if vol > 0.08:
            issues.append(("WARN", "VOLATILE", f"daily std {vol*100:.1f}%"))

    # 3. Near period low
    period_low = min(closes)
    if period_low > 0 and current < period_low * 1.15:
        issues.append(("WARN", "LOW", f"within 15% of period low ${period_low:.2f}"))

    # 4. Liquidity filter (Amihud 2002) — flag stocks with thin daily dollar volume
    if avg_dollar_vol > 0:
        if avg_dollar_vol < 1_000_000:
            issues.append(("FAIL", "ILLIQUID", f"avg daily vol ${avg_dollar_vol/1e6:.1f}M (<$1M)"))
        elif avg_dollar_vol < 5_000_000:
            issues.append(("WARN", "LOW_LIQ", f"avg daily vol ${avg_dollar_vol/1e6:.1f}M (<$5M)"))

    return issues


# ---------------------------------------------------------------------------
# Fundamental checks (yfinance, optional)
# ---------------------------------------------------------------------------

ETF_QUOTE_TYPES = {"ETF", "MUTUALFUND", "INDEX"}
_fund_cache: dict = {}


def fetch_fundamentals(ticker: str) -> dict:
    if ticker in _fund_cache:
        return _fund_cache[ticker]
    try:
        import yfinance as yf
        t    = yf.Ticker(ticker)
        info = t.info or {}
        _fund_cache[ticker] = info
        time.sleep(0.3)
        return info
    except Exception:
        _fund_cache[ticker] = {}
        return {}


def check_fundamentals(ticker: str, ret_20d: float = 0.0) -> list:
    issues = []
    info   = fetch_fundamentals(ticker)
    if not info:
        return []

    # Skip ETFs
    if info.get("quoteType", "") in ETF_QUOTE_TYPES:
        return []

    # 5. Micro-cap
    market_cap = info.get("marketCap") or 0
    if 0 < market_cap < 50_000_000:
        issues.append(("FAIL", "MICRO_CAP", f"mktcap ${market_cap/1e6:.0f}M (<$50M)"))
    elif 0 < market_cap < 300_000_000:
        issues.append(("WARN", "SMALL_CAP", f"mktcap ${market_cap/1e6:.0f}M (<$300M)"))

    # 6. Negative EPS
    trailing_eps = info.get("trailingEps")
    forward_eps  = info.get("forwardEps")
    if trailing_eps is not None and forward_eps is not None:
        if trailing_eps < 0 and forward_eps < 0:
            issues.append(("FAIL", "NEG_EPS", f"trail {trailing_eps:.2f} / fwd {forward_eps:.2f}"))
        elif trailing_eps < 0:
            issues.append(("WARN", "NEG_EPS_T", f"trailing EPS {trailing_eps:.2f}"))

    # 7. Extreme debt
    dte = info.get("debtToEquity")
    if dte is not None:
        if dte > 500:
            issues.append(("FAIL", "HIGH_DEBT", f"D/E {dte:.0f}%"))
        elif dte > 300:
            issues.append(("WARN", "DEBT", f"D/E {dte:.0f}%"))

    # 8. Negative operating cash flow
    ocf = info.get("operatingCashflow")
    if ocf is not None and ocf < 0:
        issues.append(("WARN", "NEG_OCF", f"OCF ${ocf/1e6:.0f}M"))

    # 9. Revenue shrinking
    rev_growth = info.get("revenueGrowth")
    if rev_growth is not None and rev_growth < -0.30:
        issues.append(("WARN", "REV_DOWN", f"rev {rev_growth*100:.0f}% YoY"))

    # 10. Gross profitability (Novy-Marx 2013)
    # gross_profit / total_assets — negative = company destroys value on every sale
    gross_profits = info.get("grossProfits")
    total_assets  = info.get("totalAssets")
    if gross_profits is not None and total_assets and total_assets > 0:
        gp_ratio = gross_profits / total_assets
        if gp_ratio < 0:
            issues.append(("FAIL", "NEG_GROSSPROF", f"gross_profit/assets {gp_ratio:.3f}"))
        elif gp_ratio < 0.10:
            issues.append(("WARN", "LOW_QUALITY", f"gross_profit/assets {gp_ratio:.3f} (<0.10)"))

    # 11. Accruals / earnings quality (Sloan 1996)
    # High accruals = earnings not backed by real cash — earnings manipulation signal
    net_income = info.get("netIncome")
    if net_income is not None and ocf is not None and total_assets and total_assets > 0:
        accruals = (net_income - ocf) / total_assets
        if accruals > 0.15:
            issues.append(("FAIL", "HIGH_ACCRUALS", f"accruals {accruals:.3f} (earnings quality risk)"))
        elif accruals > 0.10:
            issues.append(("WARN", "ACCRUALS", f"accruals {accruals:.3f} (watch earnings quality)"))

    # 12. Cross-check: huge runup + bad fundamentals = confirmed pump
    if ret_20d > 1.5 and any(l == "FAIL" for l, _, _ in issues):
        issues.append(("FAIL", "PUMP_CONFIRMED", f"+{ret_20d*100:.0f}% runup + bad fundamentals"))

    return issues


# ---------------------------------------------------------------------------
# Aggregate result
# ---------------------------------------------------------------------------

def evaluate(ticker: str, closes: list, volumes: list,
             ret_20d: float = 0.0,
             avg_dollar_vol: float = 0.0,
             fetch_fund: bool = False) -> dict:
    """
    Returns:
      {
        "level":   "PASS" | "WARN" | "FAIL",
        "issues":  [(level, code, detail), ...],
        "summary": "short string for table display"
      }
    """
    issues = check_price_based(ticker, closes, volumes, avg_dollar_vol=avg_dollar_vol)

    if fetch_fund:
        issues += check_fundamentals(ticker, ret_20d=ret_20d)

    if any(l == "FAIL" for l, _, _ in issues):
        level = "FAIL"
    elif any(l == "WARN" for l, _, _ in issues):
        level = "WARN"
    else:
        level = "PASS"

    summary = "OK" if level == "PASS" else " | ".join(f"[{l}] {c}: {d}" for l, c, d in issues)

    return {"level": level, "issues": issues, "summary": summary}
