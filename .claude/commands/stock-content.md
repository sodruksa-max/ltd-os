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

**Hierarchical retrieval rule (arXiv:2602.03442 A-RAG) — escalate เฉพาะเมื่อ lower level ไม่พอ:**
1. **Vault grep ก่อนเสมอ** — `grep -ri "<TICKER>" vault/` → ถ้าพบ note ที่ครอบ dimension นั้นแล้ว → ใช้เลย ไม่ต้อง search
2. **Keyword web search** — เฉพาะ dimension ที่ vault ไม่มี → search 1 query ต่อ gap
3. **Full-page fetch** — เฉพาะเมื่อ keyword search ให้ snippet ไม่พอ → fetch 1 URL ที่ most relevant
- ห้าม jump ไป web search โดยไม่ตรวจ vault ก่อน → ลด redundant searches

**Query generation rule (arXiv:2510.10009 ExpandSearch):** ก่อนรัน search แต่ละ turn — generate 4-5 semantically distinct sub-queries ก่อน (เช่น `NVDA data center Q1 2025` / `Jensen Huang FY2026 guidance` / `NVDA gross margin trend` / `NVDA China export impact`) แทนที่จะค้นด้วย 1 query — sub-queries ต้องต่างกัน semantic (ไม่ใช่แค่ rephrase) เพื่อ surface diverse evidence

| หัวข้อ | Query ตัวอย่าง |
|---|---|
| ธุรกิจ + segment | `<TICKER> business model revenue segments 2025` |
| Earnings + financials | `<TICKER> earnings results revenue margin FCF 2025` |
| Bear case | `<TICKER> bear case short thesis risks 2025` |
| Peer valuation | `<TICKER> valuation P/E EV/EBITDA peers <SECTOR>` |
| Reddit / Seeking Alpha | `<TICKER> site:seekingalpha.com OR site:reddit.com analysis` |

**Adaptive rewriter rule (arXiv:2502.15684 FinSearch):** หลังแต่ละ search call → ตรวจว่า dimension ไหนใน [A]-[E] ยังขาดข้อมูล → reformulate sub-query ถัดไปโดย target gap นั้นโดยตรง (ไม่ใช่ fixed query plan) — หยุดเมื่อ dimensions ครบหรือ budget หมด

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

**Coverage matrix check (arXiv:2508.05668 Deep Search Agents Survey):** หลัง search เสร็จทั้งหมด — fill matrix ก่อนส่งต่อ Step 3:

| Dimension | Web news | SEC/Earnings | Vault atoms | Macro KB |
|---|---|---|---|---|
| Revenue growth | | | | |
| Margin | | | | |
| Competitive moat | | | | |
| Macro sensitivity | | | | |
| Management | | | | |
| Valuation | | | | |

Cell = ✓ (has evidence) / ❓ (empty) — empty cells = gaps ที่ flag ใน [E] Data conflicts และใน Reese doc Data gaps section; หยุด search เมื่อ matrix เต็มหรือ budget หมด ไม่ใช่ fixed N queries

**Trajectory Prune (arXiv:2509.23586 AgentDiet) — บังคับก่อนส่งต่อ Step 3:**
ณ จุดนี้ raw search queries, URL snippets, และ intermediate tool outputs ถือว่า "expired" — synthesized แล้วใน [A]-[E]
- ส่งต่อ Step 3-6 **เฉพาะ structured [A]-[E] sections เท่านั้น**
- ห้าม carry raw search results, ห้าม re-read source URLs, ห้าม re-quote snippets
- Step 3, 4, 5, 6 ทำงานจาก [A]-[E] + vault KB เท่านั้น → −40-60% input tokens ต่อ downstream step

---

## STEP 3 — STOCK RESEARCH NOTE
*(arXiv:2601.22037 Meta-tool collapse: Step 2 [A]-[E] → Step 3 template เป็น single cognitive pass — ห้ามทำเป็น 2 turn แยก; เขียน template โดยตรงจาก [A]-[E] ที่อยู่ใน context ไม่ต้อง re-read [A]-[E] ก่อน)*

