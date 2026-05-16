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

---

### 2.5 OCD Layer — Cross-validate memory claims against git

ห้าม trust memory ที่ตัวเองประกาศ — ต้องยืนยันกับ git:

```bash
git log --follow --format="%ai" vault/_memory/DECISIONS.md | head -1
git log --follow --format="%ai" vault/_memory/PROJECTS.md | head -1
git log --follow --format="%ai" vault/_memory/PREFERENCES.md | head -1
```

**Cross-check logic (รัน per file):**
- Read `updated:` field from frontmatter
- Compare with git log date above
- If git date is NEWER than `updated:` header → WARN "DECISIONS.md header stale — git shows newer change on [date], header says [date]"
- If `updated:` header is missing entirely → WARN "no updated: field — cannot verify freshness"
- If dates match within 1 day → PASS

**Also cross-validate COUNCIL_LOG:**
```bash
git log --oneline vault/_memory/COUNCIL_LOG.md | head -3
```
- If COUNCIL_LOG has entries but last git touch > 30 days → WARN "council log not updated in 30+ days"

---

### 2.6 OCD Layer — Persistent WARN escalation

เป้าหมาย: WARN ที่ไม่ถูกแก้ข้ามรอบ ต้องถูก escalate — ไม่ยอมให้ WARN นิ่งอยู่นาน

**Read previous run log:**
```bash
cat vault/_memory/healthcheck-log.md 2>/dev/null || echo "(no prior log)"
```

**Escalation logic:**
- Extract all `[WARN]` lines from current run
- For each WARN: check if same text appeared in the previous run's log
- If appeared in **1 previous run** → mark as `[PERSISTED]` in report
- If appeared in **2+ previous runs** → escalate to `[FAIL — PERSISTED N runs]`

**After generating the report, update the log:**
- Write current run's date + all WARN/FAIL items to `vault/_memory/healthcheck-log.md`
- Format:

```markdown
## YYYY-MM-DD HH:MM
- [WARN] nick-signals.md >48h old
- [WARN] handoff.md >24h old
- [FAIL] scripts/screener.py not found
```

Keep last 5 runs only (truncate older).

---

### 2.7 OCD Layer — Symmetry audit

ระบบที่สมดุลต้องมี: command → script → template → folder — ถ้าขาดอันใดอันหนึ่ง = flag

**Command → script symmetry:**
- For each `.claude/commands/*.md`, grep for all `scripts/` references
- For each reference found: verify file exists
- If command exists but referenced script is missing → `[FAIL — broken command: /X calls scripts/Y which is missing]`

**Template → folder symmetry:**
- For each `vault/_templates/*.md`: check if there's a corresponding folder in vault that should exist
  - `fertilizer-formula.md` → `vault/50_formulas/fertilizer/` must exist
  - `recipe-formula.md` → `vault/50_formulas/recipes/` must exist
  - `real-trade-template.md` → `vault/20_investment/_journal/real-trades/` must exist
- If template exists but folder is missing → `[WARN — orphan template: no target folder]`

**Formula system symmetry (new domain check):**
- If `vault/50_formulas/fertilizer/` exists → verify `vault/_templates/fertilizer-formula.md` exists
- If `vault/50_formulas/recipes/` exists → verify `vault/_templates/recipe-formula.md` exists
- If either command (`new-formula`, `new-recipe`) exists → verify both template AND folder exist
- Asymmetry in any direction → WARN

### 3. Generate report

Output in this format:

```
## System Health Check — YYYY-MM-DD HH:MM
## OCD Pass: [CLEAN / WARNINGS / ESCALATED]

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

### Formula System
[PASS/WARN/FAIL] vault/50_formulas/fertilizer/
[PASS/WARN/FAIL] vault/50_formulas/recipes/
[PASS/WARN/FAIL] template: fertilizer-formula.md
[PASS/WARN/FAIL] template: recipe-formula.md
[PASS/WARN/FAIL] /new-formula command
[PASS/WARN/FAIL] /new-recipe command

### Memory Cross-validation (OCD)
[PASS/WARN] DECISIONS.md — header says: YYYY-MM-DD | git last touch: YYYY-MM-DD | [MATCH / STALE]
[PASS/WARN] PROJECTS.md — header says: YYYY-MM-DD | git last touch: YYYY-MM-DD | [MATCH / STALE]
[PASS/WARN] PREFERENCES.md — updated: field [present / missing]

### Symmetry Audit (OCD)
[PASS/FAIL] /new-formula → scripts referenced: [none / list] → all exist: [yes/no]
[PASS/FAIL] /pre-market → scripts referenced: [list] → all exist: [yes/no]
... (all commands with script references)
[PASS/WARN] template fertilizer-formula.md → folder vault/50_formulas/fertilizer/ [exists / MISSING]
[PASS/WARN] template recipe-formula.md → folder vault/50_formulas/recipes/ [exists / MISSING]

### Persistent WARNs (OCD — escalation)
[items that appeared in prior run → marked [PERSISTED] or escalated to FAIL]

---

### Summary
PASS: X | WARN: Y | FAIL: Z
Persistent (unresolved from last run): N
OCD Pass: [CLEAN / WARNINGS / ESCALATED]
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

### 4. OCD Re-verify Pass

หลังจาก report เสร็จ — รัน re-verify บน WARN items ทั้งหมด:

สำหรับแต่ละ WARN:
1. ระบุ WARN ชัดๆ ว่าคืออะไร
2. ถามตัวเองว่า "มีวิธียืนยันด้วย source อื่นไหม?" — ถ้ามีให้ verify
3. ถ้า WARN ยืนยันได้จาก 2 source → เพิ่ม `[CONFIRMED]` tag
4. ถ้า WARN ยืนยันไม่ได้ → downgrade เป็น `[UNCONFIRMED — monitor only]`

แสดงผลเป็น:
```
OCD Re-verify:
- [CONFIRMED] nick-signals.md >48h — verified by both file mtime and git log
- [UNCONFIRMED] DECISIONS.md stale — header date missing, cannot cross-validate
```

### 5. Update warning log + Ask user

อัปเดต `vault/_memory/healthcheck-log.md` ด้วย WARN/FAIL จากรอบนี้

แล้วถาม:
> ต้องการให้แก้ไขรายการไหนก่อนไหม? (ระบุหมายเลขหรือบอกว่า "ทำทั้งหมด")
> WARN ที่ persistent จากรอบก่อน: [list] — ยืนยันว่ายังยอมรับได้ไหม?

## Constraints

- Never expose secret values — only check whether keys are present and non-empty
- Do not auto-fix anything — report only, let user decide what to fix
- If bash script exits with code 2 (FAIL), highlight critical items at the top of the report
