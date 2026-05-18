#!/usr/bin/env python3
"""
Universe Screen — สแกน Semicon/AI/Datacenter/Space universe แบบ 4-tier + RS vs SPY

Tier system (เรียงจากดีสุด → แย่สุดในการเข้า position):

  [EARLY]    ก่อนวิ่ง — coiling setup, จังหวะที่ดีที่สุด
             RSI 40-60 + above MA20 + price within 15% of 52w-high + vol quiet (<1x)
             ★ = RS vs SPY กำลังหัวเลี้ยวขึ้น (แข็งแกร่งกว่าตลาด)

  [ALERT]    เริ่มวิ่ง — momentum ยังมีห้อง ยังเข้าได้
             gap >=1% + RSI 55-70 + above MA20 + vol 1.0-2.5x

  [EXTENDED] ไปไกลแล้ว — overbought / overextended, รอ pullback
             RSI > 72 หรือ gap > 6% หรือ price > 115% ของ MA20

  [WATCH]    สัญญาณผสม — ติดตามต่อ

RS Trend (Relative Strength vs SPY, 10 วัน):
  RS↑↑ = outperform SPY > +3%   (smart money เข้า)
  RS↑  = outperform SPY +1-3%   (เริ่มแข็งกว่าตลาด)
  RS→  = ใกล้เคียง SPY ±1%      (neutral)
  RS↓  = underperform SPY > -1% (อ่อนกว่าตลาด)

Usage:
    code/python/.venv/Scripts/python scripts/universe-screen.py
    code/python/.venv/Scripts/python scripts/universe-screen.py --tickers NVDA AMD MU
"""

import os
import sys
import io
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _llm import call_gemini  # noqa: E402


def llm_tier_rationales(entries: list[dict]) -> dict[str, str]:
    """Batch Gemini call — returns {ticker: one_sentence_thai}. Empty dict if no key."""
    if not entries:
        return {}
    lines = []
    for r in entries:
        rs_part = f" | RS10d={r['rs_10d']:+.1f}%" if r["rs_10d"] is not None else ""
        lines.append(
            f"{r['ticker']} [{r['tier']}]: RSI={r['rsi']} | "
            f"vs_MA20={r['pct_vs_ma']:+.1f}% | vol={r['vol_ratio']:.2f}x | "
            f"PTH={r['pth']:.2f}{rs_part}"
        )
    system = (
        "You are a technical analyst. For each ticker, write ONE sentence in Thai "
        "explaining why it is in that tier based on the indicators. "
        "Format: TICKER: sentence. One ticker per line. No other text."
    )
    text = call_gemini(system, "\n".join(lines), max_tokens=300)
    if not text:
        return {}
    result = {}
    for line in text.splitlines():
        if ":" in line:
            ticker, _, sent = line.partition(":")
            result[ticker.strip()] = sent.strip()
    return result

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# News sentiment (arXiv:2510.26228) — Alpaca news + Gemini LLM scoring
# ---------------------------------------------------------------------------

_NEWS_ENDPOINT = "https://data.alpaca.markets/v1beta1/news"


def _load_alpaca_keys() -> tuple[str, str]:
    env_file = Path(__file__).parent.parent / ".secrets" / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())
    return os.environ.get("ALPACA_API_KEY", ""), os.environ.get("ALPACA_SECRET_KEY", "")


def fetch_news_headlines(tickers: list[str], hours: int = 24) -> dict[str, list[str]]:
    """Fetch Alpaca news for tickers (last N hours). Returns {ticker: [headlines]}."""
    api_key, secret_key = _load_alpaca_keys()
    if not api_key or not secret_key:
        return {}

    now   = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)
    headers = {
        "APCA-API-KEY-ID":     api_key,
        "APCA-API-SECRET-KEY": secret_key,
    }
    by_ticker: dict[str, list[str]] = {t: [] for t in tickers}
    for i in range(0, len(tickers), 30):
        batch = tickers[i:i + 30]
        params = {
            "symbols":         ",".join(batch),
            "start":           start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end":             now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "limit":           50,
            "sort":            "desc",
            "include_content": "false",
        }
        try:
            resp = requests.get(_NEWS_ENDPOINT, params=params, headers=headers, timeout=15)
            resp.raise_for_status()
            for article in resp.json().get("news", []):
                headline = article.get("headline", "")
                for sym in (article.get("symbols") or []):
                    if sym in by_ticker and headline not in by_ticker[sym]:
                        by_ticker[sym].append(headline)
        except Exception as e:
            sys.stderr.write(f"[news-sentiment] fetch error: {e}\n")
    return by_ticker


