---
description: Full research + KB pipeline for a single ticker — stock research, Minnie idea card, Reese doc, Chris+Vera audit, Indie atoms, KB sync. No content draft.
---

# /stock-content

Combined `/stock-research` + `/research-idea` pipeline in one command. Produces a complete investment research note + KB insight atoms in a single run. No content draft (stopped at Step 6).

## Usage

```
/stock-content NVDA
/stock-content MOD — focus on datacenter cooling
```

## Language rule

**ตอบเป็นภาษาเดียวกับที่ user พิมพ์** — Thai เมื่อ user พิมพ์ Thai, English เมื่อ English. Technical terms ใช้ภาษาอังกฤษเสมอ. เนื้อหาในไฟล์ที่ save ให้ใช้ภาษาเดียวกับที่ตอบ user.

---

## STEP 1 — VAULT CHECK

**1A. ตรวจ note เดิมของ ticker:**
```bash
ls vault/20_investment/ | grep -i <TICKER>
```
- ถ้ามี: ถาม user "มี note อยู่แล้วที่ `<path>` — อัปเดต หรือสร้าง version ใหม่?"
- ถ้าไม่มี: ดำเนินต่อ

**1B. ตรวจ KB context:**
ตรวจเป็นลำดับ — โหลดเป็น context ไม่ต้อง save แยก:
1. `vault/Knowledge/THESIS_TRACKER.md` — ticker อยู่ใน active thesis ไหน?
2. `vault/Knowledge/INDEX_insights.md` — มี insight atoms เกี่ยวข้องไหม?
3. `vault/Knowledge/contradiction-registry.md` — มี contradiction ที่รู้แล้วไหม?
4. `vault/Knowledge/nick-signals.md` — ticker มี RSI/MA20/RS valuation tier label ไหม?
5. `vault/10_research/` + `vault/20_investment/` — papers และ notes ที่มีอยู่

ถ้าพบ → ใช้เป็น context ในขั้นต่อไป (vault-first: อย่า re-research สิ่งที่มีอยู่แล้ว)

---

## STEP 2 — RESEARCHER

**Budget: 5 searches max**

ถ้ามี focus angle → จำกัด searches ให้อยู่ใน focus นั้น

| หัวข้อ | Query ตัวอย่าง |
|---|---|
| ธุรกิจ + segment | `<TICKER> business model revenue segments 2025` |
| Earnings + financials | `<TICKER> earnings results revenue margin FCF 2025` |
| Bear case | `<TICKER> bear case short thesis risks 2025` |
| Peer valuation | `<TICKER> valuation P/E EV/EBITDA peers <SECTOR>` |
| Reddit / Seeking Alpha | `<TICKER> site:seekingalpha.com OR site:reddit.com analysis` |

**ข้อมูลที่ต้องดึงมา (ใส่ ❓ ถ้าหาไม่ได้):**

- Business model, revenue segments, key customers, geography
- Revenue TTM, YoY growth, gross margin, FCF, net debt
- P/E, EV/EBITDA — เทียบกับ sector median + historical range 3 ปี
- **Peer snapshot:** 1-2 peer หลักพร้อม forward P/E / EV/EBITDA เพื่อเปรียบเทียบ
- Short interest % of float + vs. average
- Insider ownership % + recent buys/sells (6 เดือน)
- Dilution history (3 ปี)
- CEO name, tenure, track record, red flags
- Next earnings date + consensus EPS estimate
- Competitive moat
- Bull case (3 ข้อ specific)
- Bear case steelman (3 ข้อ — ไม่ใช่ strawman)
- Key catalysts 6-12 เดือน

---

## STEP 3 — STOCK RESEARCH NOTE

- Template: `vault/_templates/stock-research.md`
- Save to: `vault/20_investment/<TICKER>-YYYY-MM-DD.md`
- กรอกทุก section ด้วยข้อมูลจาก Step 2
- **ห้ามเขียน Thesis ให้ user** — เว้นไว้ว่างๆ
- ใส่ `❓ verify` ทุกที่ที่ไม่มีข้อมูลยืนยัน
- Kill conditions: ต้องวัดได้ (metric/event) ไม่ใช่ vague

**เพิ่มใน Decision log:**
- ถ้า ticker อยู่ใน THESIS_TRACKER → note thesis link
- ถ้า nick-signals.md มี label สำหรับ ticker นี้ → note valuation tier

---

## STEP 4 — MINNIE IDEA CARD

อ่านจาก stock-research note ใน context (ห้าม re-read จาก disk — observation masking):

- **Central question:** คำถามหลัก 1 ข้อ
- **Sub-questions (5-8):** กรอบที่ต้องรู้เพื่อตอบ central question
- **Target audience:** ใคร รู้อะไรอยู่แล้ว
- **Hook angles (3):** claim / number / contrast — ระบุ strongest
- **Blind spots:** สิ่งที่คนมักพลาดในหัวข้อนี้

Save: `vault/30_content/ideas/<slug>-<date>.md`

---

## STEP 5 — REESE RESEARCH DOC

สังเคราะห์จาก stock-research + Minnie ใน context:

- **Narrative:** ทำไม story นี้สำคัญตอนนี้ (2-3 ย่อหน้า)
- **Bull case (3):** specific claims ไม่ใช่ vague positive
- **Bear case (3):** steelman — เหตุผลที่ thesis ผิดได้
- **Kill conditions:** metric/event ชัดเจน วัดได้
- **Upside/downside scenario:**
  - Upside: ถ้า bull case ถูก → implied price target (rough multiple expansion)
  - Downside: ถ้า kill condition trigger → implied drawdown
  - คำนวณจาก context — ไม่ต้อง search เพิ่ม
