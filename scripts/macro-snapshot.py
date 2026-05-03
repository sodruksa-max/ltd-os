#!/usr/bin/env python3
"""
Full macro snapshot: Alpaca ETF proxies + yfinance (yields, commodities, Asia).

Usage:
    code/python/.venv/Scripts/python scripts/macro-snapshot.py

Output sections (markdown, embed directly in pre-market brief):
  1. US ETF Proxies       (Alpaca)   — SPY, QQQ, IWM, VXX, TLT, USO, UUP, GLD
  2. US Futures           (yfinance) — ES=F, NQ=F, YM=F, RTY=F
  3. Macro Indicators     (yfinance) — VIX, 10Y yield, WTI, Brent, Gold, DXY
  4. Asia Markets         (yfinance) — Nikkei, Hang Seng, KOSPI, ASX 200, CSI 300

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
yfinance requires no API key.
"""

import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ALPACA_PROXIES = [
    ("SPY", "S&P 500",      "up=risk-on"),
    ("QQQ", "Nasdaq-100",   "up=tech risk-on"),
    ("IWM", "Russell 2000", "up=small-cap risk-on"),
    ("VXX", "VIX proxy",    "up=fear rising"),
    ("TLT", "Bonds 20Y",    "down=yield rising -> pressures growth"),
    ("USO", "WTI Oil",      "up=oil expensive"),
    ("UUP", "Dollar (DXY)", "up=USD strong"),
    ("GLD", "Gold",         "up=flight to safety"),
]

YF_MACRO = [
    ("^VIX",     "VIX",        "pts",   "fear index: <15 calm / 15-25 caution / >25 panic"),
    ("^TNX",     "10Y Yield",  "%",     "up=rates rising -> pressures growth stocks"),
    ("CL=F",     "WTI Crude",  "$/bbl", "up=oil expensive"),
    ("BZ=F",     "Brent",      "$/bbl", "up=global oil expensive"),
    ("GC=F",     "Gold",       "$/oz",  "up=flight to safety"),
    ("DX-Y.NYB", "DXY",        "idx",   "up=USD strong -> pressures EM"),
]

YF_FUTURES = [
    ("ES=F",  "S&P 500 Futures",  "idx",   "implied S&P open direction"),
    ("NQ=F",  "Nasdaq Futures",   "idx",   "implied Nasdaq open direction"),
    ("YM=F",  "Dow Futures",      "idx",   "implied Dow open direction"),
    ("RTY=F", "Russell Futures",  "idx",   "implied small-cap direction"),
]

YF_ASIA = [
    ("^N225",    "Nikkei 225",  "Japan"),
    ("^HSI",     "Hang Seng",   "HK/China"),
    ("^KS11",    "KOSPI",       "Korea"),
    ("^AXJO",    "ASX 200",     "Australia"),
    ("000300.SS","CSI 300",     "China (may lag)"),
]


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
        return f"{val:.2f}%"
    if unit == "pts" or unit == "idx":
        return f"{val:,.2f}"
    return f"${val:,.2f}"


def signal_alpaca(ticker, pct):
    if pct is None:
        return ""
    if ticker == "VXX":
        return "FEAR+" if pct > 3 else ("fear-" if pct < -3 else "")
    if ticker == "TLT":
        return "YIELD+" if pct < -0.5 else ("yield-" if pct > 0.5 else "")
    if ticker in ("SPY", "QQQ", "IWM"):
        return "RISK+" if pct > 0.5 else ("risk-" if pct < -0.5 else "")
    return ""


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
# yfinance fetch
# ---------------------------------------------------------------------------

_yf_rate_limited = False

def yf_quote(ticker):
    """Return (current_price, pct_change) or (None, None) on failure."""
    global _yf_rate_limited
    if _yf_rate_limited:
        return None, None
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        info = t.fast_info
        current = info.last_price
        prev = info.previous_close
        pct = (current - prev) / prev * 100 if current and prev else None
        return current, pct
    except Exception as e:
        if "Rate" in str(e) or "429" in str(e):
            _yf_rate_limited = True
            print("[warn] yfinance rate limited -- wait 5-10 min and retry")
        return None, None


