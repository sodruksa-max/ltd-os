---
date: 2026-05-17
phase: 1-brief
---

# Brief — Workflow Design: Recipe + Fertilizer System

## Context

User กำลังขยาย LTD-OS จาก investment/trading OS ไปรองรับ domain ใหม่ 2 ด้านพร้อมกัน:
1. **สูตรอาหาร** — เน้นรสชาติ, research-driven, พัฒนาเป็น version ของตัวเอง
2. **สูตรปุ๋ย organic** — target: ปาล์มน้ำมัน, เป้าหมาย = ลดต้นทุน + คงคุณภาพ, ขยายไปพืชอื่นได้ในอนาคต

User profile: ปี 1 logistics (เรียนเสาร์-อาทิตย์), ว่าง ~15 ชม/วันจันทร์-ศุกร์, ไม่เขียนโค้ดเอง, Claude เป็น executor ทั้งหมด.

ระบบที่มีอยู่แล้ว: LTD-OS vault + git + agent pipeline (researcher, writer, coder, reviewer, /paper-survey, /council)

## Goal

ออกแบบ **workflow** ที่ดีที่สุดสำหรับ: วิธีที่ user จะ (1) รับ input จาก paper/วิทยาศาสตร์, (2) พัฒนาสูตร, (3) track iteration, (4) ตัดสินว่าสูตรพร้อมใช้จริง — สำหรับทั้ง 2 domain

## Constraints

- User ไม่เขียนโค้ดเอง — ทุกอย่างผ่าน slash command หรือ agent
- ทรัพยากรจำกัด: 15K/เดือน living, ทุน trading 100K (แยก), ไม่มี budget lab ขนาดใหญ่
- สูตรปุ๋ย = real-world test กับปาล์มจริง — iteration cycle ยาว (อาจนับเป็นเดือนหรือฤดูกาล)
- สูตรอาหาร = iteration cycle สั้น (ทดสอบได้เร็ว — ชิมทันที)
- ต้องอยู่ใน LTD-OS ecosystem (vault + markdown + git) — ไม่สร้าง platform ใหม่

## Stakes

- ถ้า workflow ซับซ้อนเกิน → user จะไม่ใช้ หรือใช้แป๊บแล้วทิ้ง
- ถ้า workflow ง่ายเกินไป → ไม่ได้ความรู้สะสม, ทำซ้ำงานที่ทำไปแล้ว
- สูตรปุ๋ยที่ผิดพลาด = เสียต้นทุน real (ปุ๋ย + เสียผลผลิต) → iteration ต้องมี version control จริง
- สูตรอาหารที่ไม่ track = reinvent wheel ทุกครั้ง

## Open questions for proposers

1. **Research integration:** paper/วิทยาศาสตร์เข้าระบบอย่างไร — ก่อนสร้างสูตร หรือ หลังสูตรล้มเหลว?
2. **Iteration structure:** version ต้องมี formal approval ก่อน advance หรือ continuous?
3. **Domain separation:** สูตรอาหาร vs ปุ๋ยควรมี workflow แยกกัน หรือ shared pipeline ดีกว่า?
4. **Test/feedback loop:** สูตรปุ๋ย cycle ยาว (เดือน) vs อาหาร cycle สั้น (วัน) — ระบบรองรับทั้งสองได้ไหม?
5. **Slash command investment:** สร้าง /new-recipe + /new-formula ตอนนี้ หรือรอ validate ด้วย manual ก่อน?
6. **Knowledge sharing:** สูตรปุ๋ยกับสูตรอาหารมี cross-domain knowledge ไหม (เช่น วิทยาศาสตร์อินทรีย์ = overlap)?
