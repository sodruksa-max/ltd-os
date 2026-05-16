---
description: Post-market review — compare /pre-market predictions vs reality, or review-only if no premarket file exists. Run each morning (Thailand time) after US market close.
---

# /post-market

Review market outcomes. Two modes:
- **Full mode** — มี premarket brief: compare predictions vs reality, calibration score, setup outcomes
- **Review-only mode** — ไม่มี premarket brief: บันทึก market data + key observations เท่านั้น (ข้ามส่วน calibration)

## Usage

```
/post-market [YYYY-MM-DD]
```

- Argument is optional — defaults to **yesterday ET** (เพราะรันตอนเช้าไทย = หลังตลาด US ปิดแล้ว)
- ตัวอย่าง: `/post-market 2026-04-28`

---

## Steps

### 1. Resolve target date

If no argument provided, run:

```bash
date -d "yesterday" '+%Y-%m-%d'
```

Use the result as `<date>`. Confirm in first line: `Target date: YYYY-MM-DD`

### 2. Read pre-market files (read-only)

ลองอ่าน — **ห้ามแก้ไขทั้งสองไฟล์นี้ไม่ว่ากรณีใด:**

- `vault/20_investment/_journal/<date>-premarket.md`
- `vault/20_investment/_journal/<date>-decision-tree.md`

**ถ้าไม่พบ `<date>-premarket.md`** → switch เป็น **review-only mode** แจ้ง user:
> ℹ️ ไม่พบ `<date>-premarket.md` — รันใน **review-only mode** (ข้าม calibration, setup outcomes, และ prediction comparison)

แล้วดำเนินต่อไปยัง Step 3 (ข้าม Step 4 ส่วน prediction comparison — ดูหมายเหตุใน Step 4)

**ถ้าไม่พบ `<date>-decision-tree.md`** (และมี premarket) → ดำเนินต่อได้ แต่แจ้ง user:
> ⚠️ ไม่พบ `<date>-decision-tree.md` — Pre-Commit Rules section จะเป็น [unverified] ทั้งหมด

**ถ้าพบ premarket.md** (full mode) — extract:
- **Most Likely Scenario:** Bullish / Base / Bearish + confidence level
- **Setups 1/2/3:** ticker, direction, trigger conditions, invalidation
- **Polymarket odds** (ถ้ามีใน brief)
- **Earnings ที่ mention** (tickers)
- **Pre-commit rules** ที่ระบุไว้ใน decision tree (circuit breakers, setup invalidation, earnings signal)

### 3. Fetch actual market results

#### 3a. Run post-snapshot.py (primary — no search slots used)

```bash
code/python/.venv/Scripts/python scripts/post-snapshot.py --date <DATE>
```

Output ครอบคลุม **ทุก ETF + macro** ที่ต้องการ:
- SPY, QQQ, DIA, IWM, VXX (indexes + VIX proxy)
- XLE, XLK, XLP, XLU, XLY (sector ETFs)
- GLD, TLT (gold + bonds)
- USO, BNO (WTI + Brent proxies)
- ^VIX, ^TNX, CL=F, BZ=F, GC=F (macro indicators)

ใช้ output ของ script เป็น **Market Data section** โดยตรง — ข้อมูลมาจาก Alpaca IEX feed + Yahoo Finance direct HTTP (ไม่ใช้ web search)

**ถ้า script fail** → fallback ใช้ web search แทน (4 queries ตาม list เดิม):
- `S&P 500 Nasdaq Dow Jones close <DATE> stock market results`
- `VIX close intraday high <DATE>`
- `XLE XLK XLP XLU XLY GLD TLT ETF performance <DATE>`
- `Brent WTI crude oil close price <DATE>`

#### 3b. Earnings results (web search — เฉพาะถ้ามี earnings tickers ใน brief)

ถ้า brief ระบุ earnings tickers → search **1 query**:
```
[EARNINGS TICKERS from brief] earnings results EPS actual <DATE>
```

**Data to collect (earnings only):** EPS actual vs estimate, % move after-hours

**ถ้าไม่มี earnings tickers ใน brief → ข้ามทั้งหมด (0 search slots)**

**Conflict rule:** ถ้า 2 sources ให้ค่าต่างกัน → flag ⚠️ CONFLICT แสดงทั้งสองค่า ไม่เลือกข้างใดข้างหนึ่ง

**ถ้าหาตัวเลขไม่ได้:** ใส่ `[unverified]` — ห้าม fabricate

### 4. Determine Actual Scenario

ใช้ผลจริงของ S&P 500 เพื่อตัดสิน (quantitative threshold) — ทำทั้ง 2 mode:
- S&P 500 close > +0.3% → **Bullish**
- S&P 500 close -0.3% ถึง +0.3% → **Base**
- S&P 500 close < -0.3% → **Bearish**

**Full mode เท่านั้น** — ตรวจ **narrative alignment** (ใช้ใน Match classification):
- Sectors ที่ brief คาด outperform → ขึ้นจริงหรือเปล่า?
- VIX อยู่ใน range ที่ brief คาดหรือเปล่า?

