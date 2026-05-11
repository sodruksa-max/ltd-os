#!/usr/bin/env python3
"""
nick-signal.py — generate valuation tier signals for Nick (blinded portfolio manager).

Outputs RSI tier, MA20 distance tier, RS vs SPY tier for each thesis ticker.
NO prices are written — Nick sees only qualitative labels so he stays blinded.

Output: vault/Knowledge/nick-signals.md
Run before nick_weekly_auto.py.
"""

import sys
import io
import requests
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "vault/Knowledge/nick-signals.md"

NICK_TICKERS = [
    # Semicon WFE / Etch
    "LRCX", "AMAT", "KLAC", "ASML", "UCTT", "AEIS",
    # Memory
    "MU", "WDC",
    # AI Infrastructure
    "NVDA", "AMD", "AVGO", "MRVL", "CRDO", "ARM",
    # AI Server / Networking
    "SMCI",
    # Datacenter Cooling
    "MOD",
    # Platform AI
    "PLTR",
    # Space
    "RKLB", "ASTS", "LUNR",
    # Defense AI
    "BBAI",
    # Quantum
    "IONQ",
]

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

MA_PERIOD  = 20
RSI_PERIOD = 14
RS_PERIOD  = 10


def fetch_closes(ticker: str) -> list[float] | None:
    try:
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            f"?interval=1d&range=3mo"
        )
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        result = resp.json()["chart"]["result"][0]
        closes = result["indicators"]["quote"][0]["close"]
        clean = [c for c in closes if c is not None]
        return clean if len(clean) >= MA_PERIOD + RSI_PERIOD + 2 else None
    except Exception:
        return None


def fetch_closes_with_ts(ticker: str) -> tuple[list[float], list[int]] | tuple[None, None]:
    """Returns (closes, timestamps) for RS calculation."""
    try:
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            f"?interval=1d&range=3mo"
        )
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        result = resp.json()["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes_raw = result["indicators"]["quote"][0]["close"]
        pairs = [(ts, c) for ts, c in zip(timestamps, closes_raw) if c is not None]
        if len(pairs) < MA_PERIOD + RSI_PERIOD + 2:
            return None, None
        ts_list = [p[0] for p in pairs]
        close_list = [p[1] for p in pairs]
        return close_list, ts_list
    except Exception:
        return None, None


def calc_rsi(closes: list[float], period: int = 14) -> float | None:
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, period + 1):
        diff = closes[-(period + 1) + i] - closes[-(period + 1) + i - 1]
        (gains if diff > 0 else losses).append(abs(diff))
    avg_gain = sum(gains) / period if gains else 0.0
    avg_loss = sum(losses) / period if losses else 0.0
    if avg_loss == 0:
        return 100.0
    return round(100 - (100 / (1 + avg_gain / avg_loss)), 1)


def rsi_tier(rsi: float | None) -> str:
    if rsi is None:
        return "?"
    if rsi > 70:
        return "OVERBOUGHT"
    if rsi < 40:
        return "OVERSOLD"
    return "NEUTRAL"


def ma_tier(closes: list[float]) -> str:
    if len(closes) < MA_PERIOD:
        return "?"
    ma20 = sum(closes[-MA_PERIOD:]) / MA_PERIOD
    pct = (closes[-1] - ma20) / ma20 * 100
    if pct < -5:
        return "BELOW"
    if pct < 5:
        return "NEAR"
    if pct < 15:
        return "MID"
    return "EXTENDED"


def calc_rs(ticker_closes: list[float], ticker_ts: list[int],
            spy_map: dict[int, float]) -> float | None:
    pairs = [(c, spy_map[ts]) for c, ts in zip(ticker_closes, ticker_ts) if ts in spy_map]
    if len(pairs) < RS_PERIOD + 1:
        return None
    rs_now  = pairs[-1][0] / pairs[-1][1]
    rs_then = pairs[-(RS_PERIOD + 1)][0] / pairs[-(RS_PERIOD + 1)][1]
    return round((rs_now - rs_then) / rs_then * 100, 1)


def rs_tier(rs: float | None) -> str:
    if rs is None:
        return "?"
    if rs > 3.0:
        return "STRONG"
    if rs > -3.0:
        return "NEUTRAL"
    return "WEAK"


def main():
    print("Fetching SPY data...")
    spy_closes, spy_ts = fetch_closes_with_ts("SPY")
    spy_map: dict[int, float] = {}
    if spy_closes and spy_ts:
        spy_map = {ts: c for ts, c in zip(spy_ts, spy_closes)}

    rows = []
    for ticker in NICK_TICKERS:
        closes, ts_list = fetch_closes_with_ts(ticker)
        if not closes:
            rows.append((ticker, "?", "?", "?"))
            print(f"  {ticker}: no data")
            continue

        rsi = calc_rsi(closes, RSI_PERIOD)
        r_tier = rsi_tier(rsi)
        m_tier = ma_tier(closes)
        rs = calc_rs(closes, ts_list, spy_map)
        rs_t = rs_tier(rs)

        rows.append((ticker, r_tier, m_tier, rs_t))
        print(f"  {ticker}: RSI={r_tier} | MA20={m_tier} | RS={rs_t}")

    today = date.today()
    lines = [
        f"# Nick Market Signals — {today}",
        "",
        "*No prices — tier labels only. Generated by scripts/nick-signal.py.*",
        "",
        "## Valuation Signals",
        "",
        "| Ticker | RSI Tier | vs MA20 | RS vs SPY (10d) |",
        "|--------|----------|---------|-----------------|",
    ]
    for ticker, r, m, rs in rows:
        lines.append(f"| {ticker} | {r} | {m} | {rs} |")

    lines += [
        "",
        "## Tier Definitions",
        "",
        "**RSI Tier:** OVERBOUGHT (>70) — momentum stretched, risk of pullback | NEUTRAL (40-70) — healthy | OVERSOLD (<40) — may be value or falling knife",
        "",
        "**vs MA20:** EXTENDED (>15% above) — chase risk | MID (5-15%) — OK momentum | NEAR (<5% above) — ideal entry zone | BELOW — stock below 20d avg",
        "",
        "**RS vs SPY (10d):** STRONG (outperform >3%) — smart money entering | NEUTRAL (±3%) | WEAK (underperform >3%) — sector rotation out",
        "",
        "## Nick's Sizing Rule",
        "",
        "- **OVERBOUGHT + EXTENDED** → size 0.5x or wait for pullback",
        "- **NEUTRAL + NEAR + STRONG** → full-size entry if thesis intact",
        "- **OVERSOLD** → investigate: thesis break or buying opportunity?",
        "- **WEAK RS** → reduce conviction, consider trim if already held",
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()
