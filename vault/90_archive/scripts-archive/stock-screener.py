"""
stock-screener: US stock screener for "ต้นรอบ" (beginning of trend cycle).

Finds low-priced ($2-$20) US stocks showing early signs of momentum:
fresh volume surge, RSI building, price above 20-day moving average.

Data source: Yahoo Finance screener API (free, no account required).
Indicators: calculated from yfinance OHLCV data.

Usage:
  python scripts/stock-screener.py           # full scan, saves markdown
  python scripts/stock-screener.py --test    # fetch first 5 tickers only, no yfinance
"""

import sys
import io
import time
import argparse
import datetime
import pathlib

# Force UTF-8 output on Windows terminals (required to print Thai characters)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import numpy as np
import requests
import pandas as pd


# ─── SECTION 1: Argument parsing ─────────────────────────────────────────────
# --test mode skips yfinance and just prints the first 5 tickers from Yahoo.

parser = argparse.ArgumentParser(description="ต้นรอบ US stock screener")
parser.add_argument(
    "--test",
    action="store_true",
    help="Fetch Yahoo Finance page only and print first 5 tickers (no yfinance)",
)
args = parser.parse_args()


# ─── SECTION 2: Yahoo Finance screener fetch ─────────────────────────────────
# Yahoo Finance requires a "crumb" token (a rotating security token) to use
# its screener API. We get it by first visiting a Yahoo page to receive a
# cookie, then requesting the crumb from a special endpoint.

YAHOO_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Screener filters:
#   eodprice: end-of-day price between $2 and $20
#   avgdailyvol3m: 3-month average daily volume > 500,000 (liquidity check)
#   region: US stocks only (NYSE, NASDAQ, AMEX)
SCREENER_QUERY = {
    "operator": "and",
    "operands": [
        {"operator": "gt", "operands": ["eodprice", 2]},
        {"operator": "lt", "operands": ["eodprice", 20]},
        {"operator": "gt", "operands": ["avgdailyvol3m", 500000]},
        {"operator": "eq", "operands": ["region", "us"]},
    ],
}

# How many candidates to pull from Yahoo Finance screener (max 250 per request)
SCREENER_SIZE = 250


def get_yahoo_crumb() -> tuple[requests.Session, str]:
    """
    Creates a requests session with Yahoo Finance cookies and retrieves
    the crumb token needed for API calls. Returns (session, crumb).
    """
    session = requests.Session()
    session.headers.update(YAHOO_HEADERS)

    # Visit Yahoo Finance to get the session cookie
    try:
        session.get("https://fc.yahoo.com", timeout=10)
    except requests.exceptions.RequestException:
        pass  # Cookie endpoint sometimes returns 404 but still sets cookies

    # Get the crumb token (a rotating key Yahoo requires for API auth)
    crumb_resp = session.get(
        "https://query1.finance.yahoo.com/v1/test/getcrumb",
        timeout=10,
    )
    try:
        crumb_resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"Yahoo Finance crumb endpoint failed ({e}). "
            "The API may have changed — try updating yfinance or check your internet connection."
        ) from e
    crumb = crumb_resp.text.strip()
    return session, crumb


def fetch_yahoo_candidates(session: requests.Session, crumb: str) -> list[dict]:
    """
    Calls Yahoo Finance screener API to get a list of candidate stocks
    that pass the basic price/volume/region filters.
    Returns a list of dicts with ticker symbol, company name, and basic data.
    """
    url = "https://query1.finance.yahoo.com/v1/finance/screener"

    body = {
        "offset": 0,
        "size": SCREENER_SIZE,
        "sortField": "percentchange",  # sort by today's % change (gainers first — better ต้นรอบ signal)
        "sortType": "DESC",
        "quoteType": "EQUITY",
        "topOperator": "AND",
        "query": SCREENER_QUERY,
    }

    params = {
        "crumb": crumb,
        "lang": "en-US",
        "region": "US",
        "count": SCREENER_SIZE,
    }

    resp = session.post(url, json=body, params=params, timeout=20)
    resp.raise_for_status()

    data = resp.json()
    finance = data.get("finance", {})
    error = finance.get("error")
    if error:
        raise RuntimeError(f"Yahoo Finance screener error: {error}")

    result = finance.get("result", [])
    if not result:
        return []

    quotes = result[0].get("quotes", [])

    candidates = []
    for q in quotes:
        symbol = q.get("symbol", "")
        if not symbol:
            continue
        candidates.append({
            "ticker": symbol,
            "company": q.get("longName") or q.get("shortName") or "",
            "price": q.get("regularMarketPrice") or 0,
            "market_cap": q.get("marketCap") or 0,
            "avg_vol_3m": q.get("averageDailyVolume3Month") or 0,
            "today_vol": q.get("regularMarketVolume") or 0,
            "fifty_two_week_low": q.get("fiftyTwoWeekLow") or 0,
            "fifty_two_week_high": q.get("fiftyTwoWeekHigh") or 0,
        })

    return candidates


