# Cross-Critiques — Phase 3

Format: steelman → weakness → open question

---

## Optimist critiques Pragmatist

**Steelman:** Pragmatist's soft-filter approach (observe AH pp ทุกครั้งโดยไม่ block) เป็นวิธีที่ปลอดภัยที่สุดในการสะสม data โดยไม่ลด opportunity set มี merit ชัดในช่วง paper trading

**Weakness:** "เก็บ data ก่อนค่อยตัดสิน" เป็นแนวคิดดี แต่ Pragmatist ไม่ได้ระบุว่าถ้า Apr 30 QQQ ลงจริง (วันที่ setup ปัจจุบัน trigger แล้ว) จะทำอะไรกับ case นั้น — soft filter ไม่ช่วยป้องกัน false positive ที่กำลังเกิดขึ้นวันนี้เลย proposal นี้จึง "ดีในทฤษฎี แต่ไม่ act ในวันที่มีข้อมูล"

**คำถามที่เปิดค้าง:** ถ้า Apr 30 QQQ ลง 1%+ วันนี้ (ยืนยัน case ที่ 1 ครบวงจร) Pragmatist จะเปลี่ยนท่าทีเป็น "เริ่ม block เลย" หรือยังรอ 5 cases อยู่?

---

## Optimist critiques Skeptic

**Steelman:** Skeptic ชี้ถูกว่า implementation ambiguity ของ AH criterion เป็นปัญหาจริง — "AH net positive" หมายถึงอะไรกันแน่เมื่อ GAAP META มี $8.03B tax benefit distortion ทำให้คำนวณ weight ยาก Skeptic ยังเสนอ simpler alternative (4/4 threshold) ที่น่าสนใจ

**Weakness:** Skeptic มองว่า "เพิ่ม 4/4 threshold = simpler" แต่นั่นแก้ปัญหาคนละอย่าง — 4/4 threshold ไม่ช่วยอะไรเลยในวันที่ 4/4 beat แต่ AH net ยังลบ (ซึ่งเป็นกรณี Apr 29 พอดี) นอกจากนี้ Skeptic ตั้ง bar สูงมาก (3/4 criteria) ก่อนแก้ rule ใดๆ — ซึ่งหมายความว่าต้องรอ 2+ earnings seasons หรือ ~1 ปี ก่อน go-live เดือน 7 จะมาถึงพอดี ทำให้ไม่มีทาง validate ได้ทันเวลา

**คำถามที่เปิดค้าง:** ถ้า bar ของ Skeptic ต้องการ 3/4 criteria ก่อนแก้ rule และ go-live อยู่ที่เดือน 7 — setup นี้จะ validate ได้ทันไหม? หรือ Skeptic ยอมรับว่า QQQ Setup 3 จะเข้า go-live โดยไม่ผ่านการ validate?

---

## Pragmatist critiques Optimist

**Steelman:** Optimist ถูกในเรื่อง signal quality — AH weighted net เป็น leading indicator ที่ดีกว่า GAAP beat สำหรับ next-day direction การเพิ่มมันในช่วง paper trading มีต้นทุน opportunity cost ต่ำมาก เพราะยังไม่ใช้เงินจริง

**Weakness:** Optimist อ้าง Goldman Sachs/Morgan Stanley ว่า "capex overhang discount เป็น structural" แต่ไม่ได้อ้างอิง study จริงๆ ใน proposal — นี่คือ assertion ไม่ใช่ evidence ถ้า pattern นี้ไม่จริงหรือ episodic (ซึ่ง Pragmatist เชื่อว่าน่าจะเป็น) rule ที่เพิ่มมาจาก n=1 จะทำให้ miss entries ดีๆ โดยไม่มีเหตุผล

**คำถามที่เปิดค้าง:** Optimist ยืนยัน "AH net ≥ 0pp threshold ง่ายพอ" — แต่ในวันที่เจ้าที่รายงานไม่ครบ 4 (เช่น MSFT+AMZN รายงาน, GOOGL+META รายงานอีกวัน) จะ calculate weighted net จาก pool ที่ไหน? Pool เปลี่ยนตาม reporting date หรือรอครบ 4 ก่อน?

