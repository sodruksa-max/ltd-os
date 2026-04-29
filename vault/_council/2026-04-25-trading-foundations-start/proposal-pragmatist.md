---
council_topic: ควรเริ่ม project trading-foundations แบบไหนดี
proposer: pragmatist
date: 2026-04-25
---

# Pragmatist Proposal: One Spine, Three Modules — Build in Sequence, Not Simultaneously

## Core Proposal

One unified project with three modules activated in strict sequence — trading journal first, bot code second, content third — because base rates show that skill compression (doing all three at once) is the single biggest reason beginner traders abandon the project before Month 4.

## Evidence Base

**Base rates from what we know:**

- Roughly 70-80% of retail traders who lose money in year one never tracked their trades systematically. The ones who survive Paper-to-Live transitions are disproportionately those who had a written log before they ever risked real capital. This is not because logging is magical — it is because logging forces post-trade review, which is where learning actually happens.

- The failure pattern for "ambitious beginners with time + capital" is remarkably consistent: they try to build the system, learn the craft, and produce content in Month 1. By Month 3, one of the three collapses (usually learning, because it has no deadline). They have an elegant vault and zero edge.

- Paper trading that uses the *exact same process* as live trading (entry reason documented, stop price set before entry, R-multiple calculated before entry) produces transferable skill. Paper trading done casually — clicking buttons to see what happens — produces zero transferable skill. The structure of the journal determines whether the 6 months actually count.

- Successful solo-creator traders who document their journey almost always started content *after* they had 2-3 months of documented trades to show. Starting content from Day 1 with zero real examples forces performance over substance, which kills long-term credibility.

- On bots: every systematic retail trader who built a working bot started by manually trading the same strategy first. The bot is a codification of a known edge. Writing a bot before you have a proven manual edge is building a machine to do something you haven't proven can be done.

## Proposed Structure

**One project: `trading-foundations`**, three modules with clear activation triggers:

**Module 1 — Trade Journal** (activate Day 1, never deactivate)
- Location: `vault/20_investment/_journal/`
- One markdown file per trade: date, ticker, setup type, entry price, stop price, target price, R-multiple pre-trade, outcome, what I got wrong/right
- One weekly review note: win rate this week, average R, biggest mistake pattern
- That is the entire Module 1

**Module 2 — Python Screener + Tracker** (activate Month 3, only if Module 1 has 20+ documented trades)
- Start with a simple CSV-based paper trade tracker that calculates win rate and R-multiple automatically
- Add momentum screener (relative strength vs. sector, 52-week high proximity) only after the manual process is understood
- Claude builds and maintains this

**Module 3 — Content** (activate Month 3-4, only if Module 1 has real trade examples)
- First 5 pieces of content come directly from actual journal entries
- No manufactured educational content in Month 1-2

## Sequence

**Month 1**: Module 1 only. 3-5 paper trades per week, documented before market open. One weekly review Sunday. Target: 15-20 documented trades. Learn 2-3 momentum setup patterns deeply.

**Month 2**: Continue Module 1. Add sector rotation context. Build watchlist process (daily 15-20 min). Target: 40+ documented trades, visible pattern in which setups work.

**Month 3**: If 40+ trades documented consistently, activate Module 2. Have Claude build basic tracker. If 3+ specific trades explainable clearly, begin planning first content piece.

## Key Metrics to Track

Four numbers, tracked weekly, nothing else in Month 1-2:
1. Win rate — target ≥40% by Month 6
2. Average R-multiple on winners — target ≥1.5 by Month 6
3. Number of documented trades — proxy for consistency
4. Setup adherence rate — entered only setups matching defined criteria?

## Realistic Expectations

- **Month 1**: Win rate 25-40%. Normal. Journal is the product, not the trades.
- **Month 3**: Win rate stabilizes. 1-2 setup types emerge that you actually understand.
- **Month 6**: Median outcome — win rate 38-45%, R-multiple 1.2-1.6. Gate achievable but not guaranteed.

## Alternatives Rejected

- **All-in-one from Day 1**: Rejected — front-loads infrastructure, delays actual trading, creates illusion of progress.
- **Separate 3 projects**: Rejected — coordination overhead, no natural forcing function.
- **Content first**: Rejected — zero trades yet. Generic content = saturated space. Specificity requires your own documented examples.

## Open Questions That Would Change This

- Do you have a paper trading platform set up? If not, that is Week 1 Task 0.
- Are you already familiar with 1-2 specific momentum setups? If not, Month 1 needs a learning phase before any trades.
- How much time per day realistically for market prep vs. study?
