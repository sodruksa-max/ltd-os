---
description: Deep-analysis workflow creator for new projects. Analyzes domain first, maps available tools, detects gaps, models failure modes — produces comprehensive workflow definition (not a simple wizard).
---

# /workflow-design

สร้าง workflow สำหรับ project ใหม่แบบ **วิเคราะห์ domain ก่อน** — ไม่ใช่แค่ wizard ถาม steps
ผลลัพธ์: workflow ที่รอบครอบ, ไม่ขาด step สำคัญ, มี failure handling, และ conditions ที่ calibrated จริง

## Usage

```
/workflow-design <project-or-domain>
/workflow-design trading-morning
/workflow-design "research pipeline for macro topics"
/workflow-design fertilizer-formula
```

ต่างจาก `/new-workflow`:
- `/new-workflow` = wizard ถาม steps ทีละตัว (user กำหนด)
- `/workflow-design` = วิเคราะห์ domain → propose steps → user approve/adjust

---

## Steps

### 1. Parse input + load context

**อ่าน project context (task-scoped):**
```bash
cat vault/_memory/PROJECTS.md 2>/dev/null | head -100
```

Grep vault หา materials เกี่ยวกับ domain นั้น:
```bash
grep -ri "<DOMAIN_KEYWORDS>" vault/Knowledge/ vault/10_research/ vault/40_projects/ --include="*.md" -l 2>/dev/null | head -10
```

ดู workflows ที่มีอยู่แล้ว — เพื่อ avoid duplication และ reuse patterns:
```bash
ls vault/_workflows/*.md 2>/dev/null | grep -v ".state"
```

ดู commands + scripts ที่ available ทั้งหมด:
```bash
ls .claude/commands/*.md | sed 's|.*/||;s|\.md||'
ls scripts/*.py scripts/*.sh 2>/dev/null | sed 's|scripts/||'
```

---

### 2. Domain analysis — "Jobs to be Done" mapping

วิเคราะห์ domain ที่ user ระบุ โดย **ไม่ถามก่อน** — generate เอง แล้ว validate กับ user ทีหลัง

สำหรับ domain นั้น ตอบ 5 คำถาม:

**A. Jobs to be Done (JTBD)** — อะไรคือ tasks หลักที่ workflow นี้ต้องทำให้สำเร็จ?
(enumerate 5-10 jobs — เฉพาะจริงๆ สำหรับ domain นี้)

**B. Pre-conditions** — อะไรต้องเป็นจริงก่อนที่ workflow จะเริ่มรันได้?
(data ที่ต้องมี, เวลา, ระบบที่ต้อง online, ฯลฯ)

**C. Decision points** — จุดไหนที่ต้อง branch ตาม condition?
(condition = ตัวเลข, user input, output จาก step ก่อน)

**D. Failure modes** — แต่ละ job สามารถ fail ได้อย่างไร? และถ้า fail แล้วระบบควรทำอะไร?
(stop vs continue vs retry vs notify)

**E. Outputs and downstream** — workflow นี้ produce output อะไร? อะไรใช้ output นั้นต่อ?
(ช่วยกำหนดว่า step สุดท้ายควรทำอะไร)

---

### 3. Command-to-Job mapping

ต่อแต่ละ job จาก Step 2A → ค้นหา command หรือ script ที่ cover job นั้น:

| Job | Available Command/Script | Coverage | Gap? |
|---|---|---|---|
| [job 1] | [/cmd หรือ scripts/x.py] | full / partial | no / YES |
| [job 2] | [none] | — | YES → suggest |
| ... | ... | ... | ... |

**Gap handling:**
- Gap ที่ cover ได้ด้วย bash → เขียน inline bash step
- Gap ที่ cover ได้ด้วย Claude analysis → เขียน Claude-only step (ไม่ต้องใช้ script)
- Gap ที่ต้องสร้าง command ใหม่ → flag `[GAP: needs /new-command]` และ include placeholder step

---

### 4. Dependency graph

วาด dependency chain ระหว่าง steps:
```
step-1 (ข้อมูล A) → step-2 (ใช้ A) → step-4 (ใช้ A+B)
                  → step-3 (ข้อมูล B) ↗
```

กฎจาก dependency graph:
- Steps ที่ไม่ depend กัน → ระบุว่า "สามารถ parallel ได้" แต่ /workflow รัน sequential
- Steps ที่ depend → `on-fail: stop` บน upstream step เสมอ
- Steps ที่ produce data ที่ใช้ใน condition → ต้อง complete ก่อน conditional step เสมอ

---

### 5. Failure mode matrix

สร้าง matrix ต่อแต่ละ step:

| Step | Fail type | Probability | Impact | Rule |
|---|---|---|---|---|
| step-1 | API timeout | medium | blocks all | on-fail: stop + notify |
| step-2 | No data found | low | skippable | on-fail: continue |
| step-3 | Script error | low | blocks step-4 | on-fail: stop |

**กฎในการกำหนด on-fail:**
- Impact = HIGH (step ถัดไปพึ่งพา output นี้) → `on-fail: stop`
- Impact = LOW (step เป็น optional enrichment) → `on-fail: continue`
- Probability = HIGH + Impact = LOW → `on-fail: continue + log`

