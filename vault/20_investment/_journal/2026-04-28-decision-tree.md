# Pre-Trade Decision Tree — 2026-04-28 (วันอังคาร)
*อ้างอิงจาก [[2026-04-28-premarket]] | อัพเดตจาก Setups ใหม่ (XLE / KO-UPS / TLT) | ใช้ประกอบการตัดสินใจเท่านั้น ไม่ใช่คำแนะนำลงทุน*

---

> **Context วันนี้:** VIX 19.24 (↑ ขึ้นต่อเนื่องตลอดเช้า) | S&P futures 7,159.25 (-0.65%) | Nasdaq futures -1.23% | Dow futures +0.20% | Brent $111.57 | FOMC Day 1 | Iran stalled | KO+UPS earnings วันนี้ | Mag7 earnings พุธนี้
> **Most Likely Scenario: Base** — ตลาดรอ Powell พรุ่งนี้ ไม่มี catalyst ใหม่วันนี้ circuit breakers ยังไม่ถูก trigger
> **Risk Level:** สูงกว่าปกติ — VIX ใกล้ 20, Gold ร่วง -2.55% ทั้งที่ oil ขึ้น (สัญญาณ correlation ผิดปกติ)

---

## Today's Plan (Base Scenario)

*5 actions สำหรับวันนี้ ถ้า scenario ยังเป็น Base*

| # | Action |
|---|---|
| **1** | **XLE — เข้าครึ่งขนาด:** ถ้า Brent ≥ $108 เมื่อตลาดเปิด AND ไม่มีประกาศ Iran ceasefire → เข้า XLE ครึ่งขนาด (Swing 3–5 วัน); overall portfolio ≤ 10% เพราะ VIX สูง; ถ้า Brent ทะลุ $112 ก่อน 2:00pm ET → พิจารณาเพิ่ม |
| **2** | **KO/UPS — รอผลก่อน 10:30am ET:** ถ้าทั้งคู่ beat EPS AND ไม่มี guidance cut → monitor XLP intraday bounce; ถ้า miss → ลด total position 30% ทันที (pre-commit rule); ถ้าผลดีแต่ตลาดไม่ respond ภายใน 10:30am ET → ไม่เข้าเพิ่ม |
| **3** | **TLT — ไม่มีการ action วันนี้:** รอ Powell press conference พรุ่งนี้ 2:30pm ET; ห้าม position ก่อน press conference ทุกกรณี |
| **4** | **Cash buffer ≥ 85%:** วันนี้เป็น waiting day — เก็บ cash ไว้รอ Powell พรุ่งนี้และ Mag7 earnings พุธนี้ |
| **5** | **Time-of-day:** ไม่เข้า new position หลัง 3:00pm ET; หลีกเลี่ยง 11:30am–1:30pm ET (lunch lull — volume ต่ำ ราคาหลอกได้ง่าย) |

---

## Contingency Plans

### ถ้า flip → Bullish
**Triggers ที่ต้องเกิด (อย่างน้อย 2 ใน 3):**
- KO + UPS beat EPS + positive guidance
- VIX กลับลงใต้ 18
- S&P cash เปิดน้อยกว่า futures ที่บอก (institutional buying signal)

**ปรับ action:**
- XLE: เพิ่มจากครึ่งขนาดเป็น full allocation ของ XLE slot (overall portfolio ≤ 20%)
- KO/UPS reaction: เข้า XLP day trade ถ้า beat + respond ก่อน 10:30am ET
- Cash buffer ≥ 70% (แม้ bullish ก็ยัง FOMC week — ห้าม bet หนัก)
- ยังไม่เข้า TLT วันนี้ไม่ว่ากรณีใด — รอ Powell พรุ่งนี้

### ถ้า flip → Bearish
**Triggers ที่ต้องเกิด (อย่างน้อย 1 ใน 3):**
- KO + UPS ทั้งคู่ miss EPS + guidance cut
- VIX > 22 intraday
- S&P 500 หลุด 7,050 intraday

