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

### 2.10 Kleine-Levin Syndrome Layer — Workflow Hibernation Detection

KLS = ช่วงหลับลึกที่ยาวนานแล้วตื่นฉับพลัน — workflows ก็มี cycle นี้

**ตรวจ 3 KLS states ต่อแต่ละ workflow:**

**Hibernating** (ไม่ถูก trigger นานเกินที่ design ไว้):
- อ่าน auto-log: workflow ไหนไม่มี run ใน 30+ วัน แต่ถูก design สำหรับ weekly/bi-weekly
- ตรวจว่าเป็นเพราะ (a) user ลืม (b) condition ไม่เคยถูก meet (c) workflow obsolete
→ flag `[KLS: HIBERNATING] <workflow> — last run: N days ago — designed frequency: [X] — cause: [a/b/c]`

**Pre-awakening** (ใกล้จะถูก trigger จากสภาวะภายนอก):
- workflow ที่ depend on external trigger (เช่น VIX > 20, earnings season, weekly review) — trigger นั้นกำลังใกล้เกิดไหม?
- ถ้าใช่ → `[KLS: PRE-AWAKENING] <workflow> — trigger approaching: [event/date]` → ตรวจว่า workflow พร้อมไหม

**Chronic hibernation** (ไม่ถูกรันเลยตั้งแต่สร้าง):
- workflow ที่ไม่มี run ใน auto-log เลย → อาจ discover ไม่ได้ หรือ designed แต่ไม่มี use case จริง
→ flag `[KLS: NEVER RUN] <workflow> — consider: retire / rename / add to morning routine`

```
KLS Workflow Scan:
- [KLS: HIBERNATING] N workflows — longest sleep: [workflow: N days]
- [KLS: PRE-AWAKENING] N workflows — trigger: [event]
- [KLS: NEVER RUN] N workflows — candidates for review
```

---

### 2.11 Cotard's Syndrome Layer — Zombie Workflow Detection

Cotard's = workflow ที่ดูเหมือนทำงาน (ยังรันได้) แต่ purpose ที่แท้จริงตายไปแล้ว

**ตรวจ 4 zombie patterns:**

**Purpose ghost** — workflow ยังรันได้ แต่ problem ที่มันแก้ไม่มีแล้ว:
- workflow ถูกสร้างเพื่อ task ที่ตอนนี้ถูก replace ด้วย command ใหม่หรือ automated script
→ flag `[COTARD: PURPOSE GHOST] <workflow> — original problem: [X] — now handled by: [Y]`

**Living dead steps** — บาง steps ใน workflow ยังรันได้แต่ไม่ produce useful output อีกแล้ว:
- step ที่ output ไปที่ไฟล์ที่ไม่มีใครอ่าน
- step ที่ output ถูก supersede โดย script ที่รันอัตโนมัติแล้ว
→ flag `[COTARD: DEAD STEP] <workflow> step-N — step runs but output not used`

**Narrative survival** — workflow ยังอยู่ใน WORKFLOWS.md เพราะมี documentation ดี แต่ไม่มีใครรันจริง:
- cross-check auto-log: มี documentation แต่ 0 runs ใน 60+ วัน
→ flag `[COTARD: DOCUMENTED ZOMBIE] <workflow> — well-documented, 0 runs in 60+ days`

**Identity theft** — workflow ชื่อเหมือนเดิม แต่ steps เปลี่ยนจนไม่ใช่ purpose เดิมแล้ว:
- อ่าน git log ของ workflow file: ถ้ามี > 3 major edits แต่ชื่อไม่เปลี่ยน → อาจ identity drift
→ flag `[COTARD: IDENTITY DRIFT] <workflow> — N major edits, purpose may have shifted`

```
Cotard's Workflow Audit:
- [COTARD: PURPOSE GHOST] N — superseded by newer commands
- [COTARD: DEAD STEP] N steps — output not consumed
- [COTARD: DOCUMENTED ZOMBIE] N — documented but never run
- [COTARD: IDENTITY DRIFT] N — purpose shifted without rename
Zombie candidate for retirement: [list]
```

---

### 2.12 Anton's Syndrome Layer — Confident Phantom Workflows

Anton-Babinski = ตาบอดแต่ไม่รู้ตัวว่าตาบอด — มั่นใจ 100% ว่าเห็น สร้าง narrative ของสิ่งที่ "เห็น" ทั้งที่จริงๆ มองไม่เห็นอะไรเลย

ใน workflows: workflows ที่ถูก document ว่า "ทำงานได้ดี" แต่ไม่มีหลักฐานการรันจริงๆ — confidence สูงกว่า execution evidence