- Template: `vault/_templates/stock-research.md`
- Save to: `vault/20_investment/<TICKER>-YYYY-MM-DD.md`
- กรอกทุก section ด้วยข้อมูลจาก Step 2
- **ห้ามเขียน Thesis ให้ user** — เว้นไว้ว่างๆ
- ใส่ `❓ verify` ทุกที่ที่ไม่มีข้อมูลยืนยัน
- Kill conditions: **SPO triplet format** — Subject (metric) + Predicate (condition) + Object (exact threshold + duration) + Time horizon (when to check) + Source — เช่น `gross margin | falls below | 40% GAAP for 2 consecutive quarters | check at each earnings | company IR` — ถ้า kill condition ยังไม่สามารถแปลงเป็น SPO ได้ → ไม่ผ่าน Step 4.5

**เพิ่มใน Decision log:**
- ถ้า ticker อยู่ใน THESIS_TRACKER → note thesis link
- ถ้า nick-signals.md มี label สำหรับ ticker นี้ → note valuation tier

---

## STEP 4 — REESE RESEARCH DOC

สังเคราะห์จาก stock-research ใน context:

- **Narrative:** ทำไม story นี้สำคัญตอนนี้ (2-3 ย่อหน้า)
- **Bull case (3):** specific claims ไม่ใช่ vague positive
- **Bear case (3):** steelman — เหตุผลที่ thesis ผิดได้
- **Kill conditions:** SPO triplet — Subject (metric) + Predicate (threshold condition) + Object (exact value + duration) + Time horizon (when to check) + Source (verifiable source) — ดู Step 4.5 Claim Extraction สำหรับ validation; ถ้า kill condition ใดแปลงเป็น SPO ไม่ได้ = not measurable, ต้องแก้
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

**Social Anxiety — Narrative Perception Audit (รันก่อน save Reese doc):**

> "ถ้า skeptical analyst อ่าน doc นี้ — เขาจะมองว่า narrative ลำเอียงอย่างไร?"

สแกนหา perception bias ใน 3 มิติ:
- **Bull case tone:** ฟังดู overconfident หรือ aspirational เกินไปไหม? คำที่ signal: "clear winner", "inevitable", "only player", "dominant"
- **Bear case tone:** ฟังดูเป็น strawman ที่ตั้งไว้เพื่อ knock down ง่ายๆ ไหม? bear case ที่แข็งแกร่งควรทำให้ลังเล ไม่ใช่รู้สึกว่า "โอเคมีความเสี่ยงแต่ไม่น่าเป็นห่วง"
- **Kill conditions:** ฟังดู abstract หรือ vague ไหม? เช่น "ถ้า competitive landscape เปลี่ยน" vs "ถ้า gross margin < 40% สองไตรมาสติด"

ต่อแต่ละ bias ที่พบ → flag `[SA: NARRATIVE BIAS]` + ระบุประโยคที่ต้องแก้

ถ้าไม่พบ → `SA Narrative Audit: balanced ✅`

**Paranoid — Consensus Distrust Check (รันก่อน save Reese doc):**

ถ้า analyst consensus ≥ 80% bullish หรือ ≥ 80% bearish → ตรวจ 3 คำถาม adversarial:

**1. Who benefits from this consensus?**
- Sell-side ที่ upgrade มี banking/underwriting relationship กับบริษัทนี้ไหม?
- Consensus bullish ตรงกับช่วงที่ insider กำลัง distribute หรือ lock-up ใกล้หมดไหม?
- ถ้า consensus bearish — short sellers ที่มี large position กำลัง build narrative ไหม?

**2. Who disagrees and why?**
- ค้นหา dissenting analyst หรือ short report ที่ขัดกับ consensus
- ถ้าหาคนที่ไม่เห็นด้วยไม่ได้เลย → อาจเป็นสัญญาณว่า information ยังไม่ complete

**3. Is it already priced in?**
- ถ้า consensus 80%+ bullish แต่ราคาขึ้นมาแล้ว > 30% ใน 6 เดือน → upside อาจ exhausted
- Sentiment extreme มักเป็น contrarian signal ไม่ใช่ momentum signal

→ flag `[PARANOID: CONSENSUS TRAP] <direction> — N% consensus, priced in: [yes/no/partial]`
→ flag `[PARANOID: SELL-SIDE INCENTIVE]` ถ้าพบ banking relationship ที่ conflict

```
Paranoid Consensus Check: [N% bullish / N% bearish]
Threshold triggered: [yes / no — N < 80%]
Adversarial finding: [PARANOID: CONSENSUS TRAP / SELL-SIDE INCENTIVE / clean]
Implication: [fade consensus / wait for re-rating / proceed with caution]
```

