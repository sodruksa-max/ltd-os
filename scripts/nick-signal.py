#!/usr/bin/env python3
"""
nick-signal.py — generate valuation tier signals for Nick (blinded portfolio manager).

Reads tickers dynamically from vault/Knowledge/THESIS_TRACKER.md — no hardcoded list.
Outputs RSI tier, MA20 distance tier, RS vs SPY tier for each thesis ticker.
NO prices are written — Nick sees only qualitative labels so he stays blinded.

Output: vault/Knowledge/nick-signals.md
Scheduled: every Friday via Claude Code schedule.
"""

import re
import sys
import io
import time
import requests
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO   = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "vault/Knowledge/nick-signals.md"
THESIS = REPO / "vault/Knowledge/THESIS_TRACKER.md"

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


# ---------------------------------------------------------------------------
# Parse THESIS_TRACKER.md dynamically
# ---------------------------------------------------------------------------

def load_thesis_tickers() -> tuple[list[str], list[str]]:
    """
    Returns (thesis_tickers, clist_tickers) parsed from THESIS_TRACKER.md.
    thesis_tickers = all tickers from Active Theses sections
    clist_tickers  = tickers from C-List watch table
    """
    if not THESIS.exists():
        print(f"[WARN] THESIS_TRACKER.md not found at {THESIS}")
        return [], []

    text = THESIS.read_text(encoding="utf-8")

    # Active Theses: lines like "**Tickers:** NVDA, AMD, AVGO, ..."
    thesis_tickers = []
    for match in re.finditer(r"\*\*Tickers:\*\*\s*([A-Z0-9,\s]+)", text):
        raw = match.group(1)
        for t in re.split(r"[,\s]+", raw):
            t = t.strip()
            if t and t.isalpha() or (t and re.match(r"^[A-Z0-9]+$", t)):
                if t not in thesis_tickers:
                    thesis_tickers.append(t)

    # C-List: table rows like "| TSM | ... |"
    clist_tickers = []
    in_clist = False
    for line in text.splitlines():
        if "## C-List" in line:
            in_clist = True
            continue
        if in_clist and line.startswith("## "):
            break
        if in_clist and line.startswith("| ") and not line.startswith("| Ticker") and "---|" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                ticker = parts[1].strip()
                if re.match(r"^[A-Z]{1,5}$", ticker) and ticker not in clist_tickers:
                    clist_tickers.append(ticker)

    return thesis_tickers, clist_tickers


# ---------------------------------------------------------------------------
# Yahoo Finance fetch with retry
# ---------------------------------------------------------------------------

def _yf_fetch(ticker: str) -> dict | None:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?interval=1d&range=3mo"
    )
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=_HEADERS, timeout=10)
            if resp.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            return resp.json()["chart"]["result"][0]
        except Exception:
            if attempt < 2:
                time.sleep(2 ** attempt)
    return None


def fetch_closes_with_ts(ticker: str) -> tuple[list[float], list[int]] | tuple[None, None]:
    result = _yf_fetch(ticker)
    if not result:
        return None, None
    try:
        timestamps = result["timestamp"]
        closes_raw = result["indicators"]["quote"][0]["close"]
        pairs = [(ts, c) for ts, c in zip(timestamps, closes_raw) if c is not None]
        if len(pairs) < MA_PERIOD + RSI_PERIOD + 2:
            return None, None
        return [p[1] for p in pairs], [p[0] for p in pairs]
    except Exception:
        return None, None


# ---------------------------------------------------------------------------
# Signal calculations
# ---------------------------------------------------------------------------

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
    if rsi is None: return "?"
    if rsi > 70:    return "OVERBOUGHT"
    if rsi < 40:    return "OVERSOLD"
    return "NEUTRAL"


def ma_tier(closes: list[float]) -> str:
    if len(closes) < MA_PERIOD: return "?"
    ma20 = sum(closes[-MA_PERIOD:]) / MA_PERIOD
    pct  = (closes[-1] - ma20) / ma20 * 100
    if pct < -5:  return "BELOW"
    if pct < 5:   return "NEAR"
    if pct < 15:  return "MID"
    return "EXTENDED"


def calc_rs(ticker_closes: list[float], ticker_ts: list[int],
            spy_map: dict[int, float]) -> float | None:
    pairs = [(c, spy_map[ts]) for c, ts in zip(ticker_closes, ticker_ts) if ts in spy_map]
    if len(pairs) < RS_PERIOD + 1:
        return None
    rs_now  = pairs[-1][0]  / pairs[-1][1]
    rs_then = pairs[-(RS_PERIOD + 1)][0] / pairs[-(RS_PERIOD + 1)][1]
    return round((rs_now - rs_then) / rs_then * 100, 1)


def rs_tier(rs: float | None) -> str:
    if rs is None:  return "?"
    if rs > 3.0:    return "STRONG"
    if rs > -3.0:   return "NEUTRAL"
    return "WEAK"


