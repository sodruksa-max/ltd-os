# Pre-Trade Decision Tree — 2026-04-29 (วันพุธ)
*อ้างอิงจาก [[2026-04-29-premarket]] | สร้างต่อจาก brief | ใช้ประกอบการตัดสินใจเท่านั้น ไม่ใช่คำแนะนำลงทุน*

---

> **Context วันนี้:** VIX ~18–18.60 | S&P futures 7,170.75 (-0.00%) | Nasdaq +0.26% | Brent $113.47 | WTI $99.32 (ข้ามจิตวิทยา $100 เมื่อคืน) | Events: FOMC 2pm ET + Mag7 after close + Iran ongoing
> **Most Likely Scenario: Base** — FOMC hold ตามคาด + Powell tone ระวัง + Mag7 results mixed + Iran status quo; ตลาดเช้าเงียบ แล้วระเบิดหลัง 2pm ET
> **Risk Level:** สูงมาก (3 concurrent events → confidence = LOW ไม่มีข้อยกเว้น)

---

## Today's Plan (Base Scenario)

*5 actions สำหรับวันนี้ ถ้า scenario ยังเป็น Base*

| #     | Action                                                                                                                                                                                                                   |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1** | **XLE — รอ trigger:** เข้าก่อนได้ถ้า XLE เปิด > $57.71 **และ** Brent ยังอยู่เหนือ $112 ณ 9:30am ET; ถ้าไม่เกิด trigger ภายใน 10:30am ET → void; ถ้าเข้าแล้ว ออกทั้งหมดก่อน 2:00pm ET ไม่มีข้อยกเว้น                      |
| **2** | **TLT — รอ FOMC ก่อนเสมอ:** ห้ามเข้าก่อน 2:00pm ET; หลัง statement ออกดู reaction 15 นาที (2:00–2:15pm); ถ้า Powell hawkish → พิจารณา short TLT (TBT/TLT puts); ถ้า dovish → long TLT; entry window 2:00–2:45pm เท่านั้น |
| **3** | **QQQ — รอ Mag7 results ก่อน; entry พรุ่งนี้ (Apr 30):** ไม่เข้า QQQ วันนี้เด็ดขาด รอดู earnings after close แล้วประเมินพรุ่งนี้เช้า (≥ 3/4 beat GAAP = bullish; ≥ 2/4 miss GAAP = bearish/avoid)                        |
| **4** | **Cash buffer ≥ 40%:** เหตุผล — 3 event risks พร้อมกัน + VIX ~18 ยังในโซนระวัง; ถ้า VIX ข้าม 22 ระหว่างวัน → เพิ่ม cash เป็น 100% ทันที                                                                                  |
| **5** | **Time-of-day:** ไม่เข้า new position หลัง 3:00pm ET; ช่วง 11:30am–1:30pm ET (lunch lull — ตลาดเบา ราคาเบี่ยงง่าย) = ไม่ใช่ช่วง entry; ช่วง 2:00–2:45pm ET = TLT window เท่านั้น                                         |

---

## Contingency Plans

### ถ้า flip → Bullish
**Triggers ที่ต้องเกิด (อย่างน้อย 2 ใน 3):**
- Powell tone neutral-to-dovish อย่างชัดเจน (ไม่ปิดประตู June cut)
- 10Y Yield ลดลงหลัง FOMC statement (< 4.30%)
- VIX หลุดต่ำกว่า 17 หลัง Powell press conference

**ปรับ action:**
- XLE: ถือต่อได้จนถึง EOD ถ้า trigger แรกเกิดก่อน FOMC แล้ว Bullish flip ยืนยัน
- TLT: ปรับเป็น long TLT entry (ไม่ใช่ short)
- QQQ: setup พรุ่งนี้ยังใช้ได้ — ถ้า Mag7 results beat ด้วย → เพิ่ม confidence ขนาด position
- Cash buffer ≥ 25% (ลดได้เพราะ scenario ชัดขึ้น)

### ถ้า flip → Bearish
**Triggers ที่ต้องเกิด (อย่างน้อย 1 ใน 3):**
- Powell ปิดประตู June cut ชัดเจน หรือพูดถึง "potential hike"
- S&P 500 หลุดต่ำกว่า 7,100 intraday หลัง FOMC
- VIX ข้าม 22 ระหว่างวัน

**ปรับ action:**
- XLE Setup 1: ถ้าเข้าไปแล้ว → ออกทันทีเมื่อ Bearish trigger เกิด ไม่รอ time-stop
- TLT: ปรับเป็น short TLT / TBT (yield พุ่ง scenario) แต่รอ confirm หลัง Powell ก่อน
- QQQ: skip การ long พรุ่งนี้ทั้งหมด แม้ Mag7 beat — Bearish macro ชนะ earnings beat ในระยะสั้น
- Cash buffer ≥ 60%; ถ้า VIX ข้าม 22 → 100%

---