**Match classification (full mode เท่านั้น):**
- **Yes** = threshold ตรงกับที่ predict
- **Partial** = threshold บอก X ≠ predicted แต่ (1) S&P ข้าม boundary ≤ 0.3pp AND (2) narrative ถูก — sectors/VIX behaved as predicted
- **No** = threshold ผิด + narrative ก็ผิดด้วย

**Review-only mode:** ข้าม Match classification — บันทึก Actual Scenario เท่านั้น

### 5. Check overwrite

ถ้า `vault/20_investment/_journal/<date>-review.md` มีอยู่แล้ว → หยุดและถาม:
> ⚠️ พบ `<date>-review.md` อยู่แล้ว — overwrite? (y/n)
ถ้า n → จบโดยไม่แตะไฟล์

### 6. Generate review file

Save to `vault/20_investment/_journal/<date>-review.md`.

ใช้ template ตาม mode:

---

#### FULL MODE template (มี premarket brief)

```markdown
# Post-Market Review — YYYY-MM-DD (วัน)
*Reality check on [[YYYY-MM-DD-premarket]] | สร้างหลังตลาดปิด | ไม่ใช่คำแนะนำลงทุน*

---

## Most Likely Scenario verdict

- **Predicted:** [Bullish/Base/Bearish] @ [low/medium/high] confidence
- **Actual:** [Bullish/Base/Bearish] — S&P 500 closed [+/-X.XX%]
- **Match?** Yes / Partial / No
- **เหตุผล:** [1-2 ประโยค — ทำไม match หรือไม่ match อ้างอิงจาก catalyst ที่เกิดจริง]

---

## Calibration Score

- **Direction (up/down/flat):** correct / wrong
- **Confidence appropriate?**
  - Predicted [low/medium/high] confidence → ผล [ถูก/ผิด]
  - [ประเมิน: เช่น "มั่นใจ medium แล้วถูก = well-calibrated" | "มั่นใจ high แล้วผิด = over-confident"]
- **Verdict:** well-calibrated / over-confident / under-confident
- **Brier Score:** `BS = (confidence_decimal − outcome)²`
  - confidence_decimal = [0.3 / 0.5 / 0.7] สำหรับ low / medium / high confidence
  - outcome = 1 ถ้า scenario ถูก, 0 ถ้าผิด
  - Example: high confidence (0.7) + ผิด → BS = (0.7 − 0)² = **0.49** (bad) | medium + ถูก → (0.5 − 1)² = **0.25** (ok)
  - Rolling 10-day average BS: คำนวณจาก OUTCOMES.md โดย:
    ```bash
    grep "BS:" vault/_memory/OUTCOMES.md | tail -10
    ```
    ดึง BS values 10 entries ล่าสุด → คำนวณ average → ถ้า > 0.25 = over-confident โดยรวม
    ถ้ามีน้อยกว่า 3 entries → แสดง "ข้อมูลไม่พอคำนวณ rolling avg" แทน ห้ามประมาณ

---

## Setup Outcomes

| Setup | Ticker | Trigger เกิด? | ทิศทางที่ predict | ผลจริง | Hypothetical P/L |
|---|---|---|---|---|---|
| Setup 1 | [ticker] | Yes / No / [unverified] | [Long/Short/Skip] | [+/-X%] | [+/-X% ถ้าเข้าตาม plan / N/A ถ้า skip] |
| Setup 2 | [ticker] | Yes / No / [unverified] | [Long/Short/Skip] | [+/-X%] | [+/-X% / N/A] |
| Setup 3 | [ticker] | Yes / No / [unverified] | [Long/Short/Skip] | [+/-X%] | [+/-X% / N/A] |

*Hypothetical P/L: entry = ราคาเปิดตลาด (open) หรือ trigger price ถ้าระบุในน setup; exit = time-stop ที่ระบุหรือ EOD close; size = ตามที่ระบุใน setup (half/full); ไม่รวม slippage/commission — เพื่อ learning เท่านั้น ไม่ใช่ผลกำไรจริง ถ้าไม่มีราคา open/trigger จริง → [unverified]*

**PEAD Inconsistent Surprise Check** (ทำเฉพาะ setup ที่มี earnings):
- [ ] EPS beat แต่หุ้นลง → เช็ค analyst consensus: majority Buy/Hold หรือ Sell?
  - ถ้า consensus **Buy** (consistent surprise) → drift น้อย ปกติ ไม่น่า add
  - ถ้า consensus **Sell/Hold** (inconsistent surprise) → expect strong PEAD drift ต่ออีก 90 วัน → **hold/add ไม่ใช่ขาย** (McCarthy SSRN 5311906: drift 5.8-7.4%)
- [ ] EPS miss แต่หุ้นขึ้น → เช็ค consensus เช่นกัน — ถ้า consensus Sell อยู่ = inconsistent → drift ลงต่อได้

**PEAD follow-through action** (ทำทันทีถ้าพบ inconsistent surprise):
- Add ticker ใน `config/watchlist.txt` ถ้ายังไม่มี → `/screen` จะติดตามต่อ
- Note ใน review file: `PEAD watch: <TICKER> — inconsistent <beat/miss>, consensus <Buy/Sell>, drift expected until <date+90d>`
- Suggest: `→ รัน /stock-content <TICKER> เพื่อ research ก่อนตัดสินใจ position`

---

## Pre-Commit Rules Triggered

[ระบุ rules จาก decision tree ที่ trigger ระหว่างวัน + ผลที่เกิดถ้าทำตาม]
- `[rule condition]` → trigger เมื่อ [เวลา] → ถ้าทำตามกฎ: [ผลที่จะเกิด เช่น "หลีกเลี่ยง drawdown -2.3%"]
- [ถ้าไม่มี rule trigger]: "ไม่มี pre-commit rule trigger ระหว่างวัน"

---

## What Was Missed (Blind Spots)

[2-3 catalysts/events ที่ไม่ได้อยู่ใน brief แต่กระทบตลาดจริง]
1. [catalyst ที่พลาด + ผลกระทบจริง]
2. [catalyst ที่พลาด + ผลกระทบจริง]
3. [catalyst ที่พลาด + ผลกระทบจริง — หรือ "ไม่พบ blind spot สำคัญ"]

---

## Council Recommendation

*(สร้างเฉพาะเมื่อมี pattern ที่ต้อง debate จริง — ห้าม recommend council ทุกวัน)*

ถ้ามี pattern จาก lessons/blind spots ที่ต้อง debate:
- **หัวข้อ:** [เฉพาะเจาะจง ไม่ generic — เช่น "ควรใช้ adjusted หรือ GAAP EPS เป็น trigger criterion?" ไม่ใช่ "ลอง council ดู"]
- **Evidence จาก review นี้:** [อ้างอิงตัวเลข/เหตุการณ์จาก review วันนี้โดยตรง]
- **Suggested lens:** [engineer / financial_risk / strategist — เลือกตามลักษณะปัญหา]
- **Command:** `/council <topic> --expertise=<lens>`

ถ้าไม่มี decision ใหญ่ที่ต้อง debate → เขียน "ไม่มี council recommendation วันนี้" แล้วจบ ห้าม fabricate หัวข้อ

---

## Lessons for Next Brief

[2-3 actionable improvements สำหรับ brief วันพรุ่งนี้]
1. [improvement — เช่น "เพิ่ม Fed speakers ใน catalyst section"]
2. [improvement — เช่น "ลด confidence ใน Most Likely ถ้ามี event risk > 2 ตัวพร้อมกัน"]
3. [improvement หรือ "ไม่มี improvement เพิ่มเติม"]

---

## Sentiment Proxy Accuracy

- **Polymarket บอก:** [X%] Up → **ตลาดจริง:** [ขึ้น/ลง/ทรง] ([+/-X%])
- **Crowd ถูกหรือผิด?** [ถูก / ผิด / Partial — อธิบาย 1 ประโยค]
- [ถ้าไม่มี Polymarket data ใน brief]: [unverified — ไม่มี Polymarket data ใน brief วันนั้น]

---

## Market Data (verified)

| Metric | Close | % Change | Source |
|---|---|---|---|
| S&P 500 | | | |
| Nasdaq-100 | | | |
| Dow Jones | | | |
| VIX (close / intraday high) | / | | |
| XLE | | | |
| XLK | | | |
| XLP | | | |
| XLU | | | |
| XLY | | | |
| GLD | | | |
| TLT | | | |
| Brent crude | | | |
| WTI crude | | | |

*Sources: [ระบุทุก source พร้อม URL]*
```

