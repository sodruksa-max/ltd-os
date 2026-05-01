# Council Brief — QQQ Setup 3: AH Price Reaction Criterion

**Date:** 2026-04-30
**Topic:** ควรเพิ่ม after-hours (AH) price reaction criterion นอกจาก GAAP EPS beat ใน QQQ Setup 3 หรือไม่?
**Expertise lens:** financial_risk

---

## Context

QQQ Setup 3 ในระบบ /pre-market ปัจจุบัน:
- **Trigger condition (เงื่อนไขเข้า):** ≥3/4 Mag7 (MSFT, AMZN, GOOGL, META) รายงาน GAAP EPS beat → Long QQQ วันถัดไป
- **Logic:** GAAP EPS beat ส่วนใหญ่ = earnings quality ดี = QQQ ขึ้น

## Evidence ที่นำมา (จาก 2026-04-29 review)

4/4 Mag7 รายงาน GAAP EPS beat:
- MSFT: $4.27 vs $4.07 est (+4.9% beat) → AH -0.5%
- AMZN: $2.78 vs $1.64 est (+69.5% beat) → AH -3.0%
- GOOGL: $5.11 vs $2.62 est (+95% beat) → AH +7.05%
- META: GAAP $10.44 (inc. $8.03B tax benefit) / adj $7.31 vs $6.79 (+7.7% beat) → AH -7.0%

**Net QQQ impact (weighted):**
- GOOGL 6%: +0.42pp | META 5.5%: -0.39pp | AMZN 9.5%: -0.29pp | MSFT 8.5%: -0.04pp
- **Net ≈ -0.30pp** → QQQ ถูกกดดันแม้ทุกเจ้า GAAP beat

**เหตุผล AH negative:**
- AMZN: AI capex guidance $200B FY26 (แพงกว่าที่ตลาดคาด)
- META: ยก capex guidance ไป $125–145B + user growth miss
- Pattern: "earnings beat ≠ stock up" เมื่อ forward guidance/capex ทำให้ narrative เปลี่ยน

## คำถามหลัก

1. GAAP EPS beat เป็น lagging indicator (ตัวชี้วัดที่ตามหลัง) หรือ leading signal (นำหน้า) จริงๆ?
2. ควรบังคับดู AH price reaction ก่อนตัดสิน trigger หรือเปล่า?
3. ถ้าเพิ่ม AH criterion → threshold ที่เหมาะสมคืออะไร? (% ของ Mag7 ที่ต้อง AH บวก? weighted ≥ 0?)
4. ถ้าไม่เพิ่ม → รับความเสี่ยงว่า setup นี้อาจเป็น false positive บ่อยไหม?

## Constraints

- ผู้ใช้ยังอยู่ในช่วง **paper trading** (ยังไม่ใช้เงินจริง)
- Trading fund: 100K experiment, risk per trade ≤5% (≤5K)
- No leverage, no options
- QQQ เป็นทั้ง passive QQQM (long-term, ไม่แตะ) AND trading setup (แยก account ชัดเจน)
- คำตอบควร **ปฏิบัติได้ทันที** ไม่ต้องรอ data เพิ่ม — มีหลักฐาน 1 case study (Apr 29)

## Stakes (ความสำคัญ)

- Low-to-medium: ยัง paper trading → ผิดพลาดไม่ได้เสียเงินจริง แต่ถ้า setup นี้ใช้ผิด method จะ compound error เมื่อเปลี่ยนเป็นเงินจริงเดือน 7+
- Signal quality ของ setup นี้กระทบ win rate metric (เป้า ≥40%) ที่ต้องผ่านก่อน go-live

---

## Open Questions

- 1 case study (Apr 29) เพียงพอสำหรับ rule change หรือเปล่า?
- "Sell the news" pattern เป็น structural (เกิดประจำ) หรือ episodic (เกิดเฉพาะบางช่วง เช่น AI capex cycle)?
- ถ้า threshold ซับซ้อนเกินไป → จะ over-engineer setup และ miss entry ดีๆ หรือเปล่า?
