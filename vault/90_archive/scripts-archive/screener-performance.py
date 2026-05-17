"""
screener-performance: Tracks win rate of stocks found by stock-screener.py.

Reads all stock-screener-*.md files, parses tickers + entry prices,
fetches D+1/D+3/D+5/D+10 prices from Yahoo Finance, and writes a
performance report to vault/20_investment/screener-performance-YYYY-MM-DD.md.

Usage:
  python scripts/screener-performance.py        # full report
  python scripts/screener-performance.py --test # dry run — parse only, no API calls
"""

import sys
import io
import re
import time
import argparse
import datetime
import pathlib

# Force UTF-8 output on Windows terminals (same pattern as stock-screener.py)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import requests
import pandas as pd


# ─── SECTION 1: Argument parsing ─────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Track screener win rate across dates")
parser.add_argument(
    "--test",
    action="store_true",
    help="Parse screener files and print tickers only — no Yahoo Finance API calls",
)
args = parser.parse_args()


# ─── SECTION 2: Paths ────────────────────────────────────────────────────────

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
INVESTMENT_DIR = PROJECT_ROOT / "vault" / "20_investment"

# Checkpoint offsets in trading days (actual bars in Yahoo data, not calendar days)
CHECKPOINTS = [1, 3, 5, 10]


# ─── SECTION 3: Screener file parser ─────────────────────────────────────────
# Reads markdown files and extracts screener_date + ticker + entry_price.

_TICKER_ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*\*\*([A-Z0-9.\-]+)\*\*\s*\|"  # | N | **TICKER** |
    r"[^|]*\|\s*\$([0-9]+(?:\.[0-9]+)?)\s*\|"          # | Company | $price |
)


def parse_screener_file(path: pathlib.Path) -> list[dict]:
    """
    Parses one screener markdown file and returns a list of
    {screener_date, ticker, entry_price, source_file} dicts.
    Returns empty list if file has no results (zero-result runs).
    """
    # Extract date from filename: stock-screener-YYYY-MM-DD-XXh.md
    name = path.stem  # e.g. stock-screener-2026-05-01-07h
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", name)
    if not date_match:
        return []
    screener_date = datetime.date.fromisoformat(date_match.group(1))

    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _TICKER_ROW_RE.match(line.strip())
        if m:
            rows.append({
                "screener_date": screener_date,
                "ticker": m.group(1),
                "entry_price": float(m.group(2)),
                "source_file": path.name,
            })
    return rows


def load_all_screener_entries() -> list[dict]:
    """
    Reads all stock-screener-*.md files.
    When multiple files share the same date (03h, 04h, 07h), keeps only
    the latest run (highest hour suffix) — that's the most up-to-date scan.
    Returns a flat list of entry dicts.
    """
    files = sorted(INVESTMENT_DIR.glob("stock-screener-*.md"))
    if not files:
        print("  No screener files found in vault/20_investment/")
        return []

    # Group files by date, keep the one with the highest hour suffix
    # File names: stock-screener-YYYY-MM-DD-XXh.md
    date_to_file: dict[str, pathlib.Path] = {}
    for f in files:
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})-(\d+)h", f.stem)
        if not date_match:
            continue
        date_str = date_match.group(1)
        hour = int(date_match.group(2))
        existing = date_to_file.get(date_str)
        if existing is None:
            date_to_file[date_str] = f
        else:
            # Extract hour from existing file to compare
            ex_match = re.search(r"-(\d+)h$", existing.stem)
            existing_hour = int(ex_match.group(1)) if ex_match else 0
            if hour > existing_hour:
                date_to_file[date_str] = f

    entries = []
    for date_str, f in sorted(date_to_file.items()):
        parsed = parse_screener_file(f)
        entries.extend(parsed)
        ticker_list = [e["ticker"] for e in parsed]
        print(f"  {f.name}: {len(parsed)} tickers — {', '.join(ticker_list) or '(none)'}")

    return entries


# ─── SECTION 4: Yahoo Finance session ────────────────────────────────────────
# Reuses the same crumb pattern as stock-screener.py.

