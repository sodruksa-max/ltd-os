#!/usr/bin/env python3
"""
Nick Kill Monitor — 3-function kill condition checker (arXiv:2403.19735)
Runs as pre-step to /nick-weekly. Checks kill conditions against live data.

  1. pull_data()        — fetch prices + VIX via yfinance for holdings in nick_state.json
  2. check_thresholds() — auto-check VIX + price drop; flag manual-verify conditions
  3. write_alerts()     — write alert file to vault/20_investment/nick/alerts/ if breach

Usage:
  python scripts/nick-kill-monitor.py           # full check, write alert if needed
  python scripts/nick-kill-monitor.py --dry-run  # print only, no file write
"""

from __future__ import annotations

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE  = ROOT / "vault/20_investment/nick/nick_state.json"
ALERTS_DIR  = ROOT / "vault/20_investment/nick/alerts"

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False


# ---------------------------------------------------------------------------
# 1. Data Puller
# ---------------------------------------------------------------------------

def pull_data(state: dict) -> dict:
    """Fetch current prices for all holdings + VIX."""
    if not YF_AVAILABLE:
        return {"_error": "yfinance not installed — run: pip install yfinance"}

    result: dict = {}

    # VIX
    try:
        result["VIX"] = round(float(yf.Ticker("^VIX").fast_info.last_price), 2)
    except Exception as e:
        result["VIX"] = f"error:{e}"

    # Holdings
    for ticker in state.get("positions", {}):
        try:
            fi = yf.Ticker(ticker).fast_info
            result[ticker] = {
                "price":      round(float(fi.last_price), 2),
                "prev_close": round(float(fi.previous_close), 2),
            }
        except Exception as e:
            result[ticker] = {"error": str(e)}

    return result


# ---------------------------------------------------------------------------
# 2. Threshold Checker
# ---------------------------------------------------------------------------

def check_thresholds(state: dict, market_data: dict) -> list[dict]:
    """
    Evaluate kill conditions. Returns list of alert dicts.
    AUTO  — checks we can compute from price/VIX data
    MANUAL_VERIFY — conditions requiring earnings or news (flag for human review)
    """
    alerts: list[dict] = []
    positions = state.get("positions", {})

    # --- AUTO: VIX ---
    vix = market_data.get("VIX")
    if isinstance(vix, (int, float)):
        if vix >= 28:
            alerts.append({
                "type": "AUTO_BREACH", "severity": "HIGH",
                "condition": f"VIX {vix} >= 28 (sustained check needed)",
                "action":    "FREEZE new position adds — hold existing; re-check tomorrow",
                "tickers":   ["ALL"],
            })
        elif vix >= 24:
            alerts.append({
                "type": "AUTO_WARN", "severity": "MEDIUM",
                "condition": f"VIX {vix} approaching 28 threshold",
                "action":    "Monitor VIX daily — reduce add plans if still rising",
                "tickers":   ["ALL"],
            })

    # --- Per-position checks ---
    for ticker, pos in positions.items():
        pdata = market_data.get(ticker, {})

        if "error" in pdata:
            alerts.append({
                "type": "DATA_ERROR", "severity": "LOW",
                "condition": f"Cannot fetch {ticker}: {pdata['error']}",
                "action":    "Check manually at broker",
                "tickers":   [ticker],
            })
            continue

        current  = pdata.get("price")
        entry    = pos.get("avg_entry")
        if current and entry:
            change_pct = (current - entry) / entry * 100
            if change_pct <= -20:
                alerts.append({
                    "type": "AUTO_BREACH", "severity": "HIGH",
                    "condition": f"{ticker} down {change_pct:.1f}% from entry ${entry}  (current ${current})",
                    "action":    "Thesis integrity check required immediately — run /nick-weekly",
                    "tickers":   [ticker],
                })
            elif change_pct <= -12:
                alerts.append({
                    "type": "AUTO_WARN", "severity": "MEDIUM",
                    "condition": f"{ticker} down {change_pct:.1f}% from entry — approaching -20% alert",
                    "action":    "Review kill conditions; add to /nick-weekly priority check",
                    "tickers":   [ticker],
                })

        # MANUAL_VERIFY flags from kill_conditions text
        for kc in pos.get("kill_conditions", []):
            kc_l = kc.lower()
            if any(kw in kc_l for kw in ("rpo", "revenue", "eps", "earnings", "contract", "backlog")):
                alerts.append({
                    "type": "MANUAL_VERIFY", "severity": "INFO",
                    "condition": f"[{ticker}] {kc}",
                    "action":    "Verify at next earnings — check IR + transcript",
                    "tickers":   [ticker],
                })
            elif any(kw in kc_l for kw in ("cut", "loss", "ban", "restriction", "terminated", "cancel")):
                alerts.append({
                    "type": "MANUAL_VERIFY", "severity": "INFO",
                    "condition": f"[{ticker}] {kc}",
                    "action":    "Monitor news daily — run news-snapshot.py for signals",
                    "tickers":   [ticker],
                })

    return alerts


