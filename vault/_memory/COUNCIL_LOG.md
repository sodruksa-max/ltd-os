---
type: memory-index
updated: 2026-05-16
---

# COUNCIL_LOG.md — Council Sessions Index

Index of all `/council` sessions. Track decisions over time, see which councils led to good outcomes.

## Format

Each line:
```
- YYYY-MM-DD — <topic> — mode <A|B> — status: <open|decided|abandoned> → [[<folder>/DECISION]]
```

After deciding, update line:
```
- YYYY-MM-DD — <topic> — mode A — decided: <choice> on YYYY-MM-DD → [[<folder>/DECISION]]
```

After outcome observable (2-8 weeks), add note:
```
- YYYY-MM-DD — <topic> — outcome: ✅/⚠️/❌ — see OUTCOMES.md entry
```

## Sessions

- 2026-05-16 — /system-review build decision — lens: engineer — status: open → [[_council/2026-05-16-system-review-build/DECISION]]
- 2026-05-16 — Nick thesis and portfolio design — lens: financial_risk — status: open → [[_council/2026-05-16-nick-thesis-design/DECISION]]
- 2026-05-10 — Nick Auto-Trader + Self-Improvement System — lens: financial_risk — status: open → [[_council/2026-05-10-nick-auto-trader/DECISION]]
- 2026-04-30 — QQQ Setup 3: ควรเพิ่ม AH price reaction criterion นอกจาก GAAP EPS beat? — lens: financial_risk — status: open → [[_council/2026-04-30-qqq-setup3-ah-criterion/DECISION]]
- 2026-04-25 — ควรเริ่ม project trading-foundations แบบไหนดี — lens: financial_risk — status: open → [[_council/2026-04-25-trading-foundations-start/DECISION]]

---

## Why this file matters

After 5-10 councils, patterns emerge:
- Which mode (A vs B) you reach for more
- Which proposer's recommendations you follow most
- Which critiques you ignore that bite you later
- Hit rate of council recommendations

This data = personal decision-making intelligence.

Read this monthly. If patterns emerge → update PREFERENCES.md so future councils know.
