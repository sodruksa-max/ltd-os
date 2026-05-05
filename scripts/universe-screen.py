#!/usr/bin/env python3
"""
Universe Screen — สแกน Semicon/AI/Datacenter universe แบบ 4-tier

Tier system (เรียงจากดีสุด → แย่สุดในการเข้า position):

  [EARLY]    ก่อนวิ่ง — coiling setup, จังหวะที่ดีที่สุด
             RSI 40-60 + above MA20 + price within 15% of 52w-high + vol quiet (<1x)

  [ALERT]    เริ่มวิ่ง — momentum ยังมีห้อง ยังเข้าได้
             gap >=1% + RSI 55-70 + above MA20 + vol 1.0-2.5x

  [EXTENDED] ไปไกลแล้ว — overbought / overextended, รอ pullback
             RSI > 72 หรือ gap > 6% หรือ price > 115% ของ MA20

  [WATCH]    สัญญาณผสม — ติดตามต่อ

Usage:
    code/python/.venv/Scripts/python scripts/universe-screen.py
    code/python/.venv/Scripts/python scripts/universe-screen.py --tickers NVDA AMD MU
"""

import sys
import io
import requests
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

UNIVERSE = [
    ("NVDA",  "Nvidia"),
    ("AMD",   "AMD"),
    ("MU",    "Micron"),
    ("AVGO",  "Broadcom"),
    ("PLTR",  "Palantir"),
    ("SMCI",  "Super Micro"),
    ("MRVL",  "Marvell"),
    ("ARM",   "ARM Holdings"),
    ("ASML",  "ASML"),
    ("DELL",  "Dell"),
]

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

MA_PERIOD  = 20
RSI_PERIOD = 14


def fetch_ohlcv(ticker: str) -> list[dict] | None:
    try:
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            f"?interval=1d&range=1y"
        )
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        result = resp.json()["chart"]["result"][0]
        timestamps = result["timestamp"]
        q = result["indicators"]["quote"][0]
        bars = []
        for i, ts in enumerate(timestamps):
            o = q["open"][i]
            h = q["high"][i]
            l = q["low"][i]
            c = q["close"][i]
            v = q["volume"][i]
            if None in (o, h, l, c, v):
                continue
            bars.append({"ts": ts, "o": o, "h": h, "l": l, "c": c, "v": v})
        return bars if len(bars) >= MA_PERIOD + RSI_PERIOD + 2 else None
    except Exception:
        return None


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
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)