ถ้า consensus ไม่ถึง threshold → `Paranoid: consensus not extreme ✅`

**Stendhal Thesis Overwhelm check** — ตรวจ conviction ที่สูงผิดปกติใน Reese doc:
1. นับ superlative/absolute language ใน bull case ("unprecedented", "inevitable", "only", "perfect", "best in class")
2. ถามตัวเอง: มี ≥2 ugly elements — ตัวเลขที่แย่, risk ที่ยังแก้ไม่ได้, หรือ bear ที่ยังไม่มีคำตอบ?
3. ถ้า superlatives ≥3 AND ugly elements < 2 → `[STENDHAL: THESIS OVERWHELM]` — ต้องใส่ explicit bear scenario ก่อน save

ถ้าไม่มี overwhelm pattern → `Stendhal: thesis balanced ✅`

Save: `vault/10_research/<slug>-reese-<date>.md`

---

## STEP 4.5 — CLAIM EXTRACTION (Reese → Vera bridge)

*จาก arXiv:2505.19197 (KPI schema extraction) + arXiv:2602.11886 (SPO triplets)*

> **Observation masking:** ทำงานจาก Reese doc ใน context — ห้าม re-read ไฟล์ซ้ำ

แปลง bull case, bear case, และ kill conditions ของ Reese ทุกข้อเป็น **Claim Records** — Vera จะ audit records เหล่านี้แทน free text ทำให้ตรวจจับ hallucination ได้แม่นกว่ามาก

**Format ต่อ claim:**
```
[CLAIM-RECORD]
Claim: <exact claim text จาก Reese — 1 ประโยค active voice>
Type: bull / bear / kill-condition / data-point
Subject: <metric หรือ entity หลัก>
Predicate: <relationship — "exceeds" / "falls below" / "grows faster than" / "captures share from">
Object: <threshold หรือ comparison point — exact value ถ้ามี>
Time horizon: <quarter / year / event ที่ claim จะ verifiable>
Source reference: <URL / earnings release / filing — หรือ ❓>
Verifiable now: yes / no / partial
```

**Kill condition SPO rule (บังคับ):**
Kill condition ทุกข้อต้องแปลงเป็น SPO triplet ที่วัดได้:
- **Subject** = metric ที่วัดได้ (เช่น "gross margin")
- **Predicate** = threshold condition (เช่น "falls below")
- **Object** = exact threshold + duration (เช่น "40% for 2 consecutive GAAP quarters")
- ถ้า kill condition ใดยังไม่สามารถแปลงเป็น SPO ได้ → flag `[KILL: NOT MEASURABLE]` + แก้ Reese doc ก่อนผ่าน Step 5

**Passive voice pre-processing:**
ก่อนแปลง claim ใดเป็น record — flip passive constructions เป็น active form ก่อนเสมอ:
- "Revenue was guided down by management" → "Management guided revenue down"
- ถ้า subject เปลี่ยนหลัง flip → บันทึก subject ใหม่ใน record

**Output ท้าย Step 4.5:**
```
Claim Extraction Summary:
- Bull claims: N records
- Bear claims: N records
- Kill condition SPO triplets: N (all measurable ✅ / M [KILL: NOT MEASURABLE] ⚠️)
- Claims with source reference: N / total
- Claims needing passive-voice flip: N
```

Claim records อยู่ใน context — Vera ใช้ใน Step 5 แทน free text

---

## STEP 5 — CHRIS + VERA

> **Observation masking:** ทำงานจาก Reese doc ใน context — ห้าม re-read ไฟล์ซ้ำ

> **Structured-output-only rule (arXiv:2601.04426):** Vera output ต้องเป็น structured format เท่านั้น — ห้ามมี narrative preamble หรือ reasoning prose ก่อน output; เริ่มต้นด้วย flag/score table ทันที ไม่มี "Let me analyze..." หรือ paragraph อธิบาย → ตัด preamble tokens ก่อนส่งต่อ Indie

