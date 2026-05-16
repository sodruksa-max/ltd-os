"""
ipo-scanner.py — scan recent + upcoming IPOs, flag big or high-buzz ones.
Source: Nasdaq IPO Calendar API (free, no key needed)
Filters: deal size >= $500M, or first-week volume >= 3x avg
Output: vault/00_inbox/ipo-radar-<date>.md
"""

import requests
import time
from datetime import date, timedelta
from pathlib import Path

import yfinance as yf

REPO = Path(__file__).resolve().parent.parent
INBOX = REPO / "vault/00_inbox"
INBOX.mkdir(parents=True, exist_ok=True)
KB = REPO / "vault/Knowledge"
KB.mkdir(parents=True, exist_ok=True)

MIN_DEAL_SIZE_M = 500    # $500M minimum to flag as big
BUZZ_VOLUME_RATIO = 3.0  # first-week volume 3x+ recent avg = high buzz

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}


def fetch_nasdaq_ipos(year_month: str) -> dict:
    url = f"https://api.nasdaq.com/api/ipo/calendar?date={year_month}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json().get("data", {})
    except Exception as e:
        print(f"  Nasdaq API error ({year_month}): {e}")
        return {}


def parse_deal_size(s: str) -> float:
    if not s:
        return 0
    s = s.replace("$", "").replace(",", "").strip()
    try:
        if "B" in s.upper():
            return float(s.upper().replace("B", "")) * 1000
        elif "M" in s.upper():
            return float(s.upper().replace("M", ""))
        return float(s)
    except Exception:
        return 0


def check_buzz(ticker: str) -> dict:
    """First-week volume vs recent avg as buzz proxy. Also returns price change."""
    try:
        hist = yf.Ticker(ticker).history(period="30d")["Close"]
        vol = yf.Ticker(ticker).history(period="30d")["Volume"]
        if vol.empty or len(vol) < 3:
            return {}
        first_week_vol = vol.iloc[:5].mean()
        recent_vol = vol.iloc[-10:].mean()
        ratio = round(first_week_vol / recent_vol, 1) if recent_vol > 0 else 0
        change_pct = round((hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0] * 100, 1)
        return {
            "volume_ratio": ratio,
            "price_change_pct": change_pct,
            "current_price": round(float(hist.iloc[-1]), 2),
        }
    except Exception:
        return {}


