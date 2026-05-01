# Pre-Trade Decision Tree — 2026-04-30 (วันพฤหัสบดี)
*อ้างอิงจาก [[2026-04-30-premarket]] | สร้างต่อจาก brief | ใช้ประกอบการตัดสินใจเท่านั้น ไม่ใช่คำแนะนำลงทุน*

---

> **Context วันนี้:** VIX 18–19 (cautious) | S&P futures +0.37% (7,194.75) | Brent $114.70 (ลงจาก $126 spike) | Gold $4,643 (+1.79%) | Events: GDP+PCE+ECI 8:30am ET + AAPL earnings after close
> **Most Likely Scenario: Base** — GDP Q1 น่าจะแสดง slowdown (ชะลอ) จาก tariff drag แต่ไม่ถดถอย; PCE ยังสูงกว่า 2% target; ตลาด chop ในกรอบแคบรอ AAPL earnings
> **Risk Level:** สูง — 3 event risks พร้อมกัน (GDP/PCE/ECI + AAPL Mag7 earnings + Presidential Action Risk ที่ยังไม่ resolve) → confidence = Low เสมอ

---

## Today's Plan (Base Scenario)

*5 actions สำหรับวันนี้ ถ้า scenario ยังเป็น Base*

| # | Action |
|---|---|
| **1** | **QQQ — รอ 8:30am ET data ก่อน:** ตรวจ AH scorecard ก่อน (GOOGL +7.05% vs META -7%, AMZN -3% → net -0.30pp ใน QQQ) — ถ้า GDP ≥ 2.0% AND PCE ≤ 2.8% AND QQQ เปิดบวกและ holds 10 นาที → Long QQQ half size (ครึ่งหนึ่ง); ถ้า GDP miss หรือ QQQ เปิดแล้วขายทิ้ง → skip setup นี้ทั้งหมด; **ต้องออกก่อน 3:30pm ET** |
| **2** | **XLE — swing setup ถ้า oil stable:** ถ้า Brent ≥ $112 หลังตลาดเปิด AND ไม่มี Trump announcement ใน 90 นาทีแรก AND GDP ไม่ miss ใหญ่ → XLE swing long 2–4 วัน; ถ้า Brent หลุด $110 → skip |
| **3** | **AAPL — pre-earnings drift เท่านั้น:** ถ้า GDP in-line AND AAPL เปิดเหนือ $185 AND volume ปกติ → AAPL day long half size; **ต้องออกทั้งหมดภายใน 3:00pm ET ไม่มีข้อยกเว้น** ก่อน earnings AH |
| **4** | **Cash buffer ≥ 25%:** วันนี้มี 3 event risks → ถือ cash สูงกว่าปกติตลอดวัน เพื่อรับมือกับ surprise ทิศทางใดก็ได้ |
| **5** | **Time-of-day:** ไม่เข้า new position หลัง 3:00pm ET; หลีกเลี่ยง 11:30am–1:30pm ET (lunch lull — ช่วงพักตลาด ซื้อขายเบา); window สำคัญ: 8:30–9:45am ET (GDP/PCE reaction) และ 2:00–3:00pm ET (ก่อน close) |

---

## Contingency Plans (แผนสำรองถ้า scenario เปลี่ยน)

### ถ้า flip → Bullish
**Triggers ที่ต้องเกิด (อย่างน้อย 2 ใน 3):**
- GDP Q1 ≥ 2.0% annualized (เศรษฐกิจดีกว่าที่กลัว)
- PCE ≤ 2.5% (เงินเฟ้อลดลง → Fed ไม่จำเป็นต้องขึ้นดอกเบี้ย)
- S&P 500 ทะลุ 7,220 ใน 30 นาทีแรกหลัง data ออก

**ปรับ action:**
- Setup 1 QQQ: เพิ่ม size เป็น full (ขนาดเต็ม) แทน half
- Setup 3 AAPL: เพิ่ม confidence เล็กน้อยแต่ยังต้องออกก่อน 3:00pm ET เสมอ
- XLK, XLY พิจารณาเพิ่ม
- Cash buffer ≥ 15% (ลดได้เพราะ signal ชัดขึ้น)

### ถ้า flip → Bearish
**Triggers ที่ต้องเกิด (อย่างน้อย 1 ใน 3):**
- GDP Q1 < 1.0% (recession territory — เขตถดถอยทางเทคนิค)
- PCE > 3.0% (stagflation warning — กลัวเงินเฟ้อพุ่งพร้อมเศรษฐกิจซึม)
- Trump executive announcement ใหม่ (tariff รอบใหม่, Iran military escalation ระดับ new)

**ปรับ action:**
- ยกเลิก Setup 1 QQQ และ Setup 3 AAPL ทันที
- Setup 2 XLE: ประเมินใหม่ — ถ้า GDP miss ทำ broad selloff อาจดึง XLE ลงด้วยแม้ oil สูง
- พิจารณา: XLP (สินค้าจำเป็น — defensive), XLV (สุขภาพ), GLD (ทองคำ) แทน
- Cash buffer ≥ 40%+

