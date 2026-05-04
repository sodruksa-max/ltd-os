---
created: 2026-05-04 (afternoon/evening)
context_usage: ~90%
session_duration: ~4 hours (continued from previous)
---

# Session Handoff

## What I was doing
BTC-only trading bot — Phase 1 implementation เสร็จครบทุก module

## Current state
- **Active plan**: none — Phase 1 complete
- **Uncommitted changes**: yes — btc_bot/ ทุกไฟล์ใหม่ยังไม่ได้ commit
- **Tests status**: ทุก module รัน --once ผ่าน live Binance data ✅

## Files created this session (all uncommitted)

### BTC Bot — code/python/btc_bot/
- `data.py` — fetch OHLCV + price จาก Binance via ccxt (no key needed)
- `signals.py` — VP-MACD (arXiv 2604.26063) + MA 20/100 + 1h momentum
- `regime.py` — HMM 3-state Bull/Neutral/Bear (hmmlearn, Preprints 2026)
- `sizer.py` — Tri-Power Variation + GARCH(1,1) vol-targeted position sizing
- `risk.py` — max 30% NAV, stop-loss -3% NAV, drawdown halt -15%
- `executor.py` — market_buy/sell via ccxt (dry_run=True default)
- `main.py` — 1h loop orchestrator (`python -m btc_bot.main --once`)

### Research vault
- `vault/10_research/papers/btc-bot-papers-survey.md` — 10 BTC papers Tier 1/2/3

### Memory
- `.claude/projects/.../memory/project_trading_bot_direction.md` — BTC-only scope

## Latest live output (2026-05-04 ~15:37 UTC)
```
BTC/USDT   : $79,578
Signal     : HOLD (no VP-MACD crossover)
Regime     : NEUTRAL (HMM)
Vol fcast  : 38.3%
Action     : HOLD
```

## Decisions made (don't re-litigate)
- **BTC/USDT only** — no ETH, no altcoins
- **ccxt Binance public** for market data, API keys needed only for live orders
- **HMM regime** uses daily log return + 5d realized vol (hmmlearn GaussianHMM)
- **TPV + GARCH blend** (50/50 weight) for vol forecast
- **dry_run=True default** — live orders need BINANCE_API_KEY + BINANCE_SECRET_KEY
- **State in-memory** — no DB yet (restart loses position state) → Phase 4 fix
- **Run as module**: `python -m btc_bot.main --once` (not `python btc_bot/main.py`)

## Installed packages (this session)
- `hmmlearn` — for regime.py
- `arch` — for GARCH in sizer.py

## Phase roadmap

### Phase 1 ✅ DONE
VP-MACD signals + HMM regime + RGARCH sizer + risk guardrails + executor + main loop

### Phase 2 — Walk-forward optimization
- quarterly re-optimize VP-MACD params (arXiv 2602.10785)
- backtest framework needed

### Phase 3 — On-chain filters (free APIs available)
- **Fear & Greed Index** (alternative.me) — free, no key, block longs when < 25
- **Funding rate** (Coinglass free tier) — reduce size when overleveraged
- user asked "มีแยยฟรีไหม" — answered yes (alternative.me + Coinglass)
- user said พักก่อน (session ending)

### Phase 4 — Production hardening (needed before go-live)
- State persistence (JSON file so restart doesn't lose position)
- Alert (Line/Telegram when trade fires)
- Scheduler (Windows Task Scheduler or cron instead of time.sleep)

## Open questions
- Binance API keys — ยังไม่ได้ใส่ใน `.secrets/.env` (ต้องมีก่อน go-live)
- Phase 3 หรือ Phase 4 ก่อน? — user พักก่อน ยังไม่ตัดสินใจ
- Walk-forward backtest: ยังไม่ได้ implement เลย

## Next steps (suggested order)
1. Commit ทุก btc_bot/ files ก่อน
2. Phase 4: state persistence (save/load JSON) — สำคัญสุดก่อน go-live
3. Phase 3: onchain.py (Fear & Greed + Funding rate)
4. เพิ่ม Binance API keys ใน .secrets/.env แล้วทดสอบ --live

## Files to read first next session
1. `code/python/btc_bot/main.py` — ดู pipeline flow
2. `code/python/btc_bot/risk.py` — guardrail rules
3. `vault/10_research/papers/btc-bot-papers-survey.md` — phase roadmap