def main():
    today = date.today()

    # Fetch this month, last month, next month
    months = set()
    for delta in (-32, 0, 32):
        d = today + timedelta(days=delta)
        months.add(d.strftime("%Y-%m"))

    priced, upcoming = [], []

    for month in sorted(months):
        print(f"Fetching {month}...")
        data = fetch_nasdaq_ipos(month)

        for row in (data.get("priced", {}) or {}).get("rows", []) or []:
            priced.append({
                "company": row.get("companyName", ""),
                "ticker": (row.get("proposedTickerSymbol") or "").strip(),
                "date": row.get("pricedDate", ""),
                "price": row.get("proposedSharePrice", ""),
                "deal_size_m": parse_deal_size(row.get("dollarValueOfSharesOffered", "")),
            })

        rows = (data.get("upcoming", {}) or {}).get("upcomingTable", {}) or {}
        for row in rows.get("rows", []) or []:
            upcoming.append({
                "company": row.get("companyName", ""),
                "ticker": (row.get("proposedTickerSymbol") or "").strip(),
                "expected_date": row.get("expectedPriceDate", ""),
                "price_range": row.get("proposedSharePrice", ""),
                "deal_size_m": parse_deal_size(row.get("dollarValueOfSharesOffered", "")),
            })

    # Big priced IPOs + buzz check
    big_priced = sorted(
        [r for r in priced if r["deal_size_m"] >= MIN_DEAL_SIZE_M],
        key=lambda x: x["deal_size_m"], reverse=True,
    )
    buzz_flags = []
    for ipo in big_priced:
        if ipo["ticker"]:
            time.sleep(0.3)
            buzz = check_buzz(ipo["ticker"])
            ipo.update(buzz)
            if buzz.get("volume_ratio", 0) >= BUZZ_VOLUME_RATIO:
                buzz_flags.append(ipo)

    # Big upcoming
    upcoming_big = sorted(
        [r for r in upcoming if r["deal_size_m"] >= MIN_DEAL_SIZE_M],
        key=lambda x: x["deal_size_m"], reverse=True,
    )[:10]

    # Write report
    out = INBOX / f"ipo-radar-{today}.md"
    lines = [
        f"---",
        f"type: ipo-radar",
        f"date: {today}",
        f"---",
        f"",
        f"# IPO Radar — {today}",
        f"",
        f"Filter: deal ≥ ${MIN_DEAL_SIZE_M}M | buzz = first-week volume ≥ {BUZZ_VOLUME_RATIO}x avg",
        f"Source: Nasdaq IPO Calendar API",
        f"",
        f"---",
        f"",
        f"## Big IPOs — Already Trading",
        f"",
    ]

    if big_priced:
        lines += [
            "| Ticker | Company | IPO Date | Deal Size | IPO Price | Current | Change | Buzz |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in big_priced:
            buzz_tag = f"🔥 {r.get('volume_ratio')}x vol" if r.get("volume_ratio", 0) >= BUZZ_VOLUME_RATIO else "-"
            lines.append(
                f"| {r['ticker'] or 'TBD'} | {r['company'][:28]} | {r['date']} | "
                f"${r['deal_size_m']:.0f}M | {r['price']} | "
                f"${r.get('current_price', '?')} | {r.get('price_change_pct', '?')}% | {buzz_tag} |"
            )
    else:
        lines.append("_No big priced IPOs found in last 60 days._")

    lines += ["", "## High Buzz", ""]
    if buzz_flags:
        for r in buzz_flags:
            lines.append(
                f"- **{r['ticker']}** {r['company']} — "
                f"{r.get('volume_ratio')}x volume, {r.get('price_change_pct')}% since IPO"
            )
    else:
        lines.append("_None meeting buzz threshold._")

    lines += ["", "## Upcoming IPOs (≥ $500M)", ""]
    if upcoming_big:
        lines += [
            "| Company | Ticker | Expected Date | Price Range | Deal Size |",
            "|---|---|---|---|---|",
        ]
        for r in upcoming_big:
            lines.append(
                f"| {r['company'][:28]} | {r['ticker'] or 'TBD'} | {r['expected_date']} | "
                f"{r['price_range']} | ${r['deal_size_m']:.0f}M |"
            )
    else:
        lines.append("_No big upcoming IPOs._")

    lines += [
        "",
        "---",
        "_รัน `/stock-research <TICKER>` เพื่อ deep-dive ตัวที่น่าสนใจ_",
        "_ถ้าตรง thesis → รัน `/research-idea` → insight atoms เข้า KB → Nick เห็นในรอบถัดไป_",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nSaved: {out}")
    print(f"Big priced: {len(big_priced)} | High buzz: {len(buzz_flags)} | Upcoming: {len(upcoming_big)}")

    # Write KB-formatted candidates for Nick
    kb_lines = [
        "---",
        "type: nick-candidates",
        f"updated: {today}",
        "source: ipo-scanner.py",
        "---",
        "",
        "# Nick Candidates — IPO & Discovery Pipeline",
        f"*Auto-generated {today} | Nick: evaluate each against active theses before recommending add to THESIS_TRACKER*",
        "",
        "---",
        "",
        "## Already Trading (deal ≥ $500M)",
        "",
    ]

    if big_priced:
        kb_lines += [
            "| Ticker | Company | IPO Date | Deal Size | Price Change | Buzz |",
            "|---|---|---|---|---|---|",
        ]
        for r in big_priced:
            buzz = f"{r.get('volume_ratio')}x vol" if r.get("volume_ratio", 0) >= BUZZ_VOLUME_RATIO else "-"
            kb_lines.append(
                f"| {r['ticker'] or 'TBD'} | {r['company'][:30]} | {r['date']} | "
                f"${r['deal_size_m']:.0f}M | {r.get('price_change_pct', '❓')}% | {buzz} |"
            )
    else:
        kb_lines.append("_No big priced IPOs in last 60 days._")

    kb_lines += ["", "## High Buzz (first-week volume ≥ 3x avg)", ""]
    if buzz_flags:
        for r in buzz_flags:
            kb_lines.append(
                f"- **{r['ticker']}** {r['company']} — "
                f"{r.get('volume_ratio')}x volume, {r.get('price_change_pct')}% since IPO, "
                f"current ${r.get('current_price', '❓')}"
            )
    else:
        kb_lines.append("_None._")

    kb_lines += ["", "## Upcoming (deal ≥ $500M)", ""]
    if upcoming_big:
        kb_lines += [
            "| Company | Ticker | Expected Date | Price Range | Deal Size |",
            "|---|---|---|---|---|",
        ]
        for r in upcoming_big:
            kb_lines.append(
                f"| {r['company'][:30]} | {r['ticker'] or 'TBD'} | {r['expected_date']} | "
                f"{r['price_range']} | ${r['deal_size_m']:.0f}M |"
            )
    else:
        kb_lines.append("_No big upcoming IPOs._")

    kb_lines += [
        "",
        "---",
        "*Nick: สำหรับแต่ละ candidate — ถ้า sector ตรง thesis → เสนอ add THESIS_TRACKER; ถ้าไม่ตรง → note 'outside theses' แล้วข้าม*",
    ]

    kb_out = KB / "nick-candidates.md"
    kb_out.write_text("\n".join(kb_lines), encoding="utf-8")
    print(f"KB candidates: {kb_out}")


if __name__ == "__main__":
    main()
