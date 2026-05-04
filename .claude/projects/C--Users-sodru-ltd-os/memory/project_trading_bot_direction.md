---
name: Trading bot direction — BTC-only bot, stock screener kept
description: Crypto bot scope narrowed to BTC/USDT only on Binance; all stock screener code preserved
type: project
---

User is building a BTC-only trading bot on Binance, alongside the existing stock screener (kept intact).

**Why:** BTC only — deeper liquidity, cleaner signals, simpler position management vs multi-coin universe. Stock screener kept for US equity workflow.

**How to apply:**
- Never delete or refactor screener.py, discovery.py, junk_filter.py, auto-buy.py, update-universe.py, dashboard stock tabs
- Crypto bot = additive — new scripts, BTC/USDT only, no ETH or altcoins
- Any research papers to find must be BTC-specific (BTC momentum, BTC regime detection, BTC volatility, BTC on-chain signals) — not generic crypto or multi-asset
- Planned stack: ccxt library, Binance, BTC/USDT only
