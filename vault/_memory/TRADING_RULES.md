# Trading Rules — Live Document

*ย้ายจาก WORKFLOWS.md เพื่อให้ trading tasks โหลดเฉพาะไฟล์นี้แทน WORKFLOWS.md ทั้งหมด*
*Load: trading tasks (pre-market, post-market, stock-research, eod, weekly-calibration)*

---

## Confidence calibration (mandatory ใน /pre-market)

- นับ event risks: FOMC/Powell, Mag7 earnings week, Major geopolitical unresolved, CPI/PCE/NFP, Major Fed speakers
- 0-1 events → ดุลพินิจ | 2+ events → cap low (ห้ามใช้ medium หรือ high)
- *Updated 2026-05-02: threshold เข้มขึ้นจาก "2 events → medium" → "2+ events → low"*
- Binary geopolitical event = Low cap เสมอ ไม่ขึ้นกับ event count *(approved 2026-05-11)*

## Polymarket interpretation rule *(approved 2026-05-11)*

- Polymarket ผิดทิศทาง 4/5 reviews (Apr28: 67%Up→down, Apr29: 61%Up→flat, Apr30: 45%Up→+1%, May5: 84%Hormuz→oil-3.9%)
- ถ้า odds ≥80% ในทิศทางเดียว → ระบุ contrarian interpretation ด้วยใน brief
- ใช้ Polymarket เป็น 1 ใน 3 เหตุผล scenario ได้ แต่ห้าม reinforce ตรงๆ ถ้า odds extreme

## Presidential Action Risk *(approved 2026-05-11)*

- ถ้ามีเรื่อง Trump/executive action ที่ยัง active → เพิ่ม row "Presidential Action Risk" ใน Risk Framework แยกจาก Geopolitical
- Format: `**Presidential Action Risk:** [สถานการณ์] → trigger: [oil/USD/defense/equities] → magnitude: [ต่ำ/กลาง/สูง]`

## Oil crash → sector beneficiary *(approved 2026-05-11)*

- ถ้า WTI หรือ Brent ลง ≥3% → ระบุ XLK + QQQM เป็น primary beneficiary ใน Bullish scenario
- Evidence: May 5 oil -3.9% → XLK +2.2%; Apr 30 oil คลาย → Nasdaq rally

## Trade setup discipline

- Forward-looking เท่านั้น — if-then ไม่ใช่ already-true
- Time-stop ทุก setup (Day = exact ET time, Swing = days)
- Profit-taking rules กำหนดก่อนเข้า — ไม่ใช่หลังกำไร
- ห้าม entry หลัง 3pm ET; lunch lull 11:30–13:30 ET = no entry
- **Earnings EPS criterion**: ระบุ GAAP หรือ adjusted ชัดเจน — ใช้ GAAP เป็น primary; adjusted ต่างจาก GAAP ≥5% → flag divergence *(evidence: Apr 28 UPS)*
- **QQQ/Mag7 trigger**: ≥3/4 GAAP beat AND ≥2/4 AH positive → full size; AH split → half size หรือรอ open *(evidence: Apr 29)*

## Pre-commit rules 5 ประเภท

1. Circuit breakers — ปิด position ทันที
2. Setup invalidation — thesis ตาย
3. Profit-taking — lock gains
4. Time-of-day — เวลาห้าม trade
5. Earnings/news triggers

## Source verification

- ทุกตัวเลขต้องมี source attribution
- Conflict ระหว่าง sources → flag ชัด
- ห้าม fabricate — ใช้ `[unverified]` ถ้าหาไม่ได้
- Live data > cached > forecast model

## Command modification rules

- ห้ามแก้ command ทุกวัน — แก้เมื่อ pattern ซ้ำ ≥3 ครั้งเท่านั้น
- Encode lesson เป็น rule generalizable ไม่ใช่ fix เฉพาะกรณี
- หลังแก้ → commit + version bump (v6, v7…)

## Weekly calibration cycle

- `/weekly-calibration` → aggregate reviews → หา pattern ที่ data แข็งพอ
- ถ้าเห็น improvement candidate → encode เข้า command
- ห้าม tweak จาก single data point
