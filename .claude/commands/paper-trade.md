---
description: Place a paper trade via Alpaca paper trading account — real order simulation, auto-tracked by /eod
---

# /paper-trade

Place a paper trade order through Alpaca's paper trading account. Auto-tracked — no manual log needed.

## Prerequisites

Paper account must have balance > $0. If $0, fund it first:
1. Go to alpaca.markets → login
2. Switch to "Paper Trading" mode (top-right)
3. Click "Reset Account" → set balance (e.g. $100,000)
4. Come back and run `/paper-trade`

Check status: `code/python/.venv/Scripts/python scripts/alpaca-paper.py account`

## Usage

```
/paper-trade TICKER DIRECTION SHARES [at PRICE]
```

Examples:
- `/paper-trade NVDA long 5` — buy 5 NVDA at market
- `/paper-trade NVDA long 5 at 900` — buy 5 NVDA limit $900
- `/paper-trade SPY short 3` — short 3 SPY at market

## Steps

### 1. Parse intent

Extract from user input:
- `ticker` — stock symbol (uppercase)
- `direction` — long (buy) / short (sell short)
- `shares` — number of shares
- `price` — optional limit price (if user said "at $X" or "limit $X")
- `stop` — optional stop price (if user said "stop $X")

### 2. Show preview + ask for stop/target

Before placing:

```
Paper trade preview:
  TICKER   : NVDA
  Direction: Long (BUY)
  Shares   : 5
  Order    : Market [or Limit @ $900]

  Risk parameters (optional but recommended):
  Stop loss target  : $? (type a price or skip)
  Profit target     : $? (type a price or skip)
```

If user provides stop/target, calculate and show:
- Risk per share = |entry approx - stop|
- R-multiple at target = (target - entry) / risk_per_share
- If R < 1.5 → warn: "R:R ต่ำกว่า 1.5 — ยืนยันไหม?"

Ask: "ยืนยันส่ง order? (y/n)"

### 3. Place order

**Buy (long):**
```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py buy TICKER SHARES [--limit PRICE] [--stop STOP]
```

**Sell/Short:**
```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py sell TICKER SHARES [--limit PRICE]
```

Print the output — show Order ID and Status.

### 4. Report

```
Order placed: BUY 5 x NVDA [market]
Order ID: xxxxxxxx
Status: pending_new / filled

Run /eod to see current position and P&L.
```

If order fails → show error and suggest:
- Check account balance: `scripts/alpaca-paper.py account`
- Check market hours (orders queue if market closed, fill at open)

## Other useful commands

Show current paper positions and P&L:
```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py positions
```

Show recent orders:
```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py orders
```

Show account summary:
```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py account
```

Cancel an order:
```bash
code/python/.venv/Scripts/python scripts/alpaca-paper.py cancel ORDER_ID
```

## Closing a paper position

```
/paper-trade close NVDA 5
```

→ runs: `scripts/alpaca-paper.py sell NVDA 5`

Alpaca auto-records the fill price and closes the position.
Run `/eod` to confirm position is gone.

## Notes

- Orders placed after market hours queue and fill at next open
- Market orders during extended hours may not fill — use limit orders
- Paper fills use last trade price, not necessarily bid/ask — slight slippage difference from real
- `/eod` shows paper positions from Alpaca automatically (no manual log needed)
