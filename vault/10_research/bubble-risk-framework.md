---
title: US Market Bubble Risk Framework
tags: [macro, risk, bubble, framework]
created: 2026-05-10
related: [[macro-snapshot]], [[pre-market]]
---

# US Market Bubble Risk Framework

Framework สำหรับติดตาม risk vectors ที่บ่งชี้ภาวะฟองสบู่ในตลาด US — แต่ละ vector มี leading indicator + threshold ชัดเจน ใช้อ้างอิงใน /pre-market และ /stock-research

---

## Risk Vectors

### 1. AI Circular Financing
**คืออะไร:** Hyperscalers (MSFT, GOOGL, AMZN, META) กู้เพื่อใช้จ่าย AI capex โดยคาดว่า AI revenue จะมาชำระหนี้ — แต่ revenue ยังไม่มา ทำให้เป็น circular dependency

| Leading Indicator | Threshold ⚠️ | Data Source |
|---|---|---|
| Hyperscaler capex YoY growth | > 40% YoY (3 ไตรมาสติดต่อกัน) | ดูจาก earnings call |
| AI revenue recognition | Capex/Revenue ratio > 0.35 | 10-Q filings |
| Earnings revision trend | Consensus EPS ปรับลง > 5% QoQ | Factset/Bloomberg |

**Trigger:** ถ้า capex สูงแต่ AI revenue ต่ำกว่า consensus 2 ไตรมาสติดต่อกัน → derating risk สูง

---

### 2. Hyperscaler Accounting Quality
**คืออะไร:** ต้นทุน compute ถูก capitalize แทน expense → กำไรดูดีเกินจริง; depreciation schedules ยาวขึ้นจาก 4Y → 6Y

| Leading Indicator | Threshold ⚠️ | Data Source |
|---|---|---|
| D&A / Capex ratio | < 0.60 (depreciation น้อยกว่าที่ควร) | 10-K |
| PP&E useful life changes | เปลี่ยนโดยไม่มีเหตุผลชัด | 10-K footnotes |
| Free cash flow vs Net income | FCF/NI < 0.70 | Earnings reports |

**Trigger:** SEC inquiry หรือ analyst note เรื่อง useful life extension → immediate derating

---

### 3. Index Concentration
**คืออะไร:** S&P 500 top-7 (Magnificent 7) มี weight รวม > 33% — systemic risk สูงถ้า sector หนึ่งล้ม

| Leading Indicator | Threshold ⚠️ | Data Source |
|---|---|---|
| Top-7 weight ใน S&P 500 | > 35% | S&P fact sheet รายเดือน |
| Equal-weight vs cap-weight gap | RSP underperform SPY > 5% YTD | Yahoo: RSP vs SPY |
| Breadth: % stocks above MA200 | < 50% ขณะ index ทำ high | StockCharts / barchart |

**Trigger:** Top-7 drawdown > 15% โดย breadth ไม่ฟื้น → index ร่วงแรงกว่า equal-weight มาก

---

### 4. Long-end Yield
**คืออะไร:** 10Y Treasury yield ขึ้นกด P/E multiple ของ growth stocks — โดยเฉพาะ AI stocks ที่ value อยู่ที่ terminal growth

| Leading Indicator | Threshold ⚠️ | Data Source |
|---|---|---|
| 10Y yield | > 4.75% (P/E compression zone) | Yahoo: ^TNX |
| 10Y-2Y spread | > +50bps (term premium กลับมา) | Yahoo: ^TNX - ^IRX |
| 30Y mortgage rate | > 7.5% (real economy slowing) | Freddie Mac weekly |
| 10Y real yield (TIPS) | > 2.5% | Yahoo: ^TYX proxy |

**Trigger:** 10Y ทะลุ 5.0% อีกครั้ง → de-risking จาก duration-sensitive funds

---

### 5. Yen Carry Trade
**คืออะไร:** นักลงทุน borrow ใน JPY (rate ต่ำ) แล้วลงทุนใน US risk assets — ถ้า JPY แข็งค่าเร็ว → forced unwind → liquidity หาย overnight

| Leading Indicator | Threshold ⚠️ | Data Source |
|---|---|---|
| USD/JPY level | < 145 (carry unwind zone) | Yahoo: JPY=X |
| USD/JPY 5-day change | < -3% ใน 5 วัน | คำนวณจาก Yahoo |
| BOJ meeting + statement | Hawkish surprise | BOJ calendar |
| VIX spike coincident | VIX ขึ้น > 5pts พร้อม JPY แข็ง | Yahoo: ^VIX |

**Trigger:** USD/JPY ร่วงจาก > 155 → < 145 ใน 2 สัปดาห์ = redo Aug 2024 carry unwind

---

### 6. Private Credit / CRE
**คืออะไร:** Private credit market ($1.7T+) และ Commercial Real Estate มี mark-to-market ล่าช้า — ถ้า rate สูงนาน → default wave ที่ยังไม่โชว์ใน public data

| Leading Indicator | Threshold ⚠️ | Data Source |
|---|---|---|
| BDC (Business Dev Co) discount | > 15% discount to NAV | Yahoo: ARCC, FS KKR |
| Office REIT occupancy | < 80% national average | NAREIT quarterly |
| CMBS delinquency rate | > 5% | Trepp monthly |
| Regional bank CRE exposure | CRE/Tier1 Capital > 300% | FDIC call reports |

**Trigger:** Regional bank เริ่มตั้ง provision สูงขึ้น + BDC NAV discount ขยาย = stress กำลังแพร่

---

## Composite Bubble Pressure Score

รัน `bubble-risk-monitor.py` เพื่อดู score อัตโนมัติ — หรือประเมิน manually ด้านล่าง

| Vector | Weight | Status | Score |
|---|---|---|---|
| AI Circular Financing | 20% | 🟡 Monitor | |
| Hyperscaler Accounting | 15% | 🟡 Monitor | |
| Index Concentration | 20% | 🔴 Alert (>33%) | |
| Long-end Yield | 25% | 🟡 Monitor | |
| Yen Carry | 10% | 🟢 Calm | |
| Private Credit/CRE | 10% | 🟡 Monitor | |
| **COMPOSITE** | 100% | | /10 |

**Score interpretation:**
- 0–3: Low risk — full position size OK
- 4–6: Elevated — reduce size 20-30%, tighten stops
- 7–10: High risk — defensive posture, cash > 30%

---

## How to Use in /pre-market

1. รัน `macro-snapshot.py` → ดู Bubble Risk Pulse section (10Y, JPY, VIX term structure)
2. ถ้า 2+ threshold ถูก trigger → ดูที่นี่ว่า vector ไหนกำลัง stress
3. รัน `bubble-risk-monitor.py` สำหรับ composite score รายสัปดาห์

## How to Use in /stock-research

- ถ้า stock อยู่ใน AI / hyperscaler ecosystem → ตรวจ vector 1+2 ก่อน
- ถ้า rate-sensitive → ตรวจ vector 4
- ถ้า entry size ใหญ่ → ตรวจ composite score ก่อนเสมอ
