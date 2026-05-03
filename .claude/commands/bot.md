---
description: Auto-trading bot — screens watchlist by momentum, places Alpaca paper orders for top picks
---

# /bot

Run the auto-trading pipeline: screen → rank → buy top picks on Alpaca paper account.

## Prerequisites

1. Paper account must have balance > $0:
   `code/python/.venv/Scripts/python scripts/alpaca-paper.py account`
   → If $0: go to alpaca.markets → Paper Trading → Reset Account

2. Watchlist at `config/watchlist.txt` — edit to add/remove tickers

## Usage

```
/bot                  # screen + buy (live paper orders)
/bot --dry-run        # show what WOULD be bought, no orders
/bot --top 3          # consider top 3 screener picks (default: 2)
/bot --size 0.03      # 3% of portfolio per position (default: 5%)
```

## Steps

### 1. Check account state

```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py account
code/python/.venv/Scripts/python scripts/alpaca-paper.py positions
```

Show to user: portfolio value, buying power, open positions count.
If already at 4 positions → skip buy step, just show screener.

### 2. Run screener

```bash
code/python/.venv/Scripts/python scripts/screener.py
```

Show full screener table to user. Explain the top 2-3 picks briefly:
- Why AMD scored high (RS, volume, MA)
- Any notable flags (below MA50 = skip, low volume = weak signal)

Ask user: "ยืนยันให้ bot ซื้อ top picks ไหม? (y/n/dry-run)"

### 3. Run auto-buy

**If user confirms (y):**
```bash
code/python/.venv/Scripts/python scripts/auto-buy.py
```

**If user wants dry-run first:**
```bash
code/python/.venv/Scripts/python scripts/auto-buy.py --dry-run
```
Then ask again to confirm live run.

**Custom top N or size:**
```bash
code/python/.venv/Scripts/python scripts/auto-buy.py --top 3 --size 0.03
```

### 4. Confirm result

```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py positions
```

Show updated positions. Report:
```
Bot run complete:
  Orders placed: N
  New positions: [TICKER, TICKER]
  Run /eod for full P&L view.
```

## Rules applied by auto-buy.py

| Rule | Value | Source |
|---|---|---|
| Max positions | 4 | PREFERENCES.md |
| Position size | 5% of portfolio | PREFERENCES.md |
| Skip if already held | yes | — |
| Skip if below MA50 | yes | trend filter |
| Skip if buying power insufficient | yes | — |
| Order type | Market (DAY) | fills at next tick |

## Watchlist management

Edit `config/watchlist.txt` to customize the universe:
- Add tickers: one per line
- Remove: delete the line
- Comment out: prefix with `#`
- Screener evaluates all non-commented tickers each run

## Scheduling (advanced)

To run bot automatically every day before market open:
→ Use `/schedule` to set up a cron job

Example: run at 8:30am ET (21:30 Thailand time) on weekdays:
```
/schedule "run /bot --dry-run at 21:30 every weekday"
```

## What this is NOT

- Not a live trading bot (Alpaca paper = simulation only)
- Not financial advice
- Screener uses price momentum only — no fundamental analysis
- Always review screener output before running live (even in paper)
