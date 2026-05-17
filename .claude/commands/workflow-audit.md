---
description: Audit all workflow definitions — find broken references, stale steps, skipped patterns, and new commands that should be incorporated. Proposes changes, user approves before saving.
---

# /workflow-audit

ตรวจสุขภาพ workflow definitions ทั้งหมด — หาของเสีย, ของล้าสมัย, และของที่ควรเพิ่ม
รันหลังจาก: เพิ่ม command ใหม่, เพิ่ม script ใหม่, หรือทุก 2 สัปดาห์

## Usage

```
/workflow-audit                    — audit ทุก workflow
/workflow-audit morning            — audit เฉพาะ workflow นั้น
/workflow-audit --fix-all          — apply ทุก suggestion ที่ไม่ conflict โดยไม่ถาม
```

---

## Steps

### 1. Load audit baseline

รันทั้ง 3 พร้อมกัน:

**A. ดู workflow files ทั้งหมด:**
```bash
ls vault/_workflows/*.md 2>/dev/null | grep -v ".state"
```

**B. ดู commands ที่มีอยู่จริง:**
```bash
ls .claude/commands/*.md | sed 's|.*/||;s|\.md||'
```

**C. ดู scripts ที่มีอยู่จริง:**
```bash
ls scripts/*.py scripts/*.sh 2>/dev/null | sed 's|scripts/||'
```

**D. อ่าน auto-log จาก WORKFLOWS.md:**
```bash
grep -A 999 "^## Auto-Log" vault/_memory/WORKFLOWS.md | grep "^|" | grep -v "^| Date"
```

**E. ดู git log ของ workflow files — หาว่าอัปเดตล่าสุดเมื่อไหร่:**
```bash
for f in vault/_workflows/*.md; do
  echo "$f: $(git log -1 --format='%ai' -- "$f" 2>/dev/null || echo 'untracked')"
done
```

**F. ดู commands ที่ถูก add ใน 30 วันที่ผ่านมา:**
```bash
git log --oneline --since="30 days ago" --diff-filter=A -- '.claude/commands/*.md' 'scripts/*.py' 'scripts/*.sh'
```

---

### 2. Validate ทุก workflow definition

สำหรับแต่ละ workflow file — อ่านและตรวจ 5 dimensions:

#### 2A. Command existence check
ต่อทุก `cmd:` และ `yes-cmd:` field ใน workflow:
- ถ้า `/command-name` → ตรวจว่า `.claude/commands/<command-name>.md` มีอยู่
- ถ้า `scripts/file.py` หรือ `scripts/file.sh` → ตรวจว่าไฟล์นั้นมีอยู่
- Flag: `[BROKEN-REF] step-N: cmd '<x>' not found`

#### 2B. Staleness detection
- อ่าน `Last refined` จาก workflow frontmatter (หรือ `# created` ถ้าไม่มี)
- เทียบกับ git log ของ workflow file
- เทียบกับ new commands/scripts จาก Step F ด้านบน
- ถ้า new commands ถูก add หลัง workflow ถูก last refined → flag: `[STALE] workflow '<name>' — N new commands added since last update: [list]`

#### 2C. Auto-log pattern analysis
อ่าน auto-log จาก Step D — หา patterns:
- Step ที่ถูก `skipped` ทุกครั้ง → condition อาจ miscalibrated หรือ step ไม่จำเป็น
- Workflow ที่ status = `failed` บ่อย → `on-fail` rule หรือ step อาจต้องปรับ
- Workflow ที่ไม่เคยถูกรันเลย → อาจตั้งชื่อไม่ชัดหรือไม่ถูก discover
- Flag: `[PATTERN] step-N always skipped (N/M runs)` หรือ `[PATTERN] workflow never run since created`

#### 2D. Coverage gap — new commands ที่ควรอยู่ใน workflow
จาก Step F (commands added ใน 30 วัน):
- สำหรับแต่ละ new command → ดูว่า workflow ไหน น่าจะ benefit จาก command นั้น
- ถ้า new command fit กับ purpose ของ workflow → flag: `[MISSING] workflow '<name>' should consider adding /<new-cmd>`

#### 2E. Step ordering and dependency check
อ่าน workflow step sequence:
- Step ที่ใช้ output จาก step ก่อน — แต่ `on-fail: continue` บน step ก่อน → อาจ run ด้วยข้อมูลไม่ครบ
- Step ที่ require-input แต่วางอยู่หลัง conditional step → อาจถูก skip โดยไม่ได้รับ input
- Flag: `[DEP-RISK] step-N depends on step-M output but step-M has on-fail: continue`

---

### 2.5 OCD Layer — Re-verify + Persistent WARN Escalation

**Re-verify ทุก WARN จาก 2 sources:**
ต่อแต่ละ flag ที่พบใน 2A-2E:
- หา source อิสระที่ 2 ที่ยืนยัน flag นั้น (เช่น broken-ref → ตรวจทั้ง `ls` และ `grep` ใน commands อื่น)
- ถ้ายืนยันได้จาก 2 sources → `[OCD: CONFIRMED]`
- ถ้ายืนยันไม่ได้ → downgrade เป็น `[OCD: UNCONFIRMED — monitor]` ไม่ใช่ FAIL

