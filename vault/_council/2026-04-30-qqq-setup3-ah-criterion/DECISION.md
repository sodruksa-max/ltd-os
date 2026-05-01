---
council_topic: "QQQ Setup 3: ควรเพิ่ม after-hours price reaction criterion นอกจาก GAAP EPS beat?"
expertise_lens: financial_risk
date: 2026-04-30
status: open
---

# Council Decision: QQQ Setup 3 — AH Criterion

## TL;DR

Council ไม่ตัดสินว่าควรเพิ่ม AH criterion หรือไม่ — แต่พบว่าคำถามที่สำคัญกว่าคือ: (1) rule-change กลางช่วง paper trade contaminate go-live sample และ (2) devil's advocate ตั้งคำถามว่า Setup 3 ควรมีอยู่ต่อไปหรือเปล่าในยุค AI capex regime นี้ ก่อนตัดสินใจต้องตอบ 3 open questions ก่อน

---

## Decision matrix

| Dimension | Optimist (เพิ่ม AH ทันที) | Pragmatist (observe ก่อน) | Skeptic (รอ/เพิ่ม 4/4) |
|---|---|---|---|
| Signal quality | สูง | ปานกลาง | ต่ำ–ปานกลาง |
| Sample contamination risk | **สูง** | ต่ำ | ต่ำ |
| Sample count risk | **สูง** | ต่ำ | ปานกลาง |
| Go-live validation ทันเดือน 7? | เสี่ยง | ผ่านได้ | เสี่ยง |
| Rule stability (ถ้า AI capex cycle จบ) | ต่ำ | กลาง | สูง |
| แก้ปัญหา Apr 29 จริงๆ? | ใช่ | ไม่ block แต่บันทึก | ไม่ (4/4 ไม่ช่วยกรณีนี้) |

---

## Expertise warnings (financial_risk lens)

> **3 ข้อที่ทุก proposer พลาด — อ่านก่อนตัดสิน:**

1. **Rule-change mid-experiment = sample contamination.** ถ้าเปลี่ยน rule กลางช่วง paper trade แล้ว pool trades จาก rule เดิม + rule ใหม่รวมกัน → win rate ≥40% gate ที่ Month 7 จะ interpret ไม่ได้อย่างถูกต้อง ถ้าเปลี่ยน rule ต้อง **reset trade counter เป็น 0**

2. **False negative มีต้นทุนซ่อนสูงกว่า false positive** ในบริบทนี้: false positive = 5K paper loss (priced in) แต่ false negative = ลด sample count → delay/invalidate go-live decision ทั้งหมด

3. **n=5 correlation threshold มี statistical significance ต่ำมาก** — correlation ≥60% จาก 5 data points ไม่ valid ทางสถิติ แต่ถูก endorse ใน Hybrid A โดยไม่มีคำเตือน = false precision

---

## Devil's advocate warnings

> **5 คำถามที่ council ยังตอบไม่ได้:**

1. Setup 3 ควรมีอยู่ต่อไปหรือเปล่าในยุค AI capex regime ที่ตลาด fade EPS beat ด้วย capex narrative?
2. n=5 cases จะเกิดขึ้นทันก่อน go-live เดือน 7 หรือเปล่า? (อาจต้องรอถึงปี 2028)
3. GAAP EPS beat เป็น trigger ที่ใช้ได้ในยุคที่ตลาดตอบสนองต่อ forward guidance ไม่ใช่ backward EPS?
4. Setup 3 มี edge อะไรที่ beat random QQQ entry ได้?
5. Synthesis lean ไปที่ Pragmatist แต่ endorses n=5 correlation threshold ที่รู้ว่า statistically invalid — นั่นคือ false precision

---

## Recommendation framework

ถ้าให้น้ำหนัก **sample integrity + go-live timeline** → **Pragmatist** (Hybrid A: observe ไม่ block + reset counter ถ้าเปลี่ยน rule ในอนาคต)

ถ้าให้น้ำหนัก **signal precision** → **Optimist** แต่ต้อง reset trade counter เป็น 0 วันนี้ และยอมรับว่า go-live อาจล่าออกไป

ถ้าเห็นด้วยกับ devil's advocate → **พิจารณา scrap Setup 3** และออกแบบ setup ใหม่ที่มี edge ชัดกว่าในยุค AI capex regime

---

## Hard questions YOU must answer first

- [ ] **QQQ Apr 30 ปิดเท่าไหร่?** — ถ้าลง ≥0.5% case ที่ 1 ครบวงจร ถ้าขึ้น AH criterion คือ false negative
- [ ] **ถ้าเพิ่ม AH criterion แล้ว Month 7 มี trades แค่ 8 ครั้ง จะ delay go-live หรือ go ต่อ?** — คำตอบนั้นบอกว่า go-live gate จริงๆ คืออะไร
- [ ] **ยอม reset trade counter เป็น 0 ไหม ถ้าจะเปลี่ยน rule?** — ถ้าไม่ยอม → อย่าเปลี่ยน rule กลางช่วง
- [ ] **Setup 3 มี thesis ที่ยัง valid ในยุค AI capex หรือเปล่า?** — ถ้าตอบไม่ได้อย่างชัดเจน → พิจารณา scrap

---

## All artifacts

- [[brief]]
- [[proposal-optimist]] / [[proposal-pragmatist]] / [[proposal-skeptic]]
- [[critiques]]
- [[expertise-financial_risk]]
- [[synthesis]]
- [[final-challenge]]

---

## Outcome (fill later when known)

- Date decided:
- Choice:
- Outcome (after N weeks):
