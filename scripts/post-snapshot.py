#!/usr/bin/env python3
"""
Post-market snapshot: fetch EOD close prices for a target trading date.

Replaces 4 web searches in /post-market (index + sector + VIX + oil).
Earnings results still require web search (Alpaca has no EPS data).

Usage:
    python scripts/post-snapshot.py [--date YYYY-MM-DD]

Default date: yesterday (ET timezone).

Output (markdown): embed directly as Market Data section in post-market review.
Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import sys
import os
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# (ticker, label) — Alpaca historical bars
ALPACA_TICKERS = [
    ("SPY",  "S&P 500 proxy"),
    ("QQQ",  "Nasdaq-100 proxy"),
    ("DIA",  "Dow Jones proxy"),
    ("IWM",  "Russell 2000 proxy"),
    ("VXX",  "VIX proxy"),
    ("XLE",  "Energy"),
    ("XLK",  "Technology"),
    ("XLP",  "Cons Staples"),
    ("XLU",  "Utilities"),
    ("XLY",  "Cons Discretionary"),
    ("GLD",  "Gold ETF"),
    ("TLT",  "Bonds 20Y"),
    ("USO",  "WTI proxy"),
    ("BNO",  "Brent proxy"),
]

# (ticker, label, unit) — Yahoo Finance direct HTTP
MACRO_TICKERS = [
    ("^VIX", "VIX",       "pts"),
    ("^TNX", "10Y Yield", "%"),
    ("CL=F", "WTI Crude", "$/bbl"),
    ("BZ=F", "Brent",     "$/bbl"),
    ("GC=F", "Gold spot", "$/oz"),
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
        return "[unverified]"
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.2f}%"


def scenario_label(spy_pct):
    if spy_pct is None:
        return "[unverified]"
    if spy_pct > 0.3:
        return "Bullish"
    if spy_pct < -0.3:
        return "Bearish"
    return "Base"


# ---------------------------------------------------------------------------
# Alpaca: historical EOD bars
# ---------------------------------------------------------------------------

def fetch_alpaca_bars(target_date: date):
    """Returns dict: ticker -> {close, prev_close, pct, high, low, open} for target_date."""
    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        return None, "ALPACA_API_KEY / ALPACA_SECRET_KEY not set"

    try:
        client = StockHistoricalDataClient(api_key, secret_key)
        tickers = [t[0] for t in ALPACA_TICKERS]

        start = datetime.combine(target_date - timedelta(days=14), datetime.min.time())
        end   = datetime.combine(target_date + timedelta(days=1),  datetime.min.time())

        resp = client.get_stock_bars(
            StockBarsRequest(
                symbol_or_symbols=tickers,
                timeframe=TimeFrame.Day,
                start=start,
                end=end,
                feed="iex",
            )
        )
        bars_by_ticker = resp.data

        result = {}
        for ticker in tickers:
            bars = bars_by_ticker.get(ticker, [])
            if not bars:
                result[ticker] = {}
                continue

            def _date(b):
                ts = b.timestamp if hasattr(b, "timestamp") else b["timestamp"]
                return ts.date() if hasattr(ts, "date") else ts.date()

            def _val(b, attr):
                return getattr(b, attr) if hasattr(b, attr) else b[attr]

            # Find target date bar + prior bar
            target_bar = prev_bar = None
            for i, b in enumerate(bars):
                if _date(b) == target_date:
                    target_bar = b
                    if i > 0:
                        prev_bar = bars[i - 1]
                    break
                elif _date(b) < target_date:
                    prev_bar = b

            # Fallback: last bar within 3 days
            if target_bar is None and bars:
                last = bars[-1]
                if (target_date - _date(last)).days <= 3:
                    target_bar = last
                    if len(bars) >= 2:
                        prev_bar = bars[-2]

            if target_bar is None:
                result[ticker] = {}
                continue

            close      = _val(target_bar, "close")
            prev_close = _val(prev_bar,   "close") if prev_bar else None
            pct = (close - prev_close) / prev_close * 100 if close and prev_close else None

            result[ticker] = {
                "close":      close,
                "prev_close": prev_close,
                "pct":        pct,
                "high":       _val(target_bar, "high"),
                "low":        _val(target_bar, "low"),
                "open":       _val(target_bar, "open"),
            }

        return result, None

    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# Yahoo Finance: direct HTTP OHLCV
# ---------------------------------------------------------------------------

def fetch_yf_ohlc(ticker: str, target_date: date):
    """Returns (close, high, low, pct) for target_date via Yahoo Finance v8.
    Retries up to 3 times with exponential backoff on rate-limit (429) or errors.
    """
    import requests, time
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?interval=1d&range=15d"
    )

    for attempt in range(3):
        try:
            resp = requests.get(url, headers=_YF_HEADERS, timeout=10)
            if resp.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            result = resp.json()["chart"]["result"][0]
            timestamps = result["timestamp"]
            quotes     = result["indicators"]["quote"][0]
            closes     = quotes.get("close", [])
            highs      = quotes.get("high",  [])
            lows       = quotes.get("low",   [])

            # Pair timestamps with data
            pairs = []
            for i, ts in enumerate(timestamps):
                ts_date = datetime.utcfromtimestamp(ts).date()
                c = closes[i] if i < len(closes) else None
                h = highs[i]  if i < len(highs)  else None
                l = lows[i]   if i < len(lows)   else None
                pairs.append((ts_date, c, h, l))

            # Find target date
            idx = next(
                (i for i, (d, c, _, _) in enumerate(pairs) if d == target_date and c is not None),
                None,
            )
            # Fallback: last valid bar
            if idx is None:
                for i in range(len(pairs) - 1, -1, -1):
                    if pairs[i][1] is not None:
                        idx = i
                        break

            if idx is None:
                return None, None, None, None

            _, close, high, low = pairs[idx]

            # Prev close
            prev_close = None
            for i in range(idx - 1, -1, -1):
                if pairs[i][1] is not None:
                    prev_close = pairs[i][1]
                    break

            pct = (close - prev_close) / prev_close * 100 if close and prev_close else None
            return close, high, low, pct

        except Exception:
            if attempt < 2:
                time.sleep(2 ** attempt)

    return None, None, None, None


# ---------------------------------------------------------------------------
# Print sections
# ---------------------------------------------------------------------------

def _fmt_macro(val, unit):
    if val is None:
        return "[unverified]"
    if unit == "%":
        return f"{val:.3f}%"
    if unit == "pts":
        return f"{val:.2f}"
    return f"${val:,.2f}"


def print_alpaca_section(data: dict):
    print("### ETF Closes (Alpaca)")
    print("| ETF | Label | Close | % Change | High | Low |")
    print("|---|---|---|---|---|---|")
    for ticker, label in ALPACA_TICKERS:
        d = data.get(ticker, {})
        close = f"${d['close']:.2f}" if d.get("close") else "[unverified]"
        pct   = pct_str(d.get("pct"))
        high  = f"${d['high']:.2f}"  if d.get("high") else "—"
        low   = f"${d['low']:.2f}"   if d.get("low")  else "—"
        print(f"| **{ticker}** | {label} | {close} | {pct} | {high} | {low} |")
    print()


def print_macro_section(macro: dict):
    print("### Macro Indicators (Yahoo Finance direct)")
    print("| Indicator | Close | % Change | Intraday High | Intraday Low |")
    print("|---|---|---|---|---|")
    for ticker, label, unit in MACRO_TICKERS:
        d     = macro.get(ticker, {})
        close = _fmt_macro(d.get("close"), unit)
        pct   = pct_str(d.get("pct"))
        high  = _fmt_macro(d.get("high"), unit) if d.get("high") else "—"
        low   = _fmt_macro(d.get("low"),  unit) if d.get("low")  else "—"
        print(f"| **{label}** ({ticker}) | {close} | {pct} | {high} | {low} |")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_env()

    parser = argparse.ArgumentParser(description="Post-market ETF + macro snapshot")
    parser.add_argument("--date", help="Target date YYYY-MM-DD (default: yesterday ET)")
    args = parser.parse_args()

    if args.date:
        target_date = date.fromisoformat(args.date)
    else:
        # Yesterday local time — when run in morning Bangkok = last US trading day
        target_date = date.today() - timedelta(days=1)

    fetched_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    day_name = target_date.strftime("%A")
    print(f"## Post-Market Snapshot — {target_date} ({day_name})")
    print(f"*Alpaca EOD bars + Yahoo Finance direct HTTP | สร้างโดย post-snapshot.py | fetched: {fetched_at}*\n")
    print("---\n")

    # Alpaca bars
    alpaca_data, err = fetch_alpaca_bars(target_date)
    if err:
        print(f"*[Alpaca unavailable: {err}]*\n")
        alpaca_data = {}
    else:
        print_alpaca_section(alpaca_data)

    # Macro via Yahoo Finance
    macro = {}
    for ticker, label, unit in MACRO_TICKERS:
        close, high, low, pct = fetch_yf_ohlc(ticker, target_date)
        macro[ticker] = {"close": close, "high": high, "low": low, "pct": pct}
    print_macro_section(macro)

    # Scenario verdict
    spy_pct = alpaca_data.get("SPY", {}).get("pct")
    vxx_pct = alpaca_data.get("VXX", {}).get("pct")
    vix_d   = macro.get("^VIX", {})

    scenario = scenario_label(spy_pct)
    print("---\n")
    print("### Scenario Verdict")
    print(f"- **SPY:** {pct_str(spy_pct)} → **{scenario}**")

    if vix_d.get("close"):
        vix_zone = (
            "calm" if vix_d["close"] < 15 else
            "caution" if vix_d["close"] < 20 else
            "ELEVATED" if vix_d["close"] < 25 else
            "PANIC"
        )
        high_str = f"{vix_d['high']:.2f}" if vix_d.get("high") else "[unverified]"
        print(f"- **VIX close / intraday high:** {vix_d['close']:.2f} / {high_str} [{vix_zone}]")

    if vxx_pct is not None:
        fear = "fear rising" if vxx_pct > 3 else ("fear falling" if vxx_pct < -3 else "")
        print(f"- **VXX:** {pct_str(vxx_pct)}{' — ' + fear if fear else ''}")

    tnx_d = macro.get("^TNX", {})
    if tnx_d.get("close"):
        print(f"- **10Y yield:** {tnx_d['close']:.3f}% ({pct_str(tnx_d.get('pct'))} in yield terms)")

    print()
    print(f"*Source: Alpaca historical bars + Yahoo Finance v8 chart API | {target_date}*")


if __name__ == "__main__":
    main()
