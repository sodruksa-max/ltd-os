---
description: Interactive wizard to create a new named workflow in vault/_workflows/. Asks name, steps, conditions, schedule — saves runnable definition file.
---

# /new-workflow

Wizard สร้าง workflow definition ใหม่ใน `vault/_workflows/` — รัน `/workflow <name>` ได้ทันที

## Usage

```
/new-workflow
/new-workflow <name>    — ถ้าบอกชื่อมาแล้ว ข้าม question แรก
```

---

## Steps

### 1. Collect name + description

ถาม (ถ้าไม่ได้บอกมาใน args):
> "ชื่อ workflow คืออะไร? (lowercase, no spaces — เช่น `morning`, `deep-research`, `eod-review`)"

ตรวจว่าชื่อไม่ซ้ำกับไฟล์ที่มีอยู่:
```bash
ls vault/_workflows/*.md 2>/dev/null | sed 's|.*/||;s|\.md||'
```
ถ้าซ้ำ → แจ้งและถามว่า overwrite หรือเปลี่ยนชื่อ

ถาม description (1 บรรทัด):
> "อธิบาย workflow นี้สั้นๆ (1 ประโยค):"

### 2. Collect steps

ถาม steps ทีละตัว — loop จนกว่า user จะบอกว่าเสร็จ:

> "Step 1 รัน command อะไร? (เช่น `/pre-market`, `/screen`, `/nick-weekly`, หรือ bash script เช่น `scripts/macro-snapshot.py`)"
> "Step 1 ถ้า fail ให้ทำอะไร? (stop / continue) [default: stop]"

Repeat สำหรับ step 2, 3, ... จนกว่า user จะตอบ "เสร็จแล้ว" หรือ "done"

### 3. Collect conditions

สำหรับแต่ละ step ที่มีมากกว่า 1 step ถามว่า:
> "ระหว่าง step [N] และ step [N+1] มี condition ไหมที่ต้องตรวจก่อน? (เช่น 'ถ้า VIX > 20' หรือ 'ถามก่อน') — หรือ enter เพื่อข้าม"

ถ้า user ระบุ condition:
> "ถ้า condition = true: รัน step [N+1] ปกติ หรือรัน command อื่น?"
> "ถ้า condition = false: skip / รัน command อื่น?"

### 4. Collect schedule

> "รัน workflow นี้แบบ manual หรือ schedule? (manual / daily / weekly / friday-close)"

ถ้า schedule ≠ manual → แจ้ง:
> "ระบบจะ remind ให้รัน — แต่ cron job จริงต้องตั้งแยกด้วย `/cron` หรือ `scripts/install-cron.sh`"

### 5. Collect estimated time

> "workflow นี้น่าจะใช้เวลาประมาณเท่าไหร่? (เช่น 20-35 min)"

### 6. Save workflow definition

สร้างไฟล์ที่ `vault/_workflows/<name>.md` ตาม template:

```markdown
---
name: <name>
description: <description>
schedule: <schedule>
estimated-time: <time>
---

# Workflow: <name>

<description>

---

## Steps

<for each step:>
### step-N: <command-slug>
**cmd:** <command>
**description:** <อธิบาย step นี้ทำอะไร>
[**condition:** <condition text — ถ้ามี>]
[**yes-cmd:** <command — ถ้ามี>]
[**no:** skip|<command>]
[**requires-input:** <field — ถ้ามี>]
**on-fail:** stop|continue
**on-success:** next|done

---
<end for each step>

## Conditions Reference

| Condition | Source | Rule |
|---|---|---|
[<for each condition: fill table>]

## Notes

- สร้างโดย /new-workflow เมื่อ <date>
- แก้ไขได้โดยตรงที่ vault/_workflows/<name>.md
```

### 7. Confirm + offer to run

แสดง workflow ที่สร้าง:
```
✓ บันทึกแล้ว: vault/_workflows/<name>.md

Steps:
  1. <step> [on-fail: <x>]
  2. <step> [condition: <c>] [on-fail: <x>]
  ...

รัน workflow นี้เลยไหม? → /workflow <name>
หรือแก้ไขก่อน → เปิด vault/_workflows/<name>.md ใน Obsidian
```

---

## Constraints

- **ห้ามสร้าง workflow โดยไม่มีอย่างน้อย 2 steps** — 1 step ใช้ command ตรงๆ ได้เลย ไม่ต้องเป็น workflow
- **ชื่อต้องเป็น lowercase, no spaces, no special chars** — เช่น `morning`, `deep-research`, `eod-review`
- **Condition description เป็น plain Thai/English** — Claude evaluate เอง ไม่ต้องเป็น code
- **ห้าม overwrite โดยไม่ confirm** — ถ้าชื่อซ้ำต้องถามก่อนทุกครั้ง
