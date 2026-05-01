# Paper Trading Stats Dashboard
*Updated: 2026-04-30 (initial) | คำนวณอัตโนมัติจาก `scripts/stats-paper-trade.py`*

---

## Phase Status

❌ ยังไม่พร้อม — ขาด: trades 0/12, win rate 0%/40%, avg R 0/1.5

| Metric | ค่าปัจจุบัน | เป้าหมาย | ผ่าน? |
|---|---|---|---|
| Trades ทั้งหมด | 0 | ≥12 | ❌ |
| Win rate (อัตราชนะ) | 0% | ≥40% | ❌ |
| Avg R-multiple (คุณภาพ trade เฉลี่ย) | 0 R | ≥1.5 R | ❌ |
| Total P/L (กำไรขาดทุนสมมติ) | $0 | — | — |
| Wins / Losses / B/E | 0W / 0L / 0B | — | — |

*ต้องผ่านทั้ง 3 metric พร้อมกัน (AND ไม่ใช่ OR) และต้อง ≥12 trades ก่อนประเมิน*

---

## Trade Log

| วันปิด | Ticker | Dir | Entry | Exit | Size | R | W/L |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — |

---

## วิธีใช้

1. Copy `vault/_templates/paper-trade-template.md`
   → บันทึกเป็น `vault/20_investment/_journal/trades/YYYY-MM-DD-TICKER.md`
2. กรอก frontmatter (บรรทัดบน): ticker, direction, entry, stop, size, date_open
3. ตอนปิด trade: กรอก exit, date_close, แล้วเปลี่ยน status → closed
4. รัน script: `python scripts/stats-paper-trade.py`
   → ไฟล์นี้อัปเดตอัตโนมัติ

**R-multiple คืออะไร:**
`R = (ราคาออก − ราคาเข้า) ÷ (ราคาเข้า − stop loss)` สำหรับ long
- R = +1.5 หมายความว่าได้กำไร 1.5 เท่าของความเสี่ยงที่รับ
- R = −1.0 หมายความว่าเสียเท่ากับที่ตั้ง stop ไว้พอดี
