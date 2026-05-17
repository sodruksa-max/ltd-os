#!/usr/bin/env python3
"""
Bubble Risk Monitor — weekly composite Bubble Pressure Score

Monitors 5 risk vectors from vault/10_research/bubble-risk-framework.md:
  1. Long-end Yield     — 10Y level + 10Y-2Y spread
  2. Yen Carry          — USD/JPY level + 5-day change
  3. VIX Term Structure — VIX9D/VIX ratio (backwardation = fear)
  4. Index Concentration — RSP vs SPY YTD gap (equal-weight vs cap-weight)
  5. CAPE               — manual entry (no free API); prompt if stale

All data from Yahoo Finance. CAPE updated manually when prompted.
Outputs composite score 0-10 + per-vector breakdown.

Usage:
    code/python/.venv/Scripts/python scripts/bubble-risk-monitor.py
    code/python/.venv/Scripts/python scripts/bubble-risk-monitor.py --cape 36.5
"""

import sys
import io
import json
import argparse
import requests
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CAPE_CACHE_FILE = Path(__file__).parent.parent / ".secrets" / "cape_cache.json"

sys.path.insert(0, str(Path(__file__).parent))
from _llm import call_llm as call_gemini  # noqa: E402  — cascade: Gemini→Haiku fallback


def llm_bubble_narrative(score: float, details: list[tuple]) -> str | None:
    """2-sentence Thai narrative via Gemini Flash (free). Returns None if no key."""
    vector_lines = "\n".join(
        f"  [{s}/2] {name}: {detail}" for name, _, s, detail in details
    )
    system = (
        "You are a macro risk analyst. Write EXACTLY 2 sentences in Thai explaining: "
        "(1) which bubble risk vectors are most elevated this week, "
        "(2) what it means for equity position sizing. Be specific, cite numbers."
    )
    user = f"Bubble Pressure Score: {score}/10\n\nVector breakdown:\n{vector_lines}"
    return call_gemini(system, user, max_tokens=150)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


# ---------------------------------------------------------------------------
# Data fetch
# ---------------------------------------------------------------------------

def fetch_closes(ticker: str, range_: str = "1mo") -> list[float]:
    try:
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            f"?interval=1d&range={range_}"
        )
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        closes = resp.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        return [c for c in closes if c is not None]
    except Exception:
        return []


def fetch_current(ticker: str) -> float | None:
    closes = fetch_closes(ticker, "5d")
    return closes[-1] if closes else None


def fetch_ytd_return(ticker: str) -> float | None:
    """Approximate YTD return using 6-month range as proxy."""
    closes = fetch_closes(ticker, "6mo")
    if len(closes) < 2:
        return None
    # Use first close of year approximation: oldest available
    return round((closes[-1] - closes[0]) / closes[0] * 100, 1)


# ---------------------------------------------------------------------------
# CAPE cache
# ---------------------------------------------------------------------------

def load_cape_cache() -> dict:
    if CAPE_CACHE_FILE.exists():
        try:
            return json.loads(CAPE_CACHE_FILE.read_text())
        except Exception:
            pass
    return {}


def save_cape_cache(value: float):
    CAPE_CACHE_FILE.parent.mkdir(exist_ok=True)
    CAPE_CACHE_FILE.write_text(json.dumps({
        "cape": value,
        "updated": datetime.now().strftime("%Y-%m-%d"),
    }))


def get_cape(cli_value: float | None) -> tuple[float | None, str]:
    """Returns (cape_value, source_note)."""
    if cli_value is not None:
        save_cape_cache(cli_value)
        return cli_value, "manual (CLI)"
    cache = load_cape_cache()
    if cache:
        return cache["cape"], f"cached {cache.get('updated', '?')} — run with --cape <value> to update"
    return None, "not set — run with --cape <value> (source: multpl.com/shiller-pe)"


# ---------------------------------------------------------------------------
# Scoring — each vector returns (score: int 0-2, detail: str)
# ---------------------------------------------------------------------------

def score_yield(tnx: float | None, irx: float | None) -> tuple[int, str]:
    if tnx is None:
        return 0, "10Y: n/a"
    parts = [f"10Y={tnx:.3f}%"]
    score = 0
    if tnx > 5.0:
        score += 2
        parts.append("[!!] >5.0% — high compression risk")
    elif tnx > 4.75:
        score += 1
        parts.append("[!] >4.75% — compression zone")

    if tnx is not None and irx is not None:
        irx_pct = irx / 100 if irx > 10 else irx
        spread = round(tnx - irx_pct, 2)
        parts.append(f"spread={spread:+.2f}%")
        if spread > 1.0:
            score = min(score + 1, 2)
            parts.append("[!] >100bps term premium")
        elif spread > 0.5:
            parts.append("term premium elevated")

    return min(score, 2), " | ".join(parts)


def score_yen(jpy_closes: list[float]) -> tuple[int, str]:
    if not jpy_closes:
        return 0, "USD/JPY: n/a"
    current = jpy_closes[-1]
    parts = [f"USD/JPY={current:.2f}"]
    score = 0

    if current < 145:
        score = 2
        parts.append("[!!] <145 — carry unwind active")
    elif current < 150:
        score = 1
        parts.append("[!] <150 — watch zone")

    if len(jpy_closes) >= 6:
        change_5d = round((current - jpy_closes[-6]) / jpy_closes[-6] * 100, 1)
        parts.append(f"5d={change_5d:+.1f}%")
        if change_5d < -3.0:
            score = min(score + 1, 2)
            parts.append("[!] rapid JPY appreciation")

    return min(score, 2), " | ".join(parts)


