---
description: สร้าง fertilizer formula note จาก template — สำหรับพัฒนาสูตรปุ๋ย organic เพื่อขาย
---

# /new-formula

สร้าง fertilizer formula note ใหม่ พร้อม version control และ selling framework

## Usage

```
/new-formula <ชื่อสูตร> [crop]
/new-formula palm-organic-base palm
/new-formula high-k-fruiting-blend palm
```

## Language rule

ตอบเป็นภาษาเดียวกับที่ user พิมพ์ — Thai หรือ English

---

## Steps

### 1. Parse input

- **Formula name** (required): ชื่อสูตร → สร้าง slug (lowercase, dash-separated)
- **Crop** (optional, default: `palm`): พืชเป้าหมาย

### 2. Vault check

ตรวจ `vault/50_formulas/fertilizer/` ว่ามีสูตรชื่อนี้อยู่แล้วไหม:
- ถ้ามี → ถาม "มีสูตรนี้อยู่แล้ว — สร้าง v2 หรือสร้างสูตรใหม่?"
- ถ้าไม่มี → ดำเนินต่อ

ตรวจ `vault/50_formulas/fertilizer/_research/` และ `vault/Knowledge/insight-atoms/` (filter: `domain:fertilizer`):
- ถ้ามี research เกี่ยวข้อง → โหลดเป็น context ก่อนสร้าง template

### 3. Prompt user (3 คำถาม)

ถามก่อน fill template:
1. **Hypothesis:** ทำไม combination นี้ถึงควรได้ผล? (1-2 ประโยค)
2. **Key ingredients:** วัตถุดิบหลักที่มีอยู่ในมือ หรือหาได้ในพื้นที่?
3. **Selling angle:** สูตรนี้ต่างจากปุ๋ยตลาดยังไง? (1 ประโยค)

### 4. Create formula file

- Template: `vault/_templates/fertilizer-formula.md`
- Save to: `vault/50_formulas/fertilizer/<slug>/v1.md`
- กรอกจาก user input + context ที่มี
- **ห้ามกรอก trial log** — ยังไม่มีข้อมูลจริง
- **ต้องกรอก:** selling point, hypothesis, kill condition, content angle

### 5. Cross-check market standard

ตรวจ `vault/50_formulas/fertilizer/palm-v0-market-standard.md` ถ้ามี:
- เทียบ NPK ratio กับ market standard
- กรอก "Market comparison" section

### 6. Extract insight atom (ถ้า hypothesis มี mechanism ชัดเจน)

ถ้า hypothesis อ้างอิง mechanism ที่ตรวจสอบได้:
- สร้าง atom ใน `vault/Knowledge/insight-atoms/fertilizer-<slug>-v1-<date>.md`
- Tag: `domain:fertilizer`, `theme cluster: sector/agri` (หรือที่เหมาะ)
- Append ใน `vault/Knowledge/INDEX_insights.md`

### 7. Report back

```
สร้างแล้ว: vault/50_formulas/fertilizer/<slug>/v1.md

กรอกแล้ว: Selling point ✓ | Hypothesis ✓ | Kill condition ✓ | Content angle ✓
ต้องกรอกเพิ่ม: Ingredients (ปริมาณ + ราคา), Application (วิธีและช่วงเวลา)

Market comparison: NPK ของสูตรนี้ vs 15-15-15 = [สรุป]
Insight atom: [สร้างหรือไม่สร้าง + เหตุผล]

ขั้นต่อไป:
→ กรอก Ingredients table พร้อมราคา
→ กำหนดแปลงทดสอบ (แนะนำ: 3-5 ต้น ไม่ใช่ทั้งสวน)
→ วันที่ใส่ปุ๋ย → บันทึกใน trial log
→ ตั้ง reminder +12 สัปดาห์ สำหรับ observation แรก
```

### 8. Commit

```bash
git add vault/50_formulas/fertilizer/<slug>/v1.md
bash scripts/safe-commit.sh "vault: new-formula <slug> v1"
```

---

## Constraints

- **ห้ามสร้างตัวเลข NPK** ที่ไม่ได้มาจาก research หรือ user input — ใส่ ❓ แทน
- **ห้าม advance version** ก่อน 12 สัปดาห์นับจากวันใส่ปุ๋ยจริง
- **ห้ามทดสอบทั้งสวน** — เริ่มจาก 3-5 ต้นเสมอ
- **ทุกสูตรต้องมี kill condition** ที่วัดได้ — ห้าม vague
