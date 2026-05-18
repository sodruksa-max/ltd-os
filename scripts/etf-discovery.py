#!/usr/bin/env python3
"""
ETF Discovery — ค้นหาหุ้นใหม่นอก watchlist ที่ยังไม่ตกรถ

ดึง top holdings จาก sector ETFs แล้วกรองเฉพาะ EARLY★ / EARLY / ALERT
(ตัดพวก EXTENDED ออก = ไปไกลแล้ว)

ETFs scanned:
  SOXX — Semicon / Memory
  UFO  — Space (pure-play)
  XLK  — Broad Tech / Datacenter / AI Infra

Usage:
    code/python/.venv/Scripts/python scripts/etf-discovery.py
    code/python/.venv/Scripts/python scripts/etf-discovery.py --top 10
"""

import sys
import io
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# AI software — ไม่เอา (ไม่แน่นอน ผู้ใช้ exclude)
BLACKLIST_TICKERS = {"CRM", "SNOW", "NOW", "WDAY", "ADBE", "INTU", "TEAM", "ZS", "OKTA", "DDOG", "MDB"}

# ตัวที่อยู่ใน watchlist แล้ว — ข้ามได้เลย
UNIVERSE_TICKERS = {
    # T1
    "NVDA","AMD","AVGO","SMCI","MU","MRVL","LRCX","MOD","DELL","HPE",
    # T2
    "ASML","ARM","CRDO","AEIS","UCTT","WDC","ONTO",
    # T3
    "RKLB","ASTS","LUNR","KTOS","BBAI",
    # T4
    "PLTR","CRM","SNOW",
    # T5
    "IONQ","RGTI","QBTS","QUBT",
    # T6
    "ISRG","TER","CGNX","ROK","SYM","PATH","AVAV",
    # Tier 2
    "MRNA","CRSP","BEAM","RXRX",
    "CRWD","PANW","ZS","NET","OKTA",
    "COIN","HOOD","SOFI","SQ",
    "CEG","VST","SMR","NNE","ETN",
    "SHOP","MELI","SE",
    "AXON","HII",
    "DKNG","DUOL","TTD",
    # C-list + large-caps to skip
    "TSM","GOOGL","MSFT","AMZN","META","AAPL","INTC","TXN","QCOM",
}

ETF_LIST = [
    ("SOXX", "Semicon [T2]"),
    ("UFO",  "Space [T3]"),
    ("ROKT", "Space/Satellite [T3]"),
    ("XLK",  "Broad Tech [T1]"),
    ("BOTZ", "Robotics/AI [T6]"),
    ("ITA",  "Defense [T3]"),
]

TOP_N_HOLDINGS   = 30   # holdings ต่อ ETF ที่ดึงมา
MIN_AVG_DOLLAR_VOL = 30_000_000  # กรอง illiquid: avg dollar volume < $30M/day

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
RS_PERIOD  = 10


# ── ETF holdings ──────────────────────────────────────────────────────────────

def fetch_etf_holdings(etf: str) -> list[tuple[str, str]]:
    """ดึง top holdings จาก stockanalysis.com → [(symbol, name), ...]"""
    try:
        url  = f"https://stockanalysis.com/etf/{etf.lower()}/holdings/"
        resp = requests.get(url, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("table tbody tr")[:TOP_N_HOLDINGS]
        result = []
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) >= 3:
                sym  = cols[1].upper()
                name = cols[2]
                if sym and sym.isalpha():
                    result.append((sym, name))
        return result
    except Exception:
        return []


def collect_candidates() -> list[tuple[str, str, str]]:
    """รวม holdings จากทุก ETF, dedup, กรอง universe → [(symbol, name, etf_label)]"""
    seen: dict[str, tuple[str, str]] = {}  # symbol → (name, etf_label)
    for etf, label in ETF_LIST:
        holdings = fetch_etf_holdings(etf)
        if not holdings:
            print(f"  [warn] {etf}: holdings fetch failed")
            continue
        for sym, name in holdings:
            if sym in UNIVERSE_TICKERS or sym in BLACKLIST_TICKERS:
                continue
            if sym not in seen:
                seen[sym] = (name, label)
    return [(sym, name, label) for sym, (name, label) in seen.items()]


# ── Price / momentum logic (same as universe-screen.py) ──────────────────────

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
            o, h, l, c, v = q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i]
            if None in (o, h, l, c, v):
                continue
            bars.append({"ts": ts, "o": o, "h": h, "l": l, "c": c, "v": v})
        return bars if len(bars) >= MA_PERIOD + RSI_PERIOD + 2 else None
    except Exception:
        return None


def build_spy_map(spy_bars: list[dict]) -> dict:
    return {b["ts"]: b["c"] for b in spy_bars}


