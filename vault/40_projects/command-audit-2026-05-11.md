---
type: project-backlog
date: 2026-05-11
status: pending
review-week: 2026-05-18
---

# Command Audit — Must-Have Fixes

ตรวจ 26 command files พบ gap ที่ต้องแก้ก่อนสัปดาห์หน้า จัดลำดับตาม impact

---

## HIGH — แก้ก่อน

### 1. `post-market` — KB sync missing
**ปัญหา:** generate calibration data + lessons แต่ไม่เคย update INDEX_insights หรือ contradiction-registry เมื่อพบ pattern ใหม่
**แก้:** เพิ่ม Indie-style atom extraction + contradiction append หลัง review เสร็จ

### 2. `weekly-calibration` — Kill condition check missing
**ปัญหา:** อ่าน review history เพื่อ propose rules แต่ไม่ตรวจว่า kill condition ใน THESIS_TRACKER trigger ไปแล้วหรือยัง
**แก้:** เพิ่ม step ตรวจ THESIS_TRACKER.md — kill condition triggered ≥2 ครั้ง = flag thesis invalidated ให้ user

### 3. `stock-research` — Watchlist sync missing
**ปัญหา:** research เสร็จแต่ไม่เพิ่ม ticker ใน `config/watchlist.txt` — /screen และ /bot ไม่รู้ว่ามี ticker นี้
**แก้:** append ticker ใน watchlist.txt หลัง save note (เหมือนที่ stock-content ทำ)

### 4. `stock-content` — Vera contradiction append missing
**ปัญหา:** Step 6 Vera flag ❓ แต่ไม่ได้ append จริงใน contradiction-registry.md
**แก้:** เพิ่ม explicit "append ใน contradiction-registry.md ทันที" ใน Vera section

### 5. `bot` — No kill condition pre-flight
**ปัญหา:** screen + place orders โดยไม่ตรวจว่า buy candidate มี kill condition triggered ใน THESIS_TRACKER
**แก้:** เพิ่ม pre-flight step ตรวจ THESIS_TRACKER ก่อน place order — ถ้า kill condition triggered = skip ticker

### 6. `paper-trade` — No position log
**ปัญหา:** place order แต่ไม่มี forward-facing position ledger — /eod รู้ post-fill เท่านั้น ไม่มีไฟล์ที่ track entry intent
**แก้:** append entry ใน `vault/20_investment/_journal/position-ledger.md` ทุกครั้งที่ place

### 7. `eod` — No kill condition alert
**ปัญหา:** report open positions แต่ไม่ตรวจ kill conditions สำหรับ position ที่เปิดอยู่
**แก้:** เพิ่ม step ตรวจ THESIS_TRACKER kill conditions สำหรับแต่ละ ticker ที่มี open position — alert ถ้า trigger

---

## MEDIUM — แก้สัปดาห์หน้า

### 8. `challenge` — Output orphaned จาก KB
**ปัญหา:** devil's advocate flags risks แต่ไม่ append ใน contradiction-registry หรือ suggest update kill conditions
**แก้:** เพิ่ม step สุดท้าย — ถ้า challenge พบ risk ใหม่ → suggest append ใน contradiction-registry + update kill conditions

### 9. `eod` — No THESIS_TRACKER context
**ปัญหา:** รายงาน P&L แต่ไม่รู้ว่า ticker ไหน active thesis ไหนหรือ kill condition ใกล้ trigger
**แก้:** โหลด THESIS_TRACKER context → แสดง "kill condition status" ต่อ open position

### 10. `daily-brief` — ไม่ suggest /weekly-calibration
**ปัญหา:** ไม่ตรวจว่า calibration ครั้งล่าสุดนานแค่ไหน → user ลืม run
**แก้:** ถ้า last calibration > 7 วัน → แสดง "→ ถึงเวลา /weekly-calibration แล้ว"

### 11. `nlm` — Artifacts orphaned
**ปัญหา:** download artifacts ลง _assets/ แต่ไม่ suggest /import-notebooklm หรือ KB link
**แก้:** หลัง download → suggest "รัน /import-notebooklm เพื่อ file ใน vault"

### 12. `council` — ไม่ link กับ THESIS_TRACKER
**ปัญหา:** debate เรื่อง investment decisions แต่ output ไม่ link กับ active theses
**แก้:** เพิ่ม step สุดท้าย — ถ้า topic เกี่ยวกับ thesis → suggest update THESIS_TRACKER หรือ kill conditions

### 13. `pre-market` — Sector-thesis alignment missing
**ปัญหา:** เขียน sector radar แต่ไม่ตรวจว่า tone ขัดกับ thesis ใน THESIS_TRACKER ไหม
**แก้:** load THESIS_TRACKER → ถ้า sector bullish แต่ thesis invalidated = flag ⚠️

### 14. `condense` — ไม่ update INDEX_insights เมื่อ archive
**ปัญหา:** move notes ไป 90_archive/ แต่ถ้า notes เดิมมี insight atoms ใน INDEX_insights จะกลายเป็น dead link
**แก้:** ก่อน archive → ตรวจ INDEX_insights.md ว่ามี reference ถึงไฟล์นั้นไหม ถ้ามี = flag ให้ user

### 15. `weekly-market` — Thesis regime cross-check missing
**ปัญหา:** รายงาน sector rotation แต่ไม่ตรวจว่า regime ขัดกับ thesis assumption ไหม
**แก้:** load THESIS_TRACKER → flag ถ้า risk-off week แต่ thesis bet on cyclical growth

---

## SUMMARY

| Priority | Count | คำสั่งหลักที่ต้องแก้ |
|---|---|---|
| HIGH (แก้ก่อน) | 7 | post-market, weekly-calibration, stock-research, stock-content, bot, paper-trade, eod |
| MEDIUM (สัปดาห์หน้า) | 8 | challenge, daily-brief, nlm, council, pre-market, condense, weekly-market |

**Root cause ที่ทำให้เกิด gap เยอะ:** คำสั่งส่วนใหญ่สร้างมาก่อน THESIS_TRACKER และ contradiction-registry จะ mature — ต้องย้อนกลับมาเชื่อม KB sync ทีละคำสั่ง

---

*Audit by: Claude Code 2026-05-11 — 26 commands reviewed*
