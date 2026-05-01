---
name: Show exact change before asking approval
description: User wants to see the exact content that will change before confirming any approval prompt
type: feedback
---

เมื่อขอ approve อะไรก็ตาม (tool permission, proposal, overwrite, save) ต้องแสดง **ข้อความที่จะเปลี่ยนจริงๆ** ก่อนถาม y/n เสมอ

**Why:** User เห็นแค่ y/n โดยไม่รู้ว่า approve แล้วไฟล์จะเปลี่ยนเป็นอะไร ทำให้ตัดสินใจไม่ได้

**How to apply:**
- Bash tool: description ต้องบอก "ทำอะไรกับไฟล์ไหน" ชัดเจน ไม่ใช่แค่ชื่อ command
- weekly-calibration proposals: แสดง diff (เดิม/ใหม่) ก่อนถาม approve
- overwrite prompts: แสดง path + สิ่งที่จะถูก overwrite ก่อนถาม
- ทุก y/n prompt: ต้องมี context "ถ้า y แล้วจะเกิดอะไร" อยู่ด้วยเสมอ