def calc_rs_trend(bars: list[dict], spy_map: dict, period: int = RS_PERIOD) -> float | None:
    pairs = [(b["c"], spy_map[b["ts"]]) for b in bars if b["ts"] in spy_map]
    if len(pairs) < period + 1:
        return None
    rs_now  = pairs[-1][0]  / pairs[-1][1]
    rs_then = pairs[-(period + 1)][0] / pairs[-(period + 1)][1]
    return round((rs_now - rs_then) / rs_then * 100, 1)


def rs_label(rs: float | None) -> str:
    if rs is None: return "RS?"
    if rs > 3.0:   return "RS↑↑"
    if rs > 1.0:   return "RS↑"
    if rs > -1.0:  return "RS→"
    return "RS↓"


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


def calc_atr(bars: list[dict], period: int = 14) -> float | None:
    if len(bars) < period + 1:
        return None
    recent = bars[-(period + 1):]
    trs = []
    for i in range(1, len(recent)):
        h, l, pc = recent[i]["h"], recent[i]["l"], recent[i - 1]["c"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return sum(trs) / len(trs)


def analyze(ticker: str, bars: list[dict], spy_map: dict) -> dict | None:
    closes  = [b["c"] for b in bars]
    highs   = [b["h"] for b in bars]
    volumes = [b["v"] for b in bars]

    current  = closes[-1]
    prev     = closes[-2]
    gap_pct  = (current - prev) / prev * 100
    ma20     = sum(closes[-MA_PERIOD:]) / MA_PERIOD
    above_ma = current > ma20
    pct_vs_ma = (current - ma20) / ma20 * 100

    avg_vol   = sum(volumes[-MA_PERIOD:]) / MA_PERIOD
    vol_ratio = volumes[-1] / avg_vol if avg_vol else None

    # กรอง illiquid
    avg_dollar_vol = avg_vol * current
    if avg_dollar_vol < MIN_AVG_DOLLAR_VOL:
        return None

    rsi          = calc_rsi(closes, RSI_PERIOD)
    high_52w     = max(highs[-252:]) if len(highs) >= 252 else max(highs)
    pct_from_high = (current - high_52w) / high_52w * 100

    atr_now  = calc_atr(bars, 14)
    atr_prev = calc_atr(bars[:-5], 14) if len(bars) > 20 else None
    atr_contracting = (atr_now < atr_prev * 0.85) if (atr_now and atr_prev) else False

    rs_10d = calc_rs_trend(bars, spy_map, RS_PERIOD)

    gap_extended = gap_pct > 6.0 and (rsi is not None and rsi > 50) and above_ma
    extended = (
        (rsi is not None and rsi > 72) or
        gap_extended or
        pct_vs_ma > 15.0
    )
    early_score = sum([
        rsi is not None and 40 <= rsi <= 62,
        above_ma and pct_vs_ma < 8.0,
        pct_from_high >= -15.0,
        (vol_ratio or 1.0) < 1.0,
        rs_10d is not None and rs_10d > 1.0,
    ])
    alert_score = sum([
        gap_pct >= 1.0,
        rsi is not None and 55 <= rsi <= 70,
        above_ma,
        vol_ratio is not None and 1.0 <= vol_ratio <= 2.5,
    ])

    rsi_coiling = rsi is not None and rsi <= 62
    if extended:
        tier = "EXTENDED"
    elif early_score >= 3 and rsi_coiling:
        tier = "EARLY"
    elif alert_score >= 3:
        tier = "ALERT"
    elif early_score == 2 or alert_score == 2:
        tier = "WATCH"
    else:
        tier = "-"

    star = (tier == "EARLY" and rs_10d is not None and rs_10d > 1.0)

    return {
        "ticker":        ticker,
        "price":         current,
        "gap_pct":       round(gap_pct, 2),
        "pct_vs_ma":     round(pct_vs_ma, 1),
        "above_ma":      above_ma,
        "vol_ratio":     round(vol_ratio, 2) if vol_ratio else None,
        "rsi":           rsi,
        "pct_from_high": round(pct_from_high, 1),
        "atr_contract":  atr_contracting,
        "rs_10d":        rs_10d,
        "tier":          tier,
        "star":          star,
    }


# ── KB save ───────────────────────────────────────────────────────────────────

def save_to_kb(results: list) -> None:
    """Write/update the ETF Discovery section in vault/Knowledge/nick-candidates.md."""
    from datetime import date as _date
    kb_file = Path(__file__).resolve().parent.parent / "vault/Knowledge/nick-candidates.md"
    if not kb_file.exists():
        print(f"  [skip] {kb_file} not found")
        return

    today = _date.today()
    header_lines = [
        "",
        "## ETF Discovery — หุ้นนอก watchlist ที่ RS กำลังขึ้น",
        "",
        f"*Auto-updated: {today} | ETFs: {', '.join(e for e, _ in ETF_LIST)}*",
        "",
    ]

    visible = [r for r in results if r[3]["tier"] in ("EARLY", "ALERT")]
    if visible:
        header_lines += [
            "| Ticker | ETF Source | Price | Signal | RS10d | vs MA20 |",
            "|---|---|---|---|---|---|",
        ]
        for sym, name, etf_label, r in visible:
            star = "★" if r["star"] else ""
            tier_s = f"[{r['tier']}{star}]"
            rs_s = rs_label(r["rs_10d"])
            vsma = f"{r['pct_vs_ma']:+.1f}%"
            header_lines.append(
                f"| {sym} | {etf_label} | ${r['price']:.2f} | {tier_s} | {rs_s} | {vsma} |"
            )
    else:
        header_lines.append("_ไม่พบ setup EARLY/ALERT นอก watchlist วันนี้_")

    header_lines += [
        "",
        "*ถ้าสนใจตัวไหน: `/stock-content TICKER` ก่อนตัดสินใจ*",
        "",
    ]
    new_section = "\n".join(header_lines)

    text = kb_file.read_text(encoding="utf-8")
    if "## ETF Discovery" in text:
        before = text.split("## ETF Discovery")[0].rstrip()
        text = before + new_section
    else:
        text = text.rstrip() + "\n" + new_section

    kb_file.write_text(text, encoding="utf-8")
    print(f"  KB updated: {kb_file.name} ({len(visible)} EARLY/ALERT entries)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    top_n = None
    if "--top" in sys.argv:
        idx = sys.argv.index("--top")
        try:
            top_n = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            pass

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("## ETF Discovery — หุ้นใหม่นอก watchlist ที่ยังไม่ตกรถ")
    print(f"*{now}*")
    print(f"*ETFs: {', '.join(e for e, _ in ETF_LIST)} | min avg vol $30M/day | ตัด EXTENDED ออก*")
    print()

    print("กำลังดึง ETF holdings...")
    candidates = collect_candidates()
    print(f"พบ {len(candidates)} ตัวนอก watchlist — กำลังวิเคราะห์...\n")

    spy_bars = fetch_ohlcv("SPY")
    spy_map  = build_spy_map(spy_bars) if spy_bars else {}

    results: list[tuple[str, str, str, dict]] = []  # (sym, name, etf, analysis)

    for sym, name, etf_label in candidates:
        bars = fetch_ohlcv(sym)
        if bars is None:
            continue
        r = analyze(sym, bars, spy_map)
        if r is None:
            continue  # illiquid หรือ data ไม่พอ
        if r["tier"] in ("EXTENDED", "-"):
            continue  # ไปไกลแล้ว หรือ ไม่มี setup
        results.append((sym, name, etf_label, r))

    # เรียง: EARLY★ → EARLY → ALERT → WATCH
    tier_order = {"EARLY": 0, "ALERT": 1, "WATCH": 2}
    results.sort(key=lambda x: (tier_order.get(x[3]["tier"], 9), -(x[3]["rs_10d"] or 0)))

    if top_n:
        results = results[:top_n]

    if not results:
        print("ไม่พบ setup ที่น่าสนใจวันนี้")
        return

    header = (
        f"{'Ticker':<7} {'Name':<22} {'ETF':<20} {'Price':>9} "
        f"{'Gap%':>7} {'RSI':>5} {'vs MA20':>8} {'Vol/Avg':>8} {'vs 52wH':>8} {'RS10d':>6}  Tier"
    )
    print(header)
    print("-" * (len(header) + 5))

    for sym, name, etf_label, r in results:
        star_s   = "★" if r["star"] else ""
        atr_s    = " coil" if r["atr_contract"] else ""
        tier_s   = f"[{r['tier']}{star_s}]{atr_s}"
        price_s  = f"${r['price']:,.2f}"
        gap_s    = f"{r['gap_pct']:+.2f}%"
        vsma_s   = f"{r['pct_vs_ma']:+.1f}%"
        vshigh_s = f"{r['pct_from_high']:+.1f}%"
        vol_s    = f"{r['vol_ratio']:.2f}x" if r["vol_ratio"] else "n/a"
        rsi_s    = str(r["rsi"]) if r["rsi"] else "n/a"
        rs_s     = rs_label(r["rs_10d"])
        name_s   = name[:20]

        print(
            f"{sym:<7} {name_s:<22} {etf_label:<20} {price_s:>9} "
            f"{gap_s:>7} {rsi_s:>5} {vsma_s:>8} {vol_s:>8} {vshigh_s:>8} {rs_s:>6}  {tier_s}"
        )

    print()
    print(f"พบ {len(results)} setup | EARLY★=ก่อนวิ่ง+RS↑ EARLY=ก่อนวิ่ง ALERT=เริ่มวิ่งยังเข้าได้")
    print("ถ้าสนใจตัวไหน: /screen TICKER หรือ /stock-research TICKER")

    if "--save-kb" in sys.argv:
        save_to_kb(results)


if __name__ == "__main__":
    main()