def fetch_yf_section(items):
    result = {}
    for ticker, *_ in items:
        current, pct = yf_quote(ticker)
        result[ticker] = {"current": current, "pct": pct}
    return result


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


def print_macro_section(data):
    print("### Macro Indicators (yfinance)")
    print("| Indicator | Ticker | Value | Change | Context |")
    print("|---|---|---|---|---|")
    for ticker, label, unit, meaning in YF_MACRO:
        d = data.get(ticker, {})
        val = price_str(d.get("current"), unit)
        ch = pct_str(d.get("pct"))
        print(f"| **{label}** | {ticker} | {val} | {ch} | {meaning} |")
    print()


def print_futures_section(data):
    print("### US Futures (yfinance)")
    print("| Futures | Level | Change | Context |")
    print("|---|---|---|---|")
    for ticker, label, unit, meaning in YF_FUTURES:
        d = data.get(ticker, {})
        val = price_str(d.get("current"), unit)
        ch = pct_str(d.get("pct"))
        print(f"| **{label}** | {val} | {ch} | {meaning} |")
    print()


def print_asia_section(data):
    print("### Asia Markets (yfinance)")
    print("| Market | Level | Change | Region |")
    print("|---|---|---|---|")
    for ticker, label, region in YF_ASIA:
        d = data.get(ticker, {})
        val = price_str(d.get("current"), "idx")
        ch = pct_str(d.get("pct"))
        print(f"| **{label}** | {val} | {ch} | {region} |")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_env()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("## Macro Snapshot")
    print(f"*{now} | Alpaca (US ETFs) + yfinance (macro + Asia) | embed in pre-market brief*\n")
    print("---\n")

    # Alpaca
    alpaca_data, alpaca_err = fetch_alpaca()
    print_alpaca_section(alpaca_data or {}, alpaca_err)

    # yfinance futures
    yf_futures_data = fetch_yf_section(YF_FUTURES)
    print_futures_section(yf_futures_data)

    # yfinance macro
    yf_macro_data = fetch_yf_section(YF_MACRO)
    print_macro_section(yf_macro_data)

    # yfinance Asia
    yf_asia_data = fetch_yf_section(YF_ASIA)
    print_asia_section(yf_asia_data)

    # Quick read summary
    reads = []
    if alpaca_data:
        spy_pct = alpaca_data.get("SPY", {}).get("pct")
        vxx_pct = alpaca_data.get("VXX", {}).get("pct")
        tlt_pct = alpaca_data.get("TLT", {}).get("pct")
        if spy_pct and spy_pct > 0.3:
            reads.append(f"SPY +{spy_pct:.1f}% pre-mkt")
        elif spy_pct and spy_pct < -0.3:
            reads.append(f"SPY {spy_pct:.1f}% pre-mkt")
        if vxx_pct and abs(vxx_pct) > 2:
            reads.append(f"VXX {'+' if vxx_pct > 0 else ''}{vxx_pct:.1f}% fear {'up' if vxx_pct > 0 else 'down'}")
        if tlt_pct and abs(tlt_pct) > 0.4:
            reads.append(f"TLT {'+' if tlt_pct > 0 else ''}{tlt_pct:.1f}% yield {'down' if tlt_pct > 0 else 'up'}")

    vix_val = yf_macro_data.get("^VIX", {}).get("current")
    if vix_val:
        zone = "calm" if vix_val < 15 else ("CAUTION" if vix_val < 25 else "PANIC")
        reads.append(f"VIX {vix_val:.1f} [{zone}]")

    if reads:
        print("**Quick read:** " + " | ".join(reads))


if __name__ == "__main__":
    main()
