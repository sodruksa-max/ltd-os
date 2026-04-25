---
type: memory-index
updated: by-analyst
---

# Analyst Log

Record of insights from `/analyst` command — what was suggested, what you approved/rejected.

## Rules
- Newest on top
- Claude appends when `/analyst` runs, with user's decision
- Format below

## Format

```
## YYYY-MM-DD — <short title>

**Insight**: <what analyst noticed>
**Suggested**: <what change was proposed>
**Decision**: approved | rejected | modified
**Reason**: <why>
**Commit**: <hash if applied>
```

---

## Entries

(empty — first entry will appear after first /analyst run)