> **Parallel execution rule (arXiv:2511.07784):** Chris และ Vera ต้อง run อิสระจากกัน — **Vera ห้ามเห็น Chris critique ก่อนที่ Vera จะ run fact-check เสร็จ** เพื่อป้องกัน conformity bias รัน Chris ก่อน (บันทึก output ไว้ในใจ) → รัน Vera โดยไม่ใช้ Chris output เป็น context → reconcile ทั้งคู่หลังเสร็จ; ถ้า Chris และ Vera ขัดแย้งกัน → เชื่อ Vera (data-first) ไม่ใช่ Chris (logic-first)

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
- **Passive voice rule (arXiv:2602.11886):** ก่อน check subject identity ของ claim ใดๆ — flip passive constructions เป็น active form ก่อนเสมอ ("Revenue was guided down" → "Management guided revenue down") — passive voice คือ root cause หลักของ subject hallucination ใน financial text; ถ้า subject เปลี่ยนหลัง flip → re-verify claim ใหม่ทั้งหมด
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

**Vera Hyperlexia Fine-Print Audit (รันหลัง synesthesia — อ่านทุกตัวอักษรที่คนอื่นข้าม):**

สแกน source documents ที่ใช้ใน research (10-K, 10-Q, earnings release, press release) โดยเฉพาะ:
- **Footnotes และ MD&A Risk Factors** — อ่านทุกบรรทัด ไม่ข้าม
- **Earnings call Q&A** — ไม่ใช่แค่ prepared remarks
- **Forward-looking statements section** — หา qualifiers ที่ซ่อนไว้

**Flag patterns:**
- Adjusted metric qualifier: "excluding", "non-GAAP", "adjusted", "constant currency", "ex-acquisitions" → `[HYPERLEXIA: ADJUSTED METRIC]` + หา unadjusted value
- Evasion patterns in Q&A: คำถามที่ถามซ้ำ 2+ ครั้งโดย analyst ต่างคนแต่ยังไม่ได้คำตอบตรงๆ → `[HYPERLEXIA: EVASION]`
- Risk factor language ที่ escalated จาก prior filing: เช่น "may" เปลี่ยนเป็น "could materially affect" → `[HYPERLEXIA: ESCALATED RISK]`

Vera สรุป hyperlexia audit:
```
Vera Hyperlexia Summary:
- [HYPERLEXIA: ADJUSTED METRIC] N — unadjusted values needed
- [HYPERLEXIA: EVASION] M — Q&A deflections logged
- [HYPERLEXIA: ESCALATED RISK] K — risk language strengthened vs prior filing
```

**Vera Misophonia Trigger Registry Scan (รันหลัง hyperlexia — check ต่อ trigger registry):**

```bash
cat vault/Knowledge/misophonia-triggers.md | grep "^\[" | grep -v "Market-Level" | head -30
```

Check ทุก Company-Level trigger ใน registry ต่อ source documents ที่อ่านมาแล้ว:
- Any match → `[MISOPHONIA: TRIGGER] <pattern name>` — ห้าม suppress, ห้าม rationalize ทิ้ง
- ต้องถูก address ใน Reese doc หรือ contradiction-registry ก่อนจบ pipeline

Vera สรุป misophonia scan:
```
Vera Misophonia Summary:
- Triggers checked: N (จาก registry)
- [MISOPHONIA: TRIGGER] M fired — must address before proceeding
- Registry path: vault/Knowledge/misophonia-triggers.md
```
ถ้าไม่พบ trigger → `Misophonia scan: clean ✅`

**Vera Layer 7 — HSP Communication Shift Detection**

เปรียบเทียบ tone ของ management communication ระหว่างรอบนี้กับรอบก่อน — HSP จับ shift เล็กๆ ที่ตัวเลขไม่บอก

ตรวจ 3 shift patterns:

**1. Confidence Shift** — เปรียบ earnings call transcript รอบนี้กับรอบก่อน:
- คำที่หายไป: "we are confident", "strong demand", "accelerating" → replaced by hedging language
- คำที่เพิ่มขึ้น: "monitoring", "remain cautious", "dependent on", "subject to"
→ flag `[HSP: CONFIDENCE SHIFT]` — "CFO tone เปลี่ยนจาก [X] เป็น [Y]: [quote]"

**2. Specificity Drop** — management เริ่มตอบคำถามด้วย narrative แทน numbers:
- Q: "guidance Q4?" → A: "we expect to perform well in line with market conditions" (ไม่มีตัวเลข)
- Q: "margin pressure?" → A: "we're focused on operational excellence" (ไม่ตอบตรง)
→ flag `[HSP: SPECIFICITY DROP]` — "คำถาม X ตอบด้วย narrative ไม่ใช่ตัวเลข"

