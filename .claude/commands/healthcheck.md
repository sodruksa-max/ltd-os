---
description: Full system audit — find broken scripts, missing files, stale memory, and get improvement suggestions
---

# /healthcheck

Audit the entire LTD-OS system. Find what's broken, what's degraded, and what can be improved.

## Steps

### 1. Run automated checks

```bash
bash scripts/healthcheck.sh
```

Parse the output. Collect all FAIL and WARN lines.

### 2. Deep analysis (Claude reads key files)

After the script, do a deeper check that bash can't do:

**Commands vs scripts cross-check:**
- For each command in `.claude/commands/`, check whether the scripts it calls (e.g. `scripts/macro-snapshot.py`) actually exist
- Flag any command that calls a non-existent script

**Memory freshness:**
- Read `vault/_memory/DECISIONS.md` — check `updated:` frontmatter date. If >30 days old → WARN
- Read `vault/_memory/PROJECTS.md` — same check
- Read `vault/_memory/PREFERENCES.md` — check it has real content (not just template placeholders)

**Trade directory:**
- Glob `vault/20_investment/_journal/real-trades/*.md`
- If empty: WARN — no trades recorded yet (system untested end-to-end)
- If has files: check that each has required frontmatter fields (ticker, status, entry_usd, shares, stop_usd)

**Handoff staleness:**
- Read `.claude/handoff.md` — check `created:` date in frontmatter
- If created > 3 days ago: WARN — may be stale, consider `/handoff` to refresh

### 3. Generate report

Output in this format:

```
## System Health Check — YYYY-MM-DD HH:MM

### Infrastructure
[PASS/WARN/FAIL] venv
[PASS/WARN/FAIL] alpaca-py
[PASS/WARN/FAIL] yfinance
[PASS/WARN/FAIL] .env keys

### Scripts
[PASS/FAIL] scripts/macro-snapshot.py
[PASS/FAIL] scripts/sr-levels.py
[PASS/FAIL] scripts/eod-report.py
... (all scripts)

### Commands
[PASS/WARN] /pre-market — note if any referenced script missing
... (all commands)

### Vault Structure
[PASS/FAIL] directories
[PASS/WARN] memory files — note staleness

### Memory Freshness
[PASS/WARN] DECISIONS.md — last updated: YYYY-MM-DD
[PASS/WARN] PROJECTS.md — last updated: YYYY-MM-DD
[PASS/WARN] PREFERENCES.md — has real content / placeholder only

### Trade System
[PASS/WARN] real-trades/ — N files, frontmatter check

---

### Summary
PASS: X | WARN: Y | FAIL: Z
Overall: [ALL SYSTEMS GO / OK WITH WARNINGS / DEGRADED]

---

### Improvement Roadmap

List actionable improvements found during the audit, prioritized:

**Critical (fix before next trading session):**
- [item] — [why it matters] — [fix command or instruction]

**High (fix this week):**
- [item] — [why] — [fix]

**Low (nice to have):**
- [item] — [why] — [fix]

**New features worth building:**
- [gap found in workflow] — [suggested command/script]
```

### 4. Ask user

After the report:
> ต้องการให้แก้ไขรายการไหนก่อนไหม? (ระบุหมายเลขหรือบอกว่า "ทำทั้งหมด")

## Constraints

- Never expose secret values — only check whether keys are present and non-empty
- Do not auto-fix anything — report only, let user decide what to fix
- If bash script exits with code 2 (FAIL), highlight critical items at the top of the report
