---
council_topic: ควรสร้าง /system-review command ใหม่หรือไม่
expertise_lens: engineer
date: 2026-05-16
status: open
---

# Council Decision: /system-review Build Decision

## TL;DR

6 agents debated 4 options: build /system-review, add --roadmap flag to /analyst, add 3-line synthesis note to /analyst, or do nothing. The decision is NOT "which option" but "which bottleneck" — if follow-through is the block, start small (Caveman/Skeptic); if discoverability is the block, integrate into /analyst with CLAUDE.md trigger; if architectural separation matters, build /system-review — but only after fixing data quality first.

---

## Decision matrix (1-5, 5 = best for solo owner)

| | Optimist (/system-review) | Pragmatist (--roadmap flag) | Skeptic (3-line note) | Caveman (one section) |
|---|---|---|---|---|
| Habit fit | 2 | 4 | 3 | 4 |
| Output actionability | 4 | 3 | 2 | 3 |
| Maintenance cost | 2 | 4 | 5 | 5 |
| Implementation risk | 2 | 4 | 5 | 5 |
| Follow-through mechanism | 2 | 3 | 1 | 2 |
| **Total** | **12** | **18** | **16** | **19** |

**Caveman wins on matrix (19pts)** — lowest cost, highest maintenance score, fits existing /analyst habit.

---

## Expertise warnings (engineer lens)

- **Optimist stretch**: /system-review reads paper-survey output, but paper-survey has no structured schema — synthesis would parse free-text, not data. High implementation risk masked as "just read files."
- **Pragmatist technically best**: --roadmap flag reuses existing /analyst infrastructure cleanly. No new command surface, no new habit loop.
- **Skeptic/Caveman lowest risk**: 3-line synthesis / one named section = zero infra, zero maintenance. Risk is output being too thin to act on.
- **Most underestimated**: paper-survey schema mismatch is the hardest part of any automated synthesis. Fix schema before building synthesis layer.

---

## Caveman gut signal

**UNEASY (split — not blocking)**

Caveman caught between two fears: "new command = forgotten cave" AND "3 lines = too small to matter." Points at behavioral salience as the real crux. Did not resolve which option crosses the threshold — that's the owner's call.

---

## Recommendation framework

**IF bottleneck = follow-through** (14 papers unimplemented, owner keeps deferring):
→ CAVEMAN/SKEPTIC: one named "System Improvement" section at end of /analyst, word-limited (max 200 words), test 4 weeks, track if acted on

**IF bottleneck = discoverability** (owner forgets paper-survey results exist):
→ PRAGMATIST: /analyst --roadmap flag + add to CLAUDE.md session-start checklist as reminder

**IF bottleneck = architectural separation** (cost-audit and system-review feel mentally separate):
→ OPTIMIST: build /system-review, but only AFTER fixing paper-survey schema and populating OUTCOMES.md/COST_LOG.md with real data

**IF uncertain which bottleneck**:
→ Caveman test: describe what /system-review would output in 1 sentence in 30 seconds. If can't → not ready to build.

---

## Hard questions to answer first (devil's advocate)

1. What specific files will the synthesis section read that /analyst doesn't already? Name them.
2. If OUTCOMES.md and COST_LOG.md are sparsely populated, synthesis produces confident-sounding noise — fix data quality first?
3. Who decided "3-5 items" as the right output size? What is that based on?
4. If synthesis proves valuable, what's the migration path — or will it get refactored in 3 months anyway?
5. "No scheduling" = never runs unless triggered manually. How is this different from owner just reading the logs themselves?

**Devil's advocate core challenge**: "Extend /analyst" is a false middle — cost-audit mode + system-review mode in one command creates cognitive overhead on every run. It serves neither purpose cleanly. Do-nothing has merit if data inputs are sparse.

---

## All artifacts

- [[brief]]
- [[proposal-optimist]] — build /system-review, 3-tier roadmap, manual trigger
- [[proposal-pragmatist]] — /analyst --roadmap flag, existing habit loop
- [[proposal-skeptic]] — 3-line synthesis note, stop conditions
- [[proposal-caveman]] — one section in /analyst, 20 min max
- [[critiques]] — 12 cross-critiques
- [[expertise-engineer]] — engineer lens evaluation: pragmatist technically best, paper-survey schema is hidden complexity
- [[synthesis]] — decision matrix + caveman gut signal + hybrid framework
- [[final-challenge]] — "extend /analyst" is false middle; steelman for do-nothing

---

## Outcome (fill later when known)

- Date decided:
- Choice:
- Outcome (after 4 weeks):