**3. Body Language Signals** (สำหรับ video earnings calls เท่านั้น):
- ถ้าไม่มี video → ข้ามขั้นตอนนี้

```
HSP Communication Shift: [TICKER]
Prior call tone: [confident / neutral / cautious]
Current call tone: [confident / neutral / cautious]
Shift direction: [more confident / no change / less confident]
Flags: [HSP: CONFIDENCE SHIFT / HSP: SPECIFICITY DROP / none]
Signal: [1 ประโยค — implication ต่อ thesis]
```

ถ้าไม่มี prior call data → `HSP Communication Shift: baseline only (no prior to compare) ✅`

**Vera Layer 8 — Alexithymia Emotional Language Purge**

อ่าน research doc ทั้งหมดอีกครั้งในฐานะผู้ตรวจสอบที่ไม่มีความรู้สึก — ลบทุกภาษาที่มี emotional loading

ตรวจหาและ flag แต่ละ instance:

| Pattern | ตัวอย่าง | แทนด้วย |
|---|---|---|
| Excitement language | "exciting opportunity", "remarkable growth" | "revenue grew X% YoY" |
| Hope language | "should recover", "expected to improve" | "consensus estimates +X% — verify source" |
| Narrative dependency | "the story is compelling" | "thesis depends on [metric] reaching [X]" |
| Vague conviction | "strong management team" | "CEO tenure X years, [specific achievement]" |
| Disaster language | "catastrophic risk", "could collapse" | "downside scenario: -X% revenue if [condition]" |

→ flag `[ALEXITHYMIA: VAGUE] "<phrase>" → replace: "<data-based alternative>"`

ถ้าพบ 3+ instances → append note ใน Reese doc: "⚠️ Alexithymia audit: doc contains emotional language — verify core claims with data before acting"

```
Alexithymia Purge: [N] emotional phrases found
- [ALEXITHYMIA: VAGUE] "<phrase>" → "[replacement]"
Overall doc tone: [data-driven / partially emotional / heavily emotional]
Action needed: [none / verify [N] claims / rewrite section]
```

ถ้าไม่พบ → `Alexithymia purge: clean ✅`

**Vera Layer 9 — AIWS Magnitude Audit**

เทียบ market reaction กับ fundamental impact จริงๆ — ตรวจว่า market กำลัง misprice ขนาดของ event นี้ไหม

**Over-reaction pattern** (ราคา react มากกว่า fundamental warrant):
- EPS miss/beat X% แต่ราคาเปลี่ยน > 3×X%
- ข่าว one-time (CEO comment, analyst upgrade) ทำให้ราคาเปลี่ยน > 5% โดยไม่มี fundamental shift
- Revenue miss เล็กน้อย (<3%) แต่ตลาดลงมากกว่า historical avg สำหรับ miss ขนาดนี้
→ flag `[AIWS: OVER-REACTION] "<event>" — price moved X%, fundamental impact = Y%`
→ implication: mean-reversion opportunity ภายใน 2-4 สัปดาห์

**Under-reaction pattern** (ราคา react น้อยกว่า fundamental warrant):
- Revenue growth accelerated อย่างมีนัยสำคัญ แต่ราคา flat หลัง earnings
- Margin expansion เกิน consensus estimate แต่ตลาดไม่ re-rate multiple
- Catalyst structural (ไม่ใช่ one-time) แต่ตลาด treat เป็น noise
→ flag `[AIWS: UNDER-REACTION] "<event>" — price moved X%, implied fundamental impact = Y%`
→ implication: accumulation opportunity ก่อนตลาดรับรู้ delayed impact

```
AIWS Magnitude Audit: [TICKER]
Event: [most recent significant event]
Price reaction: [+/-X%]
Fundamental impact estimated: [+/-Y% to revenue/EPS/margin]
Scale verdict: [PROPORTIONAL / [AIWS: OVER-REACTION] / [AIWS: UNDER-REACTION]]
Trade signal: [none / mean-revert / accumulate ahead of repricing]
```

ถ้าไม่มี recent significant event → `AIWS magnitude: no event to calibrate ✅`

**Vera Layer 10 — Aura Scotoma Map** [AURA: SCOTOMA]

