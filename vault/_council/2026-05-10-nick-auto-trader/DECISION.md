---
council_topic: Nick Auto-Trader + Self-Improvement System
expertise_lens: financial_risk
date: 2026-05-10
status: open
---

# Council Decision: Nick Auto-Trader + Self-Improvement System

## TL;DR
All 4 proposers and the expertise lens agree on the non-negotiable rules; they disagree on shadow mode, trade threshold for KB proposals, and how many positions to hold. The devil's advocate raises a harder prior question: does autonomous execution add learning value over manual /nick-weekly review, or only add infrastructure and silent failure risk? That question must be answered before any code is written.

---

## Decision matrix

| Dimension | Optimist | Pragmatist | Skeptic | Caveman |
|---|---|---|---|---|
| Self-improvement mechanism | Weekly analyzer → proposal file | Monthly human summary | Phase-gated, frozen until N=50 | Human-blocked; no mechanism specified post-gate |
| Trade threshold for proposals | N=20 total | N=30 total | N=50 total | N=20 total |
| Shadow mode first? | No | No | No | YES — 30 days |
| Max concurrent positions | Up to 4 | 1-2 max | Unspecified | Unspecified |
| KB write policy | User approves proposal | User approves monthly | User approves monthly | Human blocks until threshold |
| Benchmark used | SPY | SPY | SPY | Not addressed |
| Regime risk addressed | No | Partial | Mentioned, not solved | No |

---

## Non-negotiable rules (all 4 proposers agree)
Build any of the 3 hybrid options — these rules must be present:

1. **No autonomous KB writes** — human approval required before any THESIS_TRACKER change, in the same session (not a queued file rubber-stamped later)
2. **EARLY-only entry** — no new positions at EXTENDED tier; hold existing, no fresh buys
3. **Thesis state gates execution** — thesis = watch or killed → no entry, period
4. **Kill conditions with qualitative data are human-only** — earnings call triggers must be set manually in THESIS_TRACKER; Nick flags price-based alerts only
5. **Exit rules are fixed** — hard stop -25%, take 50% at +50%, trail remainder; no adaptive exit logic

---

## Expertise warnings (financial_risk lens)
Three findings that most change the decision space:

1. **SPY is the wrong go-live benchmark.** Nick's universe has beta 1.5-2.0 to SPY. Beating SPY in a bull AI cycle = leveraged sector beta, not alpha. Real gate benchmark: 50% QQQM + 50% SOXX, rebalanced monthly. Decide this now, not in month 6.

2. **Regime tagging must be in the trade log from day one.** Without VIX level, 10Y yield, and sector ETF trend (above/below 50MA) on every trade entry, the monthly conviction proposals cannot distinguish regime-driven losses from thesis-driven losses. Retrofitting later means months of data are unusable for conviction analysis.

3. **KB corruption risk is greatest at the $30K live allocation stage, not the paper phase.** A corrupted T1 conviction score causing 3% instead of 5% sizing across 8-12 entries costs ~$3,200 in foregone position size. Not ruin — systematic underperformance of the highest-conviction thesis while the system appears to be working. Pre-live KB audit must be a hard gate with explicit acceptance criteria before month 7.

---

## Caveman gut signal
**DANGER** — confirms the sophisticated proposals, does not contradict them.

The gut signal is not wrong. Caveman is the only proposer who said shadow mode first — 30 days of logging before any Alpaca order fires. That suggestion has zero cost and real upside. The other three proposers ignored it without good reason.

---

## Hybrid options (pick one)

**Hybrid 1: Shadow-First Minimal Executor** (simplest; fastest feedback)
Month 1 shadow mode → month 2+ daily batch runner, 1-2 positions, EARLY-only, morning-only exit check (no intraday watcher). Regime tags from day one. Monthly human summary after 30 closed trades. Benchmark: 50% QQQM + 50% SOXX.

**Hybrid 2: Layered with Hard Phase Gates** (most structured; highest build complexity)
Phase 1 (now–month 3): execute + log only, analyzer locked. Phase 2 (month 3+, 30+ trades, 8+ per thesis): weekly analyzer produces proposals, user approves. Exit watcher moved to cloud (GitHub Actions). Pre-live KB audit as hard gate before month 7.

**Hybrid 3: Nick Observed Forever** (lowest risk; already operational as /nick-weekly)
Execute trades automatically. Log everything including regime tags. Never produce autonomous conviction proposals — /nick-weekly is the self-improvement loop. Zero KB corruption risk. 15-30 min/month review cost.

---

## Devil's advocate questions (answer before committing)

**Q1:** Name one specific thing you will learn from autonomous Nick that you would NOT learn from Hybrid 3 (Nick Observed), given that all KB writes require human approval in every option. If you cannot name it concretely, autonomous execution adds infrastructure but not learning value.

**Q2:** When the exit watcher fails silently (not if, when) — what is the detection mechanism and recovery time window?

**Q3:** What does a corrupted THESIS_TRACKER look like in practice, and how would you detect it before going live? If you cannot define the corruption signature now, the pre-live KB audit has no acceptance criteria.

---

## Hard questions to answer before building anything

1. **Thesis-to-watch mid-hold: exit immediately or hold to stop/target?** This is a code-level decision, not a runtime parameter.
2. **5% risk base: $10K paper NAV ($500) or $100K experiment fund ($5,000)?** Determines whether paper results have predictive validity for live sizing.
3. **Regime tags in trade-log.json from day one?** Cannot be retrofitted — must be decided before the logger is built.
4. **Go-live benchmark: SPY or 50% QQQM + 50% SOXX?** Must be set now, not at month 6.
5. **Shadow mode first?** One month of logs-only before any Alpaca order fires. Zero cost. Real upside. Will you do it?

---

## All artifacts
- [[brief]]
- [[proposal-optimist]] / [[proposal-pragmatist]] / [[proposal-skeptic]] / [[proposal-caveman]]
- [[critiques]]
- [[expertise-financial_risk]]
- [[synthesis]]
- [[final-challenge]]

---

## Outcome (fill when decided)
- Date decided:
- Choice: (Hybrid 1 / Hybrid 2 / Hybrid 3 / Nick Observed Forever only / defer)
- Rationale:
- Outcome (after 3-6 months):
