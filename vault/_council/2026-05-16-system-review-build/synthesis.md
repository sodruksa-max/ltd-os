---
type: council-synthesis
---
# Synthesis: /system-review Build Decision

## Decision Matrix (1-5, 5=best for solo owner)

| | Optimist (/system-review) | Pragmatist (--roadmap flag) | Skeptic (3-line note) | Caveman (one section) |
|---|---|---|---|---|
| Habit fit | 2 | 4 | 3 | 4 |
| Output actionability | 4 | 3 | 2 | 3 |
| Maintenance cost | 2 | 4 | 5 | 5 |
| Implementation risk | 2 | 4 | 5 | 5 |
| Follow-through mechanism | 2 | 3 | 1 | 2 |
| **Total** | **12** | **18** | **16** | **19** |

## Where ALL agree
- No scheduling for solo-owner system
- /analyst habit loop > new command habit
- 14 unimplemented papers = bottleneck is follow-through, not synthesis
- Agent ceiling stays at 7
- "Do nothing" not acceptable

## Where they diverge
Core question: **how much output crosses from ignored footnote to decision-forcing signal?**
- SKEPTIC/CAVEMAN: 3 lines / one section = enough if actually read
- PRAGMATIST: 5 items with structure = minimum for actionability
- OPTIMIST: named artifact in separate command = only thing that changes behavior

## Caveman gut signal: UNEASY (split — not blocking)
Caught between "new cave = forgotten" AND "3 lines = too small." Points at behavioral salience as the crux. Does not resolve which option crosses the threshold.

## Hybrid recommendation framework
**IF bottleneck = follow-through** → CAVEMAN/SKEPTIC (one named section, word-limited, test 4 weeks)
**IF bottleneck = discoverability** → PRAGMATIST + add to CLAUDE.md session-start checklist
**IF bottleneck = architectural separation** → OPTIMIST, but only after resolving paper-survey schema problem first
**IF uncertain** → run Caveman test: describe output in 1 sentence in 30 seconds. If can't → not ready to build.