---

#### REVIEW-ONLY MODE template (ไม่มี premarket brief)

```markdown
# Post-Market Review — YYYY-MM-DD (วัน) [review-only]
*Market data log — ไม่มี premarket brief วันนี้ | สร้างหลังตลาดปิด | ไม่ใช่คำแนะนำลงทุน*

---

## Actual Scenario

- **S&P 500 closed:** [+/-X.XX%] → **[Bullish / Base / Bearish]**
- **สรุป:** [1-2 ประโยค — driver หลักของวัน]

---

## Key Observations

[3-5 observations ที่น่าจดบันทึก — sector rotation, outlier movers, macro event ที่เกิด]
1. [observation + ผลกระทบ]
2. [observation + ผลกระทบ]
3. [observation หรือ "ไม่มี observation เพิ่มเติม"]

---

## Council Recommendation

*(สร้างเฉพาะเมื่อมี pattern ที่ต้อง debate จริง — ห้าม recommend council ทุกวัน)*

ถ้ามี pattern จาก observations ที่ต้อง debate:
- **หัวข้อ:** [เฉพาะเจาะจง]
- **Evidence จาก review นี้:** [อ้างอิงตัวเลข/เหตุการณ์จาก review วันนี้]
- **Suggested lens:** [engineer / financial_risk / strategist]
- **Command:** `/council <topic> --expertise=<lens>`

ถ้าไม่มี → เขียน "ไม่มี council recommendation วันนี้"

---

## Market Data (verified)

| Metric | Close | % Change | Source |
|---|---|---|---|
| S&P 500 | | | |
| Nasdaq-100 | | | |
| Dow Jones | | | |
| VIX (close / intraday high) | / | | |
| XLE | | | |
| XLK | | | |
| XLP | | | |
| XLU | | | |
| XLY | | | |
| GLD | | | |
| TLT | | | |
| Brent crude | | | |
| WTI crude | | | |

*Sources: [ระบุทุก source พร้อม URL]*
```

