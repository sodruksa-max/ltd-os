#!/usr/bin/env python3
"""
Macro snapshot via Alpaca ETF proxies.

Usage:
    code/python/.venv/Scripts/python scripts/macro-snapshot.py

Fetches latest price + % change from prev close for macro ETF proxies:
  SPY  = S&P 500 proxy
  QQQ  = Nasdaq-100 proxy
  IWM  = Russell 2000 proxy
  VXX  = VIX / short-vol proxy  (up = fear rising)
  TLT  = 20Y Treasury proxy     (down = yield rising)
  USO  = WTI oil proxy
  UUP  = US Dollar proxy (DXY)
  GLD  = Gold proxy

Output: markdown table ready to embed in pre-market brief.
Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

PROXIES = [
    ("SPY",  "S&P 500",       "up=risk-on"),
    ("QQQ",  "Nasdaq-100",    "up=tech risk-on"),
    ("IWM",  "Russell 2000",  "up=small-cap risk-on"),
    ("VXX",  "VIX proxy",     "up=fear rising / down=fear falling"),
    ("TLT",  "Bonds 20Y",     "down=yield rising (pressures growth stocks)"),
    ("USO",  "WTI Oil",       "up=oil expensive, raises costs"),
    ("UUP",  "Dollar (DXY)",  "up=USD strong, pressures EM + gold"),
    ("GLD",  "Gold",          "up=flight to safety"),
]

TICKERS = [p[0] for p in PROXIES]


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


def fetch_data() -> dict[str, dict]:
    from alpaca.data import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest, StockLatestTradeRequest
    from alpaca.data.timeframe import TimeFrame

    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: ALPACA_API_KEY / ALPACA_SECRET_KEY not set in .secrets/.env")
        sys.exit(1)

    client = StockHistoricalDataClient(api_key, secret_key)

    # Latest trade (current price)
    trades_resp = client.get_stock_latest_trade(
        StockLatestTradeRequest(symbol_or_symbols=TICKERS)
    )

    # Last 3 daily bars for prev close (extra buffer for holidays)
    start = datetime.combine(date.today() - timedelta(days=10), datetime.min.time())
    bars_resp = client.get_stock_bars(
        StockBarsRequest(symbol_or_symbols=TICKERS, timeframe=TimeFrame.Day, start=start)
    )
    bars_data = bars_resp.data  # {ticker: [bar_dict, ...]}

    result = {}
    for ticker in TICKERS:
        current = None
        prev_close = None
        trade_time = None

        if ticker in trades_resp:
            t = trades_resp[ticker]
            current = t.price
            trade_time = t.timestamp

        bars = bars_data.get(ticker, [])
        if len(bars) >= 2:
            prev_close = bars[-2]["close"] if isinstance(bars[-2], dict) else bars[-2].close
        elif len(bars) == 1:
            prev_close = bars[0]["close"] if isinstance(bars[0], dict) else bars[0].close

        pct = None
        if current and prev_close:
            pct = (current - prev_close) / prev_close * 100

        result[ticker] = {
            "current": current,
            "prev_close": prev_close,
            "pct": pct,
            "time": trade_time,
        }

    return result


def arrow(pct: float | None) -> str:
    if pct is None:
        return ""
    return "+" if pct >= 0 else ""


def fmt_pct(pct: float | None) -> str:
    if pct is None:
        return "—"
    return f"{arrow(pct)}{pct:.2f}%"


def fmt_price(p: float | None) -> str:
    if p is None:
        return "—"
    return f"${p:,.2f}"


def signal(ticker: str, pct: float | None) -> str:
    if pct is None:
        return ""
    if ticker == "VXX":
        return "FEAR+" if pct > 3 else ("fear-" if pct < -3 else "")
    if ticker == "TLT":
        return "yield+" if pct < -0.5 else ("yield-" if pct > 0.5 else "")
    if ticker in ("SPY", "QQQ", "IWM"):
        return "RISK+" if pct > 0.5 else ("risk-" if pct < -0.5 else "")
    return ""


def main():
    load_env()

    try:
        data = fetch_data()
    except Exception as e:
        print(f"[macro-snapshot ERROR] {e}")
        sys.exit(1)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("## Alpaca Macro Snapshot")
    print(f"*{now} ET | ETF proxies for cross-checking macro section | Source: Alpaca*")
    print("*Note: 10Y yield + Brent crude not in Alpaca -- fetch from web as usual*\n")
    print("| ETF | Proxy | Price | Change | Meaning | Signal |")
    print("|---|---|---|---|---|---|")

    for ticker, label, meaning in PROXIES:
        d = data.get(ticker, {})
        price = fmt_price(d.get("current"))
        pct = fmt_pct(d.get("pct"))
        sig = signal(ticker, d.get("pct"))
        print(f"| **{ticker}** | {label} | {price} | {pct} | {meaning} | {sig} |")

    print()

    # Quick market read
    spy_pct = data.get("SPY", {}).get("pct")
    vxx_pct = data.get("VXX", {}).get("pct")
    tlt_pct = data.get("TLT", {}).get("pct")

    reads = []
    if spy_pct is not None:
        if spy_pct > 0.3:
            reads.append("SPY pre-market positive")
        elif spy_pct < -0.3:
            reads.append("SPY pre-market negative")
    if vxx_pct is not None and abs(vxx_pct) > 2:
        reads.append(f"VXX {'+' if vxx_pct > 0 else ''}{vxx_pct:.1f}% — fear {'rising' if vxx_pct > 0 else 'falling'}")
    if tlt_pct is not None and abs(tlt_pct) > 0.4:
        reads.append(f"TLT {'+' if tlt_pct > 0 else ''}{tlt_pct:.1f}% — yield {'falling' if tlt_pct > 0 else 'rising'}")

    if reads:
        print("*Quick read: " + " | ".join(reads) + "*")


if __name__ == "__main__":
    main()
