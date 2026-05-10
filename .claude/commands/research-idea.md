---
description: Research → content pipeline. Minnie idea card → KB lookup → sources → Reese research doc → Chris critic + Vera fact audit → Indie insight atoms → Rae content draft. 7 steps.
---

# /research-idea

Research-to-content pipeline: idea → KB → sources → synthesis → critic+audit → insight atoms → content.

## Usage

```
/research-idea <topic> [— angle: <specific angle>] [— output: yt|substack|x|slides|all]
```

ตัวอย่าง:
- `/research-idea NVDA custom ASIC threat — output: yt`
- `/research-idea AI capex cycle 2025 — angle: datacenter winners — output: substack`
- `/research-idea RKLB launch cadence — output: x`

## Language rule

**ตอบเป็นภาษาเดียวกับที่ user พิมพ์** — Thai เมื่อ user พิมพ์ Thai, English เมื่อ English. Technical terms ใช้ภาษาอังกฤษเสมอ. เนื้อหาในไฟล์ที่ save ใช้ภาษาเดียวกับที่ตอบ user.

---

## STEP 1 — MINNIE: Idea Card

สร้าง idea card สำหรับ topic นี้:

- **Central question:** คำถามหลัก 1 ข้อที่ content จะตอบ
- **Sub-questions (5-8):** คำถามย่อยที่ต้องรู้เพื่อตอบ central question
- **Target audience:** ใคร รู้อะไรอยู่แล้ว ต้องการอะไรจาก content นี้
- **Hook angles (3):** 3 วิธีเปิดที่ต่างกัน (claim / number / contrast) — เลือก strongest ใน step 7
- **Blind spots:** อะไรที่คนมักพลาดหรือเข้าใจผิดในหัวข้อนี้

Save: `vault/30_content/ideas/<slug>-<date>.md`

---

## STEP 2 — KB SWEEP

ก่อนวิจัยใหม่ → ค้นหาที่มีอยู่แล้วก่อน (vault + NotebookLM พร้อมกัน):

**2A — Vault grep:**
```bash
grep -ri "<topic>" vault/Knowledge/ vault/10_research/ --include="*.md" -l
```

สร้าง context brief (ใน context เท่านั้น ไม่ต้อง save):
- Theses ที่เกี่ยวข้อง (จาก vault/Knowledge/THESIS_TRACKER.md)
- Insight atoms ที่เกี่ยวข้อง (จาก vault/Knowledge/INDEX_insights.md)
- Papers ที่มีอยู่ใน vault/10_research/
- Contradictions ที่รู้แล้ว (จาก vault/Knowledge/contradiction-registry.md)

**2B — NotebookLM auto-query (ถ้ามี notebook ที่ตรงกับ topic):**
1. เรียก `mcp__notebooklm-mcp__notebook_list` ดู notebook ทั้งหมด
2. ถ้าชื่อ notebook ตรงกับ topic (keyword match) → query ทันทีด้วย sub-questions จาก Minnie
3. ใช้ `mcp__notebooklm-mcp__notebook_query` — ถามรวดเดียว 2-3 ข้อ เช่น:
   - "Key findings on [topic] from these papers?"
   - "What do these papers say about bull/bear case for [topic]?"
4. ผลจาก NotebookLM → รวมใน context brief เหมือน vault (ไม่ต้อง save แยก)

**ถ้า 2A + 2B มี context เพียงพอ** → แจ้ง user และ skip บางส่วนของ step 3 เพื่อประหยัด searches

---

## STEP 3 — SOURCE ANSWERS

**เลือก path ตามประเภท source:**

### Path A — Web search (default)
ใช้เมื่อ: ต้องการข้อมูลสด (earnings, news, analyst estimates)
**Budget: 5 searches max**

| ประเภท | Query |
|---|---|
| Basics | `<topic> analysis 2025` |
| Latest news | `<topic> latest news 2025` |
| Bear case | `<topic> bear case risks problems` |
| Data/numbers | `<topic> revenue margin data statistics` |
| Expert take | `<topic> expert analysis deep dive` |

### Path B — NotebookLM (optional, เมื่อมี doc ยาว)
ใช้เมื่อ: source เป็น PDF ยาว / earnings transcript / annual report / academic paper
**ไม่นับต่อ search budget**

1. แจ้ง user: "Source นี้เหมาะกับ NotebookLM — อัพไฟล์หรือ URL แล้วผมจะ query ให้"
2. User อัพขึ้น NotebookLM (หรือใช้ `/nlm` เพื่อ add source)
3. Query ผ่าน NotebookLM MCP: `mcp__notebooklm-mcp__notebook_query`
4. ผลที่ได้ → ใช้เป็น input ให้ Reese ใน step 4

**ตัวอย่างที่เหมาะกับ Path B:**
- NVDA / AVGO / ASML 10-K หรือ 10-Q (> 100 หน้า)
- Earnings call transcript ยาว (> 30 หน้า)
- arXiv paper หรือ academic research (> 20 หน้า)
- Multiple documents ที่ต้องการ cross-reference

**หมายเหตุ:** Path A และ B ใช้ร่วมกันได้ — web search หาข่าวสด + NotebookLM วิเคราะห์ doc ยาว

สร้าง Q&A doc ใน context: แต่ละ sub-question + คำตอบ + source

---

## STEP 4 — REESE: Research Doc

สังเคราะห์จาก step 2+3:

- **Narrative:** เรื่องราวหลัก 2-3 ย่อหน้า — ทำไม topic นี้สำคัญตอนนี้
- **Bull case (3):** เหตุผลที่ thesis ถูก — ต้องเป็น specific claim ไม่ใช่ vague positive
- **Bear case (3):** steelman — เหตุผลที่ผิดพลาดได้ (ไม่ใช่ strawman)
- **Kill conditions:** อะไรที่จะทำให้ thesis นี้หมดอายุ (ตัวเลข/event/metric ชัดเจน)
- **Data gaps:** อะไรที่ยังไม่รู้และควรรู้ → ใส่ ❓

Save: `vault/10_research/<slug>-reese-<date>.md`

---

## STEP 5 — CHRIS + VERA: Review + Audit

**Chris (critic) — อ่าน research doc → verdict:**
- ✅ Pass: ไปต่อได้
- ⚠️ Revise: ระบุ 3 จุดอ่อน → Reese แก้ (max 1 round แล้วบังคับ pass)

จุดที่ Chris ตรวจ:
- Narrative ชัดไหม? argument ไหลดีไหม?
- Bear case โดนไหม หรือแค่ strawman?
- Kill conditions วัดได้จริงไหม?
- มีจุดไหนที่ตรรกะกระโดดหรือขาดหายไป?

**Vera (fact audit) — ตรวจสอบ claims:**
- Flag ⚠️ ทุก claim ที่ไม่มี source ชัดเจน
- Flag ⚠️ ตัวเลขที่ไม่ verified
- เปลี่ยนเป็น ❓ verify ทุกจุดที่ไม่ confirmed
- ถ้า 2 sources ขัดแย้งกัน → append ใน `vault/Knowledge/contradiction-registry.md`

---

## STEP 6 — INDIE: Extract Insight Atoms

จาก research doc ที่ผ่าน Chris+Vera → extract 3-7 atomic insights

**Format ต่อ insight:**
```
## [Short title]
**Claim:** [1 ประโยค — falsifiable, ไม่ใช่ opinion]
**Evidence:** [data / quote / source ที่สนับสนุน]
**Implication:** [ถ้า claim นี้จริง → หมายความว่าอะไรสำหรับ investment/content]
**Source:** [URL / paper / report name]
**Date:** YYYY-MM-DD
**Thesis link:** T# (ถ้าเชื่อมกับ thesis ใน THESIS_TRACKER)
```

Save: `vault/Knowledge/insight-atoms/<topic>-<date>.md`
Append index: `vault/Knowledge/INDEX_insights.md` (+1 line ต่อ insight: `[date] [cluster] [file] — summary`)

---

## STEP 7 — RAE: Write Content

เขียน content ตาม voice profile ใน `vault/_memory/PREFERENCES.md` เสมอ

ตาม `output` flag:

**yt (YouTube script):**
- Hook (5-7 วิ): claim/number/contrast แรงๆ — เลือก strongest จาก Minnie's 3 hooks
- Body: 3 points แต่ละ point = 1 insight + ตัวอย่าง/ตัวเลขจริง
- CTA: subscribe / comment / next video
- เขียนเป็น script พูดได้เลย (ไม่ใช่ bullet list)
- ใส่ [HOOK] / [POINT 1] / [POINT 2] / [POINT 3] / [CTA] markers

**substack:**
- Hook: ย่อหน้าแรกแรง (ไม่ขึ้นต้น "สวัสดี" หรือ "วันนี้จะ...")
- Context: background 1 section
- 3 key points พร้อม evidence + ตัวเลข
- Case study / ตัวอย่างจริง
- บทสรุป + opinion ของ writer

**x (X thread):**
- Tweet 1: hook (claim / number / question แรงๆ ใน 7 คำแรก)
- Tweets 2-8: numbered points — แต่ละ tweet = 1 insight สมบูรณ์
- Tweet สุดท้าย: CTA (follow / retweet / reply with your take)

**slides:**
- Title slide + 5-10 content slides
- ต่อ slide: title + 3 bullet points + speaker note สั้น

**all:** สร้างทั้ง 4 output types

**ไม่ระบุ output flag** → ถาม user ก่อน step 7

Save: `vault/30_content/<slug>-<output>-<date>.md`

---

## Report back

```
/research-idea เสร็จ: <topic>

Minnie idea card:   vault/30_content/ideas/<slug>-<date>.md
Research doc:       vault/10_research/<slug>-reese-<date>.md
  Chris:            ✅ Pass / ⚠️ Revised (1 round)
  Vera:             N claims flagged ❓
Insight atoms (N):  vault/Knowledge/insight-atoms/<topic>-<date>.md
  INDEX อัปเดต:    +N entries
Content draft:      vault/30_content/<slug>-<output>-<date>.md

KB changes:
  INDEX_insights.md: +N entries
  contradiction-registry.md: +N entries (ถ้ามี)
  THESIS_TRACKER.md: updated (ถ้าพบ thesis ใหม่)

Used: N searches, M vault reads
```

---

## Constraints

- **ห้ามเขียน investment recommendation** — research คือ context ไม่ใช่ advice
- **ห้ามสร้างตัวเลข** — ❓ ถ้าหาไม่ได้
- **Chris verdict revise → max 1 round** — ถ้ายัง fail บอก user + save as-is พร้อม note
- **Indie extracts facts ไม่ใช่ opinions** — claim ต้องเป็น falsifiable ไม่ใช่ "NVDA ดีมาก"
- **Rae ห้าม AI cliche** — ตาม voice profile ใน PREFERENCES.md
- **Budget:** 5 searches, 10 vault reads สำหรับทั้ง pipeline