**Persistent WARN escalation:**
อ่าน prior audit log จาก WORKFLOWS.md:
```bash
grep -A 20 "### Audit:" vault/_memory/WORKFLOWS.md | tail -40
```
- ถ้า WARN เดิมปรากฏใน audit ก่อนหน้า 1 ครั้ง → mark `[PERSISTED]`
- ถ้าปรากฏ 2+ ครั้ง → escalate เป็น `[FAIL — PERSISTED N audits]` — ต้องแก้ในรอบนี้

```
OCD Re-verify: N confirmed / N unconfirmed / N escalated to FAIL
```

---

### 2.6 ADHD Layer — Cluster Detection + Novelty Radar

**Cluster detection:**
จัดกลุ่ม flags ทั้งหมดตาม root cause:
- หลาย workflows มี broken-ref ไปที่ command เดียวกัน → `[CLUSTER] /cmd-name broken in N workflows — fix once, fix all`
- หลาย workflows ไม่ได้รับ new commands จาก domain เดียวกัน → `[CLUSTER] domain: trading — 3 workflows missing recent commands`
- หลาย workflows มี auto-log skipping pattern ในช่วงเวลาเดียวกัน → `[CLUSTER] temporal — N workflows degraded after commit <hash>`

Check correlation กับ git log:
```bash
git log --oneline --since="30 days ago" -- '.claude/commands/*.md' 'scripts/*.py' | head -10
```
ถ้า cluster correlate กับ commit → `[ADHD: REGRESSION] cluster may trace to commit <hash>`

**Novelty Radar:**
สแกนหา commands/scripts ที่ added แต่ไม่อยู่ใน workflow ใดเลย:
```bash
comm -23 <(ls .claude/commands/*.md | sed 's|.*/||;s|\.md||' | sort) \
          <(grep -h "cmd:" vault/_workflows/*.md | sed 's|.*cmd:.*/?||;s| .*||' | sort -u)
```
Flag: `[NOVELTY: ORPHAN CMD] /<name> — added N days ago, not in any workflow`

```
ADHD Pass: N clusters / N orphan commands / N regressions
```

---

### 2.7 Autism Layer — Cross-Audit Consistency

เปรียบเทียบ findings ในรอบนี้กับ prior audit:

**Pattern drift detection:**
- ถ้า flag ที่ reject ใน prior audit กลับมาอีก → `[AUTISM: DRIFT] issue rejected in prior audit returned — was fix temporary?`
- ถ้า workflow ที่ผ่าน clean ใน prior audit กลับมา fail → `[AUTISM: REGRESSION] <workflow> was CLEAN — something changed`
- ถ้า fix ที่ approved ใน prior audit ไม่ได้ถูก apply จริง → `[AUTISM: FIX NOT APPLIED] approved change from <date> still missing`

**Cross-workflow inconsistency:**
- workflows ที่ cover domain เดียวกัน (เช่น trading) ควรมี common steps ที่ consistent
- ถ้า morning.md ใช้ threshold VIX > 20 แต่ weekly.md ใช้ VIX > 18 → `[AUTISM: THRESHOLD INCONSISTENCY] morning vs weekly`

```
Autism Cross-Audit:
- [AUTISM: DRIFT] N / [AUTISM: REGRESSION] N / [AUTISM: FIX NOT APPLIED] N
- Threshold inconsistencies: N
```

---

### 2.8 Paranoid Layer — Distrust Auto-Log

**ก่อนเชื่อ auto-log pattern — ตั้ง adversarial questions:**

ต่อทุก pattern จาก 2C:
- "step always skipped" → ตรวจว่า: condition evaluation logic ถูกต้องไหม? หรือ Claude misread condition ทุกครั้ง?
- "workflow always fails at step-N" → ตรวจว่า: script จริงๆ fail หรือ Claude mark failed เพราะ output format ไม่ตรงที่คาด?
- "workflow never run" → ตรวจว่า: workflow ถูก discover ไหม? ชื่อชัดเจนไหม? อยู่ในที่ที่หาได้ไหม?

**Representative sampling check:**
- auto-log มี N runs — N นั้นมากพอที่จะ conclude pattern ไหม?
- ถ้า N < 3 → `[PARANOID: INSUFFICIENT DATA] pattern from <N> runs only — cannot conclude`
- ถ้า N runs ทั้งหมดอยู่ใน time window เดียว (เช่น ทั้งหมดอยู่ใน market crash week) → `[PARANOID: BIASED SAMPLE] all runs in unusual period`

```
Paranoid Auto-Log Check:
- [PARANOID: INSUFFICIENT DATA] N patterns with < 3 runs
- [PARANOID: BIASED SAMPLE] N patterns from unrepresentative period
- Patterns confirmed reliable: N
```

---

### 2.9 Savant Layer — Condition Threshold Verification

