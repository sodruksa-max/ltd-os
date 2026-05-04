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


def print_macro_section(data):
    print("### Macro Indicators (direct HTTP)")
    print("| Indicator | Ticker | Value | Change | Context |")
    print("|---|---|---|---|---|")
    for ticker, label, unit, meaning in MACRO_TICKERS:
        d = data.get(ticker, {})
        val = price_str(d.get("current"), unit)
        ch = pct_str(d.get("pct"))
        print(f"| **{label}** | {ticker} | {val} | {ch} | {meaning} |")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_env()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("## Macro Snapshot")
    print(f"*{now} | Alpaca (US ETFs) + Yahoo Finance direct HTTP (macro) | embed in pre-market brief*\n")
    print("---\n")

    # Alpaca ETF proxies
    alpaca_data, alpaca_err = fetch_alpaca()
    print_alpaca_section(alpaca_data or {}, alpaca_err)

    # Futures via direct HTTP
    futures_data = fetch_direct_batch(FUTURES_TICKERS)
    print_futures_section(futures_data)

    # Macro via direct HTTP
    macro_data = fetch_direct_batch(MACRO_TICKERS)
    print_macro_section(macro_data)

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
