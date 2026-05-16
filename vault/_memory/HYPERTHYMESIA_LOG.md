---
type: hyperthymesia-log
description: Full-context memory of every significant market prediction and thesis decision — captures complete snapshot at time of decision, not just outcome. Append-only. Query for context-matched historical precedents.
updated: 2026-05-17
---

# Hyperthymesia Log

Full-context timeline of every prediction and decision. Unlike OUTCOMES.md (thin calibration line), each entry here captures the **complete state of the world and reasoning at time of decision** — so future sessions can ask "last time conditions were like this, what happened?"

## Query guide
- **Context match:** find entries where regime + VIX range + catalyst type resemble current conditions
- **Pattern query:** "3 entries closest to today's context" → what was the outcome?
- **Reasoning audit:** "the last 5 times I was high-confidence Bullish, what was my actual reasoning?"

## Format per entry
```
## YYYY-MM-DD — [Full / Review-only]
Regime: [trending-up / trending-down / choppy / risk-off]

**Market snapshot at decision time:**
S&P: [+/-X%] | VIX: [X] | TNX: [X%] | Oil(Brent): [$X]
Dominant sector move: [sector] [direction]

**Prediction:**
Direction: [Bullish/Base/Bearish] @ [low/medium/high] confidence
Reasoning: [exact reasoning — what made me think this]
Known unknowns: [what was uncertain when I made this call]
Key catalysts expected: [list]

**Outcome:**
Actual: [Bullish/Base/Bearish] — S&P [+/-X%]
Match: [Yes/Partial/No] | Calibration: [well-calibrated/over-confident/under-confident]
Surprise: [what happened that wasn't in the brief]
Top lesson: [1 sentence]
```

---

<!-- Entries append below — newest at bottom -->