ตรวจ blind spots ใน research — สมมติฐานที่ thesis พึ่งพาแต่ไม่มี evidence รองรับ:

```
Scotoma scan:
- Addressable market size: [sourced / [AURA: SCOTOMA — assumed]]
- Competitive moat duration: [sourced / [AURA: SCOTOMA — assumed]]
- Management execution track record: [sourced / [AURA: SCOTOMA — assumed]]
- Regulatory/macro assumptions: [sourced / [AURA: SCOTOMA — assumed]]
- Customer concentration risk: [sourced / [AURA: SCOTOMA — assumed]]
Scotoma count: N
```

ถ้า ≥2 scotomas → prepend `⚠️ Scotoma Count: N` ใน Vera section header
ถ้า < 2 → `Aura: scotoma within range ✅`

**Vera Layer 11 — Split-Brain Narrative vs Data Gap** [SPLIT-BRAIN: NARRATIVE VS DATA GAP]

ตรวจว่า narrative ใน Reese doc grounded ด้วย data หรือเป็น narrative ล้วนๆ:

```
Narrative claim: [สรุป thesis หลัก 1 ประโยค]
Data anchor: [metric/filing/event ที่รองรับ claim โดยตรง]
Gap verdict: [GROUNDED / [SPLIT-BRAIN: NARRATIVE VS DATA GAP]]
```

ถ้า GAP → ใส่ ❓ ที่ claim นั้น + note "narrative-only, unverified by data"
ถ้าไม่มี gap → `Split-Brain: narrative grounded ✅`

**Vera Layer 12 — Semantic Satiation Buzzword Strip** [SATIATION: BUZZWORD]

สแกนหาคำที่ใช้ซ้ำจนหมด meaning: "AI-powered", "platform", "ecosystem", "flywheel", "moat", "secular tailwind", "best-in-class", "disruptive":

```
Buzzwords found: [list]
Count: N
Required replacements: [buzzword → metric ที่วัดได้แทน]
```

ถ้า ≥4 → `[SATIATION: BUZZWORD]` — mandatory: แทนที่ด้วย specific metrics ก่อน approve note
ถ้า < 4 → `Satiation: language specific ✅`

**Vera Layer 13 — Hyperosmia: Faint Language Degradation**

สแกนภาษาใน filing/transcript แบบ hypersensitive — จับ shift เล็กๆ ที่ Hyperlexia อาจพลาดเพราะเน้น explicit flags

**Faint signals ที่ต้องดม:**
- คำเดี่ยวที่เปลี่ยน: "strong" → "solid" → "stable" across 3 quarters (ค่อยๆ soften)
- Qualifier ใหม่ที่เพิ่งปรากฏ 1 ครั้ง: "subject to", "contingent upon", "assuming continued" — ถ้า 1 ครั้งใน prior filing กลายเป็น 2 ครั้งในครั้งนี้ = escalation
- Section ที่ย้ายจาก Risk Factors ระดับ 2 → ระดับ 1 (priority เพิ่มขึ้น แต่ถ้อยคำเหมือนเดิม)
- ประโยคที่หายไปจาก boilerplate — missing positive statement ที่เคยมีทุกปี

→ flag `[HYPEROSMIA: FAINT DEGRADATION] "<phrase change>" — quarters: Q-2→Q-1→Q0: [tracking]`
→ ถ้าพบ drift ใน 2+ filing sections → `[HYPEROSMIA: PATTERN]` — systematic softening

```
Hyperosmia Language Scan:
- Faint degradation signals: N
- [HYPEROSMIA: FAINT DEGRADATION / PATTERN] <description>
- Assessment: [isolated / systematic drift]
```
ถ้าไม่พบ → `Hyperosmia: language stable ✅`

**Vera Layer 14 — Echolocation: Indirect Data Triangulation**

เมื่อ primary data หายหรือ verify ไม่ได้ → navigate ด้วย echo signals จาก ecosystem แทน

**Echo source hierarchy (ใช้เมื่อ direct data ไม่ได้):**
1. **Customer echoes:** ถ้า TICKER เป็น supplier → อ่าน customer earnings สำหรับ demand signal
2. **Supplier echoes:** ถ้า TICKER เป็น end-product → อ่าน supplier guidance สำหรับ cost/supply signal
3. **Competitor echoes:** competitor guidance เป็น industry proxy เมื่อ TICKER ไม่มี recent filing
4. **Patent/job echoes:** patent filings + job postings เป็น proxy สำหรับ R&D direction ที่ยังไม่ disclosed
5. **Channel echoes:** distributor earnings, reseller commentary, industry association data