def score_vix_term(vix: float | None, vix9d: float | None) -> tuple[int, str]:
    if vix is None:
        return 0, "VIX: n/a"
    parts = [f"VIX={vix:.1f}"]
    score = 0

    if vix > 30:
        score = 2
        parts.append("[!!] panic zone")
    elif vix > 20:
        score = 1
        parts.append("[!] elevated fear")

    if vix9d is not None:
        ratio = round(vix9d / vix, 3)
        parts.append(f"VIX9D/VIX={ratio:.2f}")
        if ratio < 0.85:
            score = min(score + 1, 2)
            parts.append("[!] backwardation — short-term fear spike")
        elif ratio > 1.10:
            parts.append("contango (calm)")

    return min(score, 2), " | ".join(parts)


def score_concentration(rsp_ytd: float | None, spy_ytd: float | None) -> tuple[int, str]:
    if rsp_ytd is None or spy_ytd is None:
        return 0, "RSP/SPY breadth: n/a"
    gap = round(spy_ytd - rsp_ytd, 1)
    parts = [f"SPY YTD={spy_ytd:+.1f}%", f"RSP YTD={rsp_ytd:+.1f}%", f"gap={gap:+.1f}%"]
    score = 0
    if gap > 10:
        score = 2
        parts.append("[!!] extreme concentration")
    elif gap > 5:
        score = 1
        parts.append("[!] concentration elevated")
    return score, " | ".join(parts)


def score_cape(cape: float | None) -> tuple[int, str]:
    if cape is None:
        return 0, "CAPE: not set — run with --cape <value>"
    parts = [f"CAPE={cape:.1f}"]
    score = 0
    if cape > 38:
        score = 2
        parts.append("[!!] dot-com bubble levels")
    elif cape > 30:
        score = 1
        parts.append("[!] historically elevated")
    else:
        parts.append("within historical range")
    return score, " | ".join(parts)


# ---------------------------------------------------------------------------
# Composite score
# ---------------------------------------------------------------------------

WEIGHTS = {
    "yield":         0.25,
    "yen":           0.15,
    "vix":           0.20,
    "concentration": 0.20,
    "cape":          0.20,
}

def composite_score(scores: dict[str, int]) -> float:
    """Weighted composite 0-10."""
    total = sum(scores[k] * WEIGHTS[k] for k in scores)
    return round(total / 2 * 10, 1)  # normalize: max raw = 2.0 → 10


def risk_level(score: float) -> str:
    if score >= 7:
        return "[!!] HIGH — defensive posture, cash >30%, tighten stops"
    if score >= 4:
        return "[!]  ELEVATED — reduce size 20-30%, tighten stops"
    return "[OK] LOW — full position size OK"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cape", type=float, default=None, help="Shiller CAPE ratio (from multpl.com)")
    args = parser.parse_args()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"## Bubble Risk Monitor")
    print(f"*{now} | Run weekly or before large position*\n")

    # Fetch all data
    tnx    = fetch_current("^TNX")
    irx    = fetch_current("^IRX")
    jpy_cl = fetch_closes("JPY=X", "1mo")
    vix    = fetch_current("^VIX")
    vix9d  = fetch_current("^VIX9D")
    rsp_ytd = fetch_ytd_return("RSP")
    spy_ytd = fetch_ytd_return("SPY")
    cape, cape_note = get_cape(args.cape)

    # Score each vector
    s_yield, d_yield = score_yield(tnx, irx)
    s_yen,   d_yen   = score_yen(jpy_cl)
    s_vix,   d_vix   = score_vix_term(vix, vix9d)
    s_conc,  d_conc  = score_concentration(rsp_ytd, spy_ytd)
    s_cape,  d_cape  = score_cape(cape)

    scores = {
        "yield": s_yield, "yen": s_yen, "vix": s_vix,
        "concentration": s_conc, "cape": s_cape,
    }
    comp = composite_score(scores)
    level = risk_level(comp)

    # Print breakdown
    print("### Vector Breakdown")
    rows = [
        ("Long-end Yield",      "25%", s_yield, d_yield),
        ("Yen Carry",           "15%", s_yen,   d_yen),
        ("VIX Term Structure",  "20%", s_vix,   d_vix),
        ("Index Concentration", "20%", s_conc,  d_conc),
        ("CAPE",                "20%", s_cape,  d_cape),
    ]
    bar_chars = {0: "[ ]", 1: "[=]", 2: "[X]"}
    for name, wt, score, detail in rows:
        bar = bar_chars.get(score, "?")
        print(f"  {bar} {name} ({wt}): {detail}")

    print()
    print(f"### Composite Bubble Pressure Score: {comp}/10")
    print(f"### Risk Level: {level}")
    print()

    # LLM narrative (2 sentences Thai) — skipped if no API key
    detail_rows = [
        ("Long-end Yield",      "25%", s_yield, d_yield),
        ("Yen Carry",           "15%", s_yen,   d_yen),
        ("VIX Term Structure",  "20%", s_vix,   d_vix),
        ("Index Concentration", "20%", s_conc,  d_conc),
        ("CAPE",                "20%", s_cape,  d_cape),
    ]
    narrative = llm_bubble_narrative(comp, detail_rows)
    if narrative:
        print("### Macro Narrative")
        print(narrative)
        print()

    print("Full framework: vault/10_research/bubble-risk-framework.md")
    if "cached" in cape_note or "not set" in cape_note:
        print(f"CAPE note: {cape_note}")


if __name__ == "__main__":
    main()
