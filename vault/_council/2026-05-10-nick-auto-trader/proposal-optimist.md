---
council_topic: Nick Auto-Trader + Self-Improvement System
proposer: optimist
date: 2026-05-10
---

# Optimist Proposal: Thesis-Gated Autonomous Trader with Staged Self-Improvement

## TL;DR
Build Nick as a layered system where thesis state gates every action — technical signals trigger entries only when the thesis is active, and self-improvement proposes updates for user approval rather than writing directly to KB.

## Approach
- **Layer 1 — Daily runner** (`nick-runner.py`): runs at market open, reads THESIS_TRACKER + universe-screen output, computes eligible entries, places Alpaca paper orders, logs full context snapshot per trade.
- **Layer 2 — Exit watcher**: runs intraday (every 30 min) checking stop (-25% hard, -15% review) and profit target (+50% → sell half, trail rest) against open positions.
- **Layer 3 — Trade logger**: every order (entry, exit, stop, partial) writes a structured JSON record to `vault/20_investment/nick/trade-log/YYYY-MM-DD.json` with thesis_id, screen_tier, RS_vs_SPY, sector_ETF_momentum, and macro_regime at time of entry.
- **Layer 4 — Weekly analyzer** (`nick-analyze.py`): runs Sunday, reads trade log, computes per-thesis win rate + R-multiple, surfaces patterns, writes a proposal file (`nick-conviction-update-YYYY-MM-DD.md`) for user to approve before anything in KB changes.
- **Layer 5 — Human gate**: KB conviction scores only update after user runs `/nick-approve` on the proposal file. No autonomous KB writes, ever.

## Why this could work

**1. The infrastructure is already 80% built.** Alpaca paper account is live, `universe-screen.py` already produces EARLY/ALERT/EXTENDED/WATCH tiers with RS vs SPY and sector ETF momentum. The runner just needs to read that output and translate it into Alpaca orders. This is a thin integration layer, not a research problem.

**2. Thesis-gating solves the frequency problem.** Nick's universe is ~15 tickers across 4 theses. At any moment, most will be EXTENDED or WATCH — not actionable. EARLY-only entry with thesis=active as a hard gate means the system naturally acts 2-4 times per month, not per day. That is the right cadence for a thesis-driven portfolio: low enough to hold meaningful positions, frequent enough to capture sector rotations.

**3. Proposal-only self-improvement is proven safe.** The pattern of "system proposes, human approves" is how every production ML system that touches ground truth operates. At N=20 closed trades per thesis (achievable in 4-6 months of paper trading), the win rate and R-multiple estimates are stable enough to detect real drift. Below that threshold, the analyzer runs in read-only mode — it logs patterns but does not produce proposals.

## Best case (top 20% outcome)
After 6 months of paper trading: Nick hits ≥45% win rate and R-multiple ≥1.8 across T1+T2 theses, clearly outperforming SPY by 8-12% on paper NAV. The conviction update proposals catch that EARLY-tier entries on T3 Space underperform vs T1 AI Capex, leading to a reweighting that concentrates capital where edge actually exists. This gives a data-grounded answer to "which thesis is worth sizing up when real money starts."

## Realistic case (median outcome)
After 6 months: mixed results by thesis — T1/T2 beat SPY on paper, T3/T4 roughly flat. Win rate 38-42%, R-multiple 1.3-1.6. Not enough to unlock real money yet, but the trade log provides the exact diagnostic: which screen tier produced what outcome, what the macro regime was at entry. Month 7-12 rules are informed by real data instead of assumption.

## Key assumptions
- `universe-screen.py` runs reliably daily (Monday-Friday) and its output file is stable in format.
- Alpaca paper API remains accessible without rate-limit issues for ~5-10 orders per week max.
- THESIS_TRACKER thesis status (active/watch/killed) is kept current — if a thesis goes stale in the KB, Nick will still trade it. Nick cannot self-detect stale theses; that requires the weekly qualitative review.
- Kill conditions requiring earnings call data stay as manual flags — user sets thesis=watch in THESIS_TRACKER after earnings; Nick reads that flag and exits within the next daily run.

## Risks (and how to mitigate)

| Risk | Mitigation |
|---|---|
| Conviction update proposal based on too few trades corrupts KB | Analyzer is locked to read-only until N≥20 closed trades per thesis; hard-coded threshold |
| EXTENDED-tier entries (chasing) degrade performance | EARLY-only entry rule is hard-coded in runner; EXTENDED positions are held if already open, not opened fresh |
| Kill condition not caught because earnings weren't manually flagged | Exit watcher treats -15% drawdown as automatic review flag — writes alert to vault even if thesis still shows active |
| Alpaca API error causes missed exit | Exit watcher retries 3x with 5-min backoff; if still failing, writes alert file and halts new entries until resolved |
| Self-improvement loop finds spurious patterns (small N) | Proposal file includes confidence interval and trade count explicitly — if CI is wide, proposal says "insufficient data, monitoring" not "update conviction" |

## What I'm NOT addressing
- How to automate qualitative kill condition detection (earnings call parsing) — that is a separate NLP problem; leave it manual for now.
- Position sizing optimization beyond the current ≤5% per trade rule — let pragmatist handle the conviction-weighted vs equal-weight tradeoff with actual numbers.
- Real-money transition mechanics — the paper phase is long enough (6 months) that this is a future decision.
