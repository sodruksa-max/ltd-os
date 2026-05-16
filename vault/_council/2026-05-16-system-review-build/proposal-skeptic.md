---
proposer: skeptic
---
# Skeptic: Do Less Than You Think — Extend /analyst, Don't Build New

**Pre-mortem failures:**
1. (Highest prob) Command runs, roadmap produced, nothing implemented — joins 14 papers in limbo. Real problem: not synthesis, but prioritization and follow-through.
2. (Medium) Scheduled runs → alert fatigue. Owner is one person. One more weekly report competes with pre-market, post-market, weekly-calibration.
3. (Lower but serious) Maintenance: command touching multiple sources degrades silently when one source drifts.

**Hidden costs:**
- Maintenance: /healthcheck + /analyst + paper-survey must stay consistently formatted
- Attention: synthesis removes search, not decision-making — cognitive work unchanged
- Opportunity: time building /system-review = time NOT implementing 14 papers

**The gap may be illusory:** Owner synthesizes manually in conversation already. 14 papers exist in backlog (vs 0 if system were broken) = synthesis is NOT the bottleneck.

**Conservative alternative:** Append "Synthesis note" section to existing /analyst output. 3 lines max: (1) healthcheck flag, (2) matching paper, (3) one next action. Reversible.

**Stop conditions (define before building):** If after 4 weeks roadmap caused zero concrete changes → kill. If two consecutive outputs >500 words and not read to end → kill.

**What's NOT a good reason:** "System feels incomplete," "14 papers unimplemented," "other PKM systems have meta-review," "useful sometimes."
