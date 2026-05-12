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
