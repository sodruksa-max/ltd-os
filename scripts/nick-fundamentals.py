#!/usr/bin/env python3
"""
Nick Fundamentals — Finnhub: earnings calendar, EPS surprise, analyst consensus.

Writes:
  vault/Knowledge/nick-fundamentals.md   (human-readable)
  vault/Knowledge/nick-fundamentals.json (parsed by nick-kill-monitor.py)

Requires: FINNHUB_API_KEY in .secrets/.env
          pip install finnhub-python
Rate:     Finnhub free = 60 calls/min → 1.1s sleep per API call (~3 calls/ticker)
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT          = Path(__file__).resolve().parent.parent
FUND_MD       = ROOT / "vault/Knowledge/nick-fundamentals.md"
FUND_JSON     = ROOT / "vault/Knowledge/nick-fundamentals.json"
UNIVERSE_PATH = ROOT / "code/python/nick_trader/universe.py"


def _load_env() -> None:
    env_file = ROOT / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def _load_tier1() -> list[str]:
    spec = importlib.util.spec_from_file_location("universe", UNIVERSE_PATH)
    mod  = importlib.util.module_from_spec(spec)
    sys.modules["universe"] = mod
    spec.loader.exec_module(mod)
    return list(mod.TIER1)


def _get_client():
    try:
        import finnhub
    except ImportError:
        print("  [SKIP] finnhub-python not installed — run: pip install finnhub-python")
        return None
    api_key = os.environ.get("FINNHUB_API_KEY", "").strip()
    if not api_key or api_key.startswith("<"):
        print("  [SKIP] FINNHUB_API_KEY not set")
        print("         1. Get free key at finnhub.io (sign up → Dashboard → API key)")
        print("         2. Add to .secrets/.env: FINNHUB_API_KEY=<your_key>")
        return None
    return finnhub.Client(api_key=api_key)


def _call(fn, *args, **kwargs):
    """Single Finnhub API call with rate-limit sleep. Returns None on error."""
    time.sleep(1.1)
    try:
        return fn(*args, **kwargs)
    except Exception:
        return None


def _next_earnings(client, ticker: str) -> dict:
    today  = date.today().isoformat()
    future = (date.today() + timedelta(days=120)).isoformat()
    data   = _call(client.earnings_calendar, symbol=ticker, _from=today, to=future)
    if data is None:
        return {"date": "?", "eps_est": None}
    items = (data or {}).get("earningsCalendar", [])
    if not items:
        return {"date": "?", "eps_est": None}
    it = items[0]
    return {"date": it.get("date", "?"), "eps_est": it.get("epsEstimate")}


def _last_surprise(client, ticker: str) -> dict:
    data = _call(client.company_earnings, ticker, limit=2)
    if not data:
        return {"pct": None, "label": "?", "period": "?"}
    last     = data[0]
    actual   = last.get("actual")
    estimate = last.get("estimate")
    period   = last.get("period", "?")
    if actual is not None and estimate is not None and estimate != 0:
        pct   = (actual - estimate) / abs(estimate) * 100
        return {"pct": round(pct, 1), "label": "BEAT" if pct > 0 else "MISS", "period": period}
    return {"pct": None, "label": "?", "period": period}


def _analyst_consensus(client, ticker: str) -> dict:
    data = _call(client.recommendation_trends, ticker)
    if not data:
        return {"label": "?", "bull": 0, "hold": 0, "bear": 0, "detail": "no data"}
    latest = data[0]
    bull   = latest.get("strongBuy", 0) + latest.get("buy", 0)
    hold   = latest.get("hold", 0)
    bear   = latest.get("sell", 0) + latest.get("strongSell", 0)
    total  = bull + hold + bear
    if total == 0:
        return {"label": "?", "bull": 0, "hold": 0, "bear": 0, "detail": "no data"}
    if bull / total >= 0.60:
        label = "BULL"
    elif bear / total >= 0.40:
        label = "BEAR"
    else:
        label = "MIXED"
    return {"label": label, "bull": bull, "hold": hold, "bear": bear, "detail": f"{bull}B/{hold}H/{bear}S"}


def main() -> None:
    _load_env()
    client = _get_client()
    if client is None:
        sys.exit(0)

    tickers = _load_tier1()
    est_sec = len(tickers) * 3 * 1.1
    print(f"  Fetching Finnhub data for {len(tickers)} Tier1 tickers (~{est_sec:.0f}s)...")

    rows: list[dict] = []
    for i, ticker in enumerate(tickers, 1):
        earnings  = _next_earnings(client, ticker)
        surprise  = _last_surprise(client, ticker)
        consensus = _analyst_consensus(client, ticker)
        row = {
            "ticker":      ticker,
            "next_date":   earnings["date"],
            "eps_est":     earnings["eps_est"],
            "surp_pct":    surprise["pct"],
            "surp_label":  surprise["label"],
            "surp_period": surprise["period"],
            "cons_label":  consensus["label"],
            "cons_bull":   consensus["bull"],
            "cons_hold":   consensus["hold"],
            "cons_bear":   consensus["bear"],
            "cons_detail": consensus["detail"],
        }
        rows.append(row)
        print(f"  [{i:02d}/{len(tickers)}] {ticker}: next={row['next_date']} "
              f"surp={row['surp_label']} cons={row['cons_label']}")

    # JSON side-file (parsed by nick-kill-monitor.py)
    payload = {"updated": datetime.now().isoformat(), "tickers": {r["ticker"]: r for r in rows}}
    FUND_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Markdown table
    now   = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Nick Fundamentals",
        f"*Updated: {now} via Finnhub | Tier1 universe*",
        "",
        "| Ticker | Next Earnings | EPS Est | Last Surprise | Analyst |",
        "|--------|--------------|---------|---------------|---------|",
    ]
    for r in rows:
        eps_s  = f"${r['eps_est']:.2f}" if r["eps_est"] is not None else "?"
        surp_s = (f"{r['surp_pct']:+.1f}% {r['surp_label']} ({r['surp_period']})"
                  if r["surp_pct"] is not None else f"? {r['surp_label']} ({r['surp_period']})")
        lines.append(f"| {r['ticker']} | {r['next_date']} | {eps_s} | {surp_s} | {r['cons_label']} {r['cons_detail']} |")

    bear_list = [r["ticker"] for r in rows if r["cons_label"] == "BEAR"]
    if bear_list:
        lines += ["", "## BEAR Consensus Flags", ""]
        for t in bear_list:
            r = next(x for x in rows if x["ticker"] == t)
            lines.append(f"- **{t}** — {r['cons_detail']} → verify kill conditions")

    FUND_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Wrote nick-fundamentals.md + .json ({len(rows)} tickers)")
    print(f"  BEAR flags: {bear_list if bear_list else 'none'}")


if __name__ == "__main__":
    main()
