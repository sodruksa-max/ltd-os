"""
nick_weekly_auto.py — auto-generate Nick weekly rec using Gemini Flash (free).
Runs Friday 8:30 PM Thailand (1:30 PM UTC) via GitHub Actions.
Reads: Alpaca positions + KB files → Gemini → weekly-rec.md + ORDERS block.
"""

import os
import json
import re
from datetime import date
from pathlib import Path

import yfinance as yf
from alpaca.trading.client import TradingClient
from google import genai

REPO = Path(__file__).resolve().parents[3]
NICK_DIR = REPO / "vault/20_investment/nick"
KB_DIR = REPO / "vault/Knowledge"
WEEKLY_DIR = NICK_DIR / "weekly"
WEEKLY_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK_TICKERS = ["QQQM", "SOXX", "SPY"]


def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return f"[file not found: {path}]"


def get_pct_change(ticker: str, period="5d") -> float:
    try:
        hist = yf.Ticker(ticker).history(period=period)["Close"]
        return round((hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0] * 100, 2)
    except Exception:
        return 0.0


def build_holdings_block(client: TradingClient) -> tuple[str, float]:
    """Returns formatted holdings text + current NAV"""
    account = client.get_account()
    nav = round(float(account.portfolio_value), 2)
    positions = client.get_all_positions()

    lines = [f"Current NAV: ${nav:,.2f}\n", "Holdings:"]
    for p in positions:
        ticker = p.symbol
        qty = float(p.qty)
        avg_cost = float(p.avg_entry_price)
        current = float(p.current_price)
        pnl_pct = round((current - avg_cost) / avg_cost * 100, 2)
        mkt_val = round(qty * current, 2)
        weight = round(mkt_val / nav * 100, 1)
        lines.append(
            f"  {ticker}: {qty} shares | avg ${avg_cost:.2f} | now ${current:.2f} | "
            f"P&L {pnl_pct:+.1f}% | ${mkt_val:,.0f} ({weight}% NAV)"
        )

    lines.append("\nBenchmark (week):")
    for sym in BENCHMARK_TICKERS:
        chg = get_pct_change(sym)
        lines.append(f"  {sym}: {chg:+.2f}%")

    return "\n".join(lines), nav


def validate_orders_block(text: str) -> list:
    """Extract and validate ORDERS JSON from response. Returns list or empty."""
    m = re.search(r"## ORDERS.*?```json\s*\n(\[.*?\])\s*\n```", text, re.DOTALL)
    if not m:
        return []
    try:
        orders = json.loads(m.group(1))
        valid = []
        for o in orders:
            if o.get("action", "").upper() in ("BUY", "SELL", "TRIM", "NONE") and o.get("ticker"):
                valid.append(o)
        return valid
    except json.JSONDecodeError:
        return []


def build_prompt(holdings_block: str, nav: float) -> str:
    nick_soul = load_file(KB_DIR / "nick-soul.md")
    thesis_tracker = load_file(KB_DIR / "THESIS_TRACKER.md")
    index_insights = load_file(KB_DIR / "INDEX_insights.md")
    today = date.today()

    return f"""You are Nick — a blinded thesis portfolio manager. You only know:
1. Your KB (thesis tracker, insight atoms)
2. Current market prices
You do NOT know about real trades, paper bot positions, or the user's actual portfolio.

Read your soul and principles first:
<nick-soul>
{nick_soul}
</nick-soul>

<thesis-tracker>
{thesis_tracker}
</thesis-tracker>

<recent-insights>
{index_insights}
</recent-insights>

<current-holdings>
{holdings_block}
</current-holdings>

Today: {today} (Friday close)

Generate a complete Nick Weekly Review in EXACTLY this format:

# Nick Weekly — {today}

## NAV Update
| | This week | Since inception |
|---|---|---|
| Nick NAV | $X,XXX (+X.X%) | +X.X% |
| Blended benchmark (50% QQQM + 50% SOXX) | $XXX (+X.X%) | +X.X% |
| Delta | | +/- X.X% |

## Holdings Review

### <TICKER> — [Intact / Evolving / Invalidated]
- **Thesis:** ...
- **Kill condition:** ...
- **Status this week:** ...
- **Rec:** Hold / Add / Trim / Sell
- **Reason:** ...

(repeat for each holding)

## Earnings Watch (next 4 weeks)
- <TICKER>: <date> — what to watch

## Changes recommended
- [Buy / Sell / Trim / None]: ...
- Sizing: ...
- Reason: ...

## ORDERS (machine-readable — parsed by nick-execute.py)
```json
[
  {{"action": "BUY|SELL|TRIM|NONE", "ticker": "TICKER", "conviction": "high|med|low", "reason": "1-line reason"}}
]
```

## KB Gaps — Research requests
| Priority | Topic | Why needed | Suggested command |
|---|---|---|---|
| High/Med/Low | `<topic>` | `<what's missing>` | `/research-idea <topic>` |

## Nick's note
[1-2 sentences about thesis or decision quality — not about price action]

Rules:
- EARLY-only for new BUY entries (VIX < 20)
- No autonomous KB writes — only flag gaps
- Kill conditions with qualitative data → flag for human review, do not invalidate automatically
- Benchmark is 50% QQQM + 50% SOXX, not SPY
- ORDERS block must be valid JSON
"""


def main():
    alpaca_client = TradingClient(
        os.environ["ALPACA_API_KEY"], os.environ["ALPACA_SECRET_KEY"], paper=True
    )
    gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    print("Fetching holdings from Alpaca...")
    holdings_block, nav = build_holdings_block(alpaca_client)

    print("Building prompt...")
    prompt = build_prompt(holdings_block, nav)

    for model_id in ["gemini-2.0-flash", "gemini-2.0-flash-lite"]:
        try:
            print(f"Calling {model_id}...")
            response = gemini_client.models.generate_content(
                model=model_id, contents=prompt
            )
            print(f"Success with {model_id}")
            break
        except Exception as e:
            print(f"{model_id} failed: {e}")
            response = None

    if response is None:
        raise RuntimeError("All Gemini models failed — check API key quota")
    rec_text = response.text

    orders = validate_orders_block(rec_text)
    if not orders:
        print("WARNING: No valid ORDERS block found — appending empty block")
        rec_text += '\n\n## ORDERS (machine-readable — parsed by nick-execute.py)\n```json\n[]\n```\n'

    today = date.today()
    out_file = WEEKLY_DIR / f"{today}_weekly-rec.md"
    out_file.write_text(rec_text, encoding="utf-8")
    print(f"Saved: {out_file}")
    print(f"Orders found: {len(orders)}")
    for o in orders:
        print(f"  {o.get('action')} {o.get('ticker')} ({o.get('conviction')}) — {o.get('reason')}")


if __name__ == "__main__":
    main()
