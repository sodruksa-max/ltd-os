---
description: Lite daily market log — บันทึกข้อมูลตลาดพื้นฐานวันที่ไม่ได้รัน /pre-market. ใช้เวลา ~2 นาที, ไม่มี web search, ข้อมูลเพียงพอให้ /weekly-calibration ทำงานได้.
---

# /market-log

บันทึก market data วันที่ไม่ได้เทรด — เร็ว, ไม่มี web search, เก็บ data trail ให้ `/weekly-calibration` ใช้ได้

## Usage

```
/market-log [YYYY-MM-DD]
```

- Argument optional — defaults to yesterday ET (รันตอนเช้าไทย = หลังตลาด US ปิด)
- ตัวอย่าง: `/market-log 2026-05-06`

---

## Steps

### 1. Resolve date

```bash
date -d "yesterday" '+%Y-%m-%d'
```

ใช้ผลเป็น `<date>`

### 2. Check overwrite

ถ้า `vault/20_investment/_journal/<date>-review.md` มีอยู่แล้ว → หยุดและถาม:
> ⚠️ พบ `<date>-review.md` อยู่แล้ว — overwrite? (y/n)

ถ้า n → จบโดยไม่แตะไฟล์

### 3. Run post-snapshot.py

```bash
code/python/.venv/Scripts/python scripts/post-snapshot.py --date <date>
```

ดึงจาก output เฉพาะ:
- SPY % change
- QQQ % change
- VIX close
- TLT % change (bonds direction)

ถ้า script fail → ระบุ `[unavailable]` ทุกช่อง แล้วดำเนินต่อ

### 4. Classify scenario

ใช้ SPY % (ไม่ใช่ S&P 500 futures) เพื่อ consistency กับ post-market:
- SPY > +0.3% → **Bullish**
- SPY -0.3% ถึง +0.3% → **Base**
- SPY < -0.3% → **Bearish**

### 5. Ask user for catalyst + note (optional)

แสดง:
```
[date] SPY: [+/-X%] → [Bullish/Base/Bearish] | VIX: [X] | QQQ: [+/-X%] | TLT: [+/-X%]

Catalyst วันนี้คืออะไร? (พิมพ์ 1 ประโยค หรือ Enter เพื่อ skip)
```

รอ input → ถ้า skip ใส่ `[ไม่ได้ระบุ]`

จากนั้น:
```
Personal note? (พิมพ์หรือ Enter เพื่อ skip)
```

รอ input → ถ้า skip ใส่ `-`

### 6. Save review file

```markdown
# Market Log — YYYY-MM-DD (วัน) [lite]
*ข้อมูลตลาดพื้นฐาน — ไม่มี premarket brief วันนี้ | ไม่ใช่คำแนะนำลงทุน*

## Actual Scenario

- **SPY:** [+/-X.XX%] → **[Bullish / Base / Bearish]**
- **QQQ:** [+/-X.XX%]
- **VIX:** [X.X]
- **TLT:** [+/-X.XX%] ([rising = yield falling / falling = yield rising])

## Catalyst

[user input หรือ [ไม่ได้ระบุ]]

## Personal Note

[user input หรือ -]
```

Save to: `vault/20_investment/_journal/<date>-review.md`

### 7. Append to OUTCOMES.md

Append 1 line ใต้ section `## Trading Calibration Log`:

```
<date> [lite] — Actual: <Bullish/Base/Bearish> (SPY <+/-X%>), VIX: <X>, Catalyst: <user input หรือ "-">
```

ถ้า section ยังไม่มี → append header ก่อน

### 8. Report

```
Saved: vault/20_investment/_journal/<date>-review.md [lite]
OUTCOMES.md updated.
```

---

## Constraints

- **ไม่มี web search** — ข้อมูลทั้งหมดจาก post-snapshot.py เท่านั้น
- **ไม่มี calibration score** — ไม่มี premarket brief = ไม่มีอะไรให้เปรียบ
- **ห้าม fabricate** — ถ้า script fail ให้ระบุ `[unavailable]` ทุกช่อง
- **Warn ก่อน overwrite** เสมอ

## Anti-patterns

- ❌ รัน web search ใดๆ — command นี้ต้องเร็ว
- ❌ เพิ่ม sections ที่ไม่ได้อยู่ใน template (scenario playbook, setup outcomes, blind spots)
- ❌ ข้าม OUTCOMES.md append
- ❌ Overwrite โดยไม่ถามก่อน

## Commit

หลัง /review ผ่าน → รัน:
```bash
bash scripts/safe-commit.sh "notes: market-log YYYY-MM-DD [lite]"
```