- **Data gaps:** ❓ สิ่งที่ยังไม่รู้และควรรู้

Save: `vault/10_research/<slug>-reese-<date>.md`

---

## STEP 6 — CHRIS + VERA

> **Observation masking:** ทำงานจาก Reese doc ใน context — ห้าม re-read ไฟล์ซ้ำ

**Chris (critic):**
ตรวจ: narrative ชัดไหม, bear case steelman จริงไหม, kill conditions วัดได้ไหม, logic ไหลดีไหม
- ✅ Pass → ไปต่อ
- ⚠️ Revise → ระบุ 3 จุด → แก้ (max 1 round แล้วบังคับ pass)

**Vera (fact audit):**
- Flag ⚠️ ทุก claim ที่ไม่มี source ชัดเจน
- เปลี่ยนเป็น ❓ verify ทุกจุดที่ไม่ confirmed
- ถ้า 2 sources ขัดแย้งกัน → **append ใน `vault/Knowledge/contradiction-registry.md` ทันที**

---

## STEP 7 — INDIE ATOMS

> **Observation masking:** ทำงานจาก Reese doc ใน context — ห้าม re-read ไฟล์ซ้ำ

Extract 3-7 atomic insights จาก research doc ที่ผ่าน Chris+Vera

**Format ต่อ insight:**
```
## [Short title]
**Claim:** [1 ประโยค — falsifiable, ไม่ใช่ opinion]
**Evidence:** [data / quote / source]
**Implication:** [ถ้า claim จริง → หมายความว่าอะไรสำหรับ investment]
**Source:** [URL / report name]
**Date:** YYYY-MM-DD
**Thesis link:** T# (ถ้าเชื่อมกับ thesis ใน THESIS_TRACKER)
```

**Nick-required atoms — ต้อง extract อย่างน้อย 1 atom ต่อหมวด (Nick อ่านแค่ KB — ถ้าไม่มีตรงนี้ Nick ไม่รู้):**
- **Valuation tier:** current multiple vs. historical avg vs. sector median — cheap/fair/expensive
- **Kill condition trigger level:** metric ที่วัดได้ + threshold ชัดเจนที่จะทำให้ thesis หมดอายุ
- **Catalyst timeline:** event ที่ใกล้ที่สุด + วันที่ (earnings / deal close / product launch)

ถ้าหาข้อมูลไม่ได้สำหรับหมวดใด → ใส่ atom ที่ระบุ ❓ explicitly แทน ห้ามข้ามหมวด

**Cross-reference กับ atoms ที่มีอยู่แล้วใน thesis เดียวกัน:**
- ก่อน save → ตรวจ INDEX_insights.md ว่ามี atom ที่เกี่ยวข้องใน T# เดียวกันไหม
- ถ้า reinforce → note ว่า "confirmed by <TICKER> data"
- ถ้าขัดแย้ง → append ใน `vault/Knowledge/contradiction-registry.md`

Save: `vault/Knowledge/insight-atoms/<slug>-<date>.md`
Append: `vault/Knowledge/INDEX_insights.md` (+1 line ต่อ insight)

---

## STEP 8 — THESIS KILL CONDITION CROSS-CHECK

อ่าน THESIS_TRACKER.md ใน context → เทียบ kill conditions ใน Reese doc กับ kill condition ระดับ thesis:
- ถ้า consistent → note ✅ ใน Decision log ของ stock-research note
- ถ้าขัดแย้งหรือ stock-level kill condition แคบกว่า → flag ⚠️ แจ้ง user และ suggest อัปเดต THESIS_TRACKER

---

## STEP 9 — WATCHLIST + REPORT

**Watchlist:**
เพิ่ม ticker ลงใน `config/watchlist.txt` ถ้ายังไม่มี (append ท้ายไฟล์) → `/screen` จะจับอัตโนมัติครั้งถัดไป

**Report back:**
```
บันทึกแล้ว:
  vault/20_investment/<TICKER>-YYYY-MM-DD.md
  vault/30_content/ideas/<slug>-<date>.md
  vault/10_research/<slug>-reese-<date>.md
  vault/Knowledge/insight-atoms/<slug>-<date>.md

ส่วนที่กรอกแล้ว: ✓ <list>
❓ ต้องตรวจสอบเพิ่ม: <list>
❗ เหลือให้คุณกรอกเอง: Thesis, ROI driver, Position sizing, Decision log

Thesis alignment:   T# — <thesis name> ✅ / ⚠️ kill condition conflict
Nick signal:        <RSI/MA20/RS tier ถ้ามี> / ไม่มีข้อมูล
Earnings countdown: X วันถึง earnings (~DATE) — consensus EPS $X
Upside scenario:    ~+X% ถ้า bull case (implied multiple Y)
Downside scenario:  ~-X% ถ้า kill condition trigger
Watchlist:          ✅ เพิ่ม <TICKER> ใน config/watchlist.txt
Contradiction reg:  +N entries (ถ้ามี)
INDEX_insights:     +N entries

Researcher ใช้: N searches

ก่อนตัดสินใจ:
→ เขียน Thesis ในไฟล์ก่อน
→ รัน: /challenge vault/20_investment/<TICKER>-YYYY-MM-DD.md
```

---

## Constraints

- **ห้ามเขียน thesis / buy/sell recommendation ให้ user**
- **ห้ามสร้างตัวเลข** — ❓ ถ้าหาไม่ได้
- **Search budget: 5 searches รวม ทั้ง pipeline**
- **Observation masking:** อ่าน file แล้ว → ทำงานจาก context ห้าม re-read ซ้ำ
- **Partial read:** file > 1000 words → ใช้ offset+limit
- **Scope:** 1 ticker ต่อ invocation
- **ภาษา:** ตาม language rule ด้านบน