---

## Pragmatist critiques Skeptic

**Steelman:** Skeptic ถูกที่สุดในเรื่อง "sample size สำคัญกว่า signal quality" — ถ้า filter ทำให้ setup trigger น้อยลงจาก 8 เหลือ 3 ครั้ง/ปี ใน paper trade period 6 เดือน จะ validate ได้แค่ 1-2 cases ซึ่งไม่พอสร้าง base rate ที่น่าเชื่อถือ

**Weakness:** Skeptic เสนอ 4/4 threshold เป็น "simpler alternative" แต่ไม่ได้คิดถึงว่า 4/4 จะทำให้ trigger rate ลดลงมากแค่ไหน ถ้า Mag7 earnings split เป็น 2 คืนที่ต่างกัน (MSFT+GOOGL คืนนึง, AMZN+META อีกคืน) จะนับ 4/4 ยังไง? threshold นี้ยังมี implementation ambiguity ของตัวเอง

**คำถามที่เปิดค้าง:** Skeptic บอกต้องการ correlation ≥0.5 ระหว่าง AH net และ next-day QQQ — แต่ correlation ≥0.5 จาก sample n=5 มี statistical significance แค่ไหน? ถ้าหา correlation จาก 5 data points แล้ว p-value สูงมาก จะยังใช้เป็น evidence ได้ไหม?

---

## Skeptic critiques Optimist

**Steelman:** Optimist มีจุดแข็งใน framing ที่ถูกต้อง — GAAP EPS beat เป็น lagging indicator และ AH reaction เป็น forward-looking real-time repricing framework นี้ถูกต้องในเชิงทฤษฎีและสอดคล้องกับ behavioral finance literature

**Weakness:** "100% ป้องกัน false positive จาก data ที่มี" (n=1) คือ tautology — ถ้า rule ออกแบบมาจาก case นั้น มันก็ต้องผ่าน case นั้น 100% โดยอัตโนมัติ นี่ไม่ใช่ validation มันคือ in-sample fitting ซึ่งเป็น worst form ของ overfitting Optimist ยังอ้าง win rate ~60% (GAAP only estimate) โดยไม่มี basis — ตัวเลขนี้มาจากไหน?

**คำถามที่เปิดค้าง:** ถ้า AH criterion block Apr 29 entry แล้ว QQQ Apr 30 ขึ้น 2% (กรณีที่ GOOGL AH +7% dominate) Optimist จะยังยืนยัน criterion นี้ไหม? หรือนั่นคือ false negative ที่ยอมรับไม่ได้?

---

## Skeptic critiques Pragmatist

**Steelman:** Pragmatist เสนอ "observe ก่อน act" ซึ่งเป็น scientific method ที่ถูกต้อง และ threshold สำหรับ formalizing criterion (correlation ≥60% จาก 5 cases) เป็นการตั้ง bar ที่มีเหตุผล ชัดเจน และ pre-committed ก่อน seeing data — นี่คือ best practice

**Weakness:** Pragmatist บอก "อย่า block entry ตอนนี้ แต่เก็บ data" — แต่นี่หมายความว่า ถ้า pattern ซ้ำ 3 ครั้งแรก (AH net negative + QQQ ลง) Pragmatist ก็ยังไม่ block ตาม proposal ของตัวเอง จนกว่าจะถึง 5 cases มัน prioritize completeness เหนือ risk management ในช่วง paper trade ซึ่งต่ำราคาแต่อาจ habituate นักเทรดให้ชินกับการ ignore negative signal

**คำถามที่เปิดค้าง:** Pragmatist ระบุ correlation threshold ≥60% จาก 5 cases — แต่ถ้า 4 cases เป็น negative correlation แล้วมี 1 case ที่ reverse แบบรุนแรง (เช่น AH net -1pp แต่ QQQ ขึ้น 3%) correlation จะหายไปทันที ถ้า market regime เปลี่ยน rule จะ robust ไหม?