---

### 7. Append to OUTCOMES.md

Append 1 line ใต้ section `## Trading Calibration Log` ใน `vault/_memory/OUTCOMES.md`.

ถ้า section `## Trading Calibration Log` ยังไม่มี → append section header ก่อน แล้วค่อย append entry

**Full mode:**
```
<date> — Predicted: <X> (<confidence>), Actual: <Y>, Match: <Yes/Partial/No>, Calibration: <well-calibrated/over-confident/under-confident>, BS: <value e.g. 0.25>, Top lesson: <Z>
```

**Review-only mode:**
```
<date> [review-only] — Actual: <Y> (S&P <+/-X%>), No premarket brief, Key observation: <Z>
```

### 7.5 HYPERTHYMESIA_LOG append

Append full-context entry ใน `vault/_memory/HYPERTHYMESIA_LOG.md` — ทำทั้ง full mode และ review-only mode

**Full mode entry:**
```
## <date> — Full
Regime: [trending-up / trending-down / choppy / risk-off]

**Market snapshot at decision time:**
S&P: [+/-X%] | VIX: [X] | TNX: [X%] | Oil(Brent): [$X]
Dominant sector move: [sector] [direction]

**Prediction:**
Direction: [Bullish/Base/Bearish] @ [low/medium/high] confidence
Reasoning: [exact reasoning from premarket brief — what made me think this]
Known unknowns: [อะไรที่ยังไม่แน่ใจตอน predict]
Key catalysts expected: [list จาก brief]

**Outcome:**
Actual: [Bullish/Base/Bearish] — S&P [+/-X%]
Match: [Yes/Partial/No] | Calibration: [well-calibrated/over-confident/under-confident]
Surprise: [blind spot หลักที่พลาด]
Top lesson: [1 ประโยค]
```

**Review-only mode entry (abbreviated):**
```
## <date> — Review-only
Regime: [regime]
Market: S&P [+/-X%] | VIX: [X]
Key observation: [สรุปสั้น]
```

ถ้า `vault/_memory/HYPERTHYMESIA_LOG.md` ยังไม่มี → สร้างก่อนด้วย header จาก template แล้วค่อย append

### 8. KB Sync

> **Observation masking:** ทำงานจาก review ใน context — ห้าม re-read ไฟล์ซ้ำ

ทำหลัง save review file เสมอ (ทั้ง full mode และ review-only mode)

**8a. Contradiction registry** — ถ้า review พบอย่างใดอย่างหนึ่งต่อไปนี้:
- Blind spot / Key Observation ขัดแย้งกับ assumption ของ active thesis ใน THESIS_TRACKER
- Earnings result ขัดแย้งกับ thesis narrative (เช่น beat แต่หุ้นลง 5%+ = insider distribution signal)
- Market data 2 sources ให้ค่าต่างกัน (⚠️ CONFLICT)

→ **append ใน `vault/Knowledge/contradiction-registry.md`** ทันที:
```
[YYYY-MM-DD] [TICKER/MARKET] — <claim ที่ขัดแย้ง> | Source A: <ค่า> vs Source B: <ค่า> | Thesis link: T#
```

ถ้าไม่มี contradiction → ข้ามได้ ห้าม fabricate

**8b. Insight atom** — ถ้า "Lessons for Next Brief" หรือ "Key Observations" มี claim ที่:
- Falsifiable (วัดได้ / ตรวจสอบได้)
- เกี่ยวข้องกับ active thesis (T1-T4)
- ไม่ซ้ำกับ atom ที่มีอยู่แล้วใน INDEX_insights.md

→ extract เป็น atom 1 ข้อ append ใน `vault/Knowledge/insight-atoms/post-market-<date>.md` และ append 1 line ใน `vault/Knowledge/INDEX_insights.md`
- Format: `[date] [T#] post-market-<date> — <1-line falsifiable claim>`

ถ้าไม่มี lesson ที่ falsifiable → ข้ามได้

**8c. THESIS_TRACKER kill condition check** — partial read เฉพาะ kill conditions:
```bash
grep -A 3 "Kill condition" vault/Knowledge/THESIS_TRACKER.md
```
- อ่านเฉพาะ kill condition lines — ห้ามโหลดทั้งไฟล์
- ถ้าวันนี้มี event ที่ push kill condition ใดๆ ให้ใกล้ trigger → แจ้ง user:
  `⚠️ T# kill condition ใกล้ trigger: [condition] — [ข้อมูลวันนี้ที่เกี่ยวข้อง]`
  `→ รัน /nick-weekly เพื่อให้ Nick ประเมิน hold/exit`
- ถ้าไม่มี → ไม่ต้องแจ้ง

