---
name: research
description: Deep research session — paper survey + optional stock deep-dive
schedule: manual
estimated-time: 30-60 min
---

# Workflow: research

ใช้เมื่อต้องการ research เชิงลึก — เริ่มจาก papers แล้ว optionally ต่อด้วย stock

---

## Steps

### step-1: paper-survey
**cmd:** /paper-survey [TOPIC]
**description:** ค้นหา academic papers สำหรับ topic ที่กำหนด — user ระบุ topic ตอนรัน /workflow
**requires-input:** topic (ถามก่อนเริ่ม step นี้)
**on-fail:** stop
**on-success:** next

---

### step-2: stock-content (conditional)
**condition:** ถามว่า "ต้องการ deep-dive หุ้นตัวไหนจาก papers ที่เจอไหม?" — ถ้า yes: ถาม ticker; ถ้า no: skip
**yes-cmd:** /stock-content [TICKER]
**no:** skip
**requires-input:** ticker (ถ้า yes)
**on-fail:** continue
**on-success:** done

---

## Conditions Reference

| Condition | Source | Rule |
|---|---|---|
| Stock deep-dive | User confirmation | Interactive — ถามทุกครั้ง |
| Vault coverage | Step-1 output — gap analysis | ถ้า paper ที่เจอ relate กับ ticker ใน watchlist = suggest |

---

## Notes

- Step-1 ต้องการ topic argument — workflow จะถามก่อนเริ่ม
- Step-2 เป็น interactive condition — Claude ถาม user โดยตรง
- Budget: /paper-survey ใช้ 5-15 searches; /stock-content ใช้ 5 searches เพิ่ม
