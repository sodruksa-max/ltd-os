#!/usr/bin/env python3
"""
Weekly market snapshot: aggregate EOD performance for a full trading week.

Replaces 5 of 6 web searches in /weekly-market (keeps 1 for key events/earnings).

Usage:
    python scripts/weekly-snapshot.py [--week YYYY-Www]

Default: last completed Mon-Fri week (based on local date).

Output (markdown): embed directly as Market Data section in /weekly-market.
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
    ("UUP",  "Dollar (DXY proxy)"),
]

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


def resolve_week(week_str=None):
    """Return (monday, friday, iso_label) for the target week."""
    if week_str:
        year_s, wn_s = week_str.split("-W")
        monday = date.fromisocalendar(int(year_s), int(wn_s), 1)
    else:
        today = date.today()
        wd = today.weekday()  # 0=Mon … 6=Sun
        if wd >= 5:           # Sat/Sun — week that just ended = this week
            monday = today - timedelta(days=wd)
        else:                  # Mon-Fri — last completed week
            monday = today - timedelta(days=wd + 7)
    friday = monday + timedelta(days=4)
    iso_week = monday.isocalendar()
    label = f"{iso_week[0]}-W{iso_week[1]:02d}"
    return monday, friday, label


def pct_str(pct):
    if pct is None:
        return "[unverified]"
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.2f}%"


def regime_label(spy_weekly_pct):
    if spy_weekly_pct is None:
        return "[unverified]"
    if spy_weekly_pct > 1.5:
        return "Risk-On (Strong)"
    if spy_weekly_pct > 0.3:
        return "Risk-On (Mild)"
    if spy_weekly_pct >= -0.3:
        return "Flat / Indecisive"
    if spy_weekly_pct >= -1.5:
        return "Risk-Off (Mild)"
    return "Risk-Off (Strong)"


# ---------------------------------------------------------------------------
# Alpaca: weekly aggregated bars
# ---------------------------------------------------------------------------

def fetch_weekly_alpaca(monday: date, friday: date):
    """
    Returns dict: ticker -> {mon_close, fri_close, weekly_pct,
                              weekly_high, weekly_low, num_days}

    Weekly % = (this_friday_close - prev_friday_close) / prev_friday_close
    """
    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    api_key    = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        return None, "ALPACA_API_KEY / ALPACA_SECRET_KEY not set"

    try:
        client  = StockHistoricalDataClient(api_key, secret_key)
        tickers = [t[0] for t in ALPACA_TICKERS]

        # Fetch 3 weeks of data to capture prev Friday baseline
        start = datetime.combine(monday - timedelta(days=14), datetime.min.time())
        end   = datetime.combine(friday + timedelta(days=2),  datetime.min.time())

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
        prev_friday = monday - timedelta(days=3)  # The Friday before this week

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

            # Previous Friday close (week baseline)
            prev_fri_close = None
            for b in reversed(bars):
                if _date(b) <= prev_friday:
                    prev_fri_close = _val(b, "close")
                    break

            # This week's bars
            week_bars = [b for b in bars if monday <= _date(b) <= friday]
            if not week_bars:
                result[ticker] = {}
                continue

            last_bar      = week_bars[-1]
            fri_close     = _val(last_bar, "close")
            last_bar_date = _date(last_bar)
            mon_close     = _val(week_bars[0], "close")
            weekly_high   = max(_val(b, "high") for b in week_bars)
            weekly_low    = min(_val(b, "low")  for b in week_bars)
            weekly_pct    = (
                (fri_close - prev_fri_close) / prev_fri_close * 100
                if fri_close and prev_fri_close else None
            )

            result[ticker] = {
                "mon_close":      mon_close,
                "fri_close":      fri_close,
                "last_bar_date":  last_bar_date,
                "prev_fri_close": prev_fri_close,
                "weekly_pct":     weekly_pct,
                "weekly_high":    weekly_high,
                "weekly_low":     weekly_low,
                "num_days":       len(week_bars),
            }

        return result, None

    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------------------------
# Yahoo Finance: weekly OHLCV
# ---------------------------------------------------------------------------

def fetch_yf_weekly(ticker: str, monday: date, friday: date):
    """
    Returns (fri_close, weekly_high, weekly_low, weekly_pct) for the week.
    weekly_pct = (this_friday - prev_friday) / prev_friday
    Retries up to 3 times with exponential backoff on rate-limit (429) or errors.
    """
    import requests, time
    prev_friday = monday - timedelta(days=3)
    p1 = int(datetime.combine(prev_friday - timedelta(days=5), datetime.min.time()).timestamp())
    p2 = int(datetime.combine(friday + timedelta(days=2),      datetime.min.time()).timestamp())
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={p1}&period2={p2}&interval=1d"
    )

    for attempt in range(3):
        try:
            resp = requests.get(url, headers=_YF_HEADERS, timeout=10)
            if resp.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            res    = resp.json()["chart"]["result"][0]
            tss    = res["timestamp"]
            quotes = res["indicators"]["quote"][0]
            closes = quotes.get("close", [])
            highs  = quotes.get("high",  [])
            lows   = quotes.get("low",   [])

            pairs = [
                (
                    datetime.utcfromtimestamp(tss[i]).date(),
                    closes[i] if i < len(closes) else None,
                    highs[i]  if i < len(highs)  else None,
                    lows[i]   if i < len(lows)   else None,
                )
                for i in range(len(tss))
            ]

            # Prev Friday close
            prev_fri_close = None
            for d, c, _, _ in reversed(pairs):
                if d <= prev_friday and c is not None:
                    prev_fri_close = c
                    break

            # This week bars
            week_p = [(d, c, h, l) for d, c, h, l in pairs if monday <= d <= friday and c is not None]
            if not week_p:
                return None, None, None, None

            fri_close   = week_p[-1][1]
            weekly_high = max(h for _, _, h, _ in week_p if h is not None) if any(h for _, _, h, _ in week_p) else None
            weekly_low  = min(l for _, _, _, l in week_p if l is not None) if any(l for _, _, _, l in week_p) else None
            weekly_pct  = (
                (fri_close - prev_fri_close) / prev_fri_close * 100
                if fri_close and prev_fri_close else None
            )

            return fri_close, weekly_high, weekly_low, weekly_pct

        except Exception:
            if attempt < 2:
                time.sleep(2 ** attempt)

    return None, None, None, None


# ---------------------------------------------------------------------------
# Print sections
# ---------------------------------------------------------------------------

def _fmt(val, unit="$"):
    if val is None:
        return "[unverified]"
    if unit == "%":
        return f"{val:.3f}%"
    if unit == "pts":
        return f"{val:.2f}"
    return f"${val:,.2f}"


def print_alpaca_section(data: dict):
    # Warn if SPY week is incomplete (IEX data gap or short week)
    spy_days = data.get("SPY", {}).get("num_days")
    if spy_days is not None and spy_days < 5:
        print(f"> ⚠️ **INCOMPLETE WEEK**: Alpaca IEX returned {spy_days}/5 trading days for SPY — weekly % may be misleading (holiday week or IEX data gap)\n")

    print("### Weekly ETF Performance (Alpaca IEX)")
    print("| ETF | Label | Last Close | Data date | Weekly % | Weekly High | Weekly Low | Days |")
    print("|---|---|---|---|---|---|---|---|")
    for ticker, label in ALPACA_TICKERS:
        d          = data.get(ticker, {})
        close_val  = f"${d['fri_close']:.2f}" if d.get("fri_close") else "[unverified]"
        bar_date   = d.get("last_bar_date")
        # Flag if last bar isn't Friday
        if bar_date and bar_date != friday:
            date_str = f"⚠️{bar_date.strftime('%a %d')}"
        elif bar_date:
            date_str = bar_date.strftime("%a %d")
        else:
            date_str = "—"
        pct   = pct_str(d.get("weekly_pct"))
        high  = f"${d['weekly_high']:.2f}" if d.get("weekly_high") else "—"
        low   = f"${d['weekly_low']:.2f}"  if d.get("weekly_low")  else "—"
        n     = d.get("num_days")
        days  = f"⚠️{n}" if (n is not None and n < 5) else str(n) if n is not None else "—"
        print(f"| **{ticker}** | {label} | {close_val} | {date_str} | {pct} | {high} | {low} | {days} |")
    print()


def print_macro_section(macro: dict):
    print("### Macro Weekly (Yahoo Finance direct)")
    print("| Indicator | Fri Close | Weekly % | Weekly High | Weekly Low |")
    print("|---|---|---|---|---|")
    for ticker, label, unit in MACRO_TICKERS:
        d    = macro.get(ticker, {})
        fri  = _fmt(d.get("close"), unit)
        pct  = pct_str(d.get("weekly_pct"))
        high = _fmt(d.get("high"), unit) if d.get("high") else "—"
        low  = _fmt(d.get("low"),  unit) if d.get("low")  else "—"
        print(f"| **{label}** ({ticker}) | {fri} | {pct} | {high} | {low} |")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_env()

    parser = argparse.ArgumentParser(description="Weekly market snapshot")
    parser.add_argument("--week", help="ISO week YYYY-Www (default: last completed week)")
    args = parser.parse_args()

    monday, friday, iso_label = resolve_week(args.week)
    mon_str = monday.strftime("%d %b")
    fri_str = friday.strftime("%d %b %Y")

    fetched_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print(f"## Weekly Market Snapshot — {iso_label} ({mon_str}–{fri_str})")
    print(f"*Alpaca IEX weekly bars + Yahoo Finance direct HTTP | สร้างโดย weekly-snapshot.py | fetched: {fetched_at}*\n")
    print("---\n")

    # Alpaca weekly bars
    alpaca_data, err = fetch_weekly_alpaca(monday, friday)
    if err:
        print(f"*[Alpaca unavailable: {err}]*\n")
        alpaca_data = {}
    else:
        print_alpaca_section(alpaca_data)

    # Macro weekly via Yahoo Finance
    macro = {}
    for ticker, label, unit in MACRO_TICKERS:
        fri_close, weekly_high, weekly_low, weekly_pct = fetch_yf_weekly(ticker, monday, friday)
        macro[ticker] = {
            "close":      fri_close,
            "high":       weekly_high,
            "low":        weekly_low,
            "weekly_pct": weekly_pct,
        }
    print_macro_section(macro)

    # Cross-validate SPY: Alpaca vs Yahoo Finance — flag if diff > 1pp
    spy_yf_close, _, _, spy_yf_pct = fetch_yf_weekly("SPY", monday, friday)
    spy_alpaca_pct = (alpaca_data or {}).get("SPY", {}).get("weekly_pct")
    if spy_alpaca_pct is not None and spy_yf_pct is not None:
        if abs(spy_alpaca_pct - spy_yf_pct) > 1.0:
            print(f"> ⚠️ **SPY SOURCE CONFLICT**: Alpaca IEX {pct_str(spy_alpaca_pct)} vs Yahoo Finance {pct_str(spy_yf_pct)} — diff {abs(spy_alpaca_pct - spy_yf_pct):.2f}pp — verify before using\n")

    # Regime verdict
    spy = (alpaca_data or {}).get("SPY", {})
    spy_pct = spy.get("weekly_pct")
    vix_d   = macro.get("^VIX", {})
    vxx     = (alpaca_data or {}).get("VXX", {})

    # Sector ranking
    sectors = [
        (t, alpaca_data.get(t, {}).get("weekly_pct"))
        for t in ("XLE", "XLK", "XLP", "XLU", "XLY")
    ]
    sectors_valid = [(t, p) for t, p in sectors if p is not None]
    best = max(sectors_valid, key=lambda x: x[1])  if sectors_valid else (None, None)
    worst = min(sectors_valid, key=lambda x: x[1]) if sectors_valid else (None, None)

    regime = regime_label(spy_pct)

    print("---\n")
    print("### Weekly Regime Verdict")
    print(f"- **SPY:** {pct_str(spy_pct)} → **{regime}**")

    if vix_d.get("close"):
        zone = (
            "calm" if vix_d["close"] < 15 else
            "caution" if vix_d["close"] < 20 else
            "ELEVATED" if vix_d["close"] < 25 else
            "PANIC"
        )
        high_str = f"{vix_d['high']:.2f}" if vix_d.get("high") else "[unverified]"
        print(f"- **VIX:** close {vix_d['close']:.2f} / weekly high {high_str} [{zone}]")

    if vxx.get("weekly_pct") is not None:
        print(f"- **VXX:** {pct_str(vxx['weekly_pct'])}")

    if best[0]:
        print(f"- **Best sector:** {best[0]} ({pct_str(best[1])})")
    if worst[0]:
        print(f"- **Worst sector:** {worst[0]} ({pct_str(worst[1])})")

    tnx = macro.get("^TNX", {})
    if tnx.get("close"):
        print(f"- **10Y yield end-of-week:** {tnx['close']:.3f}% ({pct_str(tnx.get('weekly_pct'))})")

    print()
    print(f"*Source: Alpaca IEX bars + Yahoo Finance v8 | {iso_label} ({monday} → {friday})*")


if __name__ == "__main__":
    main()