---

### 8.5 Psychopathy Sunk Cost Audit

ตรวจว่า analysis ใน review นี้ปนเปื้อน sunk cost หรือ emotional reasoning ไหม — รันก่อน print verdict

**ตรวจ Setup Outcomes (full mode เท่านั้น):**
- Setup ไหนที่ P/L ติดลบแต่ reasoning บอก "should have held longer" โดยอ้างถึง entry price → flag `[SUNK COST]`
- Setup ที่ trigger เกิดจริงแต่ไม่ execute เพราะ "กลัวขาดทุนเพิ่ม" → flag `[LOSS AVERSION]`
- Setup ที่ hold past invalidation โดยไม่มี thesis update → flag `[HOPE HOLD]`

**ตรวจ Lessons for Next Brief:**
- Lesson ที่มี pattern "ไม่ควรขาย X เพราะราคาลงมาแล้ว" → flag `[SUNK COST LESSON]`
- Lesson ที่ derived จาก emotion ไม่ใช่ data (ไม่มี evidence ประกอบ) → flag `[EMOTION-DERIVED]`

**ตรวจ calibration reasoning:**
- ถ้า high confidence + ผิด: ตรวจว่า predict เพราะ evidence หรือเพราะอยากให้เป็นแบบนั้น → flag `[WISHFUL CALIBRATION]`

ถ้าพบ flag → append เป็น lesson พิเศษต่อท้าย "Lessons for Next Brief" ในไฟล์ review:
```
⚠️ Psychopathy Sunk Cost Audit:
- [FLAG_TYPE] <setup/section> — <description>
```

ถ้าไม่พบ flag ใดเลย → ข้ามเงียบๆ ไม่ต้องแสดง

### 8.75 GAD Forward Threat Register — ความเสี่ยงที่กำลังสะสม

สแกนหาภัยคุกคามที่ยังไม่เกิด แต่กำลัง build up ใต้ผิวน้ำจากข้อมูลวันนี้

**Enumerate 2-3 risks ที่:**
- ยังไม่ materialize วันนี้
- แต่ข้อมูลวันนี้ (หรือรวมกับ context ก่อนหน้า) แสดงสัญญาณสะสม
- ต้องระบุ: ชื่อ risk / อะไรที่สะสม / signal แรกที่จะเห็นเมื่อ materialize

append ใน review file ต่อท้าย "Lessons for Next Brief":
```
GAD Forward Threat Register:
- [RISK] <ชื่อความเสี่ยง> — Accumulating: <สัญญาณที่เห็น> — First signal: <อะไรจะบอกว่าเกิดแล้ว>
- [RISK] ...
```

**Escalation rule — ตรวจข้าม review files:**
```bash
grep -r "\[RISK\]" vault/20_investment/_journal/ --include="*-review.md" | grep "<risk keyword>"
```
ถ้า risk เดิมปรากฏ ≥ 3 ครั้งข้าม review files → flag:
> `⚠️ [GAD: ESCALATE] <risk> — ปรากฏ 3+ ครั้ง → เสนอเป็น standing rule ใน TRADING_RULES.md`
แล้วถาม user: "ต้องการ add เป็น standing rule ไหม? (y/n)"

ถ้าไม่พบ accumulating risk ใดเลย → ข้ามเงียบๆ ไม่ต้องแสดง

### 8.8 Schizotypal — Unexplained Anomaly Log

บันทึก 1-2 สิ่งที่เกิดขึ้นวันนี้ซึ่งไม่มี model ใดอธิบายได้สมบูรณ์

**เกณฑ์ที่นับเป็น anomaly:**
- เกิดขึ้นตรงข้ามกับ consensus expectation โดยสิ้นเชิง
- ไม่สอดคล้องกับ correlation ปกติ (เช่น VIX ลงแต่ bonds ร่วง)
- timing ผิดปกติ (ราคา move ก่อน news ออก, sector diverge โดยไม่มี catalyst)

**กฎ: ไม่ต้องอธิบาย** — แค่ log ไว้; append ใน review file ต่อท้าย GAD Forward Threat Register:
```
Schizotypal Anomaly: [date]
- [ANOMALY] <อะไรเกิด> — unexplained by: <model/narrative ที่ fail>
```

**Pattern detection:**
ถ้า anomaly เดิมปรากฏซ้ำ ≥ 3 ครั้งข้าม review files → flag:
> `[SCHIZOTYPAL: SIGNAL] <anomaly> — ปรากฏ 3+ ครั้ง → /wild-thesis <topic>`

ถ้าไม่พบ anomaly → ข้ามเงียบๆ ไม่ต้องแสดง

### 8.9 Alexithymia — Emotional Residue Detector

สแกน review ทั้งวันหา emotional language ที่ฝังอยู่ใน decision rationale — ตัวเลขอาจ objective แต่ภาษาที่ใช้อธิบาย decision บอก bias ที่ซ่อนอยู่

**Pattern ที่ตรวจหา:**

