#!/usr/bin/env python3
"""
News snapshot via Alpaca News API — last 12h, market-relevant, categorized.

Usage:
    code/python/.venv/Scripts/python scripts/news-snapshot.py
    code/python/.venv/Scripts/python scripts/news-snapshot.py --nick-news

  --nick-news   Fetch per-holding company news for Nick portfolio.
                Reads nick_state.json for tickers + kill condition keywords.
                Outputs JSON to stdout: {TICKER: {clean, flags, headlines}}.
                Also writes vault/20_investment/nick/news-digest.md.

Output (markdown, embed directly in pre-market brief):
  - Geopolitical  (XLE/USO/GLD/TLT tagged + keyword detection)
  - Fed / Macro
  - Earnings / Corporate
  - Quick Read summary for Catalyst section

Requires ALPACA_API_KEY + ALPACA_SECRET_KEY in .secrets/.env
"""

import json
import os
import sys
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

NEWS_ENDPOINT      = "https://data.alpaca.markets/v1beta1/news"
LOOKBACK_HOURS     = 12
NICK_LOOKBACK_HOURS = 48   # 2 days to cover weekends / missed days
MAX_ARTICLES       = 30
NICK_STATE_PATH    = Path("vault/20_investment/nick/nick_state.json")
NICK_DIGEST_PATH   = Path("vault/20_investment/nick/news-digest.md")

# Symbols that surface geopolitical / macro-sensitive news
GEO_SYMBOLS    = ["XLE", "USO", "GLD", "TLT", "UUP", "ITA", "EEM", "XAR"]
BROAD_SYMBOLS  = ["SPY", "QQQ", "IWM"]
ALL_SYMBOLS    = GEO_SYMBOLS + BROAD_SYMBOLS

# Market channel labels per symbol
CHANNEL_MAP = {
    "XLE": "oil/energy", "USO": "oil",    "GLD": "gold/safe-haven",
    "TLT": "bonds",      "UUP": "USD",    "ITA": "defense",
    "XAR": "defense",    "EEM": "EM/risk-off",
}

# Keyword classifiers (lowercase)
GEO_KEYWORDS = {
    "war", "attack", "military", "troops", "ukraine", "russia", "iran",
    "middle east", "gaza", "israel", "missile", "airstrike", "conflict",
    "sanctions", "embargo", "strait", "naval", "ceasefire", "invasion",
    "escalat", "nuclear", "weapon", "geopolit", "terror", "coup",
}
FED_KEYWORDS = {
    "fed", "federal reserve", "fomc", "rate cut", "rate hike", "inflation",
    "powell", "cpi", "pce", "gdp", "nonfarm", "unemployment", "yield curve",
    "basis point", "monetary policy", "dovish", "hawkish", "taper", "quantitative",
}
EARNINGS_KEYWORDS = {
    "earnings", "eps", "revenue", "quarterly", "beat", "miss", "guidance",
    "profit", "loss", "outlook", "results", "q1", "q2", "q3", "q4",
    "raised guidance", "lowered guidance",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_env():
    env_file = Path(__file__).parent.parent / ".secrets" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip())


