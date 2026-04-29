---
description: Post-market review — compare /pre-market predictions vs reality. Run each morning (Thailand time) after US market close. Requires pre-existing premarket brief + decision tree for the target date.
---

# /post-market

Review market outcomes against pre-market predictions. Produces a calibration record, setup outcomes, and lessons for next brief.

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

Read both files — **ห้ามแก้ไขทั้งสองไฟล์นี้ไม่ว่ากรณีใด:**

- `vault/20_investment/_journal/<date>-premarket.md`
- `vault/20_investment/_journal/<date>-decision-tree.md`

ถ้าไฟล์ใดไม่มี → หยุดและแจ้ง user:
> ❌ ไม่พบ `<date>-premarket.md` หรือ `<date>-decision-tree.md` — ไม่สามารถทำ post-market review ได้

Extract จาก brief:
- **Most Likely Scenario:** Bullish / Base / Bearish + confidence level
- **Setups 1/2/3:** ticker, direction, trigger conditions, invalidation
- **Polymarket odds** (ถ้ามีใน brief)
- **Earnings ที่ mention** (tickers)
- **Pre-commit rules** ที่ระบุไว้ใน decision tree (circuit breakers, setup invalidation, earnings signal)

### 3. Fetch actual market results

Fire these searches **in parallel**:

**Search queries (run all at once):**
- `S&P 500 Nasdaq Dow Jones close <DATE> stock market results`
- `VIX close intraday high <DATE>`
- `XLE XLK XLP XLU XLY GLD TLT ETF performance <DATE>`
- `Brent WTI crude oil close price <DATE>`
- `[EARNINGS TICKERS from brief] earnings results EPS actual <DATE>`

**WebFetch:**
- `https://finance.yahoo.com/markets/stocks/` — extract close prices if available

**Data to collect:**

| Metric | Target |
|---|---|
| S&P 500 | open, high, low, close, % change |
| Nasdaq-100 | close, % change |
| Dow Jones | close, % change |
| VIX | close + intraday high |
| XLE, XLK, XLP, XLU, XLY | % change each |
| GLD, TLT | % change each |
| Brent crude | close |
| WTI crude | close |
| Earnings tickers | EPS actual vs estimate, % move after-hours |

**Conflict rule:** ถ้า 2 sources ให้ค่าต่างกัน → flag ⚠️ CONFLICT แสดงทั้งสองค่า ไม่เลือกข้างใดข้างหนึ่ง

**ถ้าหาตัวเลขไม่ได้:** ใส่ `[unverified]` — ห้าม fabricate

### 4. Determine Actual Scenario

ใช้ผลจริงของ S&P 500 เพื่อตัดสิน:
- S&P 500 close > +0.3% → **Bullish**
- S&P 500 close -0.3% ถึง +0.3% → **Base**
- S&P 500 close < -0.3% → **Bearish**

### 5. Check overwrite

ถ้า `vault/20_investment/_journal/<date>-review.md` มีอยู่แล้ว → หยุดและถาม:
> ⚠️ พบ `<date>-review.md` อยู่แล้ว — overwrite? (y/n)
ถ้า n → จบโดยไม่แตะไฟล์

### 6. Generate review file

Save to `vault/20_investment/_journal/<date>-review.md`:

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

---

## Setup Outcomes

| Setup | Ticker | Trigger เกิด? | ทิศทางที่ predict | ผลจริง | Hypothetical P/L |
|---|---|---|---|---|---|
| Setup 1 | [ticker] | Yes / No / [unverified] | [Long/Short/Skip] | [+/-X%] | [+/-X% ถ้าเข้าตาม plan / N/A ถ้า skip] |
| Setup 2 | [ticker] | Yes / No / [unverified] | [Long/Short/Skip] | [+/-X%] | [+/-X% / N/A] |
| Setup 3 | [ticker] | Yes / No / [unverified] | [Long/Short/Skip] | [+/-X%] | [+/-X% / N/A] |

*Hypothetical P/L = สมมติว่าเข้า position ตาม plan ตรงๆ ไม่รวม slippage/commission เป็นตัวเลขเพื่อ learning เท่านั้น ไม่ใช่ผลกำไรจริง*

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

### 7. Append to OUTCOMES.md

Append 1 line to `vault/_memory/OUTCOMES.md`:

```
<date> — Predicted: <X> (<confidence>), Actual: <Y>, Match: <Yes/Partial/No>, Calibration: <well-calibrated/over-confident/under-confident>, Top lesson: <Z>
```

ถ้าไฟล์ไม่มี → สร้างใหม่ก่อน

### 8. Print verdict + personal note prompt

แสดงให้ user:

```
Post-market review saved: vault/20_investment/_journal/<date>-review.md

Verdict: [1-2 ประโยคสรุป calibration]
Example: "Base scenario ถูก (S&P -0.6%) แต่ confidence medium เกินไปเมื่อเทียบกับ VIX ที่สูง — next time ลด confidence เป็น low ถ้า VIX > 19"
```

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
- **Token budget:** ~4K tokens — เบากว่า pre-market เพราะข้อมูล backward-looking

## Anti-patterns

- ❌ แก้ไข premarket.md หรือ decision-tree.md ไม่ว่ากรณีใด
- ❌ Fabricate P/L — ถ้าราคาจริงไม่ได้ = [unverified]
- ❌ ตัดสิน Actual scenario ด้วย "รู้สึก" — ใช้ S&P 500 % change ตาม threshold ที่กำหนดเสมอ
- ❌ ข้าม Blind Spots section — ต้องระบุเสมอ แม้จะบอกว่า "ไม่พบ blind spot"
- ❌ Skip OUTCOMES.md append — ทุก review ต้อง append ทุกครั้ง
- ❌ Overwrite review file โดยไม่ warn — ต้องถามก่อนเสมอ
- ❌ ประเมิน calibration เป็น "well-calibrated" ถ้าทิศทางผิด — direction wrong = ไม่สามารถ well-calibrated ได้
