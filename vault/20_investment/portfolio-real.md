# Real Money Portfolio — Dashboard
*Updated: 2026-05-04 01:16 | คำนวณอัตโนมัติจาก `scripts/stats-real-trade.py` | ราคาจาก Alpaca*

---

## Overview

| Metric | Value |
|---|---|
| **Open positions** | 1 |
| **Unrealized P&L** | $+808.60 |
| **Closed trades** | 0 |
| **Realized P&L (net fees)** | $+0.00 |
| **Total fees paid** | $0.00 |
| **Win rate** | 0.0% (0W / 0L) |
| **Avg R-multiple** | +0.00R |

---

## Open Positions

| Date | Ticker | Dir | Entry | Current | Shares | Unrealized P&L |
|---|---|---|---|---|---|---|
| 2026-05-03 | SPY | long | $558.00 | $719.72 | 5 | $+808.60 |

*ราคา current จาก Alpaca (อาจ delay 15 นาที สำหรับ free tier)*

---

## Closed Trades

| Date closed | Ticker | Dir | Entry | Exit | Shares | Net P&L | R | W/L |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — |

---

## Annual Summary (สรุปภาษีรายปี)

| ปี | Realized Gain (USD) | ค่าธรรมเนียมรวม | กำไรสุทธิ |
|---|---|---|---|
| — | — | — | — |

*สำหรับ ภ.ง.ด. 90/91: แปลง USD → THB ที่อัตราวันที่ทำการค้า (ดูที่ BOT หรือ Dime statement)*

---

## วิธีใช้

1. Copy `vault/_templates/real-trade-template.md`
   → บันทึกเป็น `vault/20_investment/_journal/real-trades/YYYY-MM-DD-TICKER.md`
2. กรอก frontmatter: ticker, direction, entry_usd, shares, fees_usd, stop_usd, date_open
3. ตอนปิด trade: กรอก exit_usd, exit_fees_usd, date_close → เปลี่ยน status → closed
4. รัน: `code/python/.venv/Scripts/python scripts/stats-real-trade.py`