| Flag | Pattern | ตัวอย่าง Thai | ตัวอย่าง English |
|---|---|---|---|
| Regret | ภาษาเสียดาย | "น่าเสียดาย", "ถ้าไม่..." | "unfortunately", "I should have" |
| Hope-as-plan | ใช้ความหวังเป็นแผน | "น่าจะดีขึ้น", "คงจะ..." | "should recover", "hopefully" |
| Fear-driven exit | ออกเพราะกลัว ไม่ใช่ข้อมูล | "กลัวว่า", "ไม่กล้า" | "scared of", "afraid it might" |
| Revenge trade setup | วางแผน revenge | "ต้องเอาคืน", "trade ถัดไปจะต้อง" | "need to make it back", "must recover" |
| Excitement override | ตื่นเต้นจนข้าม process | "ตื่นเต้นมาก", "รู้สึกว่าแน่นอน" | "very excited", "I'm sure this time" |

→ flag `[ALEXITHYMIA: EMOTIONAL RESIDUE] "<phrase>" — type: [regret / hope-as-plan / fear / revenge / excitement]`

**Impact assessment:**
- ถ้าพบ `revenge` หรือ `fear-driven exit` → append ใน review: "⚠️ Emotional state may have affected today's decisions — revisit tomorrow with fresh eyes"
- ถ้าพบ `excitement override` → check ว่า trade นั้นผ่าน pre-flight checklist ครบไหม

```
Alexithymia Residue: [N] patterns found
- [ALEXITHYMIA: EMOTIONAL RESIDUE] "<phrase>" — type: [type]
  Decision affected: [trade/decision ที่อาจ contaminated]
Recommendation: [none / revisit tomorrow / mandatory re-check entry criteria]
```

ถ้าไม่พบ → ข้ามเงียบๆ ไม่ต้องแสดง

### 8.95 DPDR — Third-Person Calibration Debrief

อ่าน review วันนี้ทั้งหมดในฐานะคนแปลกหน้าที่ไม่รู้จักผู้เทรด context ใดๆ เลย

> "ผมเพิ่งได้รับ trading journal ของ trader คนนึง — ไม่รู้อะไรเกี่ยวกับเขาเลย..."

ตั้งคำถาม 3 ข้อจากมุม outsider:

**1. Decision quality:** "ดูจากข้อมูลที่มี — trader คนนี้ตัดสินใจดีไหม?" (ไม่นับผล P&L — นับ process)

**2. Consistency:** "trader คนนี้ทำตาม rules ที่ตัวเองตั้งไว้ไหม? ถ้าไม่ — ทำไม?"

**3. Blind spots:** "มีอะไรที่ trader คนนี้ดูเหมือนจะไม่เห็น แต่คนภายนอกเห็นได้ชัด?"

```
DPDR Third-Person Debrief:
Decision quality: [sound / questionable — reason]
Rule consistency: [followed / [N] violations — which rules]
Blind spot identified: [อะไรที่ outsider เห็น หรือ "none obvious"]
Outsider verdict: [1 ประโยค summary จากมุมมองคนแปลกหน้า]
```

ถ้าไม่พบสิ่งผิดปกติ → `DPDR debrief: no outsider flags ✅`

### 8.96 AIWS — Time Distortion Debrief

ตรวจ events วันนี้ที่ตลาดให้ short-term weight ไม่สัดส่วนกับ long-term impact จริงๆ

**Short-term over-weighted (ตลาดให้น้ำหนักเกิน):**
- Fed speaker comment → ตลาดขยับ 1%+ แต่ไม่เปลี่ยน policy outlook
- Analyst upgrade/downgrade เดี่ยว → ราคาเปลี่ยน > 3%
- Short-covering rally ที่ดูเหมือน real demand
→ flag `[AIWS: SHORT-TERM WEIGHT] "<event>" — ตลาดขยับ X% แต่ long-term impact = ต่ำ/ไม่มี`

**Long-term under-weighted (ตลาดให้น้ำหนักน้อยเกิน):**
- Data point structural ที่ตลาด ignore เพราะ short-term noise ดัง
- Earnings call detail ที่ Q&A สำคัญแต่ headline number บดบัง
- Regulatory change ที่มีผล 12+ เดือนข้างหน้าแต่ตลาดยังไม่ price in
→ flag `[AIWS: LONG-TERM UNDERWEIGHT] "<event>" — impact จะ materialize ใน [timeframe]`

```
AIWS Time Debrief:
- [event]: [SHORT-TERM WEIGHT / LONG-TERM UNDERWEIGHT / proportional]
  Action: [none / fade today's move / accumulate ahead of delayed pricing]
Cumulative pattern: [N events flagged this week — type: over/under]
```

ถ้าไม่พบ → ข้ามเงียบๆ

### 8.97 BPD — Splitting Audit on Today's Review

สแกน review language หา idealization/devaluation ที่สุดโต่ง — ถ้าพบ = emotional state contaminated analysis

**Idealization flags** (มองสิ่งที่ได้กำไรเกินจริง):
- "perfect setup", "flawless execution", "exactly as planned"
- "knew it would work", "obviously bullish", "clear as day"
→ flag `[BPD: IDEALIZATION] "<phrase>" — trade: [trade ที่อ้างถึง]`