สำหรับทุก condition threshold ใน workflow definitions:

**ตรวจว่า threshold มี source:**
- VIX > 20 → มาจากไหน? paper? TRADING_RULES.md? user decision? หรือ default ที่ไม่มีที่มา?
- Search ใน vault:
  ```bash
  grep -ri "VIX.*20\|threshold\|condition" vault/Knowledge/ vault/_memory/TRADING_RULES.md 2>/dev/null | head -10
  ```
- ถ้าไม่มี source → `[SAVANT: UNANCHORED THRESHOLD] condition '<x>' — no source found`

**ตรวจว่า threshold ยัง current:**
- ถ้า threshold ถูกตั้งไว้มากกว่า 6 เดือนโดยไม่มี calibration → `[SAVANT: STALE THRESHOLD] '<x>' — last calibrated <date>`
- Cross-check กับ auto-log: threshold produce useful branching ไหม? หรือ branch เดียวกันตลอด?

```
Savant Threshold Audit:
- [SAVANT: UNANCHORED] N thresholds without source
- [SAVANT: STALE] N thresholds >6 months without calibration
- Well-calibrated thresholds: N
```

---

### 3. Generate audit report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Workflow Audit — YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Workflows checked: N
Commands available: N | Scripts available: N

── morning ─────────────────────────────
  Status: [PASS / WARN / FAIL]
  Last refined: YYYY-MM-DD (N days ago)
  Auto-log: N runs — X completed, Y skipped-partial, Z failed

  Issues:
  [BROKEN-REF] step-2: cmd '/screen' — .claude/commands/screen.md NOT FOUND
  [STALE] 2 commands added since last update: /eod, /market-log
  [PATTERN] step-2 (screen) skipped 4/4 runs — condition may be too strict

  Proposed changes:
  → Fix /screen reference or replace with /screen (check if renamed)
  → Consider adding /market-log after step-1 for non-high-VIX days
  → Relax screen condition: VIX > 18 instead of > 20 (4/4 false → threshold may be off)

── weekly ──────────────────────────────
  Status: [PASS]
  Last refined: YYYY-MM-DD (N days ago)
  Issues: none
  New commands to consider: none

── research ────────────────────────────
  Status: [WARN]
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: PASS: N | WARN: N | FAIL: N
Issues: N broken-ref | N stale | N patterns | N missing

Cognitive Trait Passes:
  OCD:      N confirmed / N escalated to FAIL
  ADHD:     N clusters / N orphan cmds
  Autism:   N drift / N regressions
  Paranoid: N unreliable patterns flagged
  Savant:   N unanchored thresholds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 4. Propose and apply fixes

สำหรับแต่ละ workflow ที่มี issues:

แสดง proposed changes เป็น diff:
```
workflow: morning
─── before ──────────────────────────
### step-2: screen (conditional)
**condition:** VIX > 20 หรือมี EARLY★ setups
─── after ───────────────────────────
### step-2: screen (conditional)
**condition:** VIX > 18 หรือมี EARLY★ setups (VIX threshold ลดจาก auto-log: skipped 4/4 runs)
─────────────────────────────────────
Apply this change? (yes / no / modify)
```

กฎ apply:
- `yes` → แก้ไฟล์ + อัปเดต `Last refined: YYYY-MM-DD` ใน frontmatter
- `no` → log "rejected" ใน audit summary
- `modify` → Claude รับคำสั่งปรับ then show diff อีกครั้ง

ถ้า `--fix-all` flag:
- Apply ทุก change ที่ไม่มี conflict (broken-ref fixes, stale additions) โดยไม่ถาม
- Changes ที่ต้องการ judgment (condition threshold, step removal) → ยังถามอยู่

---

### 5. Update audit log

Append ใน `vault/_memory/WORKFLOWS.md` ส่วน audit:
```markdown
### Audit: YYYY-MM-DD
Checked: N workflows | Issues: N | Fixed: N | Rejected: N
[FIXED] morning: fixed /screen ref, added /market-log
[REJECTED] morning: condition threshold change — user deferred
[CLEAN] weekly: no changes needed
```

---

### 6. Report to user

```
Audit complete — YYYY-MM-DD
Workflows checked: N | Issues found: N | Fixed: N

Next audit: run /workflow-audit in ~2 weeks or after adding new commands
Schedule tip: /cron "every 2 weeks" /workflow-audit
```

---

## Constraints

- **ห้าม apply change โดยไม่แสดง diff** ก่อนทุกครั้ง (ยกเว้น --fix-all บน safe changes)
- **ห้าม delete step** โดยไม่มีเหตุผลจาก auto-log — pattern ต้องมีอย่างน้อย 3 runs ก่อน suggest removal
- **ห้าม เปลี่ยน condition threshold** โดยไม่มีหลักฐานจาก auto-log
- **Broken-ref เป็น FAIL** ไม่ใช่ WARN — workflow ที่มี broken-ref ไม่สามารถรันได้
- **หลังแก้ทุก workflow** → อัปเดต `Last refined` ใน frontmatter เสมอ
