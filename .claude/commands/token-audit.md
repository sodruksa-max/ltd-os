---
description: 9-lens token waste audit — identify steps burning tokens without value using cognitive trait detectors.
---

# /token-audit

ตรวจ token waste ใน workflow หรือ session ที่รัน — ใช้ 9 cognitive lenses เพื่อหาขั้นตอนที่กิน tokens โดยไม่จำเป็น

## Usage

```
/token-audit                    — audit current session
/token-audit /pre-market        — audit a specific command
/token-audit /stock-content     — audit stock-content pipeline
/token-audit /nick-weekly       — audit nick-weekly pipeline
```

## Steps

รัน lenses ทั้ง 9 ต่อ workflow หรือ session steps ที่ระบุ — ถ้า audit specific command ให้ Read .claude/commands/<cmd>.md ก่อน:

---

### Lens 1 — KLS: Hibernation Check [KLS: SKIP IF SAME-DAY]

ตรวจ steps ที่ re-read files หรือ re-fetch data ที่เปลี่ยนน้อยกว่า 1×/วัน:
- macro-snapshot.py, news-snapshot.py, nick-signals.md, sector-flow.py
- THESIS_TRACKER.md, TRADING_RULES.md, pre-market-behaviors.md

**Rule:** ถ้า file/script ถูก fetch แล้วใน session นี้ภายใน 4 ชั่วโมง → ใช้ผลเดิม

→ flag `[KLS: SKIP IF SAME-DAY] <step> — data unchanged since <time>`

---

### Lens 2 — Cotard's: Zombie Steps [COTARD: ZOMBIE STEP]

ตรวจ steps ที่ produce output แต่ output นั้นไม่ถูก referenced ใน steps ถัดไปเลย:
- script รันแต่ output ไม่ถูก quote ใน brief
- Vera layer ที่ flag อะไร แต่ไม่มี downstream action
- Search ที่ทำแต่ผลไม่ถูกใช้ใน trade setup

→ flag `[COTARD: ZOMBIE STEP] <step> — output not consumed by any downstream step`

---

### Lens 3 — Alien Hand: Orphan Tool Calls [ALIEN HAND: ORPHAN CALL]

ตรวจ tool calls (Bash/Read/WebFetch) ที่ output ไม่ถูกใช้:
- Read file แต่ไม่มีการ quote หรือ reference เนื้อหาที่อ่าน
- Bash script ที่ exit ด้วยผลลัพธ์ที่ไม่ได้ถูกนำไปไหน
- WebFetch URL ที่ fetch แต่ extract ข้อมูลออกมาไม่เลย

→ flag `[ALIEN HAND: ORPHAN CALL] <tool> <target> — output unread/unused`

---

### Lens 4 — Sleep Paralysis: Duplicate Checks [SLEEP PARALYSIS: DUPLICATE CHECK]

ตรวจ metric ที่ถูก check ซ้ำกันหลาย steps:
- VIX ถูกตรวจใน Reflex scan + Synesthesia + PTSD scan = 3 ครั้ง
- Kill condition ถูก verify ใน step 4 และอีกครั้งใน step 5.5 autism check
- ข่าว macro ถูก fetch ใน script และ web search อีกครั้ง

→ flag `[SLEEP PARALYSIS: DUPLICATE CHECK] <metric> — checked N times in steps: <list>`
→ แนะนำ: merge หรือ centralize check ใน 1 step แล้ว pass result downstream

---

### Lens 5 — Narcolepsy: Early Exit Opportunities [NARCOLEPSY: EARLY EXIT]

ตรวจว่ามี decisive signal ที่ step ต้นๆ ที่ควรหยุดได้เลย:
- VIX > 30 → brief ควรสั้น, ข้าม cognitive layers
- Kill condition triggered ชัดใน step 4 → ข้าม step 5.1-5.43
- Tier 1 flash ชัดพอ → ไม่ต้อง Tier 3 deep pipeline

→ flag `[NARCOLEPSY: EARLY EXIT] possible at step <X> — signal: <signal> — skippable: steps <Y-Z>`

---

### Lens 6 — FOP: Habit Runs [FOP: HABIT RUN]

ตรวจ steps ที่รันทุกครั้งโดยไม่ check ว่า input เปลี่ยนหรือเปล่า:
- sr-levels.py รันทุกวัน แต่ข้อมูล S/R ไม่เปลี่ยนถ้าราคาไม่ผ่าน level
- sector-flow.py รันแม้ market ปิด / weekend
- nick-soul.md อ่านทุก session แม้ไม่มี new entries ตั้งแต่ครั้งก่อน