# ─── SECTION 3: OHLCV fetch + indicator calculations ─────────────────────────
# Fetch 60 days of OHLCV data via Yahoo Finance v8 chart API — reusing the
# authenticated session from the screener step (same cookies, no new handshake).
# This avoids the per-call session creation that yfinance does, which triggers
# Yahoo's 429 rate limiter when scanning many tickers in sequence.

def fetch_ohlcv(session: requests.Session, crumb: str, ticker: str) -> pd.DataFrame | None:
    """
    Fetches 90 days of daily OHLCV data for one ticker using Yahoo's v8 chart API.
    90 days gives ~63 trading bars — enough to verify 3-month history requirement.
    Reuses the existing authenticated session — avoids yfinance's per-call session
    creation which causes 429 rate limiting at scale.
    """
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {
        "interval": "1d",
        "range": "90d",
        "crumb": crumb,
        "events": "div,splits",
    }
    resp = session.get(url, params=params, timeout=15)
    if resp.status_code == 404:
        return None  # ticker not found / delisted
    resp.raise_for_status()

    data = resp.json()
    result = data.get("chart", {}).get("result", [])
    if not result:
        return None

    r = result[0]
    timestamps = r.get("timestamp", [])
    quote = r.get("indicators", {}).get("quote", [{}])[0]
    closes = quote.get("close", [])
    volumes = quote.get("volume", [])

    if not timestamps or not closes:
        return None

    df = pd.DataFrame(
        {"Close": closes, "Volume": volumes},
        index=pd.to_datetime(timestamps, unit="s"),
    )
    return df.dropna(subset=["Close"])


def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """
    Calculates RSI(14) — momentum indicator 0-100.
    45-65 = ต้นรอบ sweet spot (building, not yet overbought).
    """
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    # Check zero only at the final value: zero avg_loss means RSI = 100 by definition.
    last_loss = float(avg_loss.iloc[-1])
    if last_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi_series = 100 - (100 / (1 + rs))
    return round(float(rsi_series.iloc[-1]), 1)


