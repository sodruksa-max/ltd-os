---
description: Full research + KB pipeline for a single ticker — stock research note, Reese doc, Chris+Vera audit, Indie atoms, KB sync.
---

# /stock-content

Deep research pipeline สำหรับ 1 ticker. ผลลัพธ์: stock research note + Reese doc + insight atoms ใน KB — ทุกอย่างที่ Nick ต้องการเพื่อตัดสินใจได้.

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

**Output format — คืนเป็น 5 sections นี้เท่านั้น (ห้าม list vault files — vault context โหลดแล้ว ไม่ใช่ findings):**

**[A] Business & Financials**
Revenue TTM, YoY growth, gross margin, FCF, net debt, revenue segments, key customers, geography

**[B] Valuation vs Peers**
P/S, P/E, EV/EBITDA (trailing + forward) — vs sector median + historical range 3 ปี
Peer snapshot: 1-2 peers พร้อม forward multiples เปรียบเทียบ

**[C] Management & Ownership**
CEO name, tenure, track record, red flags
Insider ownership %, sell/buy ratio 6 เดือน, dilution history 3 ปี
Short interest % of float

**[D] Bull / Bear / Catalysts**
Bull case (3 ข้อ specific — ไม่ใช่ vague positive)
Bear case steelman (3 ข้อ — ไม่ใช่ strawman)
Key catalysts 6-12 เดือน พร้อมวันที่
Next earnings date + consensus EPS

**[E] Data conflicts**
ถ้า 2 sources ให้ค่าต่างกัน → list ที่นี่ ไม่ฝังใน sections อื่น

ใส่ ❓ ทุกที่ที่หาไม่ได้ — ห้าม fabricate

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

## STEP 4 — REESE RESEARCH DOC

สังเคราะห์จาก stock-research ใน context:

- **Narrative:** ทำไม story นี้สำคัญตอนนี้ (2-3 ย่อหน้า)
- **Bull case (3):** specific claims ไม่ใช่ vague positive
- **Bear case (3):** steelman — เหตุผลที่ thesis ผิดได้
- **Kill conditions:** metric/event ชัดเจน วัดได้
- **Upside/downside scenario:**
  - Upside: ถ้า bull case ถูก → implied price target (rough multiple expansion)
  - Downside: ถ้า kill condition trigger → implied drawdown
  - คำนวณจาก context — ไม่ต้อง search เพิ่ม
- **Data gaps:** ❓ สิ่งที่ยังไม่รู้และควรรู้

**HisRubric self-check ก่อน save (3 dimensions):**
- Data sourcing: ทุก claim มี source ชัดเจนหรือ ❓ explicit — ไม่มี bare assertion
- Reasoning quality: bull/bear logic ไม่มี circular reasoning หรือ vague qualifier ("strong growth")
- Conclusion validity: kill conditions วัดได้จริง (metric threshold / event / date) — ไม่ใช่ "outlook แย่ลง"
ถ้า dimension ใดไม่ผ่าน → แก้ก่อน save

Save: `vault/10_research/<slug>-reese-<date>.md`

---

## STEP 5 — CHRIS + VERA

> **Observation masking:** ทำงานจาก Reese doc ใน context — ห้าม re-read ไฟล์ซ้ำ

**Chris (critic) — structured scorecard:**
ให้คะแนน 3 dimensions (1-5, 5=ดีที่สุด):
- **Kill condition measurability:** kill conditions วัดได้จริง (metric/event/date) หรือยัง
- **Claim verifiability:** claim หลักมี source หรือ ❓ ชัดเจนไหม
- **Bull/Bear balance:** bear case เป็น steelman จริงไหม หรือ strawman

Output format: `Chris score: KM=X / CV=X / BB=X (total X/15)`
- Score ≥ 12/15 → ✅ Pass → ไปต่อ
- Score < 12/15 → ⚠️ Revise → ระบุ dimension ที่ต่ำสุด + 2 จุดที่ต้องแก้ → แก้แล้ว pass (max 1 round)

**Vera Tourette Reflex Layer (รันก่อน deep audit — scan-and-fire pass):**

อ่าน Reese doc แบบ **วิ่งตาเร็วๆ ทั้งเล่มก่อน** — ไม่ deep read ทีละบรรทัด:
ทุกครั้งที่มีอะไรขัดกับ KB ที่รู้อยู่แล้วหรือ "รู้สึกว่าผิด" → flag ทันทีก่อนอ่านต่อ

