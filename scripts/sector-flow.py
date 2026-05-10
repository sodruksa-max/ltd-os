#!/usr/bin/env python3
"""
Sector Money Flow — ดูว่า sector ไหนกำลังดูด money เข้าหรือออก

วัด Relative Strength (RS) ของแต่ละ sector ETF เทียบกับ SPY
ใน 2 timeframe: 5 วัน (short-term flow) และ 20 วัน (trend)

Labels:
  Leading    — RS↑ ทั้ง 5d และ 20d  (money ไหลเข้าต่อเนื่อง)
  Improving  — RS↑ 5d แต่ 20d ยังไม่ยืนยัน (เริ่มหัวเลี้ยว)
  Fading     — RS↓ 5d แต่ 20d ยังบวก (momentum กำลังหมด)
  Lagging    — RS↓ ทั้ง 5d และ 20d  (money ออก)

Usage:
    code/python/.venv/Scripts/python scripts/sector-flow.py
"""

import sys
import io
import requests
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SECTORS = [
    ("XLK",  "Technology"),
    ("XLI",  "Industrials"),
    ("XLE",  "Energy"),
    ("XLV",  "Healthcare"),
    ("XLF",  "Financials"),
    ("XLY",  "Cons Discretionary"),
    ("XLP",  "Cons Staples"),
    ("XLU",  "Utilities"),
    ("XLC",  "Communication"),
    ("XLB",  "Materials"),
    ("ROKT", "Space (ROKT ETF)"),   # SPDR S&P Kensho Final Frontiers
    ("ITA",  "Aerospace & Defense"),
]

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_closes(ticker: str, days: int = 60) -> list[dict] | None:
    try:
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            f"?interval=1d&range=3mo"
        )
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        result = resp.json()["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]
        bars = [
            {"ts": ts, "c": c}
            for ts, c in zip(timestamps, closes)
            if c is not None
        ]
        return bars if len(bars) >= 25 else None
    except Exception:
        return None


def calc_rs(ticker_bars: list[dict], spy_map: dict, period: int) -> float | None:
    pairs = [(b["c"], spy_map[b["ts"]]) for b in ticker_bars if b["ts"] in spy_map]
    if len(pairs) < period + 1:
        return None
    rs_now  = pairs[-1][0] / pairs[-1][1]
    rs_then = pairs[-(period + 1)][0] / pairs[-(period + 1)][1]
    return round((rs_now - rs_then) / rs_then * 100, 1)


def classify(rs5: float | None, rs20: float | None) -> str:
    if rs5 is None or rs20 is None:
        return "n/a"
    if rs5 > 0 and rs20 > 0:
        return "Leading"
    if rs5 > 0 and rs20 <= 0:
        return "Improving"
    if rs5 <= 0 and rs20 > 0:
        return "Fading"
    return "Lagging"


def flow_arrow(rs: float | None) -> str:
    if rs is None:
        return "  ?"
    if rs > 2:
        return " ↑↑"
    if rs > 0:
        return "  ↑"
    if rs > -2:
        return "  ↓"
    return " ↓↓"


def main():
    spy_bars = fetch_closes("SPY")
    if not spy_bars:
        print("[error] SPY fetch failed — cannot compute RS")
        sys.exit(1)
    spy_map = {b["ts"]: b["c"] for b in spy_bars}

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("## Sector Money Flow")
    print(f"*{now} | RS vs SPY — 5d (short flow) + 20d (trend)*")
    print()

    header = f"{'Sector':<22} {'5d RS':>7} {'20d RS':>7}   Label"
    print(header)
    print("-" * 55)

    results = []
    for etf, name in SECTORS:
        bars = fetch_closes(etf)
        if bars is None:
            print(f"{name:<22} [fetch error]")
            continue
        rs5  = calc_rs(bars, spy_map, 5)
        rs20 = calc_rs(bars, spy_map, 20)
        label = classify(rs5, rs20)
        results.append((etf, name, rs5, rs20, label))

        rs5_s  = f"{rs5:+.1f}%{flow_arrow(rs5)}" if rs5 is not None else "   n/a"
        rs20_s = f"{rs20:+.1f}%{flow_arrow(rs20)}" if rs20 is not None else "   n/a"
        print(f"{name:<22} {rs5_s:>10} {rs20_s:>10}   {label}")

    print()

    # --- Summary ---
    leading   = [f"{e}({n.split()[0]})" for e, n, r5, r20, l in results if l == "Leading"]
    improving = [f"{e}({n.split()[0]})" for e, n, r5, r20, l in results if l == "Improving"]
    fading    = [f"{e}({n.split()[0]})" for e, n, r5, r20, l in results if l == "Fading"]
    lagging   = [f"{e}({n.split()[0]})" for e, n, r5, r20, l in results if l == "Lagging"]

    print("Money flowing IN  :", ", ".join(leading + improving) or "ไม่มี")
    print("Money flowing OUT :", ", ".join(fading + lagging) or "ไม่มี")

    # Space-specific highlight
    space = [(e, n, r5, r20, l) for e, n, r5, r20, l in results if e in ("ROKT", "ITA")]
    if space:
        print()
        print("Space sector:")
        for e, n, r5, r20, l in space:
            r5_s  = f"{r5:+.1f}%" if r5 is not None else "n/a"
            r20_s = f"{r20:+.1f}%" if r20 is not None else "n/a"
            print(f"  {e} ({n}): 5d {r5_s} | 20d {r20_s} | {l}")

    print()
    print("-> Leading + Improving = sectors ที่ควรหา setups ใน universe-screen.py")
    print("-> Lagging = หลีกเลี่ยงการเข้า long แม้หุ้นจะ coiling")


if __name__ == "__main__":
    main()
