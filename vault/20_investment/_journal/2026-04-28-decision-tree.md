# Pre-Trade Decision Tree — 2026-04-28 (วันอังคาร)
*อ้างอิงจาก [[2026-04-28-premarket]] | สร้างก่อนตลาดเปิด | ใช้ประกอบการตัดสินใจเท่านั้น ไม่ใช่คำแนะนำลงทุน*

---

> **Context วันนี้:** VIX 18.02 | S&P 7,174 | Brent $108 | FOMC Day 1 | Iran deal ยังไม่ confirmed  
> **Risk Level:** สูงกว่าปกติ — 3 risk events converge พร้อมกัน (Iran + FOMC + Earnings)

---

## Decision Table

| | 🟢 Bullish — Iran deal confirmed + earnings beat | 🟡 Base — ทรงตัว รอ FOMC พรุ่งนี้ | 🔴 Bearish — Iran ล้มเหลว + Powell hawkish |
|---|---|---|---|
| **Setup 1**<br>DAL / UAL (Airlines)<br>*Day / Swing ขึ้นกับเวลาข่าว* | **เข้า** — Iran official confirmation + Brent < $100 = trigger ครบ โดย:<br>• ก่อน **10:30am ET** → เข้า Day trade ออกก่อน close<br>• **10:30am–2:00pm ET** → เข้า Swing hold overnight ได้<br>• หลัง **2:00pm ET** → ไม่เข้าเลย ไม่คุ้มความเสี่ยงค้างคืน | **Wait** — รอข่าว Iran ก่อน ถ้าไม่มีประกาศ → ใช้ time-window เดียวกัน หลัง 2pm ไม่เข้า | **Skip** — Iran ล้มเหลว = Brent ยิ่งพุ่ง airlines เสียหายหนักจาก fuel cost ห้ามเข้าเด็ดขาด |
| **Setup 2**<br>TLT (พันธบัตร ETF)<br>*Swing 2–3 วัน* | **Wait** — รอ Powell press conference พรุ่งนี้ **2:30pm ET** ก่อน (post-event entry rule) Iran deal อาจดัน yields เด้งแทน → ทิศทาง TLT ไม่ชัด | **Wait** — รอฟัง Powell พรุ่งนี้ ถ้า tone dovish จริง ("inflation risks balanced") ค่อยเข้าหลัง press conference | **Skip** — Powell hawkish = 10Y yield พุ่ง TLT ร่วง ไม่เข้าแม้ yield จะ dip ชั่วคราว |
| **Setup 3**<br>XLE (Energy ETF)<br>*Swing 3–5 วัน* | **Skip** — Iran deal confirmed = thesis ของ XLE ล้มเหลวทันที (setup สร้างบน "Iran ยังไม่จบ") ออกถ้าถือไว้ก่อนแล้ว | **เข้า ครึ่งขนาด** — Brent คงระดับ $105+ ไม่มีข่าวใหม่ รอ BP earnings confirm ก่อน แล้วค่อยเพิ่ม | **เข้า** — Iran rejected + Brent > $112 = XLE setup ชัดที่สุด XLE allocation 100% (ของ allocation ที่ตั้งไว้สำหรับ XLE) แต่ overall portfolio exposure ≤ 10% เพราะ VIX สูง |
| **Position size รวม**<br>(% ของ portfolio) | **≤ 20%** — แม้ optimistic ก็ยัง FOMC week ไม่ bet หนัก; DAL/UAL เป็น news-event play ขนาดเล็ก | **≤ 12%** — วันรอ: XLE ครึ่งขนาดเท่านั้น ที่เหลือ cash รอ signal ชัดขึ้น | **≤ 10%** — Correlation breakdown risk สูงวันนี้ ถ้าทุก risk เกิดพร้อมกัน = เจ็บได้ทุก position |
| **Cash buffer ขั้นต่ำ**<br>(% ของ portfolio) | **≥ 70%** — ต้องมีเงินสดพอรับมือ surprise ได้แม้ในวัน bullish | **≥ 85%** — วันนี้เป็น waiting day เก็บ cash ไว้รอ Powell พรุ่งนี้ | **≥ 90%** — ความเสี่ยง correlation breakdown (ทุก asset class ร่วงพร้อมกัน) สูงกว่าปกติมาก |

