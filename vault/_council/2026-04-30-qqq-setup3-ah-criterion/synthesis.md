---
council_topic: QQQ Setup 3 — AH weighted price reaction criterion
phase: synthesis
date: 2026-04-30
---

# Synthesis: QQQ Setup 3 — AH Criterion

## Where proposers AGREE

- n=1 ยังไม่พอ rule change ที่ถาวร — ทุกฝ่ายยอมรับข้อนี้
- AH weighted net pp ควรบันทึกทุก Setup 3 entry (soft data collection) — ทุกฝ่ายเห็นด้วย
- "Sell the news" อาจเป็น episodic (AI capex cycle) ไม่ใช่ structural ถาวร — ทุกฝ่ายเปิดโอกาสนี้ไว้
- GAAP EPS beat เป็น lagging indicator — ทุกฝ่ายเห็นตรงกัน แต่ข้อสรุปต่างกัน

## Where proposers DIVERGE

| คำถาม | Optimist | Pragmatist | Skeptic |
|---|---|---|---|
| เพิ่ม AH gate เมื่อไหร่? | ทันที | หลัง n=5 + correlation ≥60% | ไม่เพิ่ม / เพิ่ม EPS threshold แทน |
| วิธีแก้ปัญหา Apr 29 | AH gate block entry | บันทึก แต่ยัง trigger | แก้ threshold เป็น 4/4 แทน |
| ต้นทุนของ false negative | ต่ำ (ยัง paper trade) | ปานกลาง | สูง — กิน sample count |
| "Sell the news" เป็น structural? | ใช่ (อ้าง GS/MS) | ไม่แน่ | ไม่ใช่ (episodic) |

## Decision matrix

| Dimension | Optimist | Pragmatist | Skeptic |
|---|---|---|---|
| Signal quality (precision) | สูง | ปานกลาง | ต่ำ–ปานกลาง |
| Sample contamination risk | สูง | ต่ำ | ต่ำ |
| Sample count risk (false negative) | สูง | ต่ำ | ปานกลาง (4/4 ก็ลด trigger) |
| Implementation complexity | ปานกลาง | ต่ำ | ต่ำ |
| Validates ก่อน go-live เดือน 7? | เสี่ยง (trades น้อย) | ผ่านได้ | เสี่ยง (bar สูงเกิน timeline) |
| Rule stability (ถ้า capex cycle จบ) | ต่ำ | กลาง | สูง |

## Hybrid options

**Hybrid A — Pragmatist + explicit reset clause:**
บันทึก AH data ทุก entry แต่ยัง trigger ตาม rule เดิม หากถึง n=5 แล้ว AH correlates ≥60% → เพิ่ม gate + **reset trade counter เป็น 0** และนับ 12 trades ใหม่ภายใต้ rule ใหม่

**Hybrid B — Tiered flag ไม่ใช่ hard gate:**
AH net < -0.3pp = "caution flag" ใน journal แต่ไม่ block — ใช้ลด position size แทน (เช่น ครึ่ง size) แทนที่จะ void setup ทั้งหมด รักษา sample count แต่ลด exposure ใน setup ที่น่าสงสัย

## Critique patterns (เรื่องที่ถูกโจมตีซ้ำ)

1. **n=1 overfitting** — Optimist อ้าง 100% success rate จาก n=1 คือ tautology ไม่ใช่ validation
2. **Implementation ambiguity** — "weighted net" นับอย่างไรเมื่อ reporting dates ต่างกัน และ GAAP distortion (META $8.03B tax benefit) ทำให้ AH ยาก calibrate
3. **Sample count as hidden cost** — filter ที่เข้มขึ้น = trigger น้อยลง = validate ไม่ทัน go-live

## Expertise warnings (financial_risk lens — อ่านก่อนตัดสิน)

> คำเตือนที่ทุก proposer พลาด:

1. **Rule-change mid-experiment = sample contamination.** Pool trades จาก rule เดิม + rule ใหม่ → win rate ≥40% gate อาจ inflate หรือ deflate โดยไม่สะท้อนความจริง ถ้าเปลี่ยน rule ต้อง reset trade counter เป็น 0
2. **False negative มีต้นทุนซ่อนสูงกว่า false positive** ในบริบทนี้: false positive = 5K paper loss (priced in) แต่ false negative = ลด sample count → delay/invalidate go-live decision ทั้งหมด
3. **Hard question ที่ต้องตอบ:** ถ้าเพิ่ม AH criterion แล้วถึง Month 7 มีแค่ 8 trades — จะ delay go-live หรือลด threshold?

## Hidden assumptions surfaced

- **Optimist assumed:** "Sell the news" เป็น structural pattern ตลอด 2025–2027 — ไม่มี evidence ยืนยัน
- **Pragmatist assumed:** correlation ≥60% จาก n=5 มี statistical significance — จาก 5 data points p-value สูงมาก
- **Skeptic assumed:** 4/4 threshold แก้ปัญหาได้ — แต่ Apr 29 เป็น 4/4 GAAP beat + AH net negative พอดี ดังนั้น alternative นี้ไม่ address กรณีที่เกิดจริง

## Open questions for user

1. **QQQ Apr 30 จริงๆ ปิดเท่าไหร่?** — ถ้าลง ≥0.5% case ที่ 1 ครบวงจร ถ้าขึ้น criterion นี้คือ false negative
2. **Go-live gate จริงๆ คืออะไร?** — ถ้าถึง Month 7 มีแค่ 8 trades จะ delay หรือ go ต่อ?
3. **ยอม reset trade counter ไหม?** — ถ้าไม่ยอม อย่าเปลี่ยน rule กลางช่วง

## Recommendation framework (ไม่ใช่คำแนะนำ)

ถ้าให้น้ำหนัก **signal quality** สูงสุด → **Optimist** แต่ต้อง reset trade counter + ยอมรับ go-live อาจล่าช้า

ถ้าให้น้ำหนัก **sample integrity + timeline** สูงสุด → **Pragmatist** (หรือ Hybrid A)

ถ้าให้น้ำหนัก **simplicity + stability** สูงสุด → **Skeptic** แต่ต้องยอมรับว่า 4/4 ไม่แก้ปัญหา Apr 29

> ถาม: go-live gate ที่ Month 7 สำคัญกว่าหรือ signal precision สำคัญกว่า? ตอบข้อนั้น แล้ว proposal จะชัดเอง
