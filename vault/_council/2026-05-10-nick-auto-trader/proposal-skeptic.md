---
council_topic: Nick Auto-Trader + Self-Improvement System
proposer: skeptic
date: 2026-05-10
---

# Skeptic Proposal: Freeze the Self-Improvement Loop Until You Have 50+ Trades

## TL;DR
Build the execution and logging layer first. Keep the self-improvement loop locked behind human approval until Nick has at least 50 closed trades — otherwise you are teaching a system on statistically meaningless data.

## Approach
- Phase 1 (now–month 2): Nick executes paper trades automatically and logs full context (thesis tier, screen tier, macro), but NEVER writes to KB autonomously
- Phase 2 (month 3+, 50+ closed trades): Nick proposes conviction score changes as a markdown diff; user approves before any merge
- Phase 3 (month 6+, 100+ trades, documented edge): unlock autonomous updates with hard guardrails — change cap per cycle, rollback on demand
- Kill switch: one config flag disables all autonomous vault writes at any time
- Position sizing: equal-weight until edge is demonstrated, not conviction-weighted from day one

## Pre-mortem: how this fails

1. **Self-improvement corrupts KB on noise (highest probability).** With 4 theses and weeks-long holds, Nick closes 8–12 trades in the first 3 months. Updating conviction scores from 8 data points is overfit by definition. Nick "learns" that RKLB underperforms in May 2026 and permanently downgrades T3 Space — then misses the next ASTS breakout because the downgraded score stuck in THESIS_TRACKER and was never questioned.

2. **Thesis signal and price signal fight; bot acts on price signal and calls it thesis discipline.** The brief asks: thesis=active but tier=EXTENDED — what does Nick do? If code defaults to "skip EXTENDED," Nick becomes a momentum follower with thesis labels bolted on. The thesis framing becomes cosmetic; you have a tier-chasing bot that sounds more principled than it is.

3. **Kill conditions requiring qualitative text cannot be detected, so Nick holds through thesis death.** "Hyperscaler capex guidance below prior year" requires earnings call parsing. Nick cannot automate this. The result: Nick holds T1 AI Capex positions through a genuine thesis break not because it assessed risk, but because the kill signal never arrived in machine-readable form. Automated systems create false confidence that kill conditions are being watched when they are not.

4. **Thin trade count masks whether edge is real or lucky.** 40% win rate over 20 trades is a coin flip range. If the system logs "win rate 43%" after 20 trades and the user takes that as confirmation to move toward real money, the sample size is the bug, not the strategy.

## Hidden costs
- Debugging a single autonomous trade requires forensic logs (thesis state at entry, tier, macro flag) — building that logging layer correctly takes longer than the trading logic itself
- KB corruption is not visible: a degraded conviction score looks identical to a legitimate one inside THESIS_TRACKER until someone manually audits
- Every autonomous KB update Nick proposes requires a human review session — the time cost of reviewing bad proposals may exceed the time saved by automation

## Survivorship bias check
Most retail algo systems that "self-improve" fail quietly, not dramatically. NAV drifts below benchmark slowly. No single catastrophic trade — just gradual erosion while the system keeps logging, looks functional, and generates plausible-sounding reports. The ones that worked had either very high trade frequency (enough data fast) or very tight domain scope. Nick has neither: thesis-based holds are slow, and the universe is 4 theses.

## Worst case (5th percentile)
Nick runs 6 months autonomously. The self-improvement loop degrades T1 and T2 conviction scores during a sector-wide momentum drawdown that was temporary. User enters real money phase with a Nick that has systematically penalized the highest-conviction theses right before the next AI capex cycle confirms the original thesis. Real money goes in; the rebound is missed because KB says T1 is medium-conviction now.

## Conservative alternative
Log everything. Execute paper trades automatically. Surface KB change proposals monthly as a human-readable summary — "Nick suggests lowering T3 Space conviction from 8 to 6 because 3 of 4 T3 positions closed at a loss this month." User reads, decides, approves or rejects. Call this "Nick Observed." It generates identical learning value with zero KB corruption risk and costs 15 minutes of human review per month.

## Stop conditions
Define these before writing a single line of code:
- Nick's paper NAV underperforms SPY by more than 15% over any rolling 60-day window → pause all autonomous trades, human reviews before restart
- Any proposed conviction score change exceeds 20 points in a single cycle → auto-rejected, flagged for review, never merged silently
- Any position held more than 30 days with no thesis-level justification logged → force-close, log as "thesis drift," flag for audit
- If Nick proposes the same conviction score change and it gets rejected twice → that update is frozen until a new data threshold is met

## What's NOT a good reason to do this
- "It's paper money so mistakes don't matter" — KB corruption is not paper money; it propagates into real decisions when the system is trusted
- "The self-improvement loop is the interesting part" — it is also the part most likely to silently degrade quality while appearing functional
- "Autonomous AI agents are clearly the direction things are going" — FOMO on the architecture is not a thesis; 8 closed trades is not a dataset