→ flag `[ECHOLOCATION: INDIRECT] <data point> — triangulated from: [echo source] — confidence: [H/M/L]`
→ ถ้า 3 echo sources ชี้ทิศทางเดียวกัน → confidence = M (ใช้ได้แต่ mark ชัดว่าไม่ direct)
→ ถ้า echo conflict กัน → `[ECHOLOCATION: AMBIGUOUS]` — ห้ามใช้ใน kill conditions

```
Echolocation Triangulation:
- Primary data gaps: [N metrics unavailable/unverified]
- Echo signals used: [list source + direction]
- Confidence: [H/M/L per triangulated metric]
- [ECHOLOCATION: AMBIGUOUS] N — conflicting ecosystem signals
```
ถ้า primary data ครบ → `Echolocation: all primary data verified, no triangulation needed ✅`

**Vera Layer 15 — Cotard's Syndrome: Zombie Thesis Driver Check**

Cotard's = บริษัทยังมีชีวิต (มีรายได้, มี EPS) แต่ thesis driver ที่แท้จริงตายไปแล้ว — ระบบยังถือไว้เพราะเห็น "ชีพจร" แต่ไม่รู้ว่าชีพจรนั้นไม่ใช่สัญญาณชีวิตจริงแล้ว

**ตรวจ 4 Cotard's patterns:**
- **Moat ghost:** คู่แข่งมี product ที่ทำได้เหมือนกัน แต่บริษัทยังรายงาน gross margin สูงผิดปกติ (delay ก่อนที่ margin จะ compress)
- **TAM zombie:** TAM ยังใหญ่ในเอกสาร แต่ addressable portion หดลงเพราะ substitution/regulation ที่ยังไม่ price in
- **Customer concentration death:** top customer เริ่มสร้าง in-house หรือ shift supplier แต่ revenue ยังไม่ drop เพราะ backlog
- **Growth driver extinction:** segment ที่เป็น core driver ของ thesis เติบโต < 3% แต่ management highlight segment รองที่โตเร็วแทน (bait-and-switch narrative)

→ flag `[COTARD: ZOMBIE DRIVER] <driver name> — still appearing alive because: [reason] — actual status: [dead/dying]`
→ ถ้าพบ Cotard's pattern → thesis ต้องถูก re-evaluated จาก scratch ก่อน save Reese doc

```
Cotard's Thesis Driver Check:
- Drivers checked: [list thesis drivers from Reese doc]
- [COTARD: ZOMBIE DRIVER] N — driver appears alive but is not
- Assessment: [thesis intact / [COTARD: ZOMBIE] — requires thesis rewrite]
```
ถ้าไม่พบ → `Cotard's: all thesis drivers verified alive ✅`

**Vera Layer 16 — Color Blindness: Categorical Label Strip** [COLORBLIND: LABEL]

สแกน Reese doc และ research sections หาคำที่เป็น qualitative categorical ที่ไม่มี quantified backing — ภาษาที่ "ดูดี/ดูแย่" โดยไม่มีตัวเลข:

| Banned label | แทนด้วย |
|---|---|
| "strong growth" | "revenue grew X% YoY vs sector median Y%" |
| "weak competitor" | "[competitor] revenue share dropped from X% to Y% in [period]" |
| "best-in-class margin" | "gross margin X% vs peer median Y% — top Z percentile" |
| "attractive valuation" | "P/E X.X vs 3Y own avg Y.Y = [premium/discount]%" |
| "deteriorating fundamentals" | "[metric] declined from X to Y over [N quarters]" |
| "high-quality business" | "[moat indicator] = [specific metric/fact]" |
| "secular tailwind" | "market growing X% CAGR per [source] through [year]" |

→ flag `[COLORBLIND: LABEL] "<vague term>" → "<quantified replacement>"`
ถ้า ≥3 labels พบ → prepend `⚠️ Color Blind count: N — research reads as qualitative, not quantitative`

