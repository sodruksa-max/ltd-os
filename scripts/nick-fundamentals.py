#!/usr/bin/env python3
"""
Nick Fundamentals — Finnhub: earnings calendar, EPS surprise, analyst consensus.

Incremental refresh: skips tickers with data < 23h old.
Earnings override:   always re-fetches if next_earnings is within 7 days.

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

STALE_HOURS       = 23   # refresh if data older than this
EARNINGS_DAYS     = 7    # always refresh if earnings within this many days


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


def _load_stored() -> dict:
    """Load existing per-ticker data from JSON. Returns {} on missing/corrupt."""
    if not FUND_JSON.exists():
        return {}
    try:
        return json.loads(FUND_JSON.read_text(encoding="utf-8")).get("tickers", {})
    except Exception:
        return {}


def _should_refresh(ticker: str, stored: dict, now: datetime) -> tuple[bool, str]:
    """Return (should_fetch, reason_str)."""
    td = stored.get(ticker)
    if td is None:
        return True, "no prior data"

    last_str = td.get("last_fetched")
    if not last_str:
        return True, "no timestamp"

    age_h = (now - datetime.fromisoformat(last_str)).total_seconds() / 3600

    # Earnings-proximity override — always fresh within EARNINGS_DAYS
    next_date_str = td.get("next_date", "?")
    if next_date_str != "?":
        try:
            days_to = (date.fromisoformat(next_date_str) - now.date()).days
            if 0 <= days_to <= EARNINGS_DAYS:
                return True, f"earnings in {days_to}d (override)"
        except ValueError:
            pass

    if age_h >= STALE_HOURS:
        return True, f"stale ({age_h:.0f}h)"

    return False, f"fresh ({age_h:.0f}h old)"


def _get_client():
    try:
        import finnhub
    except ImportError:
        print("  [SKIP] finnhub-python not installed — run: pip install finnhub-python")
        return None
    api_key = os.environ.get("FINNHUB_API_KEY", "").strip()
    if not api_key or api_key.startswith("<"):
        print("  [SKIP] FINNHUB_API_KEY not set")
        print("         1. Get free key at finnhub.io → Dashboard → API key")
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


def _fetch_ticker(client, ticker: str, now: datetime) -> dict:
    """Fetch all 3 Finnhub dimensions for one ticker."""
    # 1. Next earnings
    today  = now.date().isoformat()
    future = (now.date() + timedelta(days=120)).isoformat()
    data   = _call(client.earnings_calendar, symbol=ticker, _from=today, to=future)
    items  = (data or {}).get("earningsCalendar", [])
    if items:
        it       = items[0]
        next_date = it.get("date", "?")
        eps_est   = it.get("epsEstimate")
    else:
        next_date, eps_est = "?", None

    # 2. Last EPS surprise
    surp = _call(client.company_earnings, ticker, limit=2)
    if surp:
        last     = surp[0]
        actual   = last.get("actual")
        estimate = last.get("estimate")
        period   = last.get("period", "?")
        if actual is not None and estimate is not None and estimate != 0:
            pct        = round((actual - estimate) / abs(estimate) * 100, 1)
            surp_label = "BEAT" if pct > 0 else "MISS"
        else:
            pct, surp_label, period = None, "?", period
    else:
        pct, surp_label, period = None, "?", "?"

    # 3. Analyst consensus
    recs  = _call(client.recommendation_trends, ticker)
    if recs:
        latest = recs[0]
        bull   = latest.get("strongBuy", 0) + latest.get("buy", 0)
        hold   = latest.get("hold", 0)
        bear   = latest.get("sell", 0) + latest.get("strongSell", 0)
        total  = bull + hold + bear
        if total > 0:
            if bull / total >= 0.60:
                cons_label = "BULL"
            elif bear / total >= 0.40:
                cons_label = "BEAR"
            else:
                cons_label = "MIXED"
            cons_detail = f"{bull}B/{hold}H/{bear}S"
        else:
            bull = hold = bear = 0
            cons_label, cons_detail = "?", "no data"
    else:
        bull = hold = bear = 0
        cons_label, cons_detail = "?", "no data"

    return {
        "ticker":      ticker,
        "next_date":   next_date,
        "eps_est":     eps_est,
        "surp_pct":    pct,
        "surp_label":  surp_label,
        "surp_period": period,
        "cons_label":  cons_label,
        "cons_bull":   bull,
        "cons_hold":   hold,
        "cons_bear":   bear,
        "cons_detail": cons_detail,
        "last_fetched": now.isoformat(),
    }


def _build_markdown(rows: list[dict], now: datetime) -> str:
    ts    = now.strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Nick Fundamentals",
        f"*Updated: {ts} via Finnhub | Tier1 universe*",
        "",
        "| Ticker | Next Earnings | EPS Est | Last Surprise | Analyst |",
        "|--------|--------------|---------|---------------|---------|",
    ]
    for r in rows:
        eps_s  = f"${r['eps_est']:.2f}" if r["eps_est"] is not None else "?"
        surp_s = (f"{r['surp_pct']:+.1f}% {r['surp_label']} ({r['surp_period']})"
                  if r["surp_pct"] is not None else f"? {r['surp_label']} ({r['surp_period']})")
        lines.append(
            f"| {r['ticker']} | {r['next_date']} | {eps_s} "
            f"| {surp_s} | {r['cons_label']} {r['cons_detail']} |"
        )

    bear_list = [r for r in rows if r["cons_label"] == "BEAR"]
    if bear_list:
        lines += ["", "## BEAR Consensus Flags", ""]
        for r in bear_list:
            lines.append(f"- **{r['ticker']}** — {r['cons_detail']} → verify kill conditions")

    return "\n".join(lines) + "\n"


def main() -> None:
    _load_env()
    client = _get_client()
    if client is None:
        sys.exit(0)

    now     = datetime.now()
    tickers = _load_tier1()
    stored  = _load_stored()

    # Decide per-ticker: fetch or skip
    to_fetch: list[tuple[str, str]] = []
    to_skip:  list[str]             = []
    for t in tickers:
        should, reason = _should_refresh(t, stored, now)
        if should:
            to_fetch.append((t, reason))
        else:
            to_skip.append(t)

    est_sec = len(to_fetch) * 3 * 1.1
    print(f"  {len(to_fetch)} fetch / {len(to_skip)} skip  (~{est_sec:.0f}s)")
    if to_skip:
        print(f"  Skipping (fresh): {', '.join(to_skip)}")

    # Fetch stale/new tickers
    updated: dict[str, dict] = dict(stored)  # start with all stored data
    for i, (ticker, reason) in enumerate(to_fetch, 1):
        row = _fetch_ticker(client, ticker, now)
        updated[ticker] = row
        print(f"  [{i:02d}/{len(to_fetch)}] {ticker} ({reason}): "
              f"next={row['next_date']} surp={row['surp_label']} cons={row['cons_label']}")

    # Preserve original TIER1 order for output
    rows = [updated[t] for t in tickers if t in updated]

    # Write JSON
    FUND_JSON.write_text(
        json.dumps({"updated": now.isoformat(), "tickers": updated}, indent=2),
        encoding="utf-8",
    )

    # Write markdown
    FUND_MD.write_text(_build_markdown(rows, now), encoding="utf-8")

    fetched_bear = [r["ticker"] for r in rows if r["cons_label"] == "BEAR" and r["ticker"] in {t for t, _ in to_fetch}]
    print(f"  Wrote nick-fundamentals.md + .json ({len(rows)} tickers, {len(to_fetch)} refreshed)")
    print(f"  BEAR flags: {[r['ticker'] for r in rows if r['cons_label'] == 'BEAR'] or 'none'}")


if __name__ == "__main__":
    main()