def llm_news_sentiment(ticker_headlines: dict[str, list[str]]) -> dict[str, str]:
    """Batch Gemini call — returns {ticker: 'B'|'N'|'R'}. Empty dict on failure."""
    if not ticker_headlines:
        return {}
    lines = []
    for ticker, headlines in ticker_headlines.items():
        lines.append(f"\n{ticker}:")
        for h in headlines[:5]:
            lines.append(f"  - {h}")
        if not headlines:
            lines.append("  (no headlines)")
    system = (
        "For each ticker below, rate the 24h news sentiment. "
        "B = bullish (beat, contract win, partnership, upgrade, record revenue). "
        "N = neutral (no clear directional impact, or no news). "
        "R = bearish (miss, guidance cut, investigation, recall, downgrade). "
        "Return exactly: TICKER: B or N or R — one per line, nothing else."
    )
    text = call_gemini(system, "\n".join(lines), max_tokens=200)
    if not text:
        return {}
    result = {}
    for line in text.splitlines():
        if ":" in line:
            ticker, _, score = line.partition(":")
            s = score.strip().upper()
            if s in ("B", "N", "R"):
                result[ticker.strip()] = s
    return result


UNIVERSE = [
    # Semicon
    ("NVDA",  "Nvidia"),
    ("AMD",   "AMD"),
    ("MU",    "Micron"),
    ("AVGO",  "Broadcom"),
    ("MRVL",  "Marvell"),
    ("ARM",   "ARM Holdings"),
    ("ASML",  "ASML"),
    # Semicon Small-Cap
    ("CRDO",  "Credo Technology"),
    ("AEIS",  "Advanced Energy"),
    ("UCTT",  "Ultra Clean Holdings"),
    # Memory / WFE
    ("LRCX",  "Lam Research"),
    ("WDC",   "Western Digital"),
    ("ONTO",  "Onto Innovation"),
    # AI Infrastructure
    ("SMCI",  "Super Micro"),
    ("DELL",  "Dell"),
    ("HPE",   "HP Enterprise"),
    # Datacenter / Cloud
    ("MSFT",  "Microsoft"),
    ("AMZN",  "Amazon"),
    ("GOOGL", "Alphabet"),
    ("META",  "Meta"),
    ("PLTR",  "Palantir"),
    # Datacenter Small-Cap
    ("MOD",   "Modine Manufacturing"),
    # Space
    ("RKLB",  "Rocket Lab"),
    ("ASTS",  "AST SpaceMobile"),
    ("LUNR",  "Intuitive Machines"),
    ("KTOS",  "Kratos Defense"),
    # Defense AI Small-Cap
    ("BBAI",  "BigBear.ai"),
    # Quantum Computing
    ("IONQ",  "IonQ"),
    ("RGTI",  "Rigetti Computing"),
    ("QBTS",  "D-Wave Quantum"),
    ("QUBT",  "Quantum Computing Inc"),
    ("IBM",   "IBM"),
]

