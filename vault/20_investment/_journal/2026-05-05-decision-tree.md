# Pre-Trade Decision Tree — 2026-05-05 (วันอังคาร)
*อ้างอิงจาก [[2026-05-05-premarket]] | สร้างต่อจาก brief | ใช้ประกอบการตัดสินใจเท่านั้น ไม่ใช่คำแนะนำลงทุน*

---

> **Context วันนี้:** VIX 18.29 (caution) | S&P Futures +0.17% | WTI $104.33 (-2%) | Brent $113.44 | 10Y Yield 4.446% | Iran-UAE war ongoing (Hormuz risk)
> **Most Likely Scenario: Base** — Futures บวกเล็กน้อย + oil ให้คืน แต่ Iran binary ยังอยู่ → confidence: Low
> **Risk Level:** กลาง-สูง (Iran tail risk active; VIX caution zone; yield elevated)

---

## Today's Plan (Base Scenario)

*5 actions สำหรับวันนี้ถ้า Base scenario ยังเป็นจริง*

| # | Action |
|---|---|
| **1** | **QQQM — เข้า (ถ้า trigger ผ่าน):** ถ้า QQQM เปิดเหนือ S1 $275.85 AND VIX ไม่ spike เหนือ 20 ใน 1 ชั่วโมงแรก → DCA entry ที่ ~PP $277.07; upside R1 $278.77; ถ้าหลุด S1 $275.85 → รอ S2 $274.15 ก่อน |
| **2** | **XLE — รอ trigger (ภายใน 10:30am ET):** ถ้า WTI ยืนใต้ $105 หลังเปิด 30 นาที AND ไม่มีข่าว Iran ใหม่ → watch XLE fade ไป $58.50-59.00; ถ้าไม่เกิด trigger ภายใน 10:30am ET → setup void ไม่เข้า |
| **3** | **TLT — รอ (ไม่เข้าวันนี้):** watch 10Y yield ไม่ให้ทะลุ 4.47% วันนี้; setup จริงคือ post-NFP ศุกร์ May 8 ไม่ใช่วันนี้ |
| **4** | **Cash buffer ≥ 30%:** Iran tail risk ยัง active; VIX 18.29 = caution zone; ลด position size 20-30% จากปกติ — ไม่ over-leverage วันนี้ |
| **5** | **Time-of-day:** ไม่เข้า new position หลัง 3:00pm ET; หลีกเลี่ยง 11:30am–1:30pm ET (lunch lull — volume얕, spreads กว้าง) |

---

## Contingency Plans

### ถ้า flip → Bullish
**Triggers ที่ต้องเกิด (อย่างน้อย 2 ใน 3):**
- ข่าว Iran-UAE ceasefire หรือเริ่มเจรจาอย่างเป็นทางการ
- WTI ร่วงใต้ $100 (Iran premium ออกหมด)
- VIX ลงใต้ 17 + QQQM ทะลุ R1 $278.77

**ปรับ action:**
- QQQM: เข้า DCA เต็มแผน ไม่รอ trigger; เพิ่ม size ได้ถ้า VIX < 17
- XLE: ยกเลิก fade setup — ถ้า oil ร่วง XLE ไม่ work ในทาง short
- Cash buffer: ลดเหลือ ≥ 15%

### ถ้า flip → Bearish
**Triggers ที่ต้องเกิด (อย่างน้อย 1 ใน 3):**
- ข่าวอิหร่านโจมตีเพิ่ม หรือ Hormuz ประกาศปิดบางส่วนอย่างเป็นทางการ
- WTI พุ่งเหนือ $108 (ราคาน้ำมันสูงกว่า peak เมื่อวาน)
- VIX spike เหนือ 22 + SPY หลุด S2 $717.60

**ปรับ action:**
- QQQM: ยกเลิก DCA entry วันนี้ → รอ stabilization; ถ้าถือแล้วให้ hold (DCA ระยะยาวไม่ขาย)
- XLE: ไม่เข้า fade setup (oil จะ surge อีกรอบ)
- TLT: รอดูทิศทาง yield ก่อน — ถ้า oil + yield พุ่งพร้อมกัน TLT ยังลงต่อ
- Cash buffer: ≥ 50%; ถ้า correlation breakdown → cash 100%

---

## Pre-Commit Rules
*rules เหล่านี้ยอมรับล่วงหน้า — ถ้าเงื่อนไขเกิดขึ้น ให้ทำตามโดยไม่ต้องคิดใหม่*

**Circuit Breakers (ปิด position ก่อน):**
- `if VIX > 22` → close all positions, ถือ cash 100% ไม่มีข้อยกเว้น
- `if SPY หลุด S2 $717.60 intraday` → ลด total exposure 50% ทันที
- `if SPY + TLT + GLD ร่วงพร้อมกัน > 1% ใน 30 นาที` → exit ทุก position, cash 100% — correlation breakdown (เหมือนสัญญาณที่เห็นเมื่อวาน)

**Setup Invalidation (ยกเลิก setup ทันที):**
- QQQM หลุด S1 $275.85 อย่างชัดเจน → Setup 1 void; รอ S2 $274.15 stabilize ก่อน
- WTI กลับขึ้นเหนือ $107 (Iran news) → Setup 2 (XLE fade) void ทันที
- 10Y yield ทะลุ 4.55% → Setup 3 (TLT watch) void; อย่าเข้า TLT ก่อน NFP

**Event Day Protocol:**
- Iran headline ใหม่ (attack / Hormuz announcement) ระหว่างวัน → หยุดทุก setup; re-evaluate ก่อนเข้าใหม่
- NFP ศุกร์ May 8 คือ event ใหญ่ — ลด position ก่อนถึงศุกร์ถ้าถือ swing; ไม่เข้า new position หลังพุธ May 6

**Profit-Taking Rules:**
- Setup 1 (QQQM DCA Position): ไม่มี profit-take — hold ระยะยาวตามแผนเกษียณ; DCA ต่อทุกเดือน
- Setup 2 (XLE Swing): ออกที่ $58.50-$59.00 หรือถ้า WTI กลับขึ้นเหนือ $106; ไม่ hold ข้าม NFP
- Setup 3 (TLT Pre-NFP): entry เฉพาะ post-NFP ศุกร์; ออกภายใน 1-2 วันหลัง NFP reaction

**Time-of-Day Rules:**
- `ห้ามเข้า new position หลัง 3:00pm ET`
- `11:30am–1:30pm ET` → ไม่ใช่ entry time — volume얕, spread กว้าง

---

## Decision Confidence Check

*ทำก่อนปิด decision tree*

- [x] Today's Plan ชัดเจนทุก action → ไม่ต้อง council
- [ ] มี dilemma ระหว่าง setups → ไม่มีในวันนี้
- [ ] Position size รู้สึกผิดปกติ → VIX 18.29 = ลด size 20-30% ตาม rule ปกติ
- [ ] Setup ขัดกับ Most Likely Scenario → Setup 1 QQQM เป็น DCA position ไม่ใช่ directional bet; สอดคล้องกับ Base scenario

**สรุป:** ไม่ต้อง `/council` วันนี้ — action ชัด; Iran tail risk manage ด้วย circuit breakers และ cash buffer

---

> **DISCLAIMER: ตารางนี้เป็น educational framework เพื่อการวางแผนความคิดเท่านั้น ไม่ใช่คำแนะนำลงทุน ทุกการตัดสินใจขึ้นอยู่กับผู้อ่านแต่เพียงผู้เดียว การลงทุนมีความเสี่ยง**
