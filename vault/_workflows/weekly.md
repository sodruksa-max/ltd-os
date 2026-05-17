---
name: weekly
description: Weekly review session — market review, learnings, Nick quarterly check
schedule: friday-close
estimated-time: 25-45 min
---

# Workflow: weekly

รันทุกวันศุกร์ปิดตลาด หรือ manual เมื่อต้องการ

---

## Steps

### step-1: weekly-market
**cmd:** /weekly-market
**description:** Sector rotation, key events สัปดาห์นี้, earnings highlights
**on-fail:** stop
**on-success:** next

---

### step-2: weekly-learnings
**cmd:** /weekly-learnings
**description:** ดึง key learnings จาก daily notes + commits สัปดาห์นี้
**on-fail:** continue
**on-success:** next

---

### step-3: nick-weekly
**cmd:** /nick-weekly
**description:** Nick review holdings สัปดาห์นี้ — kill conditions + recommendations
**on-fail:** stop
**on-success:** next

---

### step-4: nick-quarterly (conditional)
**condition:** ดูจาก output step-3 — ถ้า Nick พบ 3+ holdings ที่ verdict "Evolving" หรือ "Invalidated" ในสัปดาห์เดียวกัน → รัน quarterly audit; ถ้าน้อยกว่า → skip
**yes-cmd:** /nick-quarterly
**no:** skip
**on-fail:** continue
**on-success:** done

---

## Conditions Reference

| Condition | Source | Rule |
|---|---|---|
| Quarterly trigger | /nick-weekly output — Autism Pattern Check | ≥ 3 holdings Evolving/Invalidated = run /nick-quarterly |
| Sector conflict | /weekly-market output | Active thesis vs Lagging sector = flag |

---

## Notes

- Step-4 เป็น conditional — ส่วนใหญ่จะ skip ยกเว้นตลาดผันผวนมาก
- ถ้า skip step-4: workflow done หลัง step-3
- Run หลัง 4pm ET Friday สำหรับ close prices ที่แม่นยำ