---

## Pre-Commit Rules
*rules เหล่านี้ยอมรับล่วงหน้า — ถ้าเงื่อนไขเกิดขึ้น ให้ทำตามโดยไม่ต้องคิดใหม่*

**Circuit Breakers (ปิด position ก่อน):**
- `if VIX > 22` → close all positions, ถือ cash 100% ไม่มีข้อยกเว้น — VIX 22 = ตลาดตื่นตระหนกแล้ว
- `if S&P 500 หลุด 7,050 intraday` → ลด total exposure 50% ทันที ไม่รอ stop loss ธรรมดา
- `if S&P + TLT + GLD ร่วงพร้อมกัน > 1% ใน 30 นาที` → exit ทุก position, cash 100% — นี่คือ correlation breakdown สัญญาณที่ defensive ไม่ช่วยแล้ว

**Setup Invalidation (ยกเลิก setup ทันที):**
- `if Iran ceasefire confirmed อย่างเป็นทางการ` → exit XLE (Setup 3) ทันที ไม่รอ stop; reassess DAL/UAL ว่า Brent ร่วงถึง $100 หรือยัง
- `if Brent > $112 ก่อน 10:30am ET` → DAL/UAL (Setup 1) void ทั้งวัน airlines ไม่ใช่ play วันนี้อีกแล้ว
- `if Powell ใช้ภาษา hawkish พรุ่งนี้` → ไม่เข้า TLT (Setup 2) แม้ yield จะ dip ชั่วคราวหลัง press conference — dip นั้นเป็น noise ไม่ใช่ trend reversal

**Earnings Signal:**
- `if KO + UPS ทั้งคู่ miss EPS + guidance cut วันนี้` → ลด total position 30% ทันที — สองตัวนี้เป็น barometer เศรษฐกิจ ถ้า miss พร้อมกัน = signal ว่า consumer อ่อนแอกว่าคาดมาก

**Profit-Taking Rules:**
- `if XLE +5% intraday` → ขายครึ่ง position ทันที, ย้าย stop ขึ้นมาที่ +2% จากราคาเข้า (trail stop)
- `if DAL/UAL +3% ภายใน 1 ชั่วโมงหลังเข้า` → exit ทั้งหมดทันที — news-driven move มักไม่ sustain หลังจุดสูง
- `if TLT +1.5% หลัง FOMC` → ขายครึ่ง position, รอดูว่า trend ต่อหรือ reversal ก่อนตัดสินใจส่วนที่เหลือ

**Time-of-Day Rules:**
- `ห้ามเข้า new position หลัง 3:00pm ET` — ช่วงท้ายวันความผันผวนสูง spread กว้าง ออกยากถ้าผิดทาง
- `11:30am–1:30pm ET (lunch lull)` → ไม่ใช่ entry time ปริมาณการซื้อขายต่ำ ราคาหลอกได้ง่าย รอ volume กลับมาก่อน

**Event Day Protocol:**
- `if S&P 500 opens down > 1% พรุ่งนี้ก่อน FOMC` → no new entries ทั้งวัน รอ Powell ก่อน ตลาดกำลังบอกว่ากลัวอะไรบางอย่าง

---

> **DISCLAIMER: ตารางนี้เป็น educational framework เพื่อการวางแผนความคิดเท่านั้น ไม่ใช่คำแนะนำลงทุน ทุกการตัดสินใจขึ้นอยู่กับผู้อ่านแต่เพียงผู้เดียว การลงทุนมีความเสี่ยง**
