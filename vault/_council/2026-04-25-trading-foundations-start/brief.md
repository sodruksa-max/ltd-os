---
council_topic: ควรเริ่ม project trading-foundations แบบไหนดี
expertise_lens: financial_risk
date: 2026-04-25
phase: brief
---

# Council Brief: ควรเริ่ม project trading-foundations แบบไหนดี

## User Profile (from vault/_memory/)

- นักศึกษาปี 1 logistics, ว่าง Mon-Fri ~15h/day
- ไม่เขียนโค้ดเอง — Claude เป็น executor
- ทุน trading: 100K (experiment fund — สมมุติหายหมดได้, แยกจาก QQQM)
- เป้าหมาย 3 ทาง: Trading / Trading bots / Short-form content
- Market: US stocks | Style: momentum + small/mid cap + sector rotation
- ตอนนี้: ยังอยู่ใน paper trading phase (Month 1-6 ห้ามใช้เงินจริง)

## Context

"trading-foundations" ไม่ได้ define ชัดเจนว่าหมายถึงอะไร — มี interpretation หลายแบบ:
1. **Vault/learning project** — โครงสร้าง note สำหรับเรียนรู้ trading fundamentals (TA, FA, risk management, psychology)
2. **Code project** — stock screener, paper trading tracker, หรือ bot skeleton
3. **Content project** — series สอน trading basics สำหรับ YouTube/TikTok
4. **All-in-one** — project ที่รวมทั้ง learning + tracking + content pipeline

## Goal

ตัดสินใจว่า "trading-foundations" project ควรเริ่มต้นด้วย **scope อะไร, structure แบบไหน, sequencing ยังไง** ให้ได้ประโยชน์สูงสุดจาก 100K capital + เวลาว่าง Mon-Fri ที่มี และสอดคล้องกับ phase progression ที่ตั้งไว้

## Constraints

- Paper trading เท่านั้น 6 เดือนแรก — ห้ามมีกลไกใดที่ make it too easy to jump to real money
- ทุน 100K แยกจาก QQQM เด็ดขาด
- ไม่ควรซับซ้อนจนต้องใช้เวลา setup นาน — user ต้องการ start learning fast
- ไม่เขียนโค้ดเอง → ทุกอย่างผ่าน Claude, ต้อง maintainable โดยคนไม่รู้โค้ด
- เวลาว่างเยอะ (15h/day) แต่ยังเรียนอยู่ → focus ต้องชัดเจน ไม่ทำพร้อมกันหมด

## Stakes

- ถ้า over-engineer ตั้งแต่แรก: เสียเวลา build infrastructure, ไม่ได้ trade/เรียน
- ถ้า under-structure: ไม่มีระบบ track ผล, ทำซ้ำผิดพลาดเดิม, ไม่รู้จะ scale up เมื่อไหร่
- ถ้าเริ่มผิด scope: เรียน trading theory ไม่จบ → ไม่เคยลงมือ / เขียน bot ก่อนเข้าใจ market → bot ไม่ทำงาน

## Open Questions (council ต้องตอบ)

1. ควรทำ 1 project หรือแยก 3 projects ตาม 3 เป้าหมาย?
2. Sequence ไหนเหมาะที่สุด: Learn first → Code later / Code while learning / Content ทำพร้อมกัน?
3. Minimum viable structure ที่พอแล้วสำหรับ Month 1-3?
4. Metrics อะไรที่ต้อง track ตั้งแต่วันแรก?
5. Risk: อะไรคือ early warning ว่า project กำลัง off-track?
