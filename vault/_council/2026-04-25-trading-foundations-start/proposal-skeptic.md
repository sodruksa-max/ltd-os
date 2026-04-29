---
council_topic: ควรเริ่ม project trading-foundations แบบไหนดี
role: skeptic
date: 2026-04-25
phase: proposal
---

## Skeptic Proposal: Do One Thing First, and Make It Smaller Than You Think

---

**Core proposal:** Treat Month 1-3 as a forced single-focus period — learning and journaling only, no code, no content. The three goals are not compatible in parallel at this skill level, and trying to run all three simultaneously is the most probable failure mode by far.

---

### Key Failure Modes (ranked by probability x impact)

**1. Dunning-Kruger Paper Gains Create False Confidence (high probability, high damage)**

Paper trading in a bull phase — or with hindsight-biased setups — produces win rates that evaporate when real money and real emotions enter. The plan gates real money behind win rate >=40% and R-multiple >=1.5. The trap: these metrics are achievable in paper trading by an unconscious process of not pressing the "sell" button on losers (you know it's not real). Paper trading psychologically costs nothing. Real trading costs sleep. They are different sports.

The gate metrics are necessary but not sufficient. Someone can paper-trade profitably for 6 months and lose 30% of capital in the first 90 days of real trading. This is the most documented pattern in retail trading and the base rate for it is high.

**2. Content Creation Cannibalizes Learning Depth (medium-high probability, medium damage)**

Short-form content on trading basics rewards simplification, novelty, and confident presentation. Serious market learning rewards uncertainty, revision, and admitting what you do not know. These incentives are directly opposed. A beginner who starts documenting their "trading journey" early is building an audience that requires them to project confidence they do not yet have. This quietly shifts behavior: you stop changing your mind (optics), you start choosing positions that make good content, and you anchor to public statements. Content creation before Month 6 is an identity trap dressed as a productivity hack.

**3. Bot-Building Before Strategy Validation (medium probability, catastrophic damage)**

Writing a trading bot before proving a strategy works by hand is building an automated way to lose money faster. Every hour spent on code architecture before Month 6 is an hour not spent on the harder skill (reading markets). Bots execute a strategy; they do not create one. The sequence matters: strategy -> manual proof -> automation. Not: automation -> strategy -> discover it never worked.

---

### Proposed Structure (minimalist, sequential)

Three phases with hard gates. Each gate must be earned, not scheduled.

**Phase 1: Month 1-3 — Learning Only (no code, no content)**

- Daily: read one setup from a real-time screen, journal why you would or would not take it
- Weekly: log 5 paper trades with full entry rationale, stop placement, and R-target in `vault/20_investment/_journal/`
- No bot scaffolding, no content drafts, no screener builds
- Gate to Phase 2: 60 journal entries with complete data (entry, stop, target, actual outcome, lesson)

**Phase 2: Month 4-6 — Paper Trading + Basic Screener (code enters here, content still off)**

- Build minimal screener — price above 50-day MA, volume spike, momentum filter — nothing more
- Evaluate paper track record honestly against gate metrics
- Gate to Phase 3: win rate >=40%, R-multiple >=1.5, computed from logged trades only — no cherry-picking

**Phase 3: Month 7+ — Real Money, Then Content Decision**

- Real money starts at 10K (10% of capital), per existing PREFERENCES decision
- Content starts only after first full month of real-money trading — this ensures content reflects actual experience, not paper theory
- Bot development starts only after a manual strategy is proven on real money (Month 9+ earliest)

---

### Red Flags to Watch (early warning signs)

- You are spending more than 2 hours/day on setup or tooling vs. actual market study in Month 1
- Your paper trade journal has fewer than 3 entries per week by Week 3
- You are looking at bot tutorials before Month 4
- Any trade journal entry missing a stop-loss price at time of entry (retroactive stops are fiction)
- You open a content account "just to reserve the handle" before Month 6

---

### What the Skeptic Sees That Optimists Overlook

The 15 hours/day of free time is not an advantage — it is a risk. Beginners with abundant time fill it with activity that feels like progress: building dashboards, watching tutorials, writing notes about trading psychology, designing content templates. None of this is trading. The discipline required here is doing less than the available time allows.

The three goals (trading skill, bot development, content) each individually take 12-18 months to reach competence. Sequencing them costs 3-4 years. Running them in parallel at Year 1 skill level produces three mediocre outcomes and likely one expensive lesson.

The most honest conservative alternative: commit to Phase 1 (journaling + paper trading only) for 90 days with a written stop condition. If the journal has fewer than 50 complete trade records at Day 90, the project is not being executed seriously and should pause before any capital, code, or audience is involved.

**Stop condition to define before starting:** If by Month 3 you cannot explain in writing — without looking anything up — why a specific trade setup worked or failed, the foundation is not built and real money should not enter.