def analyze_ticker(
    ticker: str,
    candidate: dict,
    session: requests.Session,
    crumb: str,
) -> dict | None:
    """
    Fetches 90 days of OHLCV via Yahoo v8 chart API and calculates SMA20,
    RSI(14), volume ratio, and 5 additional quality filters.
    Returns a result dict if all criteria pass, or None to skip.
    """
    # Early exit: skip market cap outside $50M–$2B before any network call.
    market_cap = candidate.get("market_cap", 0)
    if market_cap > 0 and (market_cap < 50_000_000 or market_cap > 2_000_000_000):
        return None

    try:
        df = fetch_ohlcv(session, crumb, ticker)

        if df is None or len(df) < 22:
            return None  # too few bars

        close = df["Close"].astype(float)
        volume = df["Volume"].astype(float)

        # ── NEW: 3-month history check (≥63 trading bars ≈ 3 calendar months) ──
        if len(df) < 63:
            return None  # new listing or recently IPO'd — not enough track record

        current_price = float(close.iloc[-1])
        current_volume = float(volume.iloc[-1])

        sma20 = float(close.rolling(20).mean().iloc[-1])

        # Use 20 completed bars before today to avoid partial-bar bias.
        avg_vol_20 = float(volume.iloc[-21:-1].mean())
        vol_ratio = round(current_volume / avg_vol_20, 2) if avg_vol_20 > 0 else 0

        # ── NEW: 3-day avg vol (last 3 completed bars, exclude today) ──
        avg_vol_3d = float(volume.iloc[-4:-1].mean())

        rsi = calculate_rsi(close, period=14)
        pct_above_sma = round((current_price - sma20) / sma20 * 100, 1)

        # ── NEW: today's single-day % change ──
        prev_close = float(close.iloc[-2])
        today_pct_change = round((current_price - prev_close) / prev_close * 100, 1)

        # ── NEW: 52-week range position from Yahoo screener data ──
        wk52_low = candidate.get("fifty_two_week_low", 0)
        wk52_high = candidate.get("fifty_two_week_high", 0)
        if wk52_low > 0 and wk52_high > wk52_low:
            wk52_mid = wk52_low + (wk52_high - wk52_low) * 0.5
            in_lower_half_52wk = current_price <= wk52_mid
            wk52_position = round((current_price - wk52_low) / (wk52_high - wk52_low) * 100, 1)
        else:
            in_lower_half_52wk = True   # unknown → don't filter out
            wk52_position = None

        # ── Final criteria (original) ──
        if current_price < 2 or current_price > 20:
            return None
        if avg_vol_20 < 500_000:
            return None
        if vol_ratio < 1.5:
            return None
        if current_price <= sma20:
            return None
        if rsi < 45 or rsi > 65:
            return None

        # ── Final criteria (new additions) ──
        if pct_above_sma > 20:
            return None  # already extended — not a fresh breakout
        if today_pct_change >= 15:
            return None  # single-day pump/news spike — likely to reverse
        if avg_vol_3d < avg_vol_20:
            return None  # volume not sustained over 3 days — single-day spike only
        if not in_lower_half_52wk:
            return None  # in upper half of 52-week range — less room to run

        return {
            "ticker": ticker,
            "company": candidate.get("company", ""),
            "price": round(current_price, 2),
            "vol_ratio": vol_ratio,
            "rsi": rsi,
            "pct_above_sma": pct_above_sma,
            "today_pct_change": today_pct_change,
            "avg_vol_20d": int(avg_vol_20),
            "avg_vol_3d": int(avg_vol_3d),
            "today_vol": int(current_volume),
            "market_cap": candidate.get("market_cap", 0),
            "wk52_position": wk52_position,
        }

    except Exception as e:
        print(f"  [skip] {ticker}: {e}")
        return None


# ─── SECTION 4: Market cap label ─────────────────────────────────────────────
# Converts raw market cap number to a human-readable label.

def mcap_label(market_cap: int | float) -> str:
    """
    Converts a market cap number (in USD) to a readable category label.
    E.g. 500_000_000 -> 'Small $300M-$1B'
    """
    if not market_cap or market_cap == 0:
        return "—"
    if market_cap < 50_000_000:
        return "Micro <$50M"
    elif market_cap < 300_000_000:
        return "Micro $50M-$300M"
    elif market_cap < 1_000_000_000:
        return "Small $300M-$1B"
    elif market_cap < 2_000_000_000:
        return "Mid $1B-$2B"
    else:
        return ">$2B"


# ─── SECTION 5: Markdown output writer ───────────────────────────────────────
# Creates the final markdown file in vault/20_investment/