```
Color Blind Check:
- Labels found: N
- [COLORBLIND: LABEL] "<term>" → "<replacement>"
Doc tone: [quantified ✅ / partially labeled / [COLORBLIND: LABEL] — requires replacement]
```
ถ้าไม่พบ label → `Color Blind: doc is quantified ✅`

**Vera Layer 17 — Anton's Syndrome: Confident Blindness Audit** [ANTON: BLIND CONFIDENCE]

Anton-Babinski syndrome = ผู้ป่วยตาบอดแต่ไม่รู้ตัวว่าตาบอด — มั่นใจ 100% ว่ามองเห็น สร้าง narrative ของสิ่งที่ "เห็น" ทั้งที่จริงๆ มองไม่เห็นอะไรเลย

ใน research: claim ที่ stated ด้วย high confidence แต่ไม่มีข้อมูลรองรับ — researcher "เห็น" fact ที่ไม่มีอยู่จริง

ตรวจ 3 patterns:

**1. High-confidence bare assertion:** claim ที่พูดเหมือนเป็นความจริงที่รู้กันทั่วไปแต่ไม่มี source:
- "Company X is the leader in [market]" — ไม่มี market share data
- "Management has a strong track record" — ไม่มี specific achievement cited
- "The moat is defensible" — ไม่มี competitive data

**2. Evidence gap at conviction peak:** section ที่ confidence language สูงสุดแต่ footnote/source หายไป:
- "Clearly, the company..." / "Obviously, demand will..." / "It's well known that..." → ไม่มีข้อมูลตามมา

**3. Unverified forward projection:** projection ที่ไม่มี base case methodology:
- "Revenue should reach $X by [year]" โดยไม่ระบุ assumptions หรือ model

→ flag `[ANTON: BLIND CONFIDENCE] "<claim>" — evidence: none | must add source or convert to ❓`

```
Anton's Syndrome Audit:
- [ANTON: BLIND CONFIDENCE] N — confident claims with zero data
- [ANTON: EVIDENCE GAP] M — high-confidence language at empty sections
- [ANTON: UNVERIFIED PROJECTION] K — forward projections without methodology
- Verdict: [clear ✅ / N blind confidence claims — must source or flag ❓]
```
ถ้าไม่พบ → `Anton's: all high-confidence claims have evidence ✅`

**Vera Layer 18 — Narcolepsy Flash Insight** [NARCOLEPSY: FLASH]

Narcolepsy ใช้ hypnagogic state — ช่วงเปลี่ยนระหว่างตื่นกับหลับที่บางครั้งให้ insight ที่ analysis ยาวๆ ไม่ได้ให้ Vera รัน flash scan ก่อน deep audit:

**ก่อนอ่าน Reese doc อย่างละเอียด — จับ 1-sentence thesis read ทันที:**
> "ถ้าต้องสรุป thesis นี้ใน 1 ประโยคโดยไม่ดูรายละเอียด — thesis คืออะไร?"

บันทึก flash read ก่อน ห้ามแก้ทีหลัง

**หลัง deep audit เสร็จ — เปรียบเทียบ:**
- ถ้า flash ตรงกับ conclusion → `[NARCOLEPSY: FLASH CONFIRMED]` — thesis ชัดเจนพอที่จะจับได้โดยสัญชาตญาณ
- ถ้า flash ไม่ตรง → `[NARCOLEPSY: FLASH-AUDIT CONFLICT]` — thesis ซับซ้อนเกินหรือ Reese doc ไม่ได้สื่อ narrative หลักชัดพอ
- ถ้า flash ชัดกว่า conclusion ใน Reese doc → flag: narrative ใน Reese doc อาจ diluted เกินไป

```
Narcolepsy Flash:
- Flash read: "[1-sentence thesis before analysis]"
- Audit conclusion: "[what deep analysis found]"
- Match: [NARCOLEPSY: FLASH CONFIRMED / NARCOLEPSY: FLASH-AUDIT CONFLICT]
- Signal: [narrative clear ✅ / doc needs cleaner thesis statement / thesis too complex]
```

---

## STEP 6 — INDIE ATOMS

> **Observation masking:** ทำงานจาก Reese doc ใน context — ห้าม re-read ไฟล์ซ้ำ

> **Structured-output-only rule (arXiv:2601.04426):** Indie output ต้องเป็น atom format ด้านล่างทันที — ห้ามมี intro paragraph หรือ preamble ใดๆ

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
