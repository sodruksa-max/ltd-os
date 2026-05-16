#!/usr/bin/env python3
"""
Nick Outcome Scorer — scores previous weekly recs against actual 1-week price moves.
Runs automatically at the start of /nick-weekly to close the feedback loop.
Appends scored outcomes to vault/Knowledge/nick-soul.md.

Usage:
    python scripts/nick-score.py              # score all unscored recs >= 7 days old
    python scripts/nick-score.py --dry-run    # print only, no write to soul.md
"""

import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
WEEKLY_DIR = ROOT / "vault/20_investment/nick/weekly"
SOUL_FILE = ROOT / "vault/Knowledge/nick-soul.md"

sys.stdout.reconfigure(encoding="utf-8")


def load_env():
    env_file = ROOT / ".secrets/.env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def parse_orders(text: str) -> list[dict]:
    m = re.search(r"```json\s*(\[.*?\])\s*```", text, re.DOTALL)
    if not m:
        return []
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return []


def fetch_price_change(ticker: str, from_date: date, to_date: date) -> float | None:
    """Return % change from from_date close to to_date close using yfinance."""
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        hist = t.history(
            start=(from_date - timedelta(days=4)).isoformat(),
            end=(to_date + timedelta(days=4)).isoformat(),
            auto_adjust=True,
        )
        if hist.empty:
            return None
        hist.index = hist.index.date
        after_start = hist[hist.index >= from_date]
        before_end = hist[hist.index <= to_date]
        if after_start.empty or before_end.empty:
            return None
        start_price = float(after_start["Close"].iloc[0])
        end_price = float(before_end["Close"].iloc[-1])
        if start_price == 0:
            return None
        return round((end_price - start_price) / start_price * 100, 2)
    except Exception:
        return None


def score_call(action: str, pct: float | None) -> str:
    if pct is None:
        return "❓"
    if action in ("BUY", "ADD"):
        return "✅" if pct > 0 else "❌"
    if action in ("SELL", "TRIM"):
        return "✅" if pct < 0 else "❌"
    return "—"


def already_scored(soul_text: str, rec_date: date) -> bool:
    return f"[{rec_date}] Outcome Score" in soul_text


def main():
    dry_run = "--dry-run" in sys.argv
    load_env()

    today = date.today()

    if not SOUL_FILE.exists():
        print(f"ERROR: {SOUL_FILE} not found")
        sys.exit(1)

    soul_text = SOUL_FILE.read_text(encoding="utf-8")
    weekly_files = sorted(WEEKLY_DIR.glob("*_weekly-rec.md"))

    new_entries = []

    for f in weekly_files:
        try:
            rec_date = date.fromisoformat(f.name[:10])
        except ValueError:
            continue

        if (today - rec_date).days < 7:
            continue  # too recent — wait until 1 week of price data available

        if already_scored(soul_text, rec_date):
            continue

        score_date = rec_date + timedelta(days=7)
        text = f.read_text(encoding="utf-8")
        orders = parse_orders(text)

        directional = [o for o in orders if o.get("action") in ("BUY", "ADD", "SELL", "TRIM")]

        lines = [f"\n### [{rec_date}] Outcome Score (run {today})"]

        if not directional:
            lines.append(f"- Hold week — no directional calls to score (window: {rec_date} → {score_date})")
        else:
            correct = 0
            total = 0
            for o in directional:
                ticker = o.get("ticker", "?")
                action = o.get("action", "?")
                conviction = o.get("conviction", "?")
                pct = fetch_price_change(ticker, rec_date, score_date)
                result = score_call(action, pct)
                pct_str = f"{pct:+.2f}%" if pct is not None else "n/a"
                lines.append(f"- {ticker} {action} ({conviction}) → {pct_str} 1w {result}")
                if result in ("✅", "❌"):
                    total += 1
                    if result == "✅":
                        correct += 1

            lines.append(f"- Window: {rec_date} → {score_date}")
            if total > 0:
                accuracy = round(correct / total * 100)
                grade = "strong" if accuracy >= 70 else "weak" if accuracy < 50 else "ok"
                lines.append(f"- Score: {correct}/{total} correct ({accuracy}%) [{grade}]")

        entry = "\n".join(lines)
        print(entry)
        new_entries.append(entry)

    if not new_entries:
        print("nick-score: nothing to score (all recs < 7d old or already scored)")
        return

    if not dry_run:
        soul_text += "\n" + "\n".join(new_entries) + "\n"
        SOUL_FILE.write_text(soul_text, encoding="utf-8")
        print(f"\n→ Appended {len(new_entries)} outcome entry/entries to nick-soul.md")


if __name__ == "__main__":
    main()