def score_ticker(closes, ts_list, spy_map):
    rsi  = calc_rsi(closes, RSI_PERIOD)
    rs   = calc_rs(closes, ts_list, spy_map)
    return rsi_tier(rsi), ma_tier(closes), rs_tier(rs)


# ---------------------------------------------------------------------------
# Build signal rows
# ---------------------------------------------------------------------------

def build_rows(tickers: list[str], spy_map: dict) -> list[tuple]:
    rows = []
    for ticker in tickers:
        closes, ts_list = fetch_closes_with_ts(ticker)
        if not closes:
            rows.append((ticker, "?", "?", "?"))
            print(f"  {ticker}: no data")
        else:
            r, m, rs = score_ticker(closes, ts_list, spy_map)
            rows.append((ticker, r, m, rs))
            print(f"  {ticker}: RSI={r} | MA20={m} | RS={rs}")
    return rows


def flag(r, m, rs) -> str:
    """Return a one-char flag for the most actionable signal."""
    if r == "NEUTRAL" and m == "NEAR" and rs == "STRONG":
        return " ★"   # ideal entry
    if r == "OVERBOUGHT" and m == "EXTENDED":
        return " ⚠"   # chase risk
    if r == "OVERSOLD":
        return " ?"   # investigate
    return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    thesis_tickers, clist_tickers = load_thesis_tickers()
    if not thesis_tickers:
        print("[ERROR] No tickers found in THESIS_TRACKER.md — aborting")
        sys.exit(1)

    print(f"Thesis tickers ({len(thesis_tickers)}): {', '.join(thesis_tickers)}")
    print(f"C-list tickers ({len(clist_tickers)}): {', '.join(clist_tickers)}")

    print("\nFetching SPY baseline...")
    spy_closes, spy_ts = fetch_closes_with_ts("SPY")
    spy_map: dict[int, float] = {}
    if spy_closes and spy_ts:
        spy_map = {ts: c for ts, c in zip(spy_ts, spy_closes)}
    else:
        print("[WARN] SPY fetch failed — RS column will show '?'")

    print("\n--- Thesis tickers ---")
    thesis_rows = build_rows(thesis_tickers, spy_map)

    clist_rows = []
    if clist_tickers:
        print("\n--- C-List tickers ---")
        clist_rows = build_rows(clist_tickers, spy_map)

    today = date.today()
    lines = [
        f"# Nick Market Signals — {today}",
        "",
        f"*No prices — tier labels only. Auto-generated by nick-signal.py from THESIS_TRACKER.md.*",
        f"*Thesis tickers: {len(thesis_tickers)} | C-list: {len(clist_tickers)} | fetched: {today}*",
        "",
        "## Active Thesis Signals",
        "",
        "| Ticker | RSI Tier | vs MA20 | RS vs SPY (10d) | Signal |",
        "|--------|----------|---------|-----------------|--------|",
    ]
    for ticker, r, m, rs in thesis_rows:
        f = flag(r, m, rs)
        lines.append(f"| {ticker} | {r} | {m} | {rs} |{f} |")

    if clist_rows:
        lines += [
            "",
            "## C-List Watch Signals",
            "",
            "| Ticker | RSI Tier | vs MA20 | RS vs SPY (10d) | Signal |",
            "|--------|----------|---------|-----------------|--------|",
        ]
        for ticker, r, m, rs in clist_rows:
            f = flag(r, m, rs)
            lines.append(f"| {ticker} | {r} | {m} | {rs} |{f} |")

    lines += [
        "",
        "## Tier Definitions",
        "",
        "**RSI Tier:** OVERBOUGHT (>70) — momentum stretched | NEUTRAL (40-70) — healthy | OVERSOLD (<40) — investigate",
        "",
        "**vs MA20:** EXTENDED (>15% above) — chase risk | MID (5-15%) — OK | NEAR (<5%) — ideal entry | BELOW — below avg",
        "",
        "**RS vs SPY (10d):** STRONG (>+3%) — outperforming | NEUTRAL (±3%) | WEAK (<-3%) — rotation out",
        "",
        "## Nick's Sizing Rule",
        "",
        "- **★ NEUTRAL + NEAR + STRONG** → full-size entry if thesis intact",
        "- **⚠ OVERBOUGHT + EXTENDED** → size 0.5x or wait for pullback",
        "- **? OVERSOLD** → investigate: thesis break or buying opportunity?",
        "- **WEAK RS** → reduce conviction, consider trim if already held",
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nSaved: {OUTPUT}")
    print(f"★ ideal entries: {sum(1 for _, r, m, rs in thesis_rows if r=='NEUTRAL' and m=='NEAR' and rs=='STRONG')}")
    print(f"⚠ chase risk:   {sum(1 for _, r, m, rs in thesis_rows if r=='OVERBOUGHT' and m=='EXTENDED')}")


if __name__ == "__main__":
    main()