---

### 6. Comprehensiveness checklist

ตรวจ workflow ที่ออกแบบแล้วด้วย checklist นี้ก่อน draft:

- [ ] **Setup phase** — มี step ที่ load context / ตรวจ pre-conditions ก่อนเริ่ม?
- [ ] **Core execution** — JTBD ทุกข้อมี step ที่ address?
- [ ] **Review/validate phase** — มี step ที่ review output ก่อนสิ่งสำคัญ? (เช่น ก่อน commit, ก่อน trade)
- [ ] **Save/persist phase** — output ถูก save ในที่ที่เหมาะสมไหม?
- [ ] **Cleanup/notification** — มีอะไรที่ต้องทำสุดท้ายเสมอ (log, commit, notify)?
- [ ] **Edge cases** — ถ้าตลาดปิด / ข้อมูลไม่มี / user cancel กลางทาง — workflow handle ได้ไหม?
- [ ] **Idempotency** — รันซ้ำ workflow นี้ 2 ครั้งในวันเดียวกัน จะเกิดอะไร? ควบคุมได้ไหม?

ถ้า checklist ข้อไหนไม่ผ่าน → เพิ่ม step หรือ condition ก่อน draft

---

### 7. Self-critique pass — Devil's advocate

ก่อน draft workflow สุดท้าย — วิจารณ์ design เอง:

> "ถ้า workflow นี้รันใน worst-case scenario (ข้อมูลล่าช้า, script fail 1 ตัว, user ไม่ได้อยู่หน้าจอ) — อะไรจะพัง และ workflow ยังให้ output ที่ useful ได้ไหม?"

ระบุ 2-3 weakness ที่เห็น → แก้ใน design ก่อน save

---

### 8. Show proposed design to user

แสดง workflow ที่ออกแบบแล้วในรูปแบบ readable — **ก่อน save**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proposed Workflow: <name>
Domain: <domain> | Estimated: <time>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Jobs covered: N/N
Gaps found: N (flagged in design)
Failure modes modeled: N steps

Steps:
  1. [step-name] → cmd: /x | on-fail: stop
     Why: [1 ประโยค เหตุผลที่ step นี้จำเป็น]
  2. [step-name] → condition: [c] → yes: /y | no: skip | on-fail: continue
     Why: [เหตุผล]
  ...

Gaps that need new commands:
  - [GAP] [job description] → suggest: /new-command
    (สามารถสร้างด้วย /new-workflow ก่อนแล้วค่อย reference)

Weaknesses found (addressed in design):
  - [weakness 1] → mitigated by: [step or condition]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Save this workflow? (yes / modify <what> / discard)
```

ถ้า user พิมพ์ "modify X" → รับ feedback → adjust design → show อีกครั้ง (max 2 rounds)
ถ้า user พิมพ์ "yes" → save

---

### 9. Save workflow definition

Save to: `vault/_workflows/<name>.md`

รูปแบบ richer กว่า `/new-workflow` — รวม:
- Full frontmatter (name, description, domain, estimated-time, schedule, created, designed-by: workflow-design)
- Steps section (ครบทุก step พร้อม `why:` field สำหรับแต่ละ step)
- Conditions Reference table
- Failure Mode Matrix (section ย่อ)
- Edge Cases section (จาก comprehensiveness checklist)
- Gaps section (commands ที่ยังไม่มีแต่ควรสร้าง)
- Design notes (จาก self-critique)

```bash
# Offer to run immediately
echo "บันทึกแล้ว: vault/_workflows/<name>.md"
echo "รัน workflow ทันที? → /workflow <name>"
echo "ตรวจสุขภาพทุก 2 สัปดาห์ → /workflow-audit <name>"
```

---

## Design principles (บังคับ)

- **Domain-first, not wizard-first** — วิเคราะห์ก่อน ถามทีหลัง
- **Every step needs a "why"** — ถ้าอธิบายไม่ได้ว่า step นี้ทำไม → ตัดออก
- **Failure is a feature** — failure mode ของทุก step ต้องถูก modeled ก่อน save
- **Comprehensiveness > simplicity** — ดีกว่าที่จะมี step มากเกินกว่าที่จะขาด step สำคัญ
- **Idempotency awareness** — workflow ที่รันซ้ำแล้วพังระบบคือ workflow ที่ยังไม่สมบูรณ์
- **Self-critique is mandatory** — ห้ามข้าม Step 7 แม้ design จะดูดีแล้ว

## When to use vs /new-workflow

| Situation | Use |
|---|---|
| รู้แน่ๆ ว่าต้องการ steps อะไร | `/new-workflow` |
| Domain ใหม่ ไม่แน่ใจว่าต้องการอะไรบ้าง | `/workflow-design` |
| Project ใหม่ที่ต้องมั่นใจว่าไม่ขาดอะไร | `/workflow-design` |
| แค่ chain 2-3 commands ที่รู้จักอยู่แล้ว | `/new-workflow` |
| Workflow ที่จะใช้ซ้ำนาน ต้องการ robustness | `/workflow-design` |
