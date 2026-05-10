---
council_topic: Nick Auto-Trader + Self-Improvement System
phase: synthesis
date: 2026-05-10
---

# Synthesis: Nick Auto-Trader + Self-Improvement System

## Where proposers AGREE
All 4 proposers converge on these — treat as non-negotiable design rules:

1. No autonomous KB writes. Every proposal, including the optimist, requires a human gate before THESIS_TRACKER changes. The question is not IF there is a gate — it is WHEN proposals are generated and what format they take.
2. EARLY-only entry. No new positions opened at EXTENDED. Hold existing if already open. This binary rule is universal.
3. Thesis state gates execution. If thesis = killed or watch, Nick does not enter. No exceptions.
4. Qualitative kill conditions stay human-only. Earnings call data cannot be automated. Machine flags price-based warnings; human reads earnings and sets thesis state.
5. Exit rules are fixed, not adaptive. Hard stop -25%, take 50% at +50%, trail remainder. No proposal touches this.

## Where proposers DIVERGE
These are the actual decisions you must make:

| Axis | Optimist | Pragmatist | Skeptic | Caveman |
|---|---|---|---|---|
| KB proposal threshold | N=20 total closed trades | N=30 total | N=50 total | N=20 total (no stat backing) |
| Shadow mode first? | No | No | No | YES — 30 days |
| KB proposal timing | Weekly (Sunday) | Monthly | Monthly | Monthly |
| Phase gating | 1 phase from launch | 1 phase from launch | 3 explicit phases | 2 gates |
| Max concurrent positions | Up to 4 | 1-2 max | Unspecified | Unspecified |

## Decision matrix

| Dimension | Optimist | Pragmatist | Skeptic | Caveman |
|---|---|---|---|---|
| Self-improvement mechanism | Weekly analyzer → proposal file | Monthly human summary | Phase-gated, frozen until N=50 | Human-blocked; no mechanism specified post-gate |
| Trade threshold for proposals | 20 total | 30 total | 50 total | 20 total |
| KB write policy | User approves proposal file | User approves monthly | User approves monthly | User blocks until threshold |
| Kill condition handling | Price alert + manual flag | Manual flag in trade-log | Explicit human-only rule | Human-only, no exceptions |
| Position sizing clarity | 4 concurrent at 5% each | 1-2 concurrent | Not specified | Not specified |
| Exit watcher reliability | 30-min intraday cron on home machine | Morning batch only via GitHub Actions | Not specified | Not specified |
| Benchmark validity | SPY (unexamined) | SPY (unexamined) | SPY (unexamined) | Not addressed |
| Regime risk addressed | No | Partial (RS vs SPY logged) | Mentioned, not solved | Not addressed |

## Caveman gut signal
**DANGER** — and it confirms, not contradicts, the sophisticated proposals.

The gut signal is not irrational. It precisely identifies the highest-probability failure: a machine that rewrites its own rules on too-few data points, silently. The sophisticated proposals all arrive at the same conclusion through statistical reasoning. Shadow mode first is the one operational suggestion the other three ignore — and it has zero cost and real upside. The gut and the evidence agree.

## Expertise warnings (financial_risk lens)
Three findings that most change the decision space:

**1. Wrong benchmark, by design.** SPY flatters this portfolio. Nick's universe (NVDA, AMD, AVGO, ASML, ARM, MU) has beta 1.5-2.0 to SPY. T3 Space has beta 2.0-3.0+. Beating SPY in a bull AI cycle is leveraged sector beta, not alpha. The right comparison is 50% QQQM + 50% SOXX, rebalanced monthly. A go-live gate built on SPY comparison will pass the strategy even if it generated negative alpha. No proposer raised this.

**2. Regime mismatch poisons self-improvement.** Paper phase runs May–November 2026 — one specific macro window. Without VIX level, 10Y yield, and sector ETF trend direction logged on every trade entry, the monthly conviction proposals cannot distinguish regime-driven losses from thesis-driven losses. All proposals omit regime tagging from trade-log.json. This is the most silent and most permanent KB corruption path — the analyzer updates conviction based on outcome alone, not regime context.

**3. The real dollar risk is the corrupted KB entering the live phase.** At the $30K allocation stage (month 12+), a corrupted T1 conviction score causing Nick to size T1 at 3% instead of 5% across 8-12 entries costs approximately $3,200 in foregone position size. Not ruin — systematic underperformance of the highest-conviction thesis while the system appears to be working. No proposal assigns dollar amounts to this risk.

## Critique patterns
Themes flagged by 2+ critics:

