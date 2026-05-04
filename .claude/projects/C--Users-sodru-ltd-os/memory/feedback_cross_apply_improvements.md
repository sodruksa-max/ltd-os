---
name: Cross-apply improvements to related systems
description: เมื่อพัฒนา improvement ที่ทำงานได้ดี ให้ proactively แนะนำว่าควรนำไปใช้กับส่วนอื่นที่เกี่ยวข้องด้วย
type: feedback
---

เมื่อสร้างหรือแก้ไขระบบที่ได้ผลดี (script ใหม่, pattern ใหม่, approach ใหม่) ให้ระบุชัดเจนว่ามีส่วนอื่นใดในระบบที่ควรได้รับ improvement เดียวกันนี้ด้วย

**Why:** เช่น เมื่อสร้าง `post-snapshot.py` (ดึงข้อมูล EOD ผ่าน API แทน web search) ควรชี้ทันทีว่า `weekly-market` skill หรือ `weekly-calibration` ที่ยังใช้ web search ดึงข้อมูลตลาดก็ควรได้รับ approach เดียวกัน

**How to apply:** หลังจาก implement improvement และ test ผ่านแล้ว ก่อน commit ให้ scan ว่ามี skill/script อื่นที่:
1. ทำงานคล้ายกัน (เช่น ดึงข้อมูลตลาด, generate reports)
2. ยังใช้วิธีเดิมที่ด้อยกว่า (web search แทน API, manual แทน automation)
3. จะได้ประโยชน์จาก pattern เดียวกัน

แล้วแจ้ง user: "improvement นี้น่าจะใช้กับ X และ Y ด้วย — ทำเลยไหม?"
