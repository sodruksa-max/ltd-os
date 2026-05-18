#!/usr/bin/env python3
"""
watchlist-manager: Add, remove, and list tickers in scripts/watchlist.json.

Usage:
    python scripts/watchlist-manager.py --list
    python scripts/watchlist-manager.py --add IONQ "IonQ" QTUM --tags quantum --reason "quantum thesis T1"
    python scripts/watchlist-manager.py --remove IONQ
    python scripts/watchlist-manager.py --auto-discover
"""

import json
import sys
import argparse
from datetime import date
from pathlib import Path

WATCHLIST_PATH = Path(__file__).parent / "watchlist.json"


def load_watchlist() -> list[dict]:
    """Read watchlist.json and return as a list. Returns empty list if file missing."""
    if not WATCHLIST_PATH.exists():
        return []
    try:
        return json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: could not read watchlist.json: {e}")
        sys.exit(1)


def save_watchlist(data: list[dict]) -> None:
    """Write the updated list back to watchlist.json with pretty formatting."""
    WATCHLIST_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_list(data: list[dict]) -> None:
    """Print all tickers grouped by sector."""
    if not data:
        print("Watchlist is empty.")
        return

    # Group by sector
    by_sector: dict[str, list[dict]] = {}
    for entry in data:
        sector = entry.get("sector", "UNKNOWN")
        by_sector.setdefault(sector, []).append(entry)

    print(f"Watchlist — {len(data)} tickers total")
    print()
    for sector in sorted(by_sector):
        entries = by_sector[sector]
        print(f"[{sector}] — {len(entries)} tickers")
        for e in entries:
            tags = ", ".join(e.get("tags", []))
            why = e.get("why_added", "")
            tags_str = f"  tags:[{tags}]" if tags else ""
            print(f"  {e['ticker']:<7} {e.get('name', ''):<25}{tags_str}  added:{e.get('date_added', '?')}  reason:{why}")
        print()


def validate_ticker(ticker: str) -> tuple[bool, float | None]:
    """Quick check that a ticker symbol exists via yfinance fast_info. Returns (valid, price)."""
    try:
        import yfinance as yf
        info = yf.Ticker(ticker).fast_info
        price = getattr(info, "last_price", None)
        if price and price > 0:
            return True, price
        return False, None
    except ImportError:
        # yfinance not installed — skip validation, proceed
        print(f"  [warn] yfinance not available — skipping ticker validation for {ticker}")
        return True, None
    except Exception:
        return False, None


def cmd_add(data: list[dict], ticker: str, name: str, sector: str,
            tags: list[str], reason: str) -> None:
    """Add a ticker to the watchlist after validating it exists."""
    ticker = ticker.upper()

    # Check if already present
    existing = [e for e in data if e["ticker"] == ticker]
    if existing:
        print(f"SKIP: {ticker} is already in watchlist (added {existing[0].get('date_added', '?')})")
        return

    # Validate ticker exists
    print(f"Validating {ticker}...", end=" ", flush=True)
    valid, price = validate_ticker(ticker)
    if not valid:
        print(f"\nERROR: Could not verify ticker '{ticker}' exists. Check the symbol and try again.")
        sys.exit(1)
    price_str = f"${price:,.2f}" if price else "price n/a"
    print(f"OK ({price_str})")

    entry = {
        "ticker": ticker,
        "name": name,
        "sector": sector,
        "tags": tags,
        "date_added": str(date.today()),
        "why_added": reason or "manually added",
    }
    data.append(entry)
    save_watchlist(data)
    print(f"ADDED: {ticker} ({name}) | sector:{sector} | tags:{tags} | reason:{reason}")


def cmd_remove(data: list[dict], ticker: str) -> None:
    """Remove a ticker from the watchlist by symbol."""
    ticker = ticker.upper()
    before = len(data)
    data[:] = [e for e in data if e["ticker"] != ticker]
    if len(data) == before:
        print(f"NOT FOUND: {ticker} is not in watchlist.")
        return
    save_watchlist(data)
    print(f"REMOVED: {ticker} from watchlist ({before - len(data)} entry removed)")


def cmd_auto_discover(data: list[dict]) -> None:
    """
    Suggest new tickers by running ETF discovery logic.
    Prints candidates only — does NOT auto-add. Human must approve.
    """
    import subprocess

    existing_tickers = {e["ticker"] for e in data}

    print("Running ETF discovery scan (this may take 30-60 seconds)...")
    etf_script = Path(__file__).parent / "etf-discovery.py"
    if not etf_script.exists():
        print("ERROR: etf-discovery.py not found in scripts/")
        return

    result = subprocess.run(
        [sys.executable, str(etf_script)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        print(f"[warn] etf-discovery.py exited with error:\n{result.stderr[:500]}")

    output = result.stdout
    print(output)

    # Extract suggested tickers from output (look for lines with [EARLY] or [ALERT])
    suggestions = []
    for line in output.splitlines():
        # Lines look like: "AAPL  Apple Inc   XLK [T1]  $123.45 ..."
        parts = line.split()
        if not parts:
            continue
        sym = parts[0]
        if not sym.isalpha() or len(sym) > 6:
            continue
        if "[EARLY" in line or "[ALERT" in line:
            already_in = sym in existing_tickers
            flag = " [ALREADY IN WATCHLIST]" if already_in else " [NEW - consider adding]"
            suggestions.append(f"  {sym}{flag}")

    if suggestions:
        print()
        print("--- Auto-discover suggestions ---")
        for s in suggestions:
            print(s)
        print()
        print("To add a suggestion: python scripts/watchlist-manager.py --add TICKER \"Name\" SECTOR")
        print("(Human approval required — this script does NOT auto-add)")


def main():
    parser = argparse.ArgumentParser(
        description="Manage scripts/watchlist.json — single source of truth for ticker universe"
    )
    parser.add_argument("--list", action="store_true", help="Print all tickers grouped by sector")
    parser.add_argument("--add", nargs=3, metavar=("TICKER", "NAME", "SECTOR"),
                        help="Add a ticker: --add IONQ 'IonQ' QTUM")
    parser.add_argument("--tags", type=str, default="",
                        help="Comma-separated tags for --add (e.g. quantum,AI)")
    parser.add_argument("--reason", type=str, default="",
                        help="Reason for adding (e.g. 'quantum thesis T1')")
    parser.add_argument("--remove", metavar="TICKER", help="Remove a ticker from watchlist")
    parser.add_argument("--auto-discover", action="store_true",
                        help="Suggest new tickers via ETF discovery (no auto-add)")
    args = parser.parse_args()

    data = load_watchlist()

    if args.list:
        cmd_list(data)

    elif args.add:
        ticker, name, sector = args.add
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
        cmd_add(data, ticker, name, sector, tags, args.reason)

    elif args.remove:
        cmd_remove(data, args.remove)

    elif args.auto_discover:
        cmd_auto_discover(data)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