YAHOO_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_yahoo_session() -> tuple[requests.Session, str]:
    """Creates a Yahoo Finance session and returns (session, crumb)."""
    session = requests.Session()
    session.headers.update(YAHOO_HEADERS)
    try:
        session.get("https://fc.yahoo.com", timeout=10)
    except requests.exceptions.RequestException:
        pass
    crumb_resp = session.get(
        "https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10
    )
    crumb_resp.raise_for_status()
    return session, crumb_resp.text.strip()


def fetch_daily_closes(
    session: requests.Session,
    crumb: str,
    ticker: str,
) -> pd.Series | None:
    """
    Fetches 90 days of daily close prices for one ticker via Yahoo v8 chart API.
    Returns a pandas Series indexed by date (tz-naive), or None on error.
    """
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {"interval": "1d", "range": "90d", "crumb": crumb}
    try:
        resp = session.get(url, params=params, timeout=15)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()
        result = data.get("chart", {}).get("result", [])
        if not result:
            return None
        r = result[0]
        timestamps = r.get("timestamp", [])
        closes = r.get("indicators", {}).get("quote", [{}])[0].get("close", [])
        if not timestamps or not closes:
            return None
        idx = pd.to_datetime(timestamps, unit="s").normalize()
        series = pd.Series(closes, index=idx, dtype=float).dropna()
        series.index = series.index.tz_localize(None)
        return series
    except Exception as e:
        print(f"    [warn] {ticker}: fetch failed — {e}")
        return None


# ─── SECTION 5: Return calculator ────────────────────────────────────────────
# Looks up the close price N trading days after screener_date and computes %.

def get_checkpoint_price(
    closes: pd.Series,
    screener_date: datetime.date,
    n_trading_days: int,
) -> float | None:
    """
    Finds the close price exactly N trading days after screener_date.
    Trading days are counted from actual bars in the Yahoo data, so
    weekends and holidays are automatically skipped.
    Returns the price float, or None if not enough bars exist yet (pending).
    """
    # Keep only dates strictly after screener_date
    after = closes[closes.index.date > screener_date]
    if len(after) < n_trading_days:
        return None  # not enough data yet — pending
    return float(after.iloc[n_trading_days - 1])


def compute_return(entry: float, exit_price: float | None) -> str | None:
    """
    Computes percentage return as a formatted string like '+4.0%' or '-2.1%'.
    Returns None when exit_price is None (pending).
    """
    if exit_price is None:
        return None
    pct = (exit_price - entry) / entry * 100
    return f"{pct:+.1f}%"


# ─── SECTION 6: Stats calculator ─────────────────────────────────────────────
# Aggregates win rates and average returns across all entries.

def calc_stats(perf_rows: list[dict]) -> dict:
    """
    Computes overall and per-checkpoint win rate + average return.
    Only counts rows where the checkpoint is not pending.
    Returns a dict keyed by checkpoint (1, 3, 5, 10).
    """
    stats: dict[int, dict] = {n: {"wins": 0, "total": 0, "returns": []} for n in CHECKPOINTS}

    for row in perf_rows:
        for n in CHECKPOINTS:
            ret_str = row.get(f"d{n}_pct")
            price = row.get(f"d{n}_price")
            if ret_str is None or ret_str == "pending" or ret_str == "[error]":
                continue
            pct = float(ret_str.replace("%", "").replace("+", ""))
            stats[n]["total"] += 1
            stats[n]["returns"].append(pct)
            if pct > 0:
                stats[n]["wins"] += 1

    for n in CHECKPOINTS:
        rets = stats[n]["returns"]
        stats[n]["avg_return"] = (sum(rets) / len(rets)) if rets else None
        stats[n]["win_rate"] = (
            f"{stats[n]['wins'] / stats[n]['total'] * 100:.0f}%"
            f" ({stats[n]['wins']}/{stats[n]['total']})"
            if stats[n]["total"] > 0
            else "pending"
        )

    return stats


