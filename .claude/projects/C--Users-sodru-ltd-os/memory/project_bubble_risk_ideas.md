---
name: Bubble Risk System — 3 Ideas
description: ไอเดีย 3 ทิศทางต่อยอดจาก US Market Bubble Risk Analysis (โพสวิเคราะห์ตลาดเมกา 2026-05-06)
type: project
---

3 ไอเดียที่เก็บไว้ implement ต่อ ยังไม่ได้ทำ

**ทิศที่ 1 — Bubble Risk Monitor script (ใหม่)**
- ดึง indicator รายสัปดาห์: Shiller CAPE, 10Y yield vs Fed Funds (spread), USD/JPY, VIX + term structure, AI Capex vs earnings revision
- Output: composite "Bubble Pressure Score" คล้าย macro-snapshot.py แต่โฟกัส risk vector
- Tradeoff: Shiller CAPE ไม่มี free API ง่ายๆ ต้องดึงจาก FRED

**ทิศที่ 2 — Risk Framework vault document (เร็วสุด, แนะนำทำก่อน)**
- Formalize "แตกจากอะไร" framework เป็น vault note
- แต่ละ risk vector มี leading indicator + threshold เฝ้าระวัง
- ใช้ reference ใน /pre-market และ /stock-research
- Save path: vault/10_research/ หรือ vault/_memory/

**ทิศที่ 3 — เพิ่มเข้า macro-snapshot.py (ง่ายสุด)**
- เพิ่ม section "Bubble Risk Pulse" ใน script ที่มีอยู่
- เพิ่ม: 10Y yield, USD/JPY, VIX พร้อม threshold alert
- ไม่ต้องสร้าง script ใหม่

**Why:** ต่อยอดจาก US Market Bubble Risk Analysis ที่วิเคราะห์ risk vectors: AI Circular Financing, Hyperscaler Accounting Quality, Index Concentration, Long-end Yield, Yen Carry, Private Credit/CRE
**How to apply:** ถาม user ว่าอยาก resume ทิศไหนก่อน — แนะนำทิศที่ 2 เพราะเร็วและใช้ได้เลย
