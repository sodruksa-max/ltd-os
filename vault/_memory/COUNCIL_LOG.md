---
type: memory-index
updated: by-council-command
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

(empty — populates as you use /council)

---

## Why this file matters

After 5-10 councils, patterns emerge:
- Which mode (A vs B) you reach for more
- Which proposer's recommendations you follow most
- Which critiques you ignore that bite you later
- Hit rate of council recommendations

This data = personal decision-making intelligence.

Read this monthly. If patterns emerge → update PREFERENCES.md so future councils know.