def find_extremes(perf_rows: list[dict]) -> tuple[str, str]:
    """
    Returns (best_label, worst_label) strings like 'VITL +4.0% (D+1)'.
    Scans all checkpoints across all rows.
    """
    best_val, worst_val = None, None
    best_label, worst_label = "—", "—"

    for row in perf_rows:
        for n in CHECKPOINTS:
            ret_str = row.get(f"d{n}_pct")
            if ret_str is None or ret_str in ("pending", "[error]"):
                continue
            pct = float(ret_str.replace("%", "").replace("+", ""))
            if best_val is None or pct > best_val:
                best_val = pct
                best_label = f"{row['ticker']} {ret_str} (D+{n})"
            if worst_val is None or pct < worst_val:
                worst_val = pct
                worst_label = f"{row['ticker']} {ret_str} (D+{n})"

    return best_label, worst_label


# ─── SECTION 7: Markdown report writer ───────────────────────────────────────

def write_report(perf_rows: list[dict], file_count: int, date_count: int, output_path: pathlib.Path):
    """
    Builds the full markdown performance report and writes it to output_path.
    """
    today_str = datetime.date.today().isoformat()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Per-date summary rows
    dates = sorted(set(r["screener_date"] for r in perf_rows))
    summary_rows = []
    for d in dates:
        rows_for_date = [r for r in perf_rows if r["screener_date"] == d]
        n_tickers = len(rows_for_date)

        def win_rate_str(checkpoint: int) -> str:
            """Calculates win rate string for one checkpoint and one date."""
            valid = [
                r for r in rows_for_date
                if r.get(f"d{checkpoint}_pct") not in (None, "pending", "[error]")
            ]
            if not valid:
                return "pending"
            wins = sum(
                1 for r in valid
                if float(r[f"d{checkpoint}_pct"].replace("%", "").replace("+", "")) > 0
            )
            return f"{wins / len(valid) * 100:.0f}% ({wins}/{len(valid)})"

        summary_rows.append({
            "date": d.isoformat(),
            "tickers": n_tickers,
            "d1": win_rate_str(1),
            "d3": win_rate_str(3),
            "d5": win_rate_str(5),
            "d10": win_rate_str(10),
        })

    stats = calc_stats(perf_rows)
    best, worst = find_extremes(perf_rows)
    total_evaluated = stats[1]["total"]  # D+1 as proxy for "has any data"

    lines = []
    lines.append(f"# Screener Performance Report — {today_str}")
    lines.append("")
    lines.append(f"**Generated:** {now_str}")
    lines.append(f"**Screener files analyzed:** {file_count} files across {date_count} dates")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Summary by Screener Date")
    lines.append("")
    lines.append("| Screener Date | Tickers | D+1 Win% | D+3 Win% | D+5 Win% | D+10 Win% |")
    lines.append("|---|---|---|---|---|---|")
    for sr in summary_rows:
        lines.append(
            f"| {sr['date']} | {sr['tickers']} "
            f"| {sr['d1']} | {sr['d3']} | {sr['d5']} | {sr['d10']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Detail — All Tickers")
    lines.append("")
    lines.append(
        "| Screener Date | Ticker | Entry $ "
        "| D+1 $ | D+1 % "
        "| D+3 $ | D+3 % "
        "| D+5 $ | D+5 % "
        "| D+10 $ | D+10 % |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for row in perf_rows:
        def fmt_price(key: str) -> str:
            """Formats a price field as '$X.XX' or 'pending' or '[error]'."""
            v = row.get(key)
            if v is None:
                return "pending"
            if v == "[error]":
                return "[error]"
            return f"${v:.2f}"

        def fmt_pct(key: str) -> str:
            """Returns the pct string or 'pending'."""
            v = row.get(key)
            return v if v is not None else "pending"

        lines.append(
            f"| {row['screener_date']} | {row['ticker']} | ${row['entry_price']:.2f} "
            f"| {fmt_price('d1_price')} | {fmt_pct('d1_pct')} "
            f"| {fmt_price('d3_price')} | {fmt_pct('d3_pct')} "
            f"| {fmt_price('d5_price')} | {fmt_pct('d5_pct')} "
            f"| {fmt_price('d10_price')} | {fmt_pct('d10_pct')} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Overall Stats (all dates combined)")
    lines.append("")

    total_ticker_days = sum(stats[n]["total"] for n in CHECKPOINTS)
    lines.append(f"- **Total ticker-days evaluated:** {total_ticker_days} (ข้าม pending)")

    win_parts = " | ".join(
        f"**D+{n}:** {stats[n]['win_rate']}" for n in CHECKPOINTS
    )
    lines.append(f"- **Win rate** — {win_parts}")

    avg_parts = " | ".join(
        f"**D+{n}:** {stats[n]['avg_return']:+.1f}%"
        if stats[n]["avg_return"] is not None
        else f"**D+{n}:** pending"
        for n in CHECKPOINTS
    )
    lines.append(f"- **Avg return** — {avg_parts}")
    lines.append(f"- **Best performer:** {best}")
    lines.append(f"- **Worst performer:** {worst}")
    lines.append("")
    lines.append("---")
    lines.append("_Generated by `scripts/screener-performance.py` — LTD-OS_")
    lines.append("_Data: Yahoo Finance. Not financial advice._")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Saved: {output_path}")


# ─── SECTION 8: Main program flow ────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Screener Performance Tracker")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Step 1: Parse all screener markdown files
    print("\n[1/3] Parsing screener files...")
    entries = load_all_screener_entries()

    if not entries:
        print("\n  No ticker entries found. Screener files may all have zero results.")
        sys.exit(0)

    dates_found = sorted(set(e["screener_date"] for e in entries))
    file_count = len(list(INVESTMENT_DIR.glob("stock-screener-*.md")))
    print(f"\n  Found {len(entries)} total ticker entries across {len(dates_found)} screener dates")
    for e in entries:
        print(f"    {e['screener_date']}  {e['ticker']:<8}  entry=${e['entry_price']}")

    # --test mode: stop here, no API calls
    if args.test:
        print("\n  [--test] Dry run complete — no Yahoo Finance calls made.")
        print(f"  Would fetch prices for: {[e['ticker'] for e in entries]}")
        return

    # Step 2: Get Yahoo Finance session
    print("\n[2/3] Connecting to Yahoo Finance...")
    try:
        session, crumb = get_yahoo_session()
        print("  Connected. Crumb received.")
        time.sleep(1)
    except Exception as e:
        print(f"\n  ERROR: Could not connect to Yahoo Finance: {e}")
        sys.exit(1)

    # Step 3: Fetch prices and compute returns for each unique ticker
    print(f"\n[3/3] Fetching historical prices for {len(entries)} ticker entries...")

    # Deduplicate tickers — fetch once, reuse for all entries of same ticker
    unique_tickers = list(dict.fromkeys(e["ticker"] for e in entries))
    closes_cache: dict[str, pd.Series | None] = {}

    for i, ticker in enumerate(unique_tickers, 1):
        print(f"  [{i:>2}/{len(unique_tickers)}] {ticker:<8}", end="  ", flush=True)
        closes = fetch_daily_closes(session, crumb, ticker)
        closes_cache[ticker] = closes
        if closes is not None:
            print(f"got {len(closes)} bars (last: {closes.index[-1].date()})")
        else:
            print("[error]")
        time.sleep(0.5)  # 0.5s sleep to avoid 429 rate limiting

    # Build performance rows
    perf_rows = []
    for entry in entries:
        ticker = entry["ticker"]
        closes = closes_cache.get(ticker)
        row = {
            "screener_date": entry["screener_date"],
            "ticker": ticker,
            "entry_price": entry["entry_price"],
        }
        if closes is None:
            # Mark all checkpoints as error
            for n in CHECKPOINTS:
                row[f"d{n}_price"] = "[error]"
                row[f"d{n}_pct"] = "[error]"
        else:
            for n in CHECKPOINTS:
                exit_price = get_checkpoint_price(closes, entry["screener_date"], n)
                row[f"d{n}_price"] = exit_price  # None = pending
                row[f"d{n}_pct"] = compute_return(entry["entry_price"], exit_price)

        perf_rows.append(row)

    # Step 4: Write markdown report
    today_str = datetime.date.today().isoformat()
    output_path = INVESTMENT_DIR / f"screener-performance-{today_str}.md"
    write_report(perf_rows, file_count=file_count, date_count=len(dates_found), output_path=output_path)

    print(f"\n  Done. Report: {output_path}")


if __name__ == "__main__":
    main()