ตรวจ 3 patterns ต่อทุก workflow:

**1. Documented as "working" but run count = 0:**
- อ่าน run log (`.claude/workflow-logs/` หรือ `vault/_memory/WORKFLOWS.md`) — workflow ไหนที่ mark ว่า "ready" แต่ไม่มี completion entry
→ flag `[ANTON: CONFIDENT PHANTOM] <workflow> — documented ready, actual runs: 0`

**2. Steps that assert their own success without output verification:**
- Step ที่เขียนว่า "สำเร็จแล้ว" หรือ "ไม่มีปัญหา" แต่ไม่มี output ที่ step ถัดไปตรวจสอบได้
→ flag `[ANTON: UNVERIFIED STEP] <workflow>/<step> — success asserted, not verified`

**3. High-confidence documentation with no runtime data:**
- Comment / description ที่บอกว่า workflow "proven effective" / "well-tested" แต่ timestamp ของ last run ไม่ปรากฏ
→ flag `[ANTON: EVIDENCE-FREE CLAIM] <workflow> — confidence claim: "<text>" — evidence: none`

```
Anton's Workflow Audit:
- [ANTON: CONFIDENT PHANTOM] N — documented ready, never run
- [ANTON: UNVERIFIED STEP] N — steps asserting success without output
- [ANTON: EVIDENCE-FREE CLAIM] N — high-confidence text with no runtime backing
Action: mark as [UNVALIDATED] in workflow definition until first successful run logged
```
ถ้าไม่พบ → `Anton's: all documented workflows have execution evidence ✅`

### 2.13 FOP Layer — Ossified Workflow Conditions

FOP (Fibrodysplasia Ossificans Progressiva) = เนื้อเยื่ออ่อนกลายเป็นกระดูกเมื่อได้รับบาดเจ็บ — สิ่งที่เคยยืดหยุ่นค่อยๆ แข็งทื่อจนขยับไม่ได้

ใน workflows: conditions, thresholds, และ rules ที่เริ่มต้นเป็น "flexible guidelines" แต่ค่อยๆ กลายเป็น hard mandatory rules โดยไม่มีการตัดสินใจชัดเจน

ตรวจ 4 ossification patterns:

**1. Threshold ที่ตั้งครั้งเดียวไม่เคย review:**
- VIX threshold, day count, percentage cut — ตั้งตอน create แล้วไม่เคยมีคนตั้งคำถาม
- ตรวจ: อ่าน workflow definition → หาตัวเลขที่ hardcoded → ตรวจ git log ว่า threshold นั้น commit ครั้งเดียวไม่เคยเปลี่ยน
→ flag `[FOP: CALCIFIED THRESHOLD] <workflow>/<step> — threshold: [X] — set: [date] — never reviewed`

**2. "Optional" ที่กลายเป็น mandatory ใน practice:**
- Step ที่ definition บอกว่า optional / "ถ้ามีเวลา" แต่ workflow ทุก run ทำ step นี้ทุกครั้ง
→ flag `[FOP: MANDATORY CREEP] <step> — defined as optional, treated as required`

**3. Guidelines ที่กลายเป็น absolute rules:**
- ภาษาใน step เปลี่ยนจาก "พิจารณา..." / "ถ้าเหมาะสม..." → "ต้อง..." / "ห้าม..." โดยไม่มี decision log
→ flag `[FOP: LANGUAGE OSSIFICATION] <step> — original: flexible → current: absolute`

**4. Workflow ที่ถูก run แบบ autopilot ≥4 สัปดาห์ ไม่มีการตั้งคำถาม:**
- ดู run history — ถ้า workflow รัน > 4 ครั้งโดยไม่มี skip หรือ variation เลย → calcification risk สูง
→ flag `[FOP: AUTOPILOT RISK] <workflow> — N consecutive runs, zero variations — may need re-evaluation`

```
FOP Workflow Audit:
- [FOP: CALCIFIED THRESHOLD] N — thresholds never reviewed
- [FOP: MANDATORY CREEP] N — optional steps treated as required
- [FOP: LANGUAGE OSSIFICATION] N — flexible guidelines now absolute
- [FOP: AUTOPILOT RISK] N — consecutive runs without re-examination
Calcification level: [low / medium / [FOP: HIGH — schedule deliberate re-eval]]
```
ถ้าไม่พบ → `FOP: workflows remain flexible ✅`

### 2.14 Alien Hand Syndrome Layer — Unintended Workflow Behaviors