**Devaluation flags** (มองสิ่งที่เสียหายเกินจริง):
- "stupid market", "impossible to trade today", "broken system"
- "random noise", "can't predict anything", "waste of time"
→ flag `[BPD: DEVALUATION] "<phrase>" — context: [อะไรที่ทำให้พูดแบบนี้]`

**Split Day detection:**
ถ้าพบทั้ง idealization AND devaluation ในวันเดียว → `[BPD: SPLITTING DAY]`

```
BPD Splitting Audit:
Idealization: [N instances หรือ "none"]
Devaluation: [N instances หรือ "none"]
Split Day: [yes → [BPD: SPLITTING DAY] / no]
Action: [none / "revisit tomorrow — emotional state may have skewed analysis" / "mandatory cool-down before next trade"]
```

**กฎ:** ถ้า `[BPD: SPLITTING DAY]` → append ใน review: "⚠️ Emotional splitting detected — no new position entries tomorrow until debrief complete"

ถ้าไม่พบ flag ใดเลย → ข้ามเงียบๆ

### 8.98 CIP — Loss Execution Log

บันทึกทุก stop-loss trigger วันนี้และตรวจว่า executed หรือ rationalized ออกไป

สแกน review วันนี้หา:
- Position ที่ stop price ถูก hit แต่ยังถือต่อ
- Position ที่ thesis invalidated แต่ยังไม่ close
- Position ที่ rule บอกให้ exit แต่มี "เหตุผล" ให้ stay

ต่อแต่ละกรณีที่พบ → classify:
- `[CIP: DATA OVERRIDE]` — มีข้อมูลใหม่ที่ชัดเจน explicit เปลี่ยน thesis จริงๆ (acceptable)
- `[CIP: NARRATIVE OVERRIDE]` — reason เป็น vague hope หรือ rationalization ("ตลาดน่าจะ recover", "เดี๋ยวคงดีขึ้น", "ยังถือ")

```
CIP Loss Execution Log:
- [TICKER / trade]: stop triggered [yes / no]
  Executed: [yes ✅ / no → [CIP: DATA OVERRIDE] / no → [CIP: NARRATIVE OVERRIDE]]
  If DATA OVERRIDE: [ข้อมูลใหม่ที่ชัดเจน]
  If NARRATIVE OVERRIDE: [reason ที่บอก + flag for follow-up]
NARRATIVE OVERRIDE rate today: [N / total triggers]
Cumulative this week: [track ใน review file]
```

**กฎสะสม:** ถ้า NARRATIVE OVERRIDE ≥ 2 ใน week เดียวกัน → เสนอ rule update ใน weekly-calibration ถัดไป

### 8.99 Paranoid — Threat Signature Registry Update

บันทึก warning signs ที่เกิดก่อน bad trades วันนี้เป็น pattern library สะสม

ขั้นตอน:
1. ระบุ trades วันนี้ที่ outcome แย่กว่า expectation
2. สำหรับแต่ละ trade — ย้อนดูว่ามี pre-trade warning sign อะไรบ้างที่ ignore ไป:
   - Market condition ที่ไม่เอื้อ แต่ trade ต่อ
   - Setup ที่ดูดีแต่มี red flag เล็กๆ ที่ข้ามไป
   - Timing ที่ผิดปกติ (เช่น เข้าตอนที่ volume เบาผิดปกติ)
3. Append ใน `vault/Knowledge/paranoid-threat-signatures.md`:

```
[YYYY-MM-DD] [TICKER/SETUP TYPE]
Pre-trade signals ignored: [list]
Outcome: [loss magnitude / miss vs expectation]
Pattern: [คำอธิบายสั้นที่ใช้ recognize ในอนาคต]
```

**Pattern detection:** ถ้า signature เดิมปรากฏ ≥ 3 ครั้ง → append ใน pre-market brief เป็น `[PARANOID: THREAT SIGNATURE] <pattern>` อัตโนมัติ

ถ้าไม่มี bad trades วันนี้ → ข้ามเงียบๆ

### 8.991 TLE — Sequence Causality Replay

Replay chain of events วันนี้เป็น temporal sequence เพื่อหา leading indicator ที่ซ่อนอยู่

สร้าง timeline:
```
[Time A]: <event/observation>
→ [Time B]: <market reaction>
→ [Time C]: <follow-through or reversal>
→ [Outcome]: <final direction + magnitude>
```

ตรวจหา:
- **Hidden leading indicator:** สิ่งที่เกิดก่อนและ predict outcome ได้ — ถ้าเห็นอีกครั้ง → weight higher
- **False signal:** สิ่งที่ดูเหมือน leading แต่ไม่ได้ predict อะไร — ลด weight ครั้งถัดไป
- **Delayed effect:** event ที่เกิดตอนเช้าแต่ market ตอบสนองตอนบ่าย → note time lag

→ บันทึก 1 key sequence pattern ไว้ใน review: `[TLE: SEQUENCE] A → B → C led to [outcome] — watch for [A] in future sessions`