def fetch_news(api_key: str, secret_key: str) -> list:
    now   = datetime.now(timezone.utc)
    start = now - timedelta(hours=LOOKBACK_HOURS)
    params = {
        "symbols":          ",".join(ALL_SYMBOLS),
        "start":            start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end":              now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "limit":            MAX_ARTICLES,
        "sort":             "desc",
        "include_content":  "false",
    }
    headers = {
        "APCA-API-KEY-ID":    api_key,
        "APCA-API-SECRET-KEY": secret_key,
    }
    resp = requests.get(NEWS_ENDPOINT, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json().get("news", [])


def classify(headline: str, summary: str) -> str:
    text = (headline + " " + summary).lower()
    if any(kw in text for kw in GEO_KEYWORDS):
        return "GEO"
    if any(kw in text for kw in FED_KEYWORDS):
        return "FED"
    if any(kw in text for kw in EARNINGS_KEYWORDS):
        return "EARNINGS"
    return "OTHER"


def geo_magnitude(headline: str, summary: str) -> str:
    text = (headline + " " + summary).lower()
    hits = sum(1 for kw in GEO_KEYWORDS if kw in text)
    if hits >= 3:
        return "สูง"
    if hits == 2:
        return "กลาง"
    return "ต่ำ"


def affected_channels(symbols: list) -> str:
    channels = []
    for s in symbols:
        ch = CHANNEL_MAP.get(s)
        if ch and ch not in channels:
            channels.append(ch)
    return ", ".join(channels) if channels else "broad market"


def fmt_time(created_at: str) -> str:
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return dt.strftime("%H:%M UTC")
    except Exception:
        return created_at[:16]


def dedup(articles: list) -> list:
    seen, result = set(), []
    for a in articles:
        h = a.get("headline", "")
        if h not in seen:
            seen.add(h)
            result.append(a)
    return result

# ---------------------------------------------------------------------------
# Print sections
# ---------------------------------------------------------------------------

def print_geo(geo: list):
    print("### Geopolitical (market-relevant)")
    if not geo:
        print("- ไม่พบข่าว geopolitical ที่กระทบตลาดในช่วง 12 ชั่วโมงที่ผ่านมา\n")
        return
    for a in geo[:5]:
        mag      = geo_magnitude(a.get("headline", ""), a.get("summary", ""))
        channels = affected_channels(a.get("symbols", []))
        t        = fmt_time(a.get("created_at", ""))
        src      = a.get("source", "")
        print(f"- **[magnitude: {mag}]** {a['headline']}")
        print(f"  → ผลกระทบ: {channels} | {src} | {t}")
    print()


def print_fed(fed: list):
    print("### Fed / Macro")
    if not fed:
        print("- ไม่มีข่าว Fed/Macro ใหม่\n")
        return
    for a in fed[:4]:
        t   = fmt_time(a.get("created_at", ""))
        src = a.get("source", "")
        print(f"- {a['headline']} | {src} | {t}")
    print()


def print_earnings(earnings: list):
    print("### Earnings / Corporate")
    if not earnings:
        print("- ไม่มีข่าว Earnings ใหม่\n")
        return
    for a in earnings[:4]:
        syms = ", ".join(a.get("symbols", [])[:3])
        tag  = f"[{syms}] " if syms else ""
        t    = fmt_time(a.get("created_at", ""))
        src  = a.get("source", "")
        print(f"- {tag}{a['headline']} | {src} | {t}")
    print()


def print_quick_read(geo: list, fed: list, earnings: list, total: int):
    has_high_geo = any(
        geo_magnitude(a.get("headline", ""), a.get("summary", "")) == "สูง"
        for a in geo
    )
    geo_level = "สูง" if has_high_geo else ("กลาง/ต่ำ" if geo else "ไม่มี")

    print("### Quick Read — ใช้ใน Catalyst section ของ brief")
    print(f"- **Geopolitical pressure:** {geo_level}")
    print(f"- **Fed/Macro signals:** {'มี — ดูรายละเอียดด้านบน' if fed else 'ไม่มีใหม่'}")
    print(f"- **Earnings surprises:** {'มี — ดูรายละเอียดด้านบน' if earnings else 'ไม่มีใหม่'}")
    print()
    print(
        f"*Alpaca News API | Articles: {total} | "
        f"GEO: {len(geo)} | FED: {len(fed)} | EARNINGS: {len(earnings)}*"
    )

# ---------------------------------------------------------------------------
# Nick-news mode
# ---------------------------------------------------------------------------

def fetch_news_for_tickers(api_key: str, secret_key: str, tickers: list[str]) -> list:
    now   = datetime.now(timezone.utc)
    start = now - timedelta(hours=NICK_LOOKBACK_HOURS)
    params = {
        "symbols":         ",".join(tickers),
        "start":           start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end":             now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "limit":           50,
        "sort":            "desc",
        "include_content": "false",
    }
    headers = {
        "APCA-API-KEY-ID":     api_key,
        "APCA-API-SECRET-KEY": secret_key,
    }
    resp = requests.get(NEWS_ENDPOINT, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json().get("news", [])


def load_nick_state() -> dict:
    if not NICK_STATE_PATH.exists():
        return {}
    return json.loads(NICK_STATE_PATH.read_text(encoding="utf-8"))


def nick_news_mode(api_key: str, secret_key: str) -> None:
    state = load_nick_state()
    positions = state.get("positions", {})
    if not positions:
        print(json.dumps({}))
        return

    tickers = list(positions.keys())

    # Verify Alpaca symbol limit (current max is 100 per call)
    if len(tickers) > 100:
        tickers = tickers[:100]

    try:
        raw = fetch_news_for_tickers(api_key, secret_key, tickers)
    except Exception as e:
        sys.stderr.write(f"[nick-news] Alpaca fetch failed: {e}\n")
        result = {t: {"clean": True, "flags": [], "headlines": [], "error": str(e)} for t in tickers}
        print(json.dumps(result))
        return

    # Group articles by ticker
    by_ticker: dict[str, list[str]] = {t: [] for t in tickers}
    for article in dedup(raw):
        syms = article.get("symbols") or []
        headline = article.get("headline", "")
        if not syms:
            # Untagged article — skip (cannot attribute to specific holding)
            continue
        for sym in syms:
            if sym in by_ticker:
                by_ticker[sym].append(headline)

    # Evaluate kill condition keywords per ticker
    digest: dict[str, dict] = {}
    for ticker in tickers:
        headlines = by_ticker[ticker]
        if not headlines:
            sys.stderr.write(f"[nick-news] {ticker}: no news found (Alpaca returned empty)\n")

        kill_conds = positions[ticker].get("kill_conditions", [])
        flags: list[str] = []
        for cond in kill_conds:
            if cond.get("metric") != "news_keyword":
                continue
            keywords = cond.get("threshold", [])
            joined   = " ".join(h.lower() for h in headlines)
            if any(kw.lower() in joined for kw in keywords):
                flags.append(f"{cond['id']}: {cond['label']}")

        digest[ticker] = {
            "clean":     len(flags) == 0,
            "flags":     flags,
            "headlines": headlines[:5],  # cap at 5 for context budget
        }

    # Write markdown digest
    _write_nick_digest(digest, state)

    # JSON to stdout for daily_scan.py
    print(json.dumps(digest))


def _write_nick_digest(digest: dict, state: dict) -> None:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Nick News Digest",
        f"*{now_str} | Alpaca News API | Last {NICK_LOOKBACK_HOURS}h*",
        "",
    ]
    for ticker, data in digest.items():
        status = "[CLEAN]" if data["clean"] else "[FLAGS]"
        lines.append(f"## {ticker} {status}")
        if data.get("flags"):
            for f in data["flags"]:
                lines.append(f"- **KILL ALERT:** {f}")
        if data.get("headlines"):
            for h in data["headlines"]:
                lines.append(f"- {h}")
        else:
            lines.append(f"- no news found for {ticker} (Alpaca empty)")
        lines.append("")

    nav = state.get("nav", {}).get("current", "?")
    lines.append(f"*NAV: ${nav} | Generated: {now_str}*")

    NICK_DIGEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    NICK_DIGEST_PATH.write_text("\n".join(lines), encoding="utf-8")
    sys.stderr.write(f"[nick-news] digest written to {NICK_DIGEST_PATH}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    load_env()
    api_key    = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")

    if "--nick-news" in sys.argv:
        if not api_key or not secret_key:
            sys.stderr.write("[nick-news] ALPACA_API_KEY / ALPACA_SECRET_KEY not set\n")
            print(json.dumps({}))
            return
        nick_news_mode(api_key, secret_key)
        return

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("## News Snapshot")
    print(f"*{now_str} | Alpaca News API | Last {LOOKBACK_HOURS}h | embed in pre-market brief*\n")
    print("---\n")

    if not api_key or not secret_key:
        print("*[news-snapshot unavailable: ALPACA_API_KEY / ALPACA_SECRET_KEY not set]*")
        return

    try:
        raw = fetch_news(api_key, secret_key)
    except Exception as e:
        print(f"*[news-snapshot unavailable: {e}]*")
        return

    articles = dedup(raw)

    if not articles:
        print("*ไม่พบข่าวในช่วง 12 ชั่วโมงที่ผ่านมา*")
        return

    geo, fed, earnings = [], [], []
    for a in articles:
        cat = classify(a.get("headline", ""), a.get("summary", ""))
        if cat == "GEO":
            geo.append(a)
        elif cat == "FED":
            fed.append(a)
        elif cat == "EARNINGS":
            earnings.append(a)

    print_geo(geo)
    print_fed(fed)
    print_earnings(earnings)
    print_quick_read(geo, fed, earnings, len(articles))


if __name__ == "__main__":
    main()
