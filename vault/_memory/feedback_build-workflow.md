---
name: Build workflow — usecase first, then paper, then build
description: ก่อนสร้าง feature ใดๆ ต้องหา usecase ก่อนเสมอ แล้วค่อยหา paper มา support แล้วค่อย implement
type: feedback
---

ก่อนสร้างอะไรก็ตาม ให้ทำตามลำดับนี้เสมอ:
1. **หา usecase ก่อน** — ปัญหาจริงคืออะไร? ใช้ตรงไหน? แก้อะไร?
2. **หา paper** — มีงานวิจัยรองรับ approach นี้ไหม? (/paper-survey)
3. **แล้วค่อย build** — implement โดยมี evidence รองรับ

**Why:** ป้องกันการสร้าง feature ที่ซับซ้อนโดยไม่มี evidence ว่า approach นั้น work จริง — เช่น RS vs SPY, sector-flow, catalyst-calendar ที่สร้างโดยตรงโดยไม่ผ่าน usecase validation ก่อน

**How to apply:** ทุกครั้งที่ user บอก "เพิ่ม X" หรือ "สร้าง Y" ให้ถามก่อนว่า usecase คืออะไร ถ้าไม่ชัดให้ propose usecase ให้ user confirm แล้วค่อย /paper-survey แล้วค่อย implement
