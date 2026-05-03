---
description: Run momentum/reversal screener on watchlist
---

# /screen

Run the stock screener on the watchlist and show results.

## Usage

```
/screen              # momentum mode (default)
/screen --reversal   # beginning-of-trend mode (filters overextended)
/screen --top 5      # top 5 only
/screen NVDA AAPL    # specific tickers
```

## Steps

Run the screener and print results:

```bash
code/python/.venv/Scripts/python scripts/screener.py [ARGS]
```

Pass any args the user gave after `/screen` directly to the script.

Show the full output to the user. No commentary needed unless user asks.