---

## Pre-Commit Rules (กฎที่ยอมรับล่วงหน้า — ถ้าเงื่อนไขเกิดขึ้น ให้ทำตามทันทีโดยไม่ต้องคิดใหม่)

**Circuit Breakers (ปิด position ก่อน — กฎบังคับปิด position อัตโนมัติ):**
- `if VIX > 22` → close all positions (ปิดทุก position ทันที), ถือ cash 100% ไม่มีข้อยกเว้น
- `if S&P 500 หลุด 7,050 intraday` → ลด total exposure (ความเสี่ยงรวม) 50% ทันที
- `if S&P + TLT + GLD ร่วงพร้อมกัน > 1% ใน 30 นาที` → exit ทุก position, cash 100% — correlation breakdown (ทุก asset ร่วงพร้อมกัน = เครื่องมือป้องกันปกติไม่ทำงาน)

**Setup Invalidation (ยกเลิก setup ทันที):**
- QQQ Setup 1: GDP miss ใหญ่ (< 1.5%) OR PCE > 3.0% OR QQQ เปิดแล้วขายทิ้งใน 5 นาทีแรก
- XLE Setup 2: Brent หลุด $110 intraday OR Trump ประกาศ lift naval blockade
- AAPL Setup 3: AAPL เปิดต่ำกว่า $183 OR GDP miss ทำ broad selloff OR ข่าวลบ AAPL ก่อนตลาดเปิด

**Earnings Signal — AAPL Rule:**
- ถ้า pre-market AAPL leaked numbers (ข้อมูลหลุด) หรือ analyst cuts (นักวิเคราะห์ปรับลด target) → อย่าเข้า Setup 3 แม้ GDP จะดี
- AAPL AH หลังตลาดปิด: ถ้าลง > -5% → XLK และ QQQ เปิดพรุ่งนี้น่าจะกดดัน — เตรียม brief พรุ่งนี้ให้คำนึงถึงสิ่งนี้

**Profit-Taking Rules (กฎเก็บกำไร):**
- QQQ Setup 1: ถ้าได้ +0.7% → sell half (ขายครึ่งหนึ่ง), move stop-loss (ขยับจุดตัดขาดทุน) เป็น breakeven (ราคาเข้า)
- XLE Setup 2: target แรก $60 → sell half; target สอง $61 → sell ส่วนที่เหลือหรือ trail stop (stop ตามราคาขึ้น)
- AAPL Setup 3: ถ้าได้ +1.0% ก่อน 1:00pm ET → sell half; **ออกทั้งหมดก่อน 3:00pm ET ไม่มีข้อยกเว้น**

**Time-of-Day Rules:**
- `ห้ามเข้า new position หลัง 3:00pm ET`
- `11:30am–1:30pm ET (lunch lull)` → ไม่ใช่ entry time
- `ออก AAPL ก่อน 3:00pm ET` — ก่อน earnings window
- `ออก QQQ ก่อน 3:30pm ET` — ก่อน AAPL earnings ดึง QQQ

**Event Day Protocol — Triple Event Risk:**
- ก่อน 8:30am ET: ลดขนาด position ทั้งหมดลง 30–50% เพื่อรับมือ data surprise
- หลัง 8:30am ET: รอ 5–10 นาทีให้ตลาด absorb (ย่อย) data ก่อน execute (ส่งคำสั่ง)
- หลัง 3:00pm ET: no new entries; จัดการ existing positions ให้เรียบร้อยก่อนปิดตลาด
- Presidential Action Risk: ถ้า Bloomberg/Reuters headline Trump announcement ระหว่างวัน → หยุดเข้า position ใหม่ทันที รอ 15 นาทีดู market reaction ก่อน

---

## Decision Confidence Check

*ทำก่อนปิด decision tree — ทุก checkbox ที่ check ต้องมี action เฉพาะ*

- [ ] Today's Plan ชัดเจนทุก action → ไม่ต้อง council
- [ ] มี dilemma: QQQ AH scorecard ผสม (net -0.30pp) แต่ GDP อาจดี → `/council "QQQ Setup 1: AH scorecard net negative แต่ GDP ดี ควรเข้า half size หรือ skip?" --expertise=financial_risk`
- [x] **แนะนำ (จาก Apr 29 review):** `/council "QQQ Setup 3: ควรเพิ่ม after-hours price reaction criterion นอกจาก GAAP EPS beat?" --expertise=financial_risk` — ยังค้างจากเมื่อวาน ควรรันก่อนหรือหลัง brief วันนี้
- [ ] Position size ปกติถ้า VIX ≤ 20 และทำตาม cash buffer ≥ 25%

---

> **DISCLAIMER: ตารางนี้เป็น educational framework เพื่อการวางแผนความคิดเท่านั้น ไม่ใช่คำแนะนำลงทุน ทุกการตัดสินใจขึ้นอยู่กับผู้อ่านแต่เพียงผู้เดียว การลงทุนมีความเสี่ยง**
