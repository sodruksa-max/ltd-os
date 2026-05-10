"""
nick_weekly_auto.py — auto-generate Nick weekly rec using Groq (free).
Runs Friday 8:30 PM Thailand (1:30 PM UTC) via GitHub Actions.
Reads: Alpaca positions + KB files → Groq → weekly-rec.md + ORDERS block.
"""

import os
import json
import re
from datetime import date
from pathlib import Path

import yfinance as yf
from alpaca.trading.client import TradingClient
from groq import Groq

REPO = Path(__file__).resolve().parents[3]
NICK_DIR = REPO / "vault/20_investment/nick"
KB_DIR = REPO / "vault/Knowledge"
WEEKLY_DIR = NICK_DIR / "weekly"
NAV_LOG = NICK_DIR / "performance/nav_log.md"
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
    m = re.search(r"## ORDERS.*?```json\s*\n(\[.*?\])\s*\n```", text, re.DOTALL)
    if not m:
        return []
    try:
        orders = json.loads(m.group(1))
        return [o for o in orders if o.get("action", "").upper() in ("BUY", "SELL", "TRIM", "NONE") and o.get("ticker")]
    except json.JSONDecodeError:
        return []


def load_insight_atoms() -> str:
    atoms_dir = KB_DIR / "insight-atoms"
    parts = []
    for f in sorted(atoms_dir.glob("*.md")):
        if f.name == "README.md":
            continue
        parts.append(f.read_text(encoding="utf-8"))
    return "\n\n---\n\n".join(parts)


def build_prompt(holdings_block: str, nav: float) -> str:
    nick_soul = load_file(KB_DIR / "nick-soul.md")
    thesis_tracker = load_file(KB_DIR / "THESIS_TRACKER.md")
    insight_atoms = load_insight_atoms()
    today = date.today()

    return f"""You are Nick — a blinded thesis portfolio manager. You only know:
1. Your KB (thesis tracker, insight atoms with full evidence and kill conditions)
2. Current market prices
You do NOT know about real trades, paper bot positions, or the user's actual portfolio.

Read your soul and principles first:
<nick-soul>
{nick_soul}
</nick-soul>

<thesis-tracker>
{thesis_tracker}
</thesis-tracker>

<insight-atoms>
{insight_atoms}
</insight-atoms>

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
- **If portfolio is empty:** this is a new portfolio — recommend initial seed BUY orders for highest-conviction tickers from each active thesis. Size each position at 10-20% NAV. Do NOT leave ORDERS empty just because portfolio is empty.
"""


def log_weekly_nav(nav: float):
    row = f"| {date.today()} | ${nav:,.2f} | - | - | weekly snapshot (Friday close) |\n"
    with open(NAV_LOG, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    alpaca_client = TradingClient(
        os.environ["ALPACA_API_KEY"], os.environ["ALPACA_SECRET_KEY"], paper=True
    )
    groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

    print("Fetching holdings from Alpaca...")
    holdings_block, nav = build_holdings_block(alpaca_client)

    log_weekly_nav(nav)
    print(f"NAV snapshot logged: ${nav:,.2f}")

    print("Building prompt...")
    prompt = build_prompt(holdings_block, nav)

    print("Calling Groq llama-3.3-70b...")
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
        )
        rec_text = response.choices[0].message.content
        usage = response.usage
        print(f"Success — {usage.prompt_tokens} in / {usage.completion_tokens} out tokens")
    except Exception as e:
        raise RuntimeError(f"Groq API failed: {e}")

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
