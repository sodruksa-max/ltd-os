---
council_topic: ควรเริ่ม project trading-foundations แบบไหนดี
expertise_lens: financial_risk
date: 2026-04-25
status: open
---

# Council Decision: ควรเริ่ม project trading-foundations แบบไหนดี

## TL;DR

สามข้อเสนอ (Optimist/Pragmatist/Skeptic) เห็นพ้องว่า journal + pre-trade documentation เป็นสิ่งที่ขาดไม่ได้ แต่แตกต่างกันใน timing ของ content และว่า 15h/day เป็น advantage หรือ risk — ทั้งสองมุมถูกขึ้นอยู่กับ user type ผู้ใช้ต้องตัดสินใจเองว่า fear หลักคืออะไรและ consistency track record ของตัวเองเป็นอย่างไร

---

## Decision Matrix

| Dimension | Optimist | Pragmatist | Skeptic |
|---|---|---|---|
| Capital protection | 3/5 | 4/5 | 4/5 |
| Motivation (90-day dropout risk) | 4/5 | 3/5 | 2/5 |
| Skill depth at Month 6 | 3/5 | 4/5 | 4/5 |
| Implementation simplicity | 2/5 | 4/5 | 4/5 |
| Reversibility | 2/5 | 3/5 | 5/5 |
| Content risk (identity trap) | 3/5 | 3/5 | 5/5 |

---

## Expertise Warnings (Financial Risk)

> **อ่านก่อน — 4 ข้อนี้ไม่มีใน proposal ไหนเลย:**

1. **Fee-adjusted R-multiple**: position ขนาด 2,500 THB ต้องจ่าย round-trip fees 50-150 THB = 10-30% ของ risk unit 500 THB. Gate "R-multiple ≥1.5" คือตัวเลข gross — ต้องทำ gross R 1.7–1.8 เพื่อให้ได้ net 1.5 จริง บันทึกในจาก Day 1

2. **USD/THB risk ไม่มีในทุก proposal**: trade US stocks = risk denominated in USD ตอน execution ไม่ใช่ THB. Journal ต้องบันทึก USD amounts แยกจาก THB equivalents เสมอ

3. **Bidirectional gate**: gate ปัจจุบัน (win rate ≥40%, R-multiple ≥1.5) เป็น one-way door ที่ไม่ถูก. ถ้า real-money win rate ต่ำกว่า 30% ใน 15 trades → บังคับกลับ paper-only 60 วัน. กำหนด rule นี้ก่อน Month 7 ไม่ใช่ตอนที่กำลังขาดทุนอยู่แล้ว

4. **Gate metric เพิ่มเติม**: นอกจาก win rate + R-multiple ต้องมี ≥3 trade ที่ stop-loss ถูก hit และ honored ที่ราคา stop จริง (ไม่ modify, ไม่ hold through). Paper trading ทำให้คน "hold losers" ง่ายกว่าเงินจริง — gate นี้สร้าง structural trace ที่ fake ยากขึ้น

---

## The Question Nobody Asked (Devil's Advocate)

> ทุก proposal สันนิษฐานว่า **discipline คือ binding constraint** แต่จริงๆ อาจเป็น **feedback loop speed** — paper trading 6 เดือนคือ 6 เดือนที่ไม่เจ็บจริง สมองรู้ว่าเงินไม่จริง loss aversion ไม่ engage เต็มที่. คนที่ paper trade ดีมากอาจเตรียมตัวสำหรับ real trading ได้น้อยกว่าคนที่เสีย 5,000 THB จริงๆ ในเดือนแรก

---

## Recommendation Framework

ไม่มีใคร decide ให้คุณ — แต่ถ้า:

- **กลัวเสียเงิน** > กลัวเสียเวลา → **Hybrid A**: Pragmatist 3-module + Skeptic content timing (Month 7+) + expertise fee fix
- **กลัวเสียเวลา** / ต้องการ visible output → **Hybrid C**: Optimist flywheel + content start Month 7+ + fee fix + bidirectional gate
- **ต้องการ reversibility / minimum regret** → **Hybrid B**: Skeptic 90-day filter ก่อน แล้วค่อย switch Pragmatist จาก Month 4
- **ต้องการความง่าย** → **Pragmatist as-is** + เพิ่มแค่ 2 ข้อ: (a) gross R target 1.7–1.8, (b) USD/THB tracking

---

## Hard Questions to Answer First (before Day 1)

จาก Devil's Advocate — 3 คำถามที่ต้องตอบก่อน:

1. **"failing" คืออะไรสำหรับคุณ และรู้สึกยังไงถ้ามันเกิดขึ้น?** — เผย emotional driver: growth vs. performance, และว่า 6-month gate จะ motivating หรือ demoralizing

2. **มีใครสักคนที่จะดู trades กับคุณทุกสัปดาห์ไหม?** — accountability ต่อคนจริง ≠ accountability ต่อ doc. ทุก proposal ไม่มี human accountability loop เลย

3. **ถ้าถึง Month 5 paper trading แล้ว equity curve flat — จะทำต่อหรือหยุด?** — ถ้าคำตอบจริงๆ คือ "หยุด" แสดงว่า structure นี้ต้องการ real consequences เร็วกว่านั้น ไม่ใช่แค่ refine

---

## Non-Negotiables (ทุก path ต้องมี)

- [ ] Journal template บันทึก: stop price + target price ก่อน entry เสมอ
- [ ] Journal บันทึก USD amounts แยกจาก THB
- [ ] Gate metrics: win rate ≥40% + gross R-multiple ≥1.7 (≠ 1.5 net) + ≥3 stop-loss hits honored
- [ ] Bidirectional gate written down ก่อน Month 7: ถ้า real-money win rate <30% ใน 15 trades → paper-only 60 วัน
- [ ] ไม่มี code ใดๆ (รวมถึง screener) ก่อน 20+ trades บันทึกครบ

---

## All Artifacts

- [[brief]]
- [[proposal-optimist]] / [[proposal-pragmatist]] / [[proposal-skeptic]]
- [[critiques]]
- [[expertise-financial_risk]]
- [[synthesis]]
- [[final-challenge]]

---

## Outcome (fill later when known)

- **Date decided**: 
- **Choice**: 
- **Outcome (after 8 weeks)**:
