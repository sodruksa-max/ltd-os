## Financial Risk Lens

**Topic:** QQQ Setup 3 — AH weighted price reaction criterion
**Date:** 2026-04-30

---

### Per-proposal risk evaluation

**Optimist (เพิ่ม AH criterion ทันที)**
ความเสี่ยงหลักไม่ใช่ trade loss — คือ sample contamination. ถ้าเปลี่ยน rule ตอนนี้ trades ที่ paper trade ภายใต้ rule เดิม (GAAP only) กับ rule ใหม่ (GAAP + AH) คือ data จาก 2 systems ที่ต่างกัน การนำมา pool รวมเพื่อวัด win rate ≥40% เป็นการ mix samples ที่ incomparable. Worst case: win rate ดูผ่านเพราะ rule ใหม่กรอง cases ที่แย่ออก → go-live เดือน 7 ด้วย system ที่ยัง validate ไม่จริง → deploy real capital บน biased metric.

นอกจากนั้น: AH criterion ทำให้ trigger rate ลดลง → sample อาจไม่ถึง 12 trades ขั้นต่ำ ภายใน 6 เดือน → ไม่มีทาง go-live ตามแผน หรือต้อง extend paper period โดยไม่ได้ตั้งใจ.

**Pragmatist (observe แต่ไม่ block)**
Risk profile ดีที่สุดในสามข้อเสนอจาก capital preservation standpoint. บันทึก AH data ทุก trade โดยไม่เปลี่ยน trigger = สะสม data สำหรับ future rule change โดยไม่ contaminate sample ปัจจุบัน. ความเสี่ยงที่ยังมี: ถ้า "sell the news" pattern ซ้ำใน Q2 earnings (Jul 2026) และยังไม่ block → paper trade loss วันนั้น บันทึกจริงในระบบ → กดทั้ง win rate และ avg R. แต่นี่คือข้อมูลที่ถูกต้อง ไม่ใช่ noise.

**Skeptic (รอ n=5, หรือเพิ่ม 4/4 threshold)**
ความเสี่ยงซ่อนอยู่ที่ alternative ที่เสนอ: เพิ่มจาก ≥3/4 เป็น 4/4. Apr 29 เป็น 4/4 GAAP beat + AH net negative พอดี — ซึ่งหมายความว่า 4/4 threshold ไม่ได้ block case นั้นเลย. Alternative ของ Skeptic แก้ปัญหาคนละอย่างและไม่ address risk ที่ระบุ.

---

### Hidden risks all 3 missed

**Rule-change mid-experiment คือ primary risk — ไม่มีใครพูดถึงเลย.**

เมื่อเปลี่ยน rule กลางช่วง paper trading แล้วรวม trades ก่อน/หลัง rule change เข้าด้วยกัน:
- Win rate ≥40% gate อาจผ่านเพราะ rule ใหม่กรอง losses ออก = artificially inflated win rate
- หรือกลับกัน: win rate ต่ำกว่าจริงเพราะ early trades ภายใต้ rule ที่ "ยังไม่ดี"
- ไม่ว่าทิศทางไหน: go-live decision Month 7 จะ based on mixed-rule sample ที่ interpret ไม่ได้อย่างถูกต้อง

ไม่มี proposer คนไหนระบุว่าถ้าเปลี่ยน rule ควรจะ **reset trade counter เป็น 0** ด้วย.

---

### False positive vs false negative asymmetry

สำหรับ user นี้โดยเฉพาะ:

**False positive** (เข้า trade ที่ควร void) = max 5K paper loss บันทึกเป็น loser ใน journal กด win rate ลง — cost นี้ acceptable และ priced in ตาม 5% risk rule.

**False negative** (miss trade ที่ดีเพราะ AH criterion block) = 0 financial loss แต่ลด sample count โดยตรง ใน 6 เดือน paper period ที่ Mag7 earnings เกิด ~2 รอบ setup จะ trigger ~4-8 ครั้ง ถ้า AH criterion กรองออก 30-50% → sample อาจไม่ถึง 12 trades ขั้นต่ำ.

**สรุป: false negative มีต้นทุนซ่อนสูงกว่า** สำหรับ user ที่อยู่ในช่วง validation — ไม่ใช่เพราะเสียเงิน แต่เพราะ delay หรือ invalidate go-live decision ทั้งหมด.

---

### Recommendation from financial risk lens only

**Pragmatist's approach carries the lowest hidden risk.**

เหตุผลเชิง risk ล้วนๆ:
- ไม่ contaminate sample ที่กำลังสะสมเพื่อ go-live decision
- ไม่ลด trigger rate ในช่วงที่ต้องการ trades มากที่สุด
- บันทึก AH data ทุก case = สะสม evidence สำหรับ future rule update อย่างถูกต้อง

ถ้าจะเพิ่ม AH criterion จริง: ต้อง **reset trade counter เป็น 0** และเริ่มนับ 12 trades ใหม่ภายใต้ rule ใหม่เท่านั้น ถ้าไม่ยอม reset → อย่าเปลี่ยน rule กลางช่วง.

**Hard question ที่ต้องตอบ:** ถ้าเพิ่ม AH criterion ตอนนี้แล้ว Month 7 มี trades แค่ 8 ครั้ง (ไม่ถึง 12) — จะ delay go-live หรือจะลด threshold? คำตอบนั้นบอกว่า go-live gate จริงๆ คืออะไร.