```
[REFLEX CONTRA] <claim> — ขัดกับ <KB source / prior knowledge> ณ จุดแรกที่เห็น
```

กฎ: **ห้าม suppress reflex** แม้จะคิดว่า "น่าจะ resolve ได้ทีหลัง" — reflex ทุกตัวต้องปรากฏ
ถ้า autism layer resolve ทีหลัง → note `[REFLEX RESOLVED]`; ถ้าไม่ resolve → priority contradiction

Vera สรุป tourette reflex ก่อนเริ่ม deep audit:
```
Vera Reflex Summary: fired N / resolved M / priority unresolved K
```

**Vera (fact audit) — Autism Memory Edition:**
- Flag ⚠️ ทุก claim ที่ไม่มี source ชัดเจน
- เปลี่ยนเป็น ❓ verify ทุกจุดที่ไม่ confirmed
- **FAITH numerical rule:** ตัวเลขทุกตัว (revenue, growth rate, EPS, market size, margin) ต้อง trace กลับ source ได้ก่อน mark ✓ — ถ้า verify ไม่ได้ → flag ⚠️ UNVERIFIED NUMERIC (ไม่ใช่แค่ ❓)
- ถ้า 2 sources ขัดแย้งกัน → **append ใน `vault/Knowledge/contradiction-registry.md` ทันที**

**Vera Autism Layer (รันหลัง flag เสร็จ — cross-document memory):**

1. **Historical claim check:** อ่าน INDEX_insights.md → หา atoms ที่เกี่ยวกับ TICKER นี้หรือ thesis เดียวกัน
   - ถ้ามี atom เก่า (> 60 วัน) ที่พูดเรื่องเดียวกับ claim ในเอกสารนี้ → เปรียบเทียบ
   - ถ้าตรงกัน → `[CONFIRMED by prior atom <date>]`
   - ถ้าขัดแย้ง → `⚠️ STALE CONFLICT: current doc says X, atom from <date> says Y — append to registry`

2. **Echo detection:** ต่อแต่ละ claim ที่ถูก cite จากหลาย sources:
   - Trace กลับ: sources ทั้งหมดนั้น cite จาก source เดิมไหม?
   - ถ้าใช่ → flag: `⚠️ ECHO: 3 sources ล้วน cite <original source> — ไม่ใช่ independent replication`
   - ถ้าเป็น independent → flag: `✓ INDEPENDENTLY REPLICATED`

3. **Systematic gap detection:** ดู atoms ทั้งหมดของ TICKER/thesis นี้ใน vault
   - ถ้า dimension เดียวกัน (เช่น valuation, moat, management) มี ❓ ≥ 3 ครั้งใน atoms ต่างกัน → flag: `⚠️ SYSTEMATIC GAP: <dimension> — ไม่มีข้อมูลมาตลอด X เดือน`

4. **Stale claim detection:** ถ้า claim ใดใน Reese doc ดูเหมือนอิงข้อมูลที่อาจ outdated:
   - เช็ค date ของ source: ถ้า > 6 เดือน สำหรับ financial data หรือ > 12 เดือน สำหรับ structural data → flag: `⚠️ POSSIBLY STALE: claim based on data from <date>`

Vera สรุป autism check ท้าย section:
```
Vera Autism Summary:
- Confirmed by prior atoms: N claims
- Echo detected: N claims (single-source masquerading as consensus)
- Systematic gaps: [list dimensions]
- Stale claims: N claims (data > 6 months)
- New contradictions logged: N entries
```

**Vera Savant Precision Audit (รันหลัง autism layer — enforce exact numbers):**

ต่อทุกตัวเลขที่ผ่านมาใน Reese doc — ตรวจว่า exact หรือ approximate:

**Imprecision flags (บังคับ exact หรือ mark unverified):**
- "ประมาณ", "about", "roughly", "~X", "double digits", "strong growth", "significant margin" → `[SAVANT: IMPRECISE]` — ต้องหา exact value
- Revenue / EPS / margin ที่ไม่ระบุ FY หรือ quarter → `[SAVANT: UNANCHORED]` — ต้องระบุ period
- ตัวเลขที่ไม่ระบุ date ของ source → `[SAVANT: UNDATED]` — ต้องระบุ data date

