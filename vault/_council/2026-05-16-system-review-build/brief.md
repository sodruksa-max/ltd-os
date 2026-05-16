---
type: council-brief
date: 2026-05-16
topic: ควรสร้าง /system-review command ใหม่หรือไม่
expertise_lens: engineer
---

# Council Brief: /system-review Build Decision

## Context

LTD-OS คือ personal knowledge OS + investment workflow ที่ใช้ Claude Code + Obsidian vault เป็น memory. Owner ไม่ได้ code เอง — Claude เป็น executor ทั้งหมด. ระบบมี 30+ slash commands, 20+ scripts, multi-agent pipeline (Reese→Chris→Vera→Indie→Nick).

**Gap ที่ระบุได้วันนี้:** ระบบมี "eyes" (healthcheck, analyst, paper-survey) แต่ไม่มี "brain" ที่ synthesize ทั้งหมดเข้าหากันแล้วบอกว่าระบบควรไปทางไหน — การพัฒนาเป็น reactive (แก้เมื่อมีปัญหา) ไม่ใช่ proactive.

## Options on the table

**Option 1:** สร้าง `/system-review` command ใหม่ — อ่าน commands + scripts + paper surveys + analyst log → synthesize เป็น improvement roadmap (manual trigger หรือ scheduled)

**Option 2:** ต่อ `/weekly-calibration` — เพิ่ม paper-survey step เข้าไปใน weekly trading review

**Option 2b:** ต่อ `/analyst` — เพิ่ม architecture review section ใน analyst output

**Option 3:** ไม่ทำเพิ่ม — manual paper-survey + healthcheck ตามต้องการ

## Constraints

- Owner ไม่ code เอง → ระบบต้องดูแลตัวเองได้มากที่สุด
- Agent ceiling: 7 agents (DECISIONS.md) — ห้ามสร้าง agent ใหม่ถ้าไม่จำเป็น
- Cost conscious — /council ตัวนี้ cost ~$2.50 แล้ว; /system-review ต้องมี positive ROI
- ระบบมี `/schedule` skill ที่รัน remote agent ได้ตาม cron

## Stakes

- **ถ้าสร้างแล้วไม่ใช้:** เสียเวลา build ~2 ชม. + command bloat
- **ถ้าไม่สร้างแล้วระบบล้าหลัง:** missed improvements จาก papers ที่มีอยู่ (14 papers วันนี้ยังไม่ implement)
- **ถ้าสร้างแบบ scheduled:** อาจรัน noise โดยไม่มีคนดู → alert fatigue

## Open questions

1. owner จะใช้ output ของ /system-review จริงๆ ไหม หรือจะเป็น command ที่ลืม?
2. scheduled vs manual — อันไหน actionable กว่าสำหรับ owner คนเดียว?
3. มี pattern ใน DECISIONS.md ที่บอกว่า "ไม่สร้าง X เพราะ redundant กับ Y ที่มีอยู่"?
