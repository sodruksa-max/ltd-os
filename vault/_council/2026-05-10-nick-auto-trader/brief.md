---
council_topic: Nick Auto-Trader + Self-Improvement System
expertise_lens: financial_risk
date: 2026-05-10
---

# Brief: Nick Auto-Trader

## Who is Nick
Nick is a blinded thesis-driven paper portfolio manager — reads only KB (THESIS_TRACKER, INDEX_insights), not real portfolio or BTC bot positions. $10K paper NAV seeded 2026-05-10. Benchmark: SPY. Universe: T1-T4 theses.

## Current state
- Nick makes decisions manually via /nick-weekly + /nick-quarterly
- 4 active theses: T1 AI Capex (NVDA/AMD/AVGO/SMCI/DELL/HPE/MU), T2 Semicon Moats (NVDA/ASML/ARM/AMD), T3 Space (RKLB/ASTS/LUNR/KTOS), T4 AI Software (PLTR/CRM/SNOW)
- Technical signals exist: universe-screen.py (EARLY/ALERT/EXTENDED/WATCH tiers, RS vs SPY, vol-div, sector ETF momentum)
- Paper trading infra: Alpaca paper account active
- Self-improvement infra: none yet

## The ask
Build Nick into an autonomous system that:
1. Trades Alpaca paper automatically (entry + exit without human trigger)
2. Logs every trade with full context (thesis state, screen tier, macro at entry)
3. Analyzes outcomes → updates its own conviction scores → improves entry/exit rules over time

## User context
- นักศึกษา ปี 1 logistics, ว่างจันทร์-ศุกร์
- 100K trading experiment fund (separate from QQQM DCA)
- Currently in paper trading phase 1-6 months → real money only if win rate ≥40% + R-multiple ≥1.5
- Risk per trade: ≤5% of capital
- Hard rules: no leverage, no averaging down, no revenge trading

## Stakes
- Paper money only → mistakes are learning, not catastrophe
- BUT self-improvement loop touching KB directly = risk of corrupting thesis quality scores with noise from too few trades
- Design quality here affects whether Nick generates real alpha or just noise that looks like signal

## Key tensions to resolve
1. **Frequency vs noise**: thesis-based portfolio = hold weeks not hours; running daily is fine but acting too often = momentum bot disguised as thesis bot
2. **Self-improvement safety**: when is N trades enough to update conviction? too few = overfit, too many = slow to learn
3. **Kill condition detection**: some kill conditions (e.g., "hyperscaler capex guidance below prior year") require earnings call data, not just price signals — can't automate cleanly
4. **Nick's blinding**: Nick should know HIS OWN positions but not other paper trades or real portfolio

## Open questions
- Should self-improvement update THESIS_TRACKER directly, or propose changes for user approval?
- How to handle kill conditions that need qualitative data (earnings calls)?
- If thesis and technical signal conflict (thesis=active but EXTENDED) → what does Nick do?
- Position sizing: equal weight vs conviction-weighted?
