# Backtest Quality Checklist
*Based on: AlgoXpert IS-WFA-OOS (arXiv:2603.09219) + Backtest Overfitting ML Era (SSRN:4686376) | 2026-05-05*

> ใช้ก่อน deploy rule ใหม่ใดก็ตามใน system — ถ้าผ่านไม่ครบ ห้าม live

---

## Stage 1 — In-Sample (IS)

- [ ] เลือก parameter range ไม่ใช่ peak — หา stable plateau ที่ performance ไม่เปลี่ยนมากเมื่อ parameter เปลี่ยนเล็กน้อย
- [ ] ห้ามใช้ข้อมูล OOS ในขั้นตอนนี้เด็ดขาด
- [ ] ตรวจ cliff veto: ถ้า parameter เปลี่ยน 10% แล้ว Sharpe ร่วง > 50% → parameter ไม่ stable → reject

## Stage 2 — Walk-Forward Analysis (WFA)

- [ ] Rolling window: train N ปี → test M เดือน → shift 1 เดือน → repeat
- [ ] ใส่ purge gap ระหว่าง train และ test window (อย่างน้อย 1 สัปดาห์) เพื่อลด information leakage
- [ ] Majority pass rule: strategy ต้องผ่าน profit ใน > 50% ของ test windows
- [ ] Catastrophic veto: ถ้า window ไหน drawdown > 2× average drawdown → reject ทั้ง strategy
- [ ] Parameter lock: ห้ามเปลี่ยน parameter หลังเห็น WFA result

## Stage 3 — Out-of-Sample (OOS)

- [ ] ใช้ข้อมูลที่ไม่เคยแตะในทุก stage ก่อนหน้า
- [ ] Parameter lock สมบูรณ์ — ห้าม tune เพิ่มแม้แต่นิดเดียว
- [ ] คำนวณ **Deflated Sharpe Ratio (DSR)** แทน raw Sharpe

---

## Deflated Sharpe Ratio (DSR)

DSR แก้ไข Sharpe สำหรับ:
- Multiple testing (ทดลองหลาย parameter combinations)
- Non-normality ของ return distribution
- Selection bias (เลือก best-performing variant)

**กฎง่ายๆ:**
- `DSR > 0` = strategy likely genuine
- `DSR ≤ 0` = strategy likely overfit — ห้าม deploy

**วิธีคิดแบบ rule-of-thumb:**
- ทดลอง N combinations → หาร Sharpe ด้วย `√(1 + log(N))` เป็น rough DSR approximation
- ตัวอย่าง: Sharpe 1.5, ทดลอง 20 combinations → DSR ≈ 1.5 / √(1+log(20)) ≈ 1.5 / 1.98 ≈ 0.76 → ผ่าน
- ตัวอย่าง: Sharpe 1.2, ทดลอง 100 combinations → DSR ≈ 1.2 / √(1+log(100)) ≈ 1.2 / 2.45 ≈ 0.49 → ผ่าน แต่ margin บาง

---

## Circuit Breakers (สำหรับ live trading)

- `if realized drawdown > 2× backtest max drawdown` → kill switch, stop trading
- `if OOS Sharpe < 0.5 × IS Sharpe` → performance decay, review และ re-validate
- `if signal fire rate เปลี่ยน > 50% จาก backtest` → regime shift, อย่า trade จนกว่า re-validate

---

## Momentum Decay Rules (from arXiv:2512.11913)

| Signal type | Decay pattern | Max hold ก่อน re-evaluate |
|---|---|---|
| Momentum (price trend) | Hyperbolic — เร็วช่วงแรก | **7 trading days** |
| Value (V/P ratio) | ช้า — ไม่ fit hyperbolic | **30 trading days** |
| Mean-reversion | เร็วมาก — 1-3 วัน | **3 trading days** |

**Rule:** ทุก momentum trade ต้องตั้ง re-evaluate date ตอนเปิด position — ถ้าถึงวันแล้วยังไม่ถึง target → ออกหรือ size down อย่าง automatic

---

*Sources: [arXiv:2603.09219](https://arxiv.org/abs/2603.09219) | [SSRN:4686376](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4686376) | [arXiv:2512.11913](https://arxiv.org/abs/2512.11913)*