→ flag `[FOP: HABIT RUN] <step> — inputs unchanged since <date/time>, output identical`

---

### Lens 7 — Dermatographia: Over-Triggering [DERMATOGRAPHIA: OVER-TRIGGER]

ตรวจ steps ที่รัน full pipeline สำหรับ input เล็กน้อย:
- /stock-content รัน Tier 3 (23 Vera layers) สำหรับ ticker ที่มี Reese doc อายุ 2 วัน
- /pre-market รัน cognitive layers ทั้งหมดสำหรับวัน market flat (SPY < 0.3%)
- /nick-weekly รัน 43 steps สำหรับสัปดาห์ที่ SPY range < 1% ไม่มี earnings

→ flag `[DERMATOGRAPHIA: OVER-TRIGGER] <command> — input magnitude: <X>, pipeline depth: Tier <N>, recommend: Tier <M>`

---

### Lens 8 — Anton's: Context-First Violations [ANTON: CONTEXT-FIRST VIOLATION]

ตรวจ tool calls ที่ fetch ข้อมูลที่มีอยู่ใน context แล้ว:
- WebSearch สำหรับ VIX ทั้งที่ macro-snapshot.py รันแล้วใน session นี้
- Read nick-signals.md อีกครั้งหลังอ่านไปแล้วใน step ก่อนหน้า
- Search earnings date ที่มีอยู่ใน catalyst-calendar.py output แล้ว

→ flag `[ANTON: CONTEXT-FIRST VIOLATION] <tool call> — data available at: <prior step / context location>`

---

### Lens 9 — Color Blindness: Verbose Output [COLORBLIND: VERBOSE OUTPUT]

ตรวจ output sections ที่ใช้ prose ทั้งที่ table/list จะกระชับกว่า:
- Catalyst section เป็น paragraph ยาวแทนที่จะเป็น bullet 3 ข้อ
- Kill condition status เป็น narrative แทนที่จะเป็น table: holding | condition | status | distance
- Portfolio verdict เป็น prose แทนที่จะเป็น color map table

→ flag `[COLORBLIND: VERBOSE OUTPUT] <section> — prose: ~N words, table alternative: ~M words (~X% reduction)`

---

## Output format

```
## Token Audit Report — <command> — YYYY-MM-DD

### Lens results
[KLS: SKIP IF SAME-DAY] N steps — potential skip: ~X tokens
[COTARD: ZOMBIE STEP] N steps — dead outputs: ~X tokens
[ALIEN HAND: ORPHAN CALL] N calls — unused fetches: ~X tokens
[SLEEP PARALYSIS: DUPLICATE CHECK] N metrics — redundant checks: ~X tokens
[NARCOLEPSY: EARLY EXIT] N opportunities — skippable at step X: ~X tokens
[FOP: HABIT RUN] N steps — unchanged inputs: ~X tokens
[DERMATOGRAPHIA: OVER-TRIGGER] N commands — over-pipelined: ~X tokens
[ANTON: CONTEXT-FIRST VIOLATION] N calls — re-fetched from context: ~X tokens
[COLORBLIND: VERBOSE OUTPUT] N sections — prose vs table: ~X tokens saved

### Summary
Estimated waste: ~X tokens per session
Top 3 fixes:
1. [fix] — saves ~X tokens — implementation: [how]
2. [fix] — saves ~X tokens — implementation: [how]
3. [fix] — saves ~X tokens — implementation: [how]

### Recommended tier adjustment
Current depth: Tier N (actual)
Recommended: Tier M for [condition]
```

Save report: `vault/_memory/TOKEN_AUDIT_LOG.md` (append, keep last 5 runs)

## Constraints

- ห้าม auto-fix — report only, user approves changes
- ถ้า run ต่อ specific command → อ่านไฟล์ command นั้นก่อน (Read .claude/commands/<cmd>.md)
- ถ้า run ต่อ current session → analyze tool calls ที่รันใน session นี้แล้ว
- ห้ามนับ false positives — Lens 4 (duplicate check) ข้าม steps ที่ check metric เดียวกันแต่ด้วย objective ต่างกัน (เช่น VIX ใน Synesthesia เพื่อ texture vs PTSD เพื่อ threat — ต่างกัน)

## Commit

หลัง /review ผ่าน → รัน:
```bash
bash scripts/safe-commit.sh "notes: token-audit report $(date '+%Y-%m-%d')"
```
