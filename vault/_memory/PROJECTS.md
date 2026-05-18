---
type: memory-index
updated: 2026-05-19
---

# Active Projects

## Complete

### Unified Watchlist + Nick v3 Elevation
- **Status**: complete — 2026-05-19
- **Goal**: watchlist.json เป็น single source of truth ของทั้ง system — ทุก script/command อ่านจากที่เดียว ไม่ต้องแตะโค้ดเมื่อเพิ่ม/ลบหุ้น
- **Completed items:**
  1. `scripts/watchlist.json` (41 tickers) — single source of truth
  2. `scripts/watchlist-manager.py` — `--list`, `--add`, `--remove`, `--auto-discover`
  3. `scripts/universe-screen.py` — reads watchlist.json at runtime (fallback list kept)
  4. `scripts/catalyst-calendar.py` — reads watchlist.json at runtime
  5. `.claude/commands/pre-market.md` — sr-levels args built dynamically from watchlist.json
  6. `scripts/trade-log.json` — empty log initialized
  7. **Nick Tier3 wildcards** — `universe.py` `load_tier3_from_watchlist()` + `daily_scan.py` Monday scan
  8. **Nick Kill Monitor** — `scripts/nick-kill-monitor.py` + `.github/workflows/nick-kill-check.yml` (9 AM ET daily)
  9. **auto-trader.py deleted** — conflict with Nick on same Alpaca account eliminated
- **Notes**: auto-trader.yml + auto-trader.py removed; Nick v3 daily_scan.py replaces function

## Active

### LTD-OS
- **Status**: active
- **Last touch**: 2026-05-03
- **Goal**: Personal knowledge base + trading workflow OS (Claude Code + Obsidian + Alpaca)
- **Next**: paper trade smoke test → validate eod-report + stats pipeline end-to-end
- **Notes**: this repo

### Trading Experiment
- **Status**: active (paper trading phase)
- **Last touch**: 2026-05-03
- **Goal**: Learn US stock trading — paper trade 6 months, then real money if win rate ≥40% + R-multiple ≥1.5
- **Next**: log first paper trades → run /eod to test pipeline → run /weekly-calibration after 2 weeks
- **Notes**: [[vault/20_investment/_journal/]]

### Nick v3 — Blinded Paper Portfolio
- **Status**: active — live since 2026-05-18
- **Goal**: Beat SPY rolling multi-year; $2,320 starting capital on Alpaca paper; target grow to $10K–$100K
- **Architecture**: daily_scan.py (entry logic + profit ladder + ratchet stop + ATR sizing + VIX-Rank scaling) + nick-daily.sh wrapper + nick-score.py feedback loop + nick-signals-update.py (RSI/MA20/RS tiers)
- **Tier system**: Tier1 (37 core tickers, daily) | Tier2 (30 growth, Monday) | Tier3 wildcards (watchlist.json residual, Monday)
- **Kill monitor**: nick-kill-monitor.py + .github/workflows/nick-kill-check.yml — alerts on BREACH at 9 AM ET daily
- **Current holdings**: IONQ 4sh (medium conv, thesis-aligned); remaining cash ~$2,200 for NVDA post-earnings
- **Performance tracking**: vault/20_investment/nick/performance/nav_log.md (exact NAV vs SPY)
- **Last touch**: 2026-05-19
- **Next**: /nick-weekly after NVDA earnings (May 20) — check NVDA kill conditions with actual Q1 FY2027 results (EPS >$1.77, Rev >$78.8B, DC >$73B, Q2 guide >$86B)

### Token Efficiency Project
- **Status**: complete (2026-05-18)
- **Goal**: Audit + reduce token waste across all commands to extend session budget
- **Result**: ~50,500 tok/heavy session reduction — pre-market, nick-weekly, post-market, stock-content
- **Decisions logged**: see Decisions → Token audit section above
- **Last touch**: 2026-05-18