## Pre-Commit Rules
*rules เหล่านี้ยอมรับล่วงหน้า — ถ้าเงื่อนไขเกิดขึ้น ให้ทำตามโดยไม่ต้องคิดใหม่*

**Circuit Breakers (ปิด position ก่อน):**
- `if VIX > 22 intraday` → close all positions, ถือ cash 100% ไม่มีข้อยกเว้น
- `if S&P 500 หลุด 7,050 intraday` → ลด total exposure 50% ทันที
- `if S&P + TLT + GLD ร่วงพร้อมกัน > 1% ใน 30 นาที` → exit ทุก position, cash 100% — correlation breakdown
- `if WTI กลับข้ามขึ้น $100+ และ Brent ข้าม $115 ในวันเดียวกัน` → ออก XLE ทำกำไร + เพิ่ม cash (stagflation narrative เปลี่ยน risk profile)

**Setup Invalidation (ยกเลิก setup ทันที):**
- XLE Setup 1: Brent หลุดต่ำกว่า $110 หรือมีข่าว Iran ceasefire ก่อน 10:30am ET → void ทันที
- TLT Setup 2: ไม่มี reaction ชัดเจนต่อ TLT ใน 2:00–2:15pm ET → ไม่เข้า; หรือเข้าแล้วไม่ยืนยัน direction ก่อน 3:00pm ET → ออก
- QQQ Setup 3: AAPL (reports Apr 30) ผลแย่ขัดแย้งกับ Mag7 beat → รอก่อน ไม่ขยาย position

**Earnings Signal (วันพรุ่งนี้):**
- ถ้า MSFT + AMZN + GOOGL + META ทุกเจ้า miss GAAP EPS → ลด QQQ exposure / tech exposure 50% จากระดับปกติ
- ถ้า ≥ 3/4 beat GAAP + guidance คงหรือเพิ่ม → QQQ long swing เป็น valid play พรุ่งนี้เช้า
- **GAAP เท่านั้น** — adjusted beat โดยไม่มี GAAP beat ไม่นับ (lesson UPS 2026-04-28)

**Profit-Taking Rules:**
- XLE Setup 1: take partial profit ที่ $58.50 (target แรก); ถ้าถึง $59.00 → ออกทั้งหมดก่อน 2pm ET
- TLT Setup 2: take profit ถ้า TLT เคลื่อน ±1.5% จาก entry ก่อน 3pm ET; ไม่รอมากกว่านั้น
- QQQ Setup 3 (Swing): take partial profit หลัง +2% จาก entry price วันพรุ่งนี้ (Apr 30); full exit ถ้า AAPL miss หลัง close Apr 30

**Time-of-Day Rules:**
- `ห้ามเข้า new position หลัง 3:00pm ET`
- `11:30am–1:30pm ET (lunch lull)` = ไม่ใช่ช่วง entry ทุกกรณี
- `2:00–2:45pm ET` = TLT window เท่านั้น
- `ก่อน 10:30am ET` = XLE window เท่านั้น; ถ้าไม่ trigger → void

**Event Day Protocol:**
- FOMC วันนี้ (2pm ET): ลด position size ทั้งหมดลง 30–50% ก่อน 1:30pm ET; รอ reaction ก่อนสร้าง new positions ขนาดปกติ
- Mag7 after close: ห้ามถือ QQQ/tech position ขนาดใหญ่ข้ามคืน ก่อนรู้ผล earnings
- GDP + PCE + ECI พรุ่งนี้เช้า: ถ้า QQQ setup triggered → เตรียม react ต่อ macro data เช้า Apr 30 ด้วย

---

## Decision Confidence Check

*ทำก่อนปิด decision tree — ทุก checkbox ต้องมี action เฉพาะ*

- [x] **Today's Plan ชัดเจนทุก action** — XLE (ก่อน 10:30am), TLT (หลัง 2pm), QQQ (พรุ่งนี้), cash 40%, time-of-day → ไม่ต้อง council
- [ ] **มี dilemma ระหว่าง setups** — ไม่มี conflict ระหว่าง setups ทั้ง 3 เพราะ time window ต่างกันชัดเจน
- [ ] **Position size ผิดปกติ** — cash 40% ใน event day สอดคล้องกับ VIX ~18 + 3 events; ไม่ต้อง council
- [x] **ข้อควรระวัง:** XLE (Day) + TLT (Day post-FOMC) + QQQ (Swing พรุ่งนี้) เป็น 3 setup ที่มีทิศทางต่างกันได้ — ถ้า Bearish flip หลัง FOMC: XLE ออก, TLT ปรับ short, QQQ skip → action ชัดแล้วใน Contingency Plans ด้านบน

---

> **DISCLAIMER: ตารางนี้เป็น educational framework เพื่อการวางแผนความคิดเท่านั้น ไม่ใช่คำแนะนำลงทุน ทุกการตัดสินใจขึ้นอยู่กับผู้อ่านแต่เพียงผู้เดียว การลงทุนมีความเสี่ยง**
