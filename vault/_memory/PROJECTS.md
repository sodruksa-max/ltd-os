---
type: memory-index
updated: 2026-05-18
---

# Active Projects

## Active

### Full-Auto Paper Trading Bot + Unified Watchlist
- **Status**: planned — build week of 2026-05-12
- **Goal**: watchlist.json เป็น single source of truth ของทั้ง system — auto-managed, ทุก script/command อ่านจากที่เดียว ไม่ต้องแตะโค้ดเมื่อเพิ่ม/ลบหุ้น
- **Architecture** (ดู outline ใน chat 2026-05-07):
  1. `scripts/watchlist.json` — single source of truth: ticker, name, sector, tags, date_added, why_added
  2. `scripts/watchlist-manager.py` — auto-add (ETF scanner + RS > SPY + volume) / auto-remove (extended >20d หรือ volume หาย) รันทุกเช้า
  3. `scripts/universe-screen.py` — อ่าน watchlist.json แทน hardcoded UNIVERSE
  4. `scripts/sr-levels.py` — รับ args จาก watchlist.json แทน hardcoded list ใน pre-market.md
  5. `scripts/etf-discovery.py` — feed discoveries → watchlist-manager พิจารณา auto-add
  6. `scripts/catalyst-calendar.py` — filter เฉพาะ ticker ใน watchlist.json
  7. `scripts/auto-trader.py` — screen watchlist → rank → Alpaca paper order top 3
  8. `.claude/commands/pre-market.md` — build sr-levels args จาก watchlist.json อัตโนมัติ
  9. `scripts/trade-log.json` + `scripts/trade-logger.py` — บันทึกทุก order: ticker, date, entry price, size, signal tier, reason → append ทุกครั้งที่ auto-trader place order
  10. `.github/workflows/auto-trader.yml` — GitHub Actions schedule (`cron: '0 13 * * 1-5'` = 9:00 AM ET, วันจันทร์-ศุกร์): watchlist-manager → universe-screen → auto-trader → trade-logger → commit trade-log.json + watchlist.json กลับ repo อัตโนมัติ
- **Trade data feeds into**: /eod (open positions + P&L), /weekly-calibration (win rate, R-multiple patterns), future backtest
- **Trade log schema**: ticker | date | entry_price | shares | signal_tier | reason | exit_price | exit_date | pnl | r_multiple | status (open/closed)
- **Integration**: /eod, /screen, /bot ทุก command อ่าน watchlist.json + trade-log.json
- **Constraints**: paper trading เท่านั้น, Alpaca paper account, ไม่ใช้เงินจริง
- **Next**: เริ่ม build สัปดาห์หน้า — ลำดับ: watchlist.json → watchlist-manager.py → แก้ universe-screen → sr-levels dynamic → auto-trader → trade-logger → cron

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
- **Architecture**: daily_scan.py (entry logic + profit ladder + ratchet stop + ATR sizing) + nick-daily.sh wrapper + nick-score.py feedback loop + nick-signals-update.py (RSI/MA20/RS tiers)
- **Current holdings**: IONQ 4sh (medium conv, thesis-aligned); remaining cash ~$2,200 for NVDA post-earnings
- **Performance tracking**: vault/20_investment/nick/performance/nav_log.md (exact NAV vs SPY)
- **Last touch**: 2026-05-18
- **Next**: /nick-weekly after next trading day — verify kill conditions + check NVDA entry signal

### Token Efficiency Project
- **Status**: complete (2026-05-18)
- **Goal**: Audit + reduce token waste across all commands to extend session budget
- **Result**: ~50,500 tok/heavy session reduction — pre-market, nick-weekly, post-market, stock-content
- **Decisions logged**: see Decisions → Token audit section above
- **Last touch**: 2026-05-18
