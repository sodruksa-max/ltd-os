---
ticker: SPY
direction: long
status: expired
type: paper
date_open: 2026-05-03
date_close: 2026-05-16
entry_usd: 558.00
shares: 5
fees_usd: 0
stop_usd: 530.00
target_usd: 614.00
exit_usd: "[not tracked — expired after 2+ weeks]"
exit_fees_usd: ~
result: ~
setup_source: "smoke-test"
---

# Paper Trade — SPY (LONG) — 2026-05-03
*Paper trade (ไม่ใช่เงินจริง) | smoke test pipeline | type: paper*

---

## ข้อมูล Trade

| Field | Value |
|---|---|
| **Ticker** | SPY |
| **Direction** | Long |
| **Status** | Open (Paper) |
| **Date opened** | 2026-05-03 |
| **Date closed** | — |
| **Setup source** | smoke-test — ทดสอบ pipeline (/eod, stats-real-trade) |

---

## ราคา

| | ราคา USD | หมายเหตุ |
|---|---|---|
| **Entry** | $558.00 | สมมติ — ทดสอบ pipeline เท่านั้น |
| **Stop loss** | $530.00 | -5% จาก entry |
| **Target** | $614.00 | +10% จาก entry |
| **Exit** | — | *กรอกตอนปิด* |

---

## Position

| | Value |
|---|---|
| **Shares** | 5 หุ้น |
| **Cost basis** | $2,790 (สมมติ) |
| **Fees ซื้อ** | $0 (paper) |
| **Fees ขาย** | — |

---

## ผลลัพธ์ *(กรอกตอนปิด)*

| | Value |
|---|---|
| **Realized gain** | — |
| **R-multiple** | — |
| **Win / Loss** | — |

---

## Notes

### เหตุผลที่เข้า
Smoke test entry — ใช้ทดสอบว่า eod-report.py อ่าน frontmatter ได้ถูกต้อง และ Alpaca fetch ราคา SPY ได้

### เหตุผลที่ออก
—

### Lesson (1 ประโยค)
—