def write_markdown(results: list[dict], candidates_count: int, output_path: pathlib.Path):
    """
    Writes the top 20 results to a markdown file with Thai explanations,
    a ranked table, and a disclaimer.
    """
    # Always sort by vol_ratio descending inside the writer — defensive guard in
    # case the caller passes unsorted input.
    results = sorted(results, key=lambda r: r["vol_ratio"], reverse=True)

    today_str = datetime.date.today().isoformat()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append(f"# Stock Screener — ต้นรอบ — {today_str}")
    lines.append("")
    lines.append(f"**Run at:** {now_str}")
    lines.append(f"**Candidates screened (Yahoo Finance pre-filter):** {candidates_count}")
    lines.append(f"**Final results (passed all criteria):** {len(results)}")
    lines.append("")
    lines.append("> **DISCLAIMER:** For educational/paper trading purposes only.")
    lines.append("> Not financial advice. Always do your own research before buying.")
    lines.append("> Past screening results do not guarantee future performance.")
    lines.append("")

    # Screening criteria explanation in Thai
    lines.append("## เกณฑ์การคัดกรอง (Screening Criteria)")
    lines.append("")
    lines.append("| เกณฑ์ | ค่าที่กำหนด | เหตุผล |")
    lines.append("|---|---|---|")
    lines.append("| ราคา | $2 – $20 | หุ้นราคาถูก มีโอกาส upside สูง ใช้ทุนน้อย |")
    lines.append("| เฉลี่ย Volume 20 วัน | > 500,000 หุ้น/วัน | มีสภาพคล่อง ซื้อขายได้ง่าย ไม่ติดราคา |")
    lines.append("| Volume วันนี้ | > 1.5x ค่าเฉลี่ย 20 วัน | มีความสนใจใหม่เข้ามา — สัญญาณว่าเงินกำลังไหลเข้า |")
    lines.append("| Volume ต่อเนื่อง 3 วัน | avg 3 วัน ≥ avg 20 วัน | ยืนยันว่า volume เพิ่มต่อเนื่อง ไม่ใช่ spike วันเดียว |")
    lines.append("| ราคา vs SMA 20 วัน | ราคา > SMA20 และ ≤ +20% | เพิ่งผ่าน SMA20 ยังไม่ extended เกินไป |")
    lines.append("| RSI (14 วัน) | 45 – 65 | กำลังสะสมแรง ยังไม่ overbought ยังมีที่ให้วิ่ง |")
    lines.append("| เปลี่ยนแปลงวันนี้ | < +15% | กรอง pump/news spike ที่มักดึงกลับเร็ว |")
    lines.append("| 52-week range | ราคาอยู่ใน lower 50% | ยังมี room to run — ไม่ใช่หุ้นที่วิ่งถึงยอดแล้ว |")
    lines.append("| ประวัติราคา | ≥ 3 เดือน (63 วัน) | กรอง SPAC/IPO ใหม่ที่ยังไม่มี track record |")
    lines.append("| Market Cap | $50M – $2B | Small/Mid cap มีโอกาสโตได้มากกว่าหุ้นใหญ่ |")
    lines.append("| ตลาด | US (NYSE/NASDAQ/AMEX) | US stocks เท่านั้น |")
    lines.append("")

    if not results:
        lines.append("## ผลลัพธ์")
        lines.append("")
        lines.append("_ไม่พบหุ้นที่ผ่านเกณฑ์ทั้งหมดในวันนี้_")
        lines.append("")
        lines.append("**สาเหตุที่เป็นไปได้:**")
        lines.append("- ตลาดปิด (หุ้น US เปิดวันจันทร์-ศุกร์ 09:30-16:00 ET)")
        lines.append("- Volume วันนี้ยังต่ำกว่าค่าเฉลี่ย (ตลาดเงียบ)")
        lines.append("- ลองรันใหม่ในชั่วโมงที่ตลาดเปิด หรือปรับเกณฑ์ให้กว้างขึ้น")
    else:
        top_n = min(20, len(results))
        lines.append(f"## Top {top_n} — เรียงตาม Volume Ratio (มากสุดก่อน)")
        lines.append("")
        lines.append("| # | Ticker | Company | Price | Vol Ratio | RSI | % vs SMA20 | Today% | 52wk% | Market Cap |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")

        for i, row in enumerate(results[:20], start=1):
            company = (row.get("company") or "")[:22]
            mcap = mcap_label(row.get("market_cap", 0))
            wk52 = f"{row['wk52_position']:.0f}%" if row.get("wk52_position") is not None else "—"
            lines.append(
                f"| {i} | **{row['ticker']}** | {company} "
                f"| ${row['price']} "
                f"| {row['vol_ratio']}x | {row['rsi']} "
                f"| {row['pct_above_sma']:+.1f}% "
                f"| {row['today_pct_change']:+.1f}% "
                f"| {wk52} | {mcap} |"
            )

        lines.append("")
        lines.append("### คำอธิบายคอลัมน์")
        lines.append("")
        lines.append(
            "- **Vol Ratio** — Volume วันนี้ ÷ ค่าเฉลี่ย 20 วัน. "
            "2.0x = volume สองเท่าค่าเฉลี่ย = เงินกำลังไหลเข้าหุ้นนี้"
        )
        lines.append(
            "- **RSI** — Relative Strength Index 0-100. "
            "45-65 = โซน 'กำลังสะสมแรง' ยังไม่ overbought มีที่ให้วิ่งต่อ"
        )
        lines.append(
            "- **% vs SMA20** — ราคาสูงกว่าเส้นเฉลี่ย 20 วันกี่ % "
            "(เกณฑ์: +0% ถึง +20% — เพิ่งผ่าน SMA ยังไม่ extended)"
        )
        lines.append(
            "- **Today%** — % เปลี่ยนแปลงวันนี้. "
            "< +15% = ขยับแบบ organic ไม่ใช่ news spike ที่มักดึงกลับ"
        )
        lines.append(
            "- **52wk%** — ตำแหน่งราคาปัจจุบันใน 52-week range (0% = ราคาต่ำสุดรอบปี, 100% = สูงสุด). "
            "เกณฑ์: < 50% = ยังมี room to run"
        )
        lines.append(
            "- **Market Cap** — ขนาดบริษัท. Micro/Small = โอกาสโตสูง "
            "แต่ความเสี่ยงก็สูงกว่าหุ้นใหญ่"
        )

    lines.append("")
    lines.append("---")
    lines.append("_Generated by `scripts/stock-screener.py` — LTD-OS_")
    lines.append("_Data: Yahoo Finance v8 chart API. Not financial advice._")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Saved: {output_path}")


