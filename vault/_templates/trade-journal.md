---
type: trade-journal
action: # buy | sell | adjust | close
ticker: 
date: {{date}}
price: 
size_pct_of_port: 
thesis_ref: # [[20_investment/<ticker>-YYYY-MM-DD]]
tags: [trade-journal]
outcome: open # open | win | loss | breakeven
---

# {{action}} {{ticker}} — {{date}}

## What I did
- **Action**: <buy/sell/adjust>
- **Ticker**: 
- **Price**: $
- **Size**: % of portfolio
- **Total $**: $

## Why I did it (at this moment)
(paste thesis summary — don't link, capture state at time of trade)

### Thesis in 2 sentences


### Expected timeframe


### What I think the market is missing


## Position sizing (quant checks)
- **ATR14**: $ (from sr-levels.py output)
- **ATR stop (2×ATR)**: Long stop $___  / Short stop $___
- **VIX-Rank**: ___th percentile → size multiplier: ___x
- **Signal type**: <momentum / value / mean-reversion>
- **Momentum decay check**: entry date ____ → re-evaluate by ____ (momentum: +7 days; value: +30 days)
- **Is this entry planned or FOMO?**: <planned / FOMO — if FOMO, reduce size 50%>

## Risk management
- **Stop plan**: ATR-based: $___  OR  thesis-break: <condition>
- **Max loss acceptable**: $ / %
- **Exit triggers**:
  - [ ] ATR stop hit: $
  - [ ] Thesis breaks (specific event): 
  - [ ] Price target hit: $
  - [ ] Momentum re-evaluate date: (max 7 days for momentum trades)
  - [ ] Time-based: if nothing in X months, reassess

## Counter-arguments I'm aware of
(the strongest bear case — acknowledge before trade)
- 
- 
- 

## Emotional state
- Conviction (1-10): 
- FOMO level: <none/low/med/high>
- Sizing consistent with conviction? <yes/no + reason>

---

## Post-mortem (fill after exit)

### Outcome
- Exit date: 
- Exit price: $
- P&L: $ / %
- Days held: 

### What was right
- 

### What was wrong
- 

### What I'd do differently
- 

### Lesson
(1 sentence that belongs in PREFERENCES.md or _memory/DECISIONS.md if it's a principle)
- 