- **Exit watcher reliability is the critical unaddressed failure.** Optimist's 30-min intraday watcher on a home Windows machine is the highest-risk single point of failure in the most critical layer. If it goes dark, positions bleed without stop execution. No proposal specifies recovery protocol.
- **Position sizing 10x gap between paper and live is unresolved.** $500 paper trades test infrastructure. $5,000 live trades test strategy and psychology. Six months of paper data at $500 may not transfer.
- **Threshold numbers are asserted, not derived per-thesis.** Optimist N=20, skeptic N=50 — neither is per-thesis. 50 total trades could mean 5 per thesis, which is coin-flip territory for any conviction update on that thesis alone.
- **Silent failure is the dominant architecture risk.** GitHub Actions cron skips, Alpaca API times out, runner has a bug — all look like success (no error, no log). The system needs loud failures, not quiet ones.

## Hybrid options

**Hybrid 1: Shadow-First Minimal Executor (Caveman + Pragmatist)**
Month 1 shadow mode — Nick logs picks but places zero Alpaca orders. User reviews 20-30 hypothetical entries. If picks look sane, flip execution flag. Month 2+: daily batch runner, 1-2 positions max, EARLY-only, thesis-gated. Exit logic: morning runner checks prior-day close vs hard stop only — no intraday watcher on home machine. Monthly human summary for KB proposals after 30 closed trades. Regime tag (VIX, 10Y yield, sector ETF vs 50MA) on every trade-log entry from day one. Benchmark: 50% QQQM + 50% SOXX.

**Hybrid 2: Layered with Hard Phase Gates (Optimist + Skeptic)**
Build optimist's 5-layer architecture with skeptic's phase gating. Phase 1 (now–month 3): execute + log only, analyzer locked. Phase 2 (month 3+, 30+ closed trades, minimum 8 per thesis): weekly analyzer produces proposals, user approves. Phase 3 (month 6+, 80+ total): proposal cadence stays monthly, never fully autonomous. Kill rule: any proposed conviction change >20 points auto-rejected and flagged. Exit watcher moved to cloud (GitHub Actions scheduled workflow) not home machine. Pre-live KB audit added as hard gate item in PREFERENCES.

**Hybrid 3: Nick Observed Forever (Skeptic + Caveman, conservative)**
Execute trades automatically. Log everything including regime tags. Never produce autonomous conviction proposals — monthly /nick-weekly human-written calibration is the self-improvement loop. KB changes stay manual, informed by structured trade-log data instead of memory. Zero KB corruption risk. 15-30 min/month human review. Identical learning signal to any automated proposal system, because all proposals require human approval anyway.

## Open questions you must answer before a single line of code is written

1. **Thesis-to-watch mid-hold: exit immediately or hold to stop/target?** When THESIS_TRACKER changes from active to watch while Nick holds a position, does Nick (a) exit at next morning run, or (b) hold until hard stop or profit target triggers? This is a code-level decision, not a parameter to tune later.

2. **What is the 5% risk base — $10K paper NAV or $100K experiment fund?** $500 vs $5,000 per position. This changes position size 10x. Decide now so the trade log captures the scaling assumption explicitly.

3. **Will you add regime tags to every trade entry from day one?** VIX level, 10Y yield, sector ETF trend (above/below 50MA) must be in trade-log.json at build time — retrofitting later means months of data cannot be used in any conviction analysis that controls for regime.

4. **What is the real benchmark for the go-live gate?** SPY alone or blended (50% QQQM + 50% SOXX)? If you accept the financial risk lens finding, this changes the gate metric now — not in month 6 when you discover the benchmark was wrong.

5. **Does shadow mode happen first?** One month of logs-only before any Alpaca order fires costs nothing and produces a 20-30 pick validation set. You are in month 1 with zero closed trades. Is one month of observation worth the delay?

## Recommendation framework (NOT a recommendation)

If you weigh **KB integrity and real-money protection** highest → **Hybrid 3 (Nick Observed)**. Identical learning value, zero corruption risk, consistent with /nick-weekly already in place.

If you weigh **structured self-improvement with evidence** highest → **Hybrid 2 (Layered with Hard Phase Gates)**. Per-thesis N thresholds, regime-tagged log, exit watcher on cloud.

If you weigh **simplicity and fastest first feedback** highest → **Hybrid 1 (Shadow-First Minimal Executor)**. One month shadow, minimal batch runner, no intraday watcher dependency.

> Which matters more to you: seeing Nick act autonomously and generate data fast, or protecting the KB quality that informs real-money decisions in month 7? Answer that, then the architecture follows.
