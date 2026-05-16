#!/usr/bin/env python3
"""
Full macro snapshot: Alpaca ETF proxies + direct Yahoo Finance HTTP (all macro).

Usage:
    code/python/.venv/Scripts/python scripts/macro-snapshot.py

Output sections (markdown, embed directly in pre-market brief):
  1. US ETF Proxies    (Alpaca)      — SPY, QQQM, IWM, VXX, TLT, USO, UUP, GLD
  2. US Futures        (direct HTTP) — ES=F, NQ=F, YM=F, RTY=F
  3. Macro Indicators  (direct HTTP) — VIX, 10Y yield, WTI, Brent, Gold, DXY

All market data fetched via Yahoo Finance v8 chart API directly — no yfinance library,
no rate limiting issues.

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import os
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ALPACA_PROXIES = [
    ("SPY",  "S&P 500",      "up=risk-on"),
    ("QQQM", "Nasdaq-100",   "up=tech risk-on"),
    ("IWM",  "Russell 2000", "up=small-cap risk-on"),
    ("VXX",  "VIX proxy",    "up=fear rising"),
    ("TLT",  "Bonds 20Y",    "down=yield rising -> pressures growth"),
    ("USO",  "WTI Oil",      "up=oil expensive"),
    ("UUP",  "Dollar (DXY)", "up=USD strong"),
    ("GLD",  "Gold",         "up=flight to safety"),
]

MACRO_TICKERS = [
    ("CL=F",     "WTI Crude",  "$/bbl", "up=oil expensive"),
    ("BZ=F",     "Brent",      "$/bbl", "up=global oil expensive"),
    ("^VIX",     "VIX",        "pts",   "fear index: <15 calm / 15-25 caution / >25 panic"),
    ("^TNX",     "10Y Yield",  "%",     "up=rates rising -> pressures growth stocks"),
    ("GC=F",     "Gold",       "$/oz",  "up=flight to safety"),
    ("DX-Y.NYB", "DXY",        "idx",   "up=USD strong -> pressures EM"),
]

# Bubble Risk Pulse tickers
BUBBLE_TICKERS = [
    ("^TNX",   "10Y Yield",      "%",   4.75, "high", "P/E compression zone"),
    ("^IRX",   "2Y Yield",       "%",   None, None,   "for 10Y-2Y spread"),
    ("^VIX9D", "VIX 9-Day",      "pts", None, None,   "short-term fear"),
    ("JPY=X",  "USD/JPY",        "idx", 145,  "low",  "carry unwind zone if <145"),
]

FUTURES_TICKERS = [
    ("ES=F",  "S&P 500 Futures", "idx", "implied S&P open direction"),
    ("NQ=F",  "Nasdaq Futures",  "idx", "implied Nasdaq open direction"),
    ("YM=F",  "Dow Futures",     "idx", "implied Dow open direction"),
    ("RTY=F", "Russell Futures", "idx", "implied small-cap direction"),
]

_YF_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def pct_str(pct):
    if pct is None:
        return "—"
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.2f}%"


def price_str(val, unit):
    if val is None:
        return "—"
    if unit == "%":
        return f"{val:.3f}%"
    if unit in ("pts", "idx"):
        return f"{val:,.2f}"
    return f"${val:,.2f}"


def signal_alpaca(ticker, pct):
    if pct is None:
        return ""
    if ticker == "VXX":
        return "FEAR+" if pct > 3 else ("fear-" if pct < -3 else "")
    if ticker == "TLT":
        return "YIELD+" if pct < -0.5 else ("yield-" if pct > 0.5 else "")
    if ticker in ("SPY", "QQQM", "IWM"):
        return "RISK+" if pct > 0.5 else ("risk-" if pct < -0.5 else "")
    return ""


# ---------------------------------------------------------------------------
# Direct Yahoo Finance v8 fetch (no yfinance library)
# ---------------------------------------------------------------------------

def fetch_vix_history(days: int = 252) -> list[float]:
    """Fetch VIX daily closes for the past `days` calendar days."""
    import requests
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1y"
        resp = requests.get(url, headers=_YF_HEADERS, timeout=10)
        resp.raise_for_status()
        closes = resp.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        return [c for c in closes if c is not None]
    except Exception:
        return []


def calc_vix_rank(current: float, history: list[float]) -> float | None:
    """Return VIX percentile rank (0.0–1.0) vs past year."""
    if not history or current is None:
        return None
    below = sum(1 for v in history if v <= current)
    return round(below / len(history), 3)


def calc_position_multiplier(vix_rank: float | None) -> float:
    """Kelly-VIX hybrid: continuous size multiplier from vix_rank. Range [0.20, 1.00]."""
    if vix_rank is None:
        return 0.5
    return round(max(0.20, 1.0 - 0.80 * vix_rank), 2)


def fetch_direct(ticker: str):
    """Fetch (current_price, pct_change) via Yahoo Finance v8 chart API."""
    import requests
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
        resp = requests.get(url, headers=_YF_HEADERS, timeout=10)
        resp.raise_for_status()
        result = resp.json()["chart"]["result"][0]
        closes = result["indicators"]["quote"][0]["close"]
        valid = [c for c in closes if c is not None]
        if len(valid) < 2:
            return None, None
        current, prev = valid[-1], valid[-2]
        pct = (current - prev) / prev * 100 if prev else None
        return round(current, 4), pct
    except Exception:
        return None, None


def fetch_direct_batch(items):
    result = {}
    for ticker, *_ in items:
        current, pct = fetch_direct(ticker)
        result[ticker] = {"current": current, "pct": pct}
    return result


# ---------------------------------------------------------------------------
# Alpaca fetch
# ---------------------------------------------------------------------------

def fetch_alpaca():
    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest, StockLatestTradeRequest
    from alpaca.data.timeframe import TimeFrame

    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        return None, "ALPACA_API_KEY / ALPACA_SECRET_KEY not set"

    try:
        client = StockHistoricalDataClient(api_key, secret_key)
        tickers = [p[0] for p in ALPACA_PROXIES]

        trades_resp = client.get_stock_latest_trade(
            StockLatestTradeRequest(symbol_or_symbols=tickers)
        )
        start = datetime.combine(date.today() - timedelta(days=10), datetime.min.time())
        bars_resp = client.get_stock_bars(
            StockBarsRequest(symbol_or_symbols=tickers, timeframe=TimeFrame.Day, start=start)
        )
        bars_data = bars_resp.data

        result = {}
        for ticker in tickers:
            current = prev_close = None
            if ticker in trades_resp:
                current = trades_resp[ticker].price
            bars = bars_data.get(ticker, [])
            if len(bars) >= 2:
                b = bars[-2]
                prev_close = b["close"] if isinstance(b, dict) else b.close
            pct = (current - prev_close) / prev_close * 100 if current and prev_close else None
            result[ticker] = {"current": current, "pct": pct}
        return result, None
    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# Print sections
# ---------------------------------------------------------------------------

def print_alpaca_section(data, error):
    print("### US ETF Proxies (Alpaca)")
    if error:
        print(f"*[Alpaca unavailable: {error}]*\n")
        return
    print("| ETF | Proxy | Price | Change | Context | Signal |")
    print("|---|---|---|---|---|---|")
    for ticker, label, meaning in ALPACA_PROXIES:
        d = data.get(ticker, {})
        p = price_str(d.get("current"), "$")
        ch = pct_str(d.get("pct"))
        sig = signal_alpaca(ticker, d.get("pct"))
        print(f"| **{ticker}** | {label} | {p} | {ch} | {meaning} | {sig} |")
    print()


def print_futures_section(data):
    print("### US Futures (direct HTTP)")
    print("| Futures | Level | Change | Context |")
    print("|---|---|---|---|")
    for ticker, label, unit, meaning in FUTURES_TICKERS:
        d = data.get(ticker, {})
        val = price_str(d.get("current"), unit)
        ch = pct_str(d.get("pct"))
        print(f"| **{label}** | {val} | {ch} | {meaning} |")
    print()


def print_bubble_pulse(macro_data: dict):
    """Bubble Risk Pulse — derived from 4 vectors available via Yahoo Finance."""
    print("### Bubble Risk Pulse")

    alerts = []

    # 1. Long-end Yield
    tnx = macro_data.get("^TNX", {}).get("current")
    irx = macro_data.get("^IRX", {}).get("current")
    if tnx is not None:
        flag = " [!] P/E compression zone" if tnx > 4.75 else ""
        print(f"- 10Y Yield: **{tnx:.3f}%**{flag}")
        if tnx > 4.75:
            alerts.append("10Y>4.75%")
    if tnx is not None and irx is not None:
        irx_pct = irx / 100 if irx > 10 else irx
        spread = tnx - irx_pct
        flag = " [!] term premium rising" if spread > 0.5 else ""
        print(f"- 10Y-2Y Spread: **{spread:+.2f}%**{flag}")
        if spread > 0.5:
            alerts.append("spread>50bps")

    # 2. Yen Carry
    jpy = macro_data.get("JPY=X", {}).get("current")
    if jpy is not None:
        flag = " [!] carry unwind risk" if jpy < 145 else (" [?] watch" if jpy < 150 else "")
        print(f"- USD/JPY: **{jpy:.2f}**{flag}")
        if jpy < 145:
            alerts.append("JPY<145")

    # 3. VIX term structure
    vix = macro_data.get("^VIX", {}).get("current")
    vix9d = macro_data.get("^VIX9D", {}).get("current")
    if vix is not None and vix9d is not None:
        ratio = round(vix9d / vix, 3)
        if ratio < 0.85:
            structure = "backwardation [!] short-term fear spike"
            alerts.append("VIX backwardation")
        elif ratio > 1.10:
            structure = "contango (calm)"
        else:
            structure = "flat"
        print(f"- VIX term structure: VIX9D/VIX = **{ratio:.2f}** ({structure})")
    elif vix is not None:
        print(f"- VIX: **{vix:.1f}** (VIX9D unavailable)")

    # Summary
    print()
    if alerts:
        print(f"[!] Bubble Risk Alerts: {' | '.join(alerts)}")
        print("*See vault/10_research/bubble-risk-framework.md for full vector analysis*")
    else:
        print("Bubble Risk Pulse: No alerts -- all vectors within normal range")
    print()


def print_macro_section(data, vix_rank: float | None = None, pos_multiplier: float | None = None):
    print("### Macro Indicators (direct HTTP)")
    print("| Indicator | Ticker | Value | Change | Context |")
    print("|---|---|---|---|---|")
    for ticker, label, unit, meaning in MACRO_TICKERS:
        d = data.get(ticker, {})
        val = price_str(d.get("current"), unit)
        ch = pct_str(d.get("pct"))
        if ticker == "^VIX" and vix_rank is not None:
            rank_pct = int(vix_rank * 100)
            print(f"| **{label}** | {ticker} | {val} | {ch} | {meaning} — VIX-Rank {rank_pct}th pct |")
        else:
            print(f"| **{label}** | {ticker} | {val} | {ch} | {meaning} |")
    print()
    if vix_rank is not None and pos_multiplier is not None:
        rank_pct = int(vix_rank * 100)
        pct_size = int(pos_multiplier * 100)
        print(f"**Position Sizing (VIX-Rank):** VIX is at {rank_pct}th percentile of past year -> size multiplier **{pos_multiplier}x** ({pct_size}% of base size)\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_env()
    fetched_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    print("## Macro Snapshot")
    print(f"*Alpaca (US ETFs) + Yahoo Finance direct HTTP (macro) | embed in pre-market brief | fetched: {fetched_at}*\n")
    print("---\n")

    # Alpaca ETF proxies
    alpaca_data, alpaca_err = fetch_alpaca()
    print_alpaca_section(alpaca_data or {}, alpaca_err)

    # Futures via direct HTTP
    futures_data = fetch_direct_batch(FUTURES_TICKERS)
    print_futures_section(futures_data)

    # Macro via direct HTTP
    macro_data = fetch_direct_batch(MACRO_TICKERS)
    vix_history = fetch_vix_history()
    current_vix = macro_data.get("^VIX", {}).get("current")
    vix_rank = calc_vix_rank(current_vix, vix_history)
    pos_multiplier = calc_position_multiplier(vix_rank)
    print_macro_section(macro_data, vix_rank, pos_multiplier)

    # Bubble Risk Pulse — fetch extra tickers + print
    bubble_data = fetch_direct_batch([(t, None, None, None) for t, *_ in BUBBLE_TICKERS])
    merged = {**macro_data, **bubble_data}
    print_bubble_pulse(merged)

    # Quick read summary
    reads = []
    if alpaca_data:
        spy_pct = alpaca_data.get("SPY", {}).get("pct")
        vxx_pct = alpaca_data.get("VXX", {}).get("pct")
        tlt_pct = alpaca_data.get("TLT", {}).get("pct")
        if spy_pct and spy_pct > 0.3:
            reads.append(f"SPY +{spy_pct:.1f}%")
        elif spy_pct and spy_pct < -0.3:
            reads.append(f"SPY {spy_pct:.1f}%")
        if vxx_pct and abs(vxx_pct) > 2:
            reads.append(f"VXX {'+' if vxx_pct > 0 else ''}{vxx_pct:.1f}% fear {'up' if vxx_pct > 0 else 'down'}")
        if tlt_pct and abs(tlt_pct) > 0.4:
            reads.append(f"TLT {'+' if tlt_pct > 0 else ''}{tlt_pct:.1f}% yield {'down' if tlt_pct > 0 else 'up'}")

    wti = macro_data.get("CL=F", {})
    if wti.get("current"):
        pct = wti.get("pct")
        s = f"WTI ${wti['current']:.2f}"
        if pct is not None:
            s += f" ({'+' if pct >= 0 else ''}{pct:.1f}%)"
        reads.append(s)

    vix = macro_data.get("^VIX", {})
    if vix.get("current"):
        v = vix["current"]
        zone = "calm" if v < 15 else ("CAUTION" if v < 25 else "PANIC")
        reads.append(f"VIX {v:.1f} [{zone}]")

    if reads:
        print("**Quick read:** " + " | ".join(reads))


if __name__ == "__main__":
    main()