**ปรับ action:**
- ลด total position 30% ทันที (KO/UPS miss) หรือ cash 100% (VIX > 22)
- Exit XLE ทุก position ถ้าเข้าไปแล้ว — Bearish scenario มาจาก macro deterioration ไม่ใช่ Iran deal
- ไม่เข้า TLT วันนี้ถึงแม้ yield จะ dip — dip ก่อน FOMC คือ noise ไม่ใช่ trend
- Cash buffer ≥ 90%

---

## Pre-Commit Rules
*rules เหล่านี้ยอมรับล่วงหน้า — ถ้าเงื่อนไขเกิดขึ้น ให้ทำตามโดยไม่ต้องคิดใหม่*

**Circuit Breakers (ปิด position ก่อน):**
- `if VIX > 22` → close all positions, ถือ cash 100% ไม่มีข้อยกเว้น
- `if S&P 500 หลุด 7,050 intraday` → ลด total exposure 50% ทันที ไม่รอ stop loss
- `if S&P + TLT + GLD ร่วงพร้อมกัน > 1% ใน 30 นาที` → exit ทุก position, cash 100% — correlation breakdown

**Setup Invalidation (ยกเลิก setup ทันที):**
- `if Iran ceasefire confirmed อย่างเป็นทางการ` → exit XLE (Setup 1) ทันที ไม่รอ stop
- `if Brent > $112 ก่อน 10:30am ET` → XLE ยังดีอยู่ (เป็น upside สำหรับ energy) แต่ ยกเลิก KO/UPS earnings reaction ถ้ายังไม่เข้า เพราะ macro ผันผวนเกิน
- `if Powell hawkish พรุ่งนี้` → ไม่เข้า TLT (Setup 3) แม้ yield จะ dip ชั่วคราว — dip นั้นเป็น noise ไม่ใช่ trend reversal

**Earnings Signal:**
- `if KO + UPS ทั้งคู่ miss EPS + guidance cut วันนี้` → ลด total position 30% ทันที — สองตัวนี้เป็น barometer เศรษฐกิจ ถ้า miss พร้อมกัน = signal consumer อ่อนแอกว่าคาด

**Profit-Taking Rules:**
- `if XLE +5% intraday` → ขายครึ่ง position ทันที, ย้าย stop ขึ้นมาที่ +2% จากราคาเข้า (trail stop)
- `if XLP +2% ภายใน 1 ชั่วโมงหลังเข้า (KO/UPS reaction)` → exit ทั้งหมดทันที — news-driven move มักไม่ sustain หลังจุดสูง
- `if TLT +1.5% หลัง FOMC (พรุ่งนี้)` → ขายครึ่ง position, รอดูว่า trend ต่อหรือ reversal ก่อนตัดสินใจส่วนที่เหลือ

**Time-of-Day Rules:**
- `ห้ามเข้า new position หลัง 3:00pm ET` — ความผันผวนสูง spread กว้าง ออกยากถ้าผิดทาง
- `11:30am–1:30pm ET (lunch lull)` → ไม่ใช่ entry time ปริมาณการซื้อขายต่ำ ราคาหลอกได้ง่าย รอ volume กลับมาก่อน

**Event Day Protocol (พรุ่งนี้ — FOMC announcement + Mag7 earnings):**
- `if S&P 500 opens down > 1% พรุ่งนี้ก่อน FOMC` → no new entries ทั้งวัน รอ Powell ก่อน
- `if Mag7 earnings (GOOGL/AMZN/META/MSFT) miss ทั้ง 4` → reassess ทุก position ถัดไป (วันพฤหัสฯ) ก่อนพิจารณาเพิ่ม

---

> **DISCLAIMER: ตารางนี้เป็น educational framework เพื่อการวางแผนความคิดเท่านั้น ไม่ใช่คำแนะนำลงทุน ทุกการตัดสินใจขึ้นอยู่กับผู้อ่านแต่เพียงผู้เดียว การลงทุนมีความเสี่ยง**