SECTOR_MAP = {
    # Semicon → SMH
    "NVDA": "SMH", "AMD": "SMH", "MU": "SMH", "AVGO": "SMH",
    "MRVL": "SMH", "ARM": "SMH", "ASML": "SMH", "CRDO": "SMH",
    "AEIS": "SMH", "UCTT": "SMH", "LRCX": "SMH", "WDC": "SMH", "ONTO": "SMH",
    # AI Infra / Datacenter / Cloud → XLK
    "SMCI": "XLK", "DELL": "XLK", "HPE": "XLK",
    "MSFT": "XLK", "AMZN": "XLK", "GOOGL": "XLK", "META": "XLK",
    "PLTR": "XLK", "MOD": "XLK",
    # Space / Defense → UFO
    "RKLB": "UFO", "ASTS": "UFO", "LUNR": "UFO", "KTOS": "UFO", "BBAI": "UFO",
    # Quantum → QTUM
    "IONQ": "QTUM", "RGTI": "QTUM", "QBTS": "QTUM", "QUBT": "QTUM", "IBM": "QTUM",
}

SECTOR_ETFS = ["SMH", "XLK", "UFO"]

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
RS_PERIOD  = 10  # วันที่ใช้คำนวณ RS trend


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


def build_spy_map(spy_bars: list[dict]) -> dict:
    """timestamp → SPY close price"""
    return {b["ts"]: b["c"] for b in spy_bars}


def calc_rs_trend(ticker_bars: list[dict], spy_map: dict, period: int = RS_PERIOD) -> float | None:
    """
    RS trend = % change in (ticker/SPY) ratio over last `period` days.
    Positive = outperforming SPY. Negative = underperforming.
    """
    pairs = [(b["c"], spy_map[b["ts"]]) for b in ticker_bars if b["ts"] in spy_map]
    if len(pairs) < period + 1:
        return None
    rs_now  = pairs[-1][0] / pairs[-1][1]
    rs_then = pairs[-(period + 1)][0] / pairs[-(period + 1)][1]
    return round((rs_now - rs_then) / rs_then * 100, 1)


def rs_label(rs: float | None) -> str:
    if rs is None:
        return "RS?"
    if rs > 3.0:
        return "RS↑↑"
    if rs > 1.0:
        return "RS↑"
    if rs > -1.0:
        return "RS→"
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


def calc_5d_momentum(bars: list[dict]) -> float | None:
    if len(bars) < 6:
        return None
    return round((bars[-1]["c"] - bars[-6]["c"]) / bars[-6]["c"] * 100, 1)


def analyze(ticker: str, bars: list[dict], spy_map: dict, sector_momentum: float | None = None) -> dict:
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
    pct_from_high = (current - high_52w) / high_52w * 100
    pth        = round(current / high_52w, 3)  # Price-to-High: 1.0 = at 52w-high

    atr_now    = calc_atr(bars, 14)
    atr_prev   = calc_atr(bars[:-5], 14) if len(bars) > 20 else None
    atr_contracting = (atr_now < atr_prev * 0.85) if (atr_now and atr_prev) else False

    rs_10d     = calc_rs_trend(bars, spy_map, RS_PERIOD)

    # ราคาขึ้นแต่ volume ต่ำกว่าค่าเฉลี่ย = สัญญาณอ่อน
    vol_div    = gap_pct > 0 and (vol_ratio or 1.0) < 1.0
    # sector ETF 5d trend ติดลบ = macro drag ต้าน
    sector_warn = sector_momentum is not None and sector_momentum < 0

    # --- Tier classification ---

    # [EXTENDED] — check first
    # gap > 6% นับเป็น EXTENDED เฉพาะถ้า RSI > 50 และอยู่เหนือ MA20 (ป้องกัน oversold bounce ถูกตี EXTENDED ผิด)
    gap_extended = gap_pct > 6.0 and (rsi is not None and rsi > 50) and above_ma
    extended = (
        (rsi is not None and rsi > 72) or
        gap_extended or
        pct_vs_ma > 15.0
    )

    # [EARLY] — coiling before run
    # RS↑ เพิ่ม 1 คะแนน (smart money เริ่มเข้า ก่อน price วิ่ง)
    early_score = sum([
        rsi is not None and 40 <= rsi <= 62,
        above_ma and pct_vs_ma < 8.0,
        pct_from_high >= -15.0,
        (vol_ratio or 1.0) < 1.0,
        rs_10d is not None and rs_10d > 1.0,        # RS กำลังแข็งกว่า SPY
        pth > 0.90 and (vol_ratio or 0) > 1.0,      # PTH boost: near 52w-high + volume rising (Chen et al. 2024)
    ])

    # [ALERT] — momentum starting
    alert_score = sum([
        gap_pct >= 1.0,
        rsi is not None and 55 <= rsi <= 70,
        above_ma,
        vol_ratio is not None and 1.0 <= vol_ratio <= 2.5,
    ])

    # RSI ต้องอยู่ใน coiling range (≤62) ถึงจะเป็น EARLY ได้ — ถ้า RSI สูงกว่านี้คือวิ่งแล้ว
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

    # ★ marker: EARLY + RS rising = สัญญาณแข็งแกร่ง
    star = (tier == "EARLY" and rs_10d is not None and rs_10d > 1.0)

    return {
        "ticker":         ticker,
        "price":          current,
        "gap_pct":        round(gap_pct, 2),
        "ma20":           round(ma20, 2),
        "pct_vs_ma":      round(pct_vs_ma, 1),
        "above_ma":       above_ma,
        "vol_ratio":      round(vol_ratio, 2) if vol_ratio else None,
        "rsi":            rsi,
        "high_52w":       round(high_52w, 2),
        "pct_from_high":  round(pct_from_high, 1),
        "atr_contract":   atr_contracting,
        "rs_10d":         rs_10d,
        "pth":            pth,
        "vol_div":        vol_div,
        "sector_warn":    sector_warn,
        "sector_momentum": sector_momentum,
        "tier":           tier,
        "star":           star,
        "early_score":    early_score,
        "alert_score":    alert_score,
    }