**Critical numbers → Savant Archive:**
ตัวเลขที่ verified exact แล้ว และ critical ต่อ thesis หรือ kill condition → append ใน `vault/Knowledge/savant-numbers.md`:
```
[TICKER] [DATE-VERIFIED] [METRIC] = [EXACT VALUE] | Source: [source, date] | Relevant to: [thesis/kill condition]
```

Vera สรุป savant audit:
```
Vera Savant Summary:
- [SAVANT: IMPRECISE] N — imprecise numbers flagged
- [SAVANT: UNANCHORED] M — numbers without period anchor
- Critical numbers archived: K → savant-numbers.md
```

**Vera Synesthesia Multi-Modal Encoding (รันหลัง savant audit — encode ตัวเลขสำคัญแบบ multi-axis):**

ต่อทุก metric ที่ verified exact แล้ว — แปลงเป็น relative position พร้อมกัน 3 แกน:

**3 axes ต่อ metric:**
- **vs Peer median** — [ABOVE ✓] / [AT MEDIAN ~] / [BELOW ✗]
- **vs Own 3Y history** — [NEAR HIGH ↑] / [MID RANGE →] / [NEAR LOW ↓]
- **vs Kill condition** — [SAFE: DISTANT] / [WATCH: APPROACHING] / [DANGER: AT THRESHOLD]

**Format:**
```
[METRIC] [VALUE] [vs PEER] [vs HISTORY] [vs KILL]
```
ตัวอย่าง:
```
FCF margin 18% [ABOVE MEDIAN ✓] [NEAR 3Y HIGH ↑] [KILL: DISTANT]
Revenue growth 12% YoY [BELOW MEDIAN ✗] [MID RANGE →] [WATCH: APPROACHING]
Gross margin 54% [AT MEDIAN ~] [MID RANGE →] [SAFE: DISTANT]
```

**กฎ: ถ้า metric มี 2+ axes ที่เป็น warning ([BELOW ✗] / [NEAR LOW ↓] / [WATCH] หรือแย่กว่า) → flag `[SYNESTHESIA WARN]`**

Vera สรุป synesthesia encoding:
```
Vera Synesthesia Summary:
- Metrics encoded: N
- [SYNESTHESIA WARN] M — metrics with 2+ warning axes
- Encoding available for: Nick kill check / Reese narrative context
```

---

## STEP 6 — INDIE ATOMS

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
**Theme cluster:** [เลือก 1 tag — macro/ai-capex | macro/rates | sector/semicon | sector/quantum | sector/defense | sector/software | risk/concentration | risk/dilution | risk/competition | catalyst/earnings | catalyst/contract | catalyst/product]
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

## STEP 7 — THESIS KILL CONDITION CROSS-CHECK

อ่าน THESIS_TRACKER.md ใน context → เทียบ kill conditions ใน Reese doc กับ kill condition ระดับ thesis:
- ถ้า consistent → note ✅ ใน Decision log ของ stock-research note
- ถ้าขัดแย้งหรือ stock-level kill condition แคบกว่า → flag ⚠️ แจ้ง user และ suggest อัปเดต THESIS_TRACKER

---

## STEP 8 — WATCHLIST + REPORT

**Watchlist:**
เพิ่ม ticker ลงใน `config/watchlist.txt` ถ้ายังไม่มี (append ท้ายไฟล์) → `/screen` จะจับอัตโนมัติครั้งถัดไป

**Thesis convergence refresh:**
หลัง Indie atoms บันทึกแล้ว → regenerate convergence report เพื่อให้ Nick เห็น signal ล่าสุด:
```bash
code/python/.venv/Scripts/python scripts/thesis-convergence.py
```

**Report back:**
```
บันทึกแล้ว:
  vault/20_investment/<TICKER>-YYYY-MM-DD.md
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

## Commit

Chris+Vera (Step 5) คือ review gate ของ pipeline นี้ — ไม่ต้องรัน `/review` ซ้ำ
Stage ทุกไฟล์ที่สร้างแล้ว commit:
```bash
git add vault/20_investment/<TICKER>-<DATE>.md \
        vault/10_research/<slug>-reese-<DATE>.md \
        vault/Knowledge/insight-atoms/<slug>-<DATE>.md \
        vault/Knowledge/INDEX_insights.md \
        vault/Knowledge/contradiction-registry.md \
        vault/Knowledge/thesis-convergence.md \
        config/watchlist.txt
bash scripts/safe-commit.sh "vault: stock-content <TICKER>"
```