# ─── SECTION 6: Main program flow ────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  U.S. Stock Screener — ต้นรอบ (Beginning of Trend Cycle)")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Step 1: Get Yahoo Finance session + crumb token
    print("\n[1/3] Connecting to Yahoo Finance...")
    try:
        session, crumb = get_yahoo_crumb()
        print("  Connected. Crumb received.")
        time.sleep(1)  # avoid 429 between crumb fetch and screener POST
    except Exception as e:
        print(f"\n  ERROR: Could not connect to Yahoo Finance: {e}")
        print("  Check your internet connection and try again.")
        sys.exit(1)

    # Step 2: Fetch candidate tickers from Yahoo screener
    print("\n[2/3] Fetching candidates from Yahoo Finance screener...")
    try:
        candidates = fetch_yahoo_candidates(session, crumb)
    except Exception as e:
        print(f"\n  ERROR fetching candidates: {e}")
        sys.exit(1)

    print(f"  Found {len(candidates)} candidates (price $2-$20, vol >500K, US)")

    if not candidates:
        print("\n  No candidates found. Market may be closed or filters too strict.")
        sys.exit(0)

    # --test mode: print first 5 and exit without running yfinance
    if args.test:
        print("\n  [--test mode] First 5 tickers from Yahoo Finance screener:")
        for i, c in enumerate(candidates[:5], 1):
            mcap_display = f"{c['market_cap']:,}" if c['market_cap'] else "N/A"
            print(f"    {i}. {c['ticker']:<8}  ${c['price']:.2f}  vol_today={c['today_vol']:,}  mktcap={mcap_display}  {c['company'][:30]}")
        print("\n  Test passed. Run without --test for full scan.")
        return

    # Step 3: Calculate RSI, SMA20, volume ratio for each candidate via yfinance
    print(f"\n[3/3] Analyzing {len(candidates)} candidates via Yahoo v8 chart API...")
    print("  (Reusing session cookies — 0.5s sleep between tickers)")
    print("")

    results = []
    for i, candidate in enumerate(candidates, 1):
        ticker = candidate["ticker"]
        print(f"  [{i:>3}/{len(candidates)}] {ticker:<8}", end="  ", flush=True)

        result = analyze_ticker(ticker, candidate, session, crumb)
        if result:
            results.append(result)
            print(
                f"PASS  vol={result['vol_ratio']}x  RSI={result['rsi']}"
                f"  {result['pct_above_sma']:+.1f}% vs SMA20"
            )
        else:
            print("skip")

        time.sleep(0.5)   # 0.5s — shared session reduces 429 risk vs per-call yfinance

    # Sort by volume ratio descending (highest fresh interest first)
    results.sort(key=lambda r: r["vol_ratio"], reverse=True)

    # Write markdown output — filename includes hour so same-day re-runs don't overwrite.
    today_str = datetime.date.today().isoformat()
    hour_str = datetime.datetime.now().strftime("%H")
    project_root = pathlib.Path(__file__).parent.parent
    output_path = project_root / "vault" / "20_investment" / f"stock-screener-{today_str}-{hour_str}h.md"

    write_markdown(results, candidates_count=len(candidates), output_path=output_path)

    print(f"\n  {len(results)} stocks passed all criteria (out of {len(candidates)} candidates)")
    if results:
        top = results[0]
        print(f"  Top pick: {top['ticker']} — {top['vol_ratio']}x volume, RSI {top['rsi']}, {top['pct_above_sma']:+.1f}% vs SMA20")
    else:
        print("  No stocks passed all criteria today. Try again tomorrow or during market hours.")

    print("\n  Done.")


if __name__ == "__main__":
    main()