def calc_atr(bars: list[dict], period: int = 14) -> float | None:
    if len(bars) < period + 1:
        return None
    recent = bars[-(period + 1):]
    trs = []
    for i in range(1, len(recent)):
        h, l, pc = recent[i]["h"], recent[i]["l"], recent[i - 1]["c"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return sum(trs) / len(trs)


def analyze(ticker: str, bars: list[dict]) -> dict:
    closes  = [b["c"] for b in bars]
    highs   = [b["h"] for b in bars]
    volumes = [b["v"] for b in bars]

    current = closes[-1]
    prev    = closes[-2]

    gap_pct    = (current - prev) / prev * 100
    ma20       = sum(closes[-MA_PERIOD:]) / MA_PERIOD
    above_ma   = current > ma20
    pct_vs_ma  = (current - ma20) / ma20 * 100

    avg_vol    = sum(volumes[-MA_PERIOD:]) / MA_PERIOD
    vol_ratio  = volumes[-1] / avg_vol if avg_vol else None

    rsi        = calc_rsi(closes, RSI_PERIOD)

    high_52w   = max(highs[-252:]) if len(highs) >= 252 else max(highs)
    pct_from_high = (current - high_52w) / high_52w * 100  # negative = below high

    atr_now    = calc_atr(bars, 14)
    atr_prev   = calc_atr(bars[:-5], 14) if len(bars) > 20 else None
    atr_contracting = (atr_now < atr_prev * 0.85) if (atr_now and atr_prev) else False

    # --- Tier classification ---

    # [EXTENDED] — overbought / overextended: check first
    extended = (
        (rsi is not None and rsi > 72) or
        gap_pct > 6.0 or
        pct_vs_ma > 15.0
    )

    # [EARLY] — coiling before run (best entry)
    # RSI neutral + above MA20 + approaching 52w high + volume quiet
    early_score = sum([
        rsi is not None and 40 <= rsi <= 62,   # RSI neutral
        above_ma and pct_vs_ma < 8.0,           # just above MA20, not extended
        pct_from_high >= -15.0,                  # within 15% of 52w high
        (vol_ratio or 1.0) < 1.0,               # volume quiet = accumulation
    ])

    # [ALERT] — momentum starting, gap + volume rising
    alert_score = sum([
        gap_pct >= 1.0,
        rsi is not None and 55 <= rsi <= 70,
        above_ma,
        vol_ratio is not None and 1.0 <= vol_ratio <= 2.5,
    ])

    # Assign tier
    if extended:
        tier = "EXTENDED"
    elif early_score >= 3:
        tier = "EARLY"
    elif alert_score >= 3:
        tier = "ALERT"
    elif early_score == 2 or alert_score == 2:
        tier = "WATCH"
    else:
        tier = "-"

    return {
        "ticker":       ticker,
        "price":        current,
        "gap_pct":      round(gap_pct, 2),
        "ma20":         round(ma20, 2),
        "pct_vs_ma":    round(pct_vs_ma, 1),
        "above_ma":     above_ma,
        "vol_ratio":    round(vol_ratio, 2) if vol_ratio else None,
        "rsi":          rsi,
        "high_52w":     round(high_52w, 2),
        "pct_from_high": round(pct_from_high, 1),
        "atr_contract": atr_contracting,
        "tier":         tier,
        "early_score":  early_score,
        "alert_score":  alert_score,
    }


def tier_label(tier: str) -> str:
    return {
        "EARLY":    "[EARLY]    <<< เข้าได้เลย — ก่อนวิ่ง",
        "ALERT":    "[ALERT]    --- เริ่มวิ่ง ยังเข้าได้",
        "EXTENDED": "[EXTENDED]  !!! ไปไกลแล้ว รอ pullback",
        "WATCH":    "[WATCH]    ~~~ ติดตาม",
        "-":        "[-]",
    }.get(tier, tier)


def main():
    tickers = UNIVERSE
    if "--tickers" in sys.argv:
        idx = sys.argv.index("--tickers")
        custom = sys.argv[idx + 1:]
        tickers = [(t, t) for t in custom]

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("## Universe Screen — Semicon / AI / Datacenter")
    print(f"*{now}*")
    print("*Tiers: [EARLY]=ก่อนวิ่ง [ALERT]=เริ่มวิ่ง [EXTENDED]=ไปไกลแล้ว*")
    print()

    header = (
        f"{'Ticker':<7} {'Price':>9} {'Gap%':>7} {'RSI':>5} "
        f"{'vs MA20':>8} {'Vol/Avg':>8} {'vs 52wH':>8}  Tier"
    )
    print(header)
    print("-" * (len(header) + 20))

    by_tier: dict[str, list] = {"EARLY": [], "ALERT": [], "EXTENDED": [], "WATCH": [], "-": []}

    for ticker, name in tickers:
        bars = fetch_ohlcv(ticker)
        if bars is None:
            print(f"{ticker:<7} [fetch error]")
            continue

        r = analyze(ticker, bars)

        rsi_s      = str(r["rsi"]) if r["rsi"] else "n/a"
        vol_s      = f"{r['vol_ratio']:.2f}x" if r["vol_ratio"] else "n/a"
        gap_s      = f"{r['gap_pct']:+.2f}%"
        vsma_s     = f"{r['pct_vs_ma']:+.1f}%"
        vshigh_s   = f"{r['pct_from_high']:+.1f}%"
        price_s    = f"${r['price']:,.2f}"
        atr_s      = " coil" if r["atr_contract"] else ""
        tier_s     = f"[{r['tier']}]{atr_s}"

        print(
            f"{ticker:<7} {price_s:>9} {gap_s:>7} {rsi_s:>5} "
            f"{vsma_s:>8} {vol_s:>8} {vshigh_s:>8}  {tier_s}"
        )
        by_tier[r["tier"]].append((ticker, name, r))

    print()
    print("vs MA20 = ราคา vs ค่าเฉลี่ย 20 วัน | vs 52wH = ห่างจาก 52-week high | coil = ATR กำลังหด")
    print()

    # --- Summary by tier ---
    if by_tier["EARLY"]:
        print("=" * 55)
        print("[EARLY] ก่อนวิ่ง — จังหวะที่ดีที่สุด (coiling setup):")
        print("=" * 55)
        for ticker, name, r in by_tier["EARLY"]:
            notes = []
            notes.append(f"RSI {r['rsi']}")
            notes.append(f"+{r['pct_vs_ma']:.1f}% above MA20")
            notes.append(f"{r['pct_from_high']:+.1f}% from 52w-high")
            if r["atr_contract"]: notes.append("ATR contracting (coiling)")
            print(f"  {ticker} (${r['price']:,.2f}): {' | '.join(notes)}")
            print(f"  -> รอ catalyst หรือ volume spike เพื่อ trigger entry")
        print()

    if by_tier["ALERT"]:
        print("[ALERT] เริ่มวิ่ง — momentum building, ยังเข้าได้:")
        for ticker, name, r in by_tier["ALERT"]:
            notes = [f"gap {r['gap_pct']:+.1f}%", f"RSI {r['rsi']}", f"vol {r['vol_ratio']:.1f}x"]
            print(f"  {ticker} (${r['price']:,.2f}): {' | '.join(notes)}")
        print()

    if by_tier["EXTENDED"]:
        print("[EXTENDED] ไปไกลแล้ว — รอ pullback ก่อนเข้า:")
        for ticker, name, r in by_tier["EXTENDED"]:
            reason = []
            if r["rsi"] and r["rsi"] > 72:   reason.append(f"RSI {r['rsi']} (overbought)")
            if r["gap_pct"] > 6:              reason.append(f"gap {r['gap_pct']:+.1f}%")
            if r["pct_vs_ma"] > 15:           reason.append(f"+{r['pct_vs_ma']:.1f}% above MA20")
            print(f"  {ticker} (${r['price']:,.2f}): {' | '.join(reason)}")
            print(f"  -> รอ pullback มา test MA20 (${r['ma20']:,.2f}) ก่อน")
        print()

    if by_tier["WATCH"]:
        print("[WATCH] สัญญาณผสม — ติดตาม:")
        for ticker, name, r in by_tier["WATCH"]:
            print(f"  {ticker}: RSI {r['rsi']} | gap {r['gap_pct']:+.1f}% | vol {r['vol_ratio']:.2f}x | vs MA20 {r['pct_vs_ma']:+.1f}%")
        print()

    if not any(by_tier[t] for t in ["EARLY", "ALERT", "EXTENDED", "WATCH"]):
        print("ไม่มีหุ้นใน universe ที่มีสัญญาณชัดเจนวันนี้")

    print("-> รัน /pre-market สำหรับ S/R levels + full brief ของตัว [EARLY] และ [ALERT]")


if __name__ == "__main__":
    main()
