---
name: morning
description: Morning trading session — pre-market brief, conditional screen, Nick portfolio check
schedule: manual
estimated-time: 20-35 min
---

# Workflow: morning

รัน 3 tools ตามลำดับ — Claude ประเมิน condition จาก output ของ step ก่อนหน้า

---

## Steps

### step-1: pre-market
**cmd:** /pre-market
**description:** ดึงข้อมูลสดจากตลาด — futures, VIX, macro, setups
**on-fail:** stop
**on-success:** next

---

### step-2: screen (conditional)
**condition:** ดูจาก output step-1 — ถ้า VIX > 20 หรือมี EARLY★ setups จาก universe-screen ให้รัน; ถ้า VIX ≤ 20 และไม่มี EARLY★ ให้ skip
**yes-cmd:** /screen
**no:** skip
**on-fail:** continue
**on-success:** next

---

### step-3: nick-weekly
**cmd:** /nick-weekly
**description:** Nick ตรวจ holdings, kill conditions, และ recommend
**on-fail:** stop
**on-success:** done

---

## Conditions Reference

| Condition | Source | Rule |
|---|---|---|
| VIX threshold | /pre-market output — VIX row | > 20 = run /screen |
| EARLY★ setups | universe-screen output in /pre-market | any EARLY★ ticker = run /screen |
| Market closed | /pre-market timestamp check | US market closed = skip step-2 only |

---

## Notes

- Step-2 ใช้ context จาก /pre-market ที่รันแล้ว — ไม่ต้อง re-fetch
- ถ้า resume: อ่าน `.state/morning-<date>.json` → เริ่มจาก step ที่ค้างอยู่
- ถ้า /pre-market fail → หยุดทั้ง workflow (step-3 ไม่มีประโยชน์โดยไม่มี macro context)