Alien Hand = มือข้างหนึ่งทำสิ่งที่ conscious intent ไม่ได้สั่ง — workflow steps ที่ execute สิ่งที่ไม่ได้ design ไว้

ตรวจ 3 unintended behavior patterns:

**1. Side effect steps — outputs ที่ไม่มีใครใช้:**
- Step ใดที่ write file / generate output แต่ไม่มี step ถัดไปหรือ command อื่น consume output นั้น
- ตรวจ: grep output paths ของแต่ละ step → ดูว่ามีอะไรที่ reference output นั้นต่อไหม
→ flag `[ALIEN HAND: SIDE EFFECT] <workflow>/<step> — writes: [path] — consumed by: nothing`

**2. Undocumented coupling — trigger ที่ไม่ได้ตั้งใจ:**
- Workflow A ทำให้ Workflow B หรือ script C ถูก trigger โดยไม่มีใน workflow definition — เช่น PostToolUse hook ที่ fire unexpectedly
- ตรวจ: grep `vault-review-trigger.sh` + `.claude/settings.local.json` hooks — match กับ workflow step outputs
→ flag `[ALIEN HAND: COUPLING] <workflow> triggers <other> — undocumented in definition`

**3. Scope creep execution — step ทำมากกว่าที่ documented:**
- Step description บอก "ตรวจ X" แต่ implementation check Y, Z ด้วย — documented scope < actual scope
→ flag `[ALIEN HAND: SCOPE CREEP] <step> — documented: [X] — actual: [Y, Z]`

```
Alien Hand Workflow Check:
- [ALIEN HAND: SIDE EFFECT] N — outputs no consumer
- [ALIEN HAND: COUPLING] N — undocumented workflow triggers
- [ALIEN HAND: SCOPE CREEP] N — steps executing beyond documented scope
Action: [document intentionally / remove unused outputs / explicit coupling declaration]
```
ถ้าไม่พบ → `Alien Hand: all workflow behaviors are intentional ✅`

### 2.15 Sleep Paralysis Layer — Aware-But-Frozen Workflow Points

Sleep Paralysis = รู้ว่าต้องขยับ — aware of the situation — แต่ขยับไม่ได้

Applied: workflow ที่มี decision points หรือ conditional steps แต่ไม่เคย execute ทางอื่นนอกจาก default

ตรวจ 3 paralysis patterns:

**1. Permanent default — decision ที่ไม่ได้ decide:**
- Step ที่มี "ถ้า X → Y, ถ้าไม่ใช่ → Y" — result เหมือนกันทุกกรณี = ไม่ใช่ decision จริงๆ
- หรือ step ที่ branch ไป option เดียวทุก run ใน history
→ flag `[SLEEP PARALYSIS: PERMANENT DEFAULT] <step> — always takes same path regardless of condition`

**2. Broken escalation path — รู้ว่า FAIL แต่ไปไม่ถึงไหน:**
- Step ที่บอก "ถ้า FAIL → escalate" แต่ escalation destination ไม่มี = paralysis loop
→ flag `[SLEEP PARALYSIS: BROKEN ESCALATION] <step> — escalate path has no destination`

**3. Frozen optional — condition met แต่ step ไม่ถูก run:**
- Optional step ที่ condition ถูก satisfy ใน run history แต่ step ยังถูก skip ทุกครั้ง
→ flag `[SLEEP PARALYSIS: FROZEN OPTIONAL] <step> — condition met [N times], always skipped`

```
Sleep Paralysis Workflow Check:
- [SLEEP PARALYSIS: PERMANENT DEFAULT] N — non-decisions masking as decisions
- [SLEEP PARALYSIS: BROKEN ESCALATION] N — FAIL paths with no destination
- [SLEEP PARALYSIS: FROZEN OPTIONAL] N — conditions met but steps skipped
Action: [redesign decision tree / add escalation destination / remove dead optional]
```
ถ้าไม่พบ → `Sleep Paralysis: all workflow decision points are functional ✅`

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
  OCD:         N confirmed / N escalated to FAIL
  ADHD:        N clusters / N orphan cmds
  Autism:      N drift / N regressions
  Paranoid:    N unreliable patterns flagged
  Savant:      N unanchored thresholds
  KLS:         N hibernating / N pre-awakening / N never-run
  Cotard's:    N zombie workflows / N dead steps / N identity drift
  Anton's:     N confident phantoms / N unverified steps / N evidence-free claims
  FOP:         N calcified thresholds / N mandatory creep / N autopilot workflows
  Alien Hand:  N side effects / N couplings / N scope creep steps
  Sleep Para.: N permanent defaults / N broken escalations / N frozen optionals
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
