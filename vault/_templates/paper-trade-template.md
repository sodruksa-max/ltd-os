---
ticker: TICKER
direction: long
status: open
date_open: YYYY-MM-DD
date_close: ~
entry: ~
stop: ~
exit: ~
size: ~
result: ~
setup_source: ""
---

# Paper Trade — TICKER (LONG/SHORT) — YYYY-MM-DD
*Paper trading — ไม่ใช่เงินจริง | อ้างอิง [[YYYY-MM-DD-premarket]]*

---

## ข้อมูล Trade

| Field | Value |
|---|---|
| **Ticker** | TICKER |
| **Direction** | Long (ซื้อ/เดิมพันขึ้น) / Short (เดิมพันลง) |
| **Status** | Open |
| **Date opened** | YYYY-MM-DD HH:MM ET |
| **Date closed** | — |
| **Setup source** | [[YYYY-MM-DD-premarket]] Setup X |

---

## ราคา

| | ราคา | หมายเหตุ |
|---|---|---|
| **Entry (ราคาเข้า)** | $0.00 | open price หรือ trigger price ตาม setup |
| **Stop loss (จุดตัดขาดทุน)** | $0.00 | ถ้าหลุดนี้ออกทันที ไม่มีข้อยกเว้น |
| **Target 1 (เป้าแรก)** | $0.00 | exit บางส่วน (50%) |
| **Target 2 (เป้าสอง)** | $0.00 | exit ส่วนที่เหลือ (ถ้ามี) |
| **Exit (ราคาออก)** | — | *กรอกตอนปิด* |

---

## Position (ขนาดการลงทุน)

| | Value |
|---|---|
| **Size ($)** | $0 (0% of 100K) — ไม่เกิน 5K ต่อ trade ช่วงแรก |
| **Shares สมมติ** | 0 หุ้น ($size ÷ entry) |
| **Risk ($)** | $0 (entry − stop) × shares |

---

## ผลลัพธ์ *(กรอกตอนปิด — R-multiple คำนวณอัตโนมัติโดย stats script)*

| | Value |
|---|---|
| **P/L ($)** | — |
| **P/L (%)** | — |
| **R-multiple** | — *(auto-calculated)* |
| **Win / Loss / Breakeven** | — |
| **Days held** | — |

---

## Notes

### เหตุผลที่เข้า
[trigger จาก premarket คืออะไร, สอดคล้องกับ scenario ไหน]

### เหตุผลที่ออก
[hit target / stop hit / time-stop / circuit breaker triggered / manual exit]

### Lesson (1 ประโยค)
[เรียนรู้อะไร — ถ้าสำคัญพอใส่ใน next brief]