# ---------------------------------------------------------------------------
# 3. Alert Writer
# ---------------------------------------------------------------------------

def write_alerts(alerts: list[dict], market_data: dict, dry_run: bool = False) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    n_breach = sum(1 for a in alerts if a["severity"] == "HIGH"   and a["type"] != "MANUAL_VERIFY")
    n_warn   = sum(1 for a in alerts if a["severity"] == "MEDIUM" and a["type"] != "MANUAL_VERIFY")
    n_manual = sum(1 for a in alerts if a["type"] == "MANUAL_VERIFY")

    if n_breach > 0:
        status = "BREACH"
    elif n_warn > 0:
        status = "WARN"
    else:
        status = "ALL CLEAR"

    # Build markdown report
    lines = [
        f"# Nick Kill Monitor — {today}",
        "*Auto-generated by scripts/nick-kill-monitor.py (arXiv:2403.19735)*",
        "",
        f"## Status: {status}",
        f"AUTO BREACH: {n_breach} | AUTO WARN: {n_warn} | MANUAL VERIFY: {n_manual}",
        "",
        "## Market Snapshot",
    ]

    vix = market_data.get("VIX", "N/A")
    lines.append(f"- VIX: {vix}")
    for ticker, d in market_data.items():
        if ticker in ("VIX", "_error"):
            continue
        if isinstance(d, dict) and "price" in d:
            lines.append(f"- {ticker}: ${d['price']}")
    lines.append("")

    for label, sev, ttype in [
        ("HIGH — Breach", "HIGH",   None),
        ("MEDIUM — Warn",  "MEDIUM", None),
        ("INFO — Manual Verify", "INFO", "MANUAL_VERIFY"),
    ]:
        group = [a for a in alerts if a["severity"] == sev]
        if not group:
            continue
        lines.append(f"## {label}")
        for a in group:
            lines.append(f"- [{a['type']}] {a['condition']}")
            lines.append(f"  → {a['action']}")
        lines.append("")

    if status == "ALL CLEAR":
        lines += ["## Result", "All auto-checkable conditions intact. Manual items above need human review.", ""]

    output = "\n".join(lines)

    if dry_run:
        return output

    if status != "ALL CLEAR":
        ALERTS_DIR.mkdir(parents=True, exist_ok=True)
        fpath = ALERTS_DIR / f"{today}-kill-alert.md"
        fpath.write_text(output, encoding="utf-8")
        return f"Status: {status} | BREACH: {n_breach} | WARN: {n_warn}\n→ Alert saved: {fpath.relative_to(ROOT)}"

    return f"Status: ALL CLEAR — no alert file written (BREACH=0, WARN=0)"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    dry_run = "--dry-run" in sys.argv

    if not STATE_FILE.exists():
        print(f"[ERROR] {STATE_FILE} not found — run /nick-init first")
        sys.exit(1)

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    print("[1/3] Pulling market data...")
    market_data = pull_data(state)

    if "_error" in market_data:
        print(f"[ERROR] {market_data['_error']}")
        sys.exit(1)

    print("[2/3] Checking kill condition thresholds...")
    alerts = check_thresholds(state, market_data)

    print("[3/3] Writing alert report...")
    result = write_alerts(alerts, market_data, dry_run=dry_run)
    print(result)


if __name__ == "__main__":
    main()
