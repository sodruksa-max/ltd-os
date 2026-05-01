## Skeptic Proposal

### Recommendation

อย่าแก้ rule ตอนนี้ — เก็บ data เพิ่มก่อน แต่ถ้าจะแก้จริง ให้ยกเกณฑ์ GAAP EPS beat threshold จาก ≥3/4 เป็น 4/4 แทนการเพิ่ม AH criterion ซึ่งซับซ้อนกว่า

### Core argument

n=1 ไม่ใช่ pattern — Apr 29 อาจเป็น edge case ของ AI capex cycle โดยเฉพาะ ไม่ใช่หลักฐานว่า AH reaction เป็น reliable filter ที่ควรเพิ่มเป็น criterion ถาวร การเพิ่ม AH layer นำเข้ามาซึ่ง execution complexity ใหม่ (ต้องดู weighted AH ตอน midnight?) และ risk ของ over-filtering ที่อาจทำให้ miss setups ที่ดีกว่า Apr 29 มาก การแก้ rule จาก 1 data point คือ curve-fitting ไม่ใช่ system improvement

### Key failure modes to consider

**ความเสี่ยงสูงสุด — over-filtering:** ถ้า AH criterion ทำให้ entry rate ลดลงจาก 8 ครั้ง/ปี เหลือ 3 ครั้ง/ปี paper trade period 6 เดือนจะ validate ได้น้อยมาก เกณฑ์ go-live ≥40% win rate อาจไม่มีข้อมูลพอตัดสิน

**ความเสี่ยงรอง — implementation ambiguity:** "AH net positive" หมายความว่าอะไรกันแน่? Weighted average? Majority count? Threshold ที่ไหน? Apr 29 ถ้าตัด META ออก (เพราะ GAAP EPS มี $8.03B tax benefit distortion) net AH กลายเป็น +0.09pp แล้ว — rule นี้จะวัดอะไรกันแน่

**ความเสี่ยงรอง — pattern ที่ไม่ stable:** "Sell the news" ใน AI capex cycle ปี 2025-2026 อาจเป็น episodic ไม่ใช่ structural ถ้า capex cycle จบ pattern นี้หายไป แต่ rule ยังอยู่ในระบบ = false restriction

### Suggested rule

ถ้าอยากแก้จริงก่อน n=5: เพิ่ม note field ใน post-market ว่า "AH weighted: +/-X pp" แต่ยังไม่ใช้มัน block entry — เก็บเป็น data จนถึง n=4-5 cases แล้วค่อย decide ที่ /weekly-calibration เดือนพ.ค. หรือมิ.ย. ถ้าต้องการ stricter threshold ทันที: เพิ่ม EPS beat จาก ≥3/4 เป็น 4/4 — simpler, cleaner, ไม่ต้องดู midnight AH data

### Worst-case outcome if we change incorrectly

เพิ่ม AH criterion → paper trade period เหลือ 2-3 setups ในช่วง 6 เดือน → win rate sample size น้อยเกินไป → ถึงเดือน 7 ไม่รู้จริงๆ ว่า system ใช้ได้หรือเปล่า → go/no-go decision บิดเบี้ยว → scale ผิดจังหวะ

### What needs to be true for ANY rule change to be justified

ต้องมีอย่างน้อย 3 ใน 4 ข้อนี้ก่อนแก้ rule:
1. n ≥ 4 cases ที่ GAAP beat แต่ AH net negative ตามมา
2. Correlation ระหว่าง AH net และ next-day QQQ return ≥ 0.5 ใน sample นั้น
3. Pattern พบในอย่างน้อย 2 earnings season ที่ต่างกัน (ไม่ใช่ AI capex cycle เดียวกัน)
4. Rule ที่เพิ่มไม่ทำให้ sample ต่อปีหายไปเกิน 50%
