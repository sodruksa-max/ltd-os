#!/usr/bin/env python3
"""
Catalyst Calendar — upcoming earnings + space events ใน 21 วันข้างหน้า

Sources:
  1. Earnings dates — Yahoo Finance quoteSummary API (universe ทั้งหมด)
  2. Space catalysts — scripts/space-catalysts.json (อัปเดตด้วยตัวเอง)

Output: calendar เรียงตามวันที่ พร้อม urgency flag
  [TODAY]   — วันนี้
  [SOON]    — ≤3 วัน
  [WEEK]    — 4-7 วัน
  [AHEAD]   — 8-21 วัน

Usage:
    code/python/.venv/Scripts/python scripts/catalyst-calendar.py
    code/python/.venv/Scripts/python scripts/catalyst-calendar.py --days 14
"""

import sys
import io
import json
import requests
from datetime import datetime, date, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

UNIVERSE_TICKERS = [
    "NVDA", "AMD", "MU", "AVGO", "PLTR", "SMCI", "MRVL", "ARM", "ASML", "DELL",
    "RKLB", "ASTS", "LUNR", "KTOS",
    "SPY", "QQQ",  # index proxies — earnings ไม่มี แต่ check ไว้
]

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

SPACE_CATALYSTS_FILE = Path(__file__).parent / "space-catalysts.json"


def fetch_earnings_date(ticker: str) -> date | None:
    try:
        url = (
            f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
            f"?modules=calendarEvents"
        )
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        events = data["quoteSummary"]["result"][0]["calendarEvents"]
        earnings = events.get("earnings", {})
        dates_raw = earnings.get("earningsDate", [])
        if not dates_raw:
            return None
        ts = dates_raw[0].get("raw")
        if ts is None:
            return None
        return date.fromtimestamp(ts)
    except Exception:
        return None


def load_space_catalysts() -> list[dict]:
    if not SPACE_CATALYSTS_FILE.exists():
        return []
    try:
        with open(SPACE_CATALYSTS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        events = []
        for ticker, items in data.items():
            if ticker.startswith("_"):
                continue
            for item in items:
                try:
                    d = date.fromisoformat(item["date"])
                    events.append({
                        "date":   d,
                        "ticker": ticker,
                        "event":  item["event"],
                        "type":   item.get("type", "event"),
                        "source": "space-catalysts.json",
                    })
                except Exception:
                    continue
        return events
    except Exception:
        return []


def urgency_label(days_away: int) -> str:
    if days_away == 0:
        return "[TODAY] "
    if days_away <= 3:
        return "[SOON]  "
    if days_away <= 7:
        return "[WEEK]  "
    return "[AHEAD] "


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=21)
    args = parser.parse_args()
    horizon = args.days

    today    = date.today()
    end_date = today + timedelta(days=horizon)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"## Catalyst Calendar — next {horizon} days")
    print(f"*{now} | earnings: Yahoo Finance | space: space-catalysts.json*")
    print()

    events: list[dict] = []

    # 1. Earnings dates
    print(f"Fetching earnings dates for {len(UNIVERSE_TICKERS)} tickers...", end=" ", flush=True)
    for ticker in UNIVERSE_TICKERS:
        d = fetch_earnings_date(ticker)
        if d and today <= d <= end_date:
            events.append({
                "date":   d,
                "ticker": ticker,
                "event":  f"{ticker} Earnings",
                "type":   "earnings",
                "source": "Yahoo Finance",
            })
    print("done")

    # 2. Space catalysts
    space_events = load_space_catalysts()
    for e in space_events:
        if today <= e["date"] <= end_date:
            events.append(e)

    if not events:
        print("ไม่มี catalyst ใน universe ใน", horizon, "วันข้างหน้า")
        print()
        print("-> อัปเดต scripts/space-catalysts.json เพื่อเพิ่ม upcoming events")
        return

    # Sort by date
    events.sort(key=lambda x: x["date"])

    # Print
    current_week = None
    for e in events:
        days_away = (e["date"] - today).days
        week_label = e["date"].strftime("%Y-W%V")

        if week_label != current_week:
            print()
            print(f"--- Week of {e['date'].strftime('%b %d')} ---")
            current_week = week_label

        urgency = urgency_label(days_away)
        day_str = e["date"].strftime("%a %b %d")
        type_tag = f"[{e['type']}]" if e["type"] != "earnings" else "[earnings]"
        print(f"  {urgency} {day_str}  {e['ticker']:<6} {type_tag:<12} {e['event']}")

    print()

    # Summary — nearest catalyst per ticker
    print("Nearest catalyst per space ticker:")
    space_tickers = ["RKLB", "ASTS", "LUNR", "KTOS"]
    for ticker in space_tickers:
        ticker_events = [e for e in events if e["ticker"] == ticker]
        if ticker_events:
            nearest = ticker_events[0]
            days_away = (nearest["date"] - today).days
            print(f"  {ticker}: {nearest['event']} — {nearest['date']} ({days_away}d away)")
        else:
            print(f"  {ticker}: ไม่มี catalyst ใน {horizon} วัน")

    print()
    print("-> อัปเดต space-catalysts.json เมื่อมีข่าว launch / contract / deployment ใหม่")


if __name__ == "__main__":
    main()
