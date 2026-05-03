---
name: verify_workflow_feasibility_before_proposing
description: ต้อง verify ว่า workflow ที่เสนอทำได้จริงในสภาพแวดล้อมที่ user ใช้ ก่อนเสนอ
type: feedback
---

ห้ามเสนอ workflow ที่ยังไม่ได้ verify feasibility ก่อน

**Why:** เสนอ "ถ่าย screenshot → ส่งมา Claude Code → Claude อ่าน → อัปเดต" แต่ Claude Code CLI รับ image input จาก user ไม่ได้ — ทำให้ user เสียเวลาและเกิดความเข้าใจผิดเรื่อง capability จริง

**How to apply:** ก่อนเสนอ workflow ใดๆ ที่มี technical step ให้ถามตัวเองก่อนว่า "interface ที่ user ใช้รองรับ step นี้ไหม?" โดยเฉพาะ:
- การส่งไฟล์/รูปเข้า Claude Code CLI → ไม่ได้ (ต้องใช้ file path บนเครื่อง)
- การดึงข้อมูลจาก service ที่ไม่มี API → ต้อง verify ก่อนเสมอ
- Auto workflow ใดๆ → ต้อง verify ทุก step ก่อน propose