ถ้าไม่มี notable sequence วันนี้ → ข้ามเงียบๆ

### 8.992 Parasomnia — Autopilot Rate Audit

ตรวจว่า decisions วันนี้มีกี่ % ที่ผ่าน conscious checklist vs เกิดจาก reflex

นับ decisions ทุกอัน (entry, exit, hold, skip) แล้ว classify:
- **Conscious:** ผ่าน IF-THEN check ก่อนทำ + มี explicit reason
- **Autopilot/Reflex:** ทำเพราะ momentum / habit / เห็นแล้วทำเลย

```
Parasomnia Autopilot Rate:
Total decisions today: N
- Conscious: X (X%)
- Autopilot/Reflex: Y (Y%)
Autopilot Rate: Y%
```

**Thresholds:**
- < 20% autopilot → `[PARASOMNIA: CONTROLLED]` — process intact
- 20–30% → `[PARASOMNIA: ELEVATED]` — note patterns ที่ trigger reflex
- > 30% → `[PARASOMNIA: HIGH AUTOPILOT]` — flag วันนี้ว่า "review quality questionable" + mandatory: redo 1 key decision tomorrow with fresh analysis

ถ้าไม่มี active trading วันนี้ → ข้ามเงียบๆ

### 9. Print verdict + personal note prompt

แสดงให้ user:

**Full mode:**
```
Post-market review saved: vault/20_investment/_journal/<date>-review.md

Verdict: [1-2 ประโยคสรุป calibration]
Example: "Base scenario ถูก (S&P -0.6%) แต่ confidence medium เกินไปเมื่อเทียบกับ VIX ที่สูง — next time ลด confidence เป็น low ถ้า VIX > 19"
```

**Review-only mode:**
```
Post-market review saved: vault/20_investment/_journal/<date>-review.md [review-only]

Summary: [1-2 ประโยค — วันนี้ตลาดเป็นยังไง, driver หลัก]
```

**Weekly-calibration reminder** — ตรวจ OUTCOMES.md หา entry ล่าสุดที่มี "weekly-calibration" หรือดู date ของ review file ล่าสุดใน `vault/20_investment/_journal/`:
```bash
ls vault/20_investment/_journal/*-review.md | tail -1
```
ถ้า review file ล่าสุดที่มี calibration > 7 วันก่อน → แสดง:
`→ /weekly-calibration ยังไม่ได้รัน X วัน — แนะนำรันก่อนสิ้นสัปดาห์`

จากนั้นถาม:
> **อยาก add note ส่วนตัวลง OUTCOMES ก่อน save? (y/n)**

ถ้า y → รอ user พิมพ์ note → append ต่อท้าย entry ใน OUTCOMES.md:
`... | Personal note: <user input>`

ถ้า n → จบ

---

## Constraints

- **Brief + decision tree: read-only** — ห้ามแก้ไขไม่ว่ากรณีใด
- **ทุก market data ต้อง verify จาก source** — flag conflicts, ใส่ `[unverified]` ถ้าหาไม่เจอ
- **ห้าม fabricate ตัวเลข** — Hypothetical P/L ต้องคำนวณจาก trigger + ราคาจริง ถ้าไม่มีราคาจริงให้ใส่ [unverified]
- **Warn ก่อน overwrite** — ถ้า `<date>-review.md` มีอยู่แล้วต้องถามก่อนเสมอ
- **Token budget:** ~5-6K tokens — เพิ่มจาก KB sync (grep + potential writes)

## Anti-patterns

- ❌ แก้ไข premarket.md หรือ decision-tree.md ไม่ว่ากรณีใด
- ❌ Fabricate P/L — ถ้าราคาจริงไม่ได้ = [unverified]
- ❌ ตัดสิน Actual scenario ด้วย "รู้สึก" — ใช้ S&P 500 % change ตาม threshold ที่กำหนดเสมอ
- ❌ ข้าม Blind Spots section (full mode) — ต้องระบุเสมอ แม้จะบอกว่า "ไม่พบ blind spot"
- ❌ Skip OUTCOMES.md append — ทุก review ต้อง append ทุกครั้ง (ทั้ง 2 mode)
- ❌ Overwrite review file โดยไม่ warn — ต้องถามก่อนเสมอ
- ❌ ประเมิน calibration เป็น "well-calibrated" ถ้าทิศทางผิด — direction wrong = ไม่สามารถ well-calibrated ได้
- ❌ หยุด (abort) เมื่อไม่พบ premarket.md — ต้อง switch เป็น review-only mode แทน ไม่ใช่หยุด
- ❌ Fabricate contradiction ใน 8a — append เฉพาะถ้ามี source ขัดแย้งจริงเท่านั้น ห้ามสร้างขึ้นมา
- ❌ Extract atom ที่เป็น opinion ใน 8b — claim ต้อง falsifiable เท่านั้น ("VIX > 20 นำ S&P ลง" ✅ / "ตลาดน่ากลัว" ❌)

## Commit

หลัง /review ผ่าน → รัน:
```bash
bash scripts/safe-commit.sh "notes: post-market YYYY-MM-DD"
```
