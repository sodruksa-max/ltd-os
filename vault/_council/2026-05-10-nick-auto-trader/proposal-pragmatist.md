---
council_topic: Nick Auto-Trader + Self-Improvement System
proposer: pragmatist
date: 2026-05-10
---

# Pragmatist Proposal: Minimal-Footprint Thesis Executor with Human-Gated Learning

## TL;DR
Build Nick as a daily batch executor — screen, rank, order, log — with zero automated KB modification. Self-improvement happens on a human-approved monthly cadence, not autonomously, because trade sample size will be too small for any automated update to be statistically meaningful for 4-6 months minimum.

## Approach
- **Daily batch** (`auto-trader.py`): runs 9:00 AM ET via GitHub Actions cron — reads `watchlist.json`, runs universe-screen tier logic, selects top 1-2 EARLY/ALERT tickers whose thesis is active in THESIS_TRACKER, places Alpaca paper orders, appends full context to `trade-log.json` (tier, thesis ID, RS vs SPY, sector ETF momentum at entry).
- **Conflict resolution** (thesis active but EXTENDED): Nick does not enter. Hold existing positions. Queue for re-entry on pullback to ALERT. This prevents momentum-chasing disguised as thesis investing — the single biggest integrity drift risk.
- **Exit logic** (fixed, not adaptive): hard stop at -25% from entry; take 50% off at +50%; trail remainder with 15% ATR stop. Matches already-approved PREFERENCES rules — no new logic to invent.
- **Kill condition monitoring** (human-gated): auto-trader checks price signals only. Qualitative kill conditions (earnings guidance, capex revisions) trigger a `[FLAG: kill-condition-check-needed]` comment in trade-log — user reviews next session, no automated KB edit.
- **Monthly calibration** (human-approved): after 30+ closed trades, Claude surfaces win rate, R-multiple, and tier-hit-rate breakdown, proposes conviction score changes to THESIS_TRACKER, user approves before any write.

## Base rate evidence
- ~90% of retail algo systems fail to beat buy-and-hold in year 1. The failure mode is almost always overfit parameters updated too frequently on too-few trades.
- Thesis-driven momentum strategies (hold weeks) have documented Sharpe > 0.5 in academic literature — but only when holding period matches the signal frequency. Daily screening against weekly-thesis logic is the correct pairing.
- Minimum trade count before a parameter update has statistical validity: 30-50 out-of-sample closed trades. At 1-2 trades/week (thesis cadence), that is 4-6 months minimum before any self-update is meaningful.

## Realistic outcome (50th percentile)
By month 6: ~40-60 closed paper trades. Win rate 35-45%, R-multiple 1.3-1.8 — likely below the 40%/1.5 threshold to go live. The correct expectation at this stage. The value at month 6 is not P&L; it is a clean trade log that makes the first real calibration statistically honest.

## Time to first feedback
- Week 2: first 2-4 closed trades confirm pipeline works (not strategy signal)
- Month 3: first pattern on which tiers generate positive R
- Month 6: first statistically defensible calibration round

## Required skills/resources
- Alpaca paper account (active)
- GitHub Actions free tier (handles weekday cron)
- `auto-trader.py` built by Claude as executor — user does not touch code
- `trade-log.json` reviewed by user weekly via `/eod`

## Comparison: alternatives I rejected

**Full autonomy with auto-KB updates**: With 1-2 trades/week, the system would update conviction scores on 8-10 observations — statistically meaningless and KB-corrupting.

**Intraday signals / tighter stops**: Nick is a thesis portfolio, not a momentum scalper. Matching signal frequency to holding period is the single biggest determinant of thesis-bot integrity. Acting on hourly signals inside a thesis with a 3-month horizon destroys the edge.

**All 4 theses simultaneously at equal weight**: at 5% risk/trade and $10K NAV, 4 concurrent positions = 20% NAV at risk. Above the spirit of the ≤5% rule. 1-2 positions at a time concentrates on highest-conviction tier and keeps the learning signal clean.

## Open questions for user
- If a thesis tier degrades from active to watch mid-hold, does Nick exit immediately or hold until stop/target triggers?
- Is 5% risk-per-trade calculated on paper NAV ($10K → $500/trade) or on the 100K experiment fund ($5,000/trade)? This changes position size 10x and matters for comparing paper results to future live sizing.
- Should `trade-log.json` commit daily (full history) or only on exit events (cleaner log, less noise in git)?