def tier_label(tier: str, star: bool = False) -> str:
    labels = {
        "EARLY":    "[EARLY★]   <<< ก่อนวิ่ง + RS แข็ง — จังหวะดีที่สุด" if star else "[EARLY]    <<< เข้าได้เลย — ก่อนวิ่ง",
        "ALERT":    "[ALERT]    --- เริ่มวิ่ง ยังเข้าได้",
        "EXTENDED": "[EXTENDED]  !!! ไปไกลแล้ว รอ pullback",
        "WATCH":    "[WATCH]    ~~~ ติดตาม",
        "-":        "[-]",
    }
    return labels.get(tier, tier)


def main():
    tickers = UNIVERSE
    if "--tickers" in sys.argv:
        idx = sys.argv.index("--tickers")
        custom = sys.argv[idx + 1:]
        tickers = [(t, t) for t in custom]

    # Fetch SPY once — ใช้เป็น benchmark RS
    spy_bars = fetch_ohlcv("SPY")
    spy_map  = build_spy_map(spy_bars) if spy_bars else {}
    if not spy_map:
        print("[warn] SPY fetch failed — RS trend unavailable")

    # Fetch sector ETFs — SMH / XLK / UFO (5-day momentum)
    sector_5d: dict[str, float | None] = {}
    for etf in SECTOR_ETFS:
        etf_bars = fetch_ohlcv(etf)
        sector_5d[etf] = calc_5d_momentum(etf_bars) if etf_bars else None

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("## Universe Screen — Semicon / AI / Datacenter / Space")
    print(f"*{now}*")
    print("*Tiers: [EARLY★]=ก่อนวิ่ง+RS↑ [EARLY]=ก่อนวิ่ง [ALERT]=เริ่มวิ่ง [EXTENDED]=ไปไกลแล้ว*")
    print()

    # Sector ETF momentum summary
    etf_parts = []
    for etf in SECTOR_ETFS:
        m = sector_5d.get(etf)
        etf_parts.append(f"{etf} {m:+.1f}%" if m is not None else f"{etf} n/a")
    print(f"Sector 5d: {' | '.join(etf_parts)}")
    print()

    header = (
        f"{'Ticker':<7} {'Price':>9} {'Gap%':>7} {'RSI':>5} "
        f"{'vs MA20':>8} {'Vol/Avg':>8} {'vs 52wH':>8} {'RS10d':>6}  Tier"
    )
    print(header)
    print("-" * (len(header) + 20))

    by_tier: dict[str, list] = {"EARLY": [], "ALERT": [], "EXTENDED": [], "WATCH": [], "-": []}

    for ticker, name in tickers:
        bars = fetch_ohlcv(ticker)
        if bars is None:
            print(f"{ticker:<7} [fetch error]")
            continue

        etf_key  = SECTOR_MAP.get(ticker)
        sec_mom  = sector_5d.get(etf_key) if etf_key else None
        r = analyze(ticker, bars, spy_map, sector_momentum=sec_mom)

        rsi_s    = str(r["rsi"]) if r["rsi"] else "n/a"
        vol_s    = f"{r['vol_ratio']:.2f}x" if r["vol_ratio"] else "n/a"
        gap_s    = f"{r['gap_pct']:+.2f}%"
        vsma_s   = f"{r['pct_vs_ma']:+.1f}%"
        vshigh_s = f"{r['pct_from_high']:+.1f}%"
        price_s  = f"${r['price']:,.2f}"
        rs_s     = rs_label(r["rs_10d"])
        atr_s    = " coil" if r["atr_contract"] else ""
        star_s   = "★" if r["star"] else ""
        flags    = (" ⚠vol-div" if r["vol_div"] else "") + (" ⚠sector↓" if r["sector_warn"] else "")
        tier_s   = f"[{r['tier']}{star_s}]{atr_s}{flags}"

        print(
            f"{ticker:<7} {price_s:>9} {gap_s:>7} {rsi_s:>5} "
            f"{vsma_s:>8} {vol_s:>8} {vshigh_s:>8} {rs_s:>6}  {tier_s}"
        )
        by_tier[r["tier"]].append((ticker, name, r))

    print()
    print("vs MA20 = ราคา vs ค่าเฉลี่ย 20 วัน | vs 52wH = ห่างจาก 52-week high | coil = ATR กำลังหด")
    print("RS10d = Relative Strength vs SPY 10 วัน | ↑↑>3% ↑>1% →±1% ↓<-1%")
    print()

    # --- Summary by tier ---
    stars = [(t, n, r) for t, n, r in by_tier["EARLY"] if r["star"]]
    non_stars = [(t, n, r) for t, n, r in by_tier["EARLY"] if not r["star"]]

    if stars:
        print("=" * 60)
        print("[EARLY★] ก่อนวิ่ง + RS แข็งกว่า SPY — สัญญาณแข็งแกร่งที่สุด:")
        print("=" * 60)
        for ticker, name, r in stars:
            notes = [
                f"RSI {r['rsi']}",
                f"+{r['pct_vs_ma']:.1f}% above MA20",
                f"{r['pct_from_high']:+.1f}% from 52w-high",
                f"PTH {r['pth']:.2f}",
                f"RS {r['rs_10d']:+.1f}% vs SPY",
            ]
            if r["atr_contract"]:
                notes.append("ATR contracting (coiling)")
            if r["vol_div"]:
                notes.append("⚠ vol-div (ราคาขึ้น volume ต่ำ)")
            if r["sector_warn"]:
                etf = SECTOR_MAP.get(ticker, "?")
                notes.append(f"⚠ sector↓ ({etf} {r['sector_momentum']:+.1f}% 5d)")
            print(f"  {ticker} (${r['price']:,.2f}): {' | '.join(notes)}")
            print(f"  -> RS rising = smart money เข้าแล้ว รอ volume spike เพื่อ confirm entry")
        print()

    if non_stars:
        print("[EARLY] ก่อนวิ่ง — coiling setup (RS ยังไม่ยืนยัน):")
        for ticker, name, r in non_stars:
            notes = [
                f"RSI {r['rsi']}",
                f"+{r['pct_vs_ma']:.1f}% above MA20",
                f"{r['pct_from_high']:+.1f}% from 52w-high",
                f"PTH {r['pth']:.2f}",
                f"RS {r['rs_10d']:+.1f}% vs SPY" if r["rs_10d"] is not None else "RS n/a",
            ]
            if r["atr_contract"]:
                notes.append("ATR contracting (coiling)")
            if r["vol_div"]:
                notes.append("⚠ vol-div (ราคาขึ้น volume ต่ำ)")
            if r["sector_warn"]:
                etf = SECTOR_MAP.get(ticker, "?")
                notes.append(f"⚠ sector↓ ({etf} {r['sector_momentum']:+.1f}% 5d)")
            print(f"  {ticker} (${r['price']:,.2f}): {' | '.join(notes)}")
            print(f"  -> รอ catalyst หรือ volume spike + RS ยืนยันก่อน entry")
        print()

    if by_tier["ALERT"]:
        print("[ALERT] เริ่มวิ่ง — momentum building, ยังเข้าได้:")
        for ticker, name, r in by_tier["ALERT"]:
            rs_str = f"RS {r['rs_10d']:+.1f}%" if r["rs_10d"] is not None else "RS n/a"
            notes = [f"gap {r['gap_pct']:+.1f}%", f"RSI {r['rsi']}", f"vol {r['vol_ratio']:.1f}x", rs_str]
            print(f"  {ticker} (${r['price']:,.2f}): {' | '.join(notes)}")
        print()

    if by_tier["EXTENDED"]:
        ext_parts = ", ".join(
            f"{t}(RSI {r['rsi']} | MA20=${r['ma20']:,.0f})"
            for t, n, r in by_tier["EXTENDED"]
        )
        print(f"[EXTENDED] รอ pullback มา MA20 ก่อน (ไม่ entry): {ext_parts}")
        print()

    if by_tier["WATCH"]:
        watch_parts = ", ".join(
            f"{t}(RSI {r['rsi']} | {rs_label(r['rs_10d'])})"
            for t, n, r in by_tier["WATCH"]
        )
        print(f"[WATCH] สัญญาณผสม: {watch_parts}")
        print()

    if not any(by_tier[t] for t in ["EARLY", "ALERT", "EXTENDED", "WATCH"]):
        print("ไม่มีหุ้นใน universe ที่มีสัญญาณชัดเจนวันนี้")

    # LLM tier rationales — batch call for EARLY + ALERT only
    actionable = [r for _, _, r in by_tier["EARLY"] + by_tier["ALERT"]]
    rationales = llm_tier_rationales(actionable)
    if rationales:
        print("### Why (AI rationale)")
        for ticker, sentence in rationales.items():
            print(f"  {ticker}: {sentence}")
        print()

    # News sentiment — EARLY + ALERT tickers only (arXiv:2510.26228)
    actionable_tickers = [t for t, _, _ in by_tier["EARLY"] + by_tier["ALERT"]]
    if actionable_tickers:
        news = fetch_news_headlines(actionable_tickers)
        tickers_with_news = {t: h for t, h in news.items() if h}
        sentiments = llm_news_sentiment(tickers_with_news)
        _sent_label = {"B": "Bullish", "N": "Neutral", "R": "Bearish"}
        print("### News Sentiment — 24h (arXiv:2510.26228)")
        for ticker in actionable_tickers:
            if not news:  # API unavailable
                print(f"  {ticker}: [-] N/A (news API unavailable)")
                continue
            score = sentiments.get(ticker, "N")
            heads = news.get(ticker, [])
            label = _sent_label.get(score, "N/A")
            top   = f' | "{heads[0][:80]}"' if heads else " | (no recent news)"
            print(f"  {ticker}: [{score}] {label} | {len(heads)} headlines{top}")
        print()

    print("-> รัน /pre-market สำหรับ S/R levels + full brief ของตัว [EARLY★] และ [ALERT]")
    print("-> รัน sector-flow.py เพื่อดูว่า sector ไหนกำลังดูด money")


if __name__ == "__main__":
    main()
