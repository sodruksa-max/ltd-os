---
description: สร้าง recipe formula note จาก template — สำหรับพัฒนาสูตรอาหารเพื่อขาย
---

# /new-recipe

สร้าง recipe note ใหม่ พร้อม version control และ selling framework

## Usage

```
/new-recipe <ชื่อเมนู> [category]
/new-recipe pad-krapao thai-stirfry
/new-recipe nam-prik-pao sauce
```

## Language rule

ตอบเป็นภาษาเดียวกับที่ user พิมพ์ — Thai หรือ English

---

## Steps

### 1. Parse input

- **Recipe name** (required): ชื่อเมนู → สร้าง slug
- **Category** (optional): ประเภทอาหาร เช่น `thai-stirfry`, `sauce`, `curry`, `dessert`

### 2. Vault check

ตรวจ `vault/50_formulas/recipes/` ว่ามีสูตรชื่อนี้อยู่แล้วไหม:
- ถ้ามี → ถาม "สร้าง v2 หรือสูตรใหม่?"
- ถ้าไม่มี → ดำเนินต่อ

ตรวจ `vault/Knowledge/insight-atoms/` (filter: `domain:recipe`) และ `vault/50_formulas/recipes/_research/`:
- ถ้ามี research เกี่ยวข้อง → โหลดเป็น context

### 3. Prompt user (3 คำถาม)

ถามก่อน fill template:
1. **Inspiration:** สูตรนี้มาจากไหน? (ร้าน / เชฟ / เมนูต้นแบบ)
2. **Key difference:** สิ่งที่อยากพัฒนาหรือทำให้ดีกว่าต้นแบบคืออะไร?
3. **Target buyer:** ใครจะซื้อสูตรนี้ — home cook, ร้านอาหาร, catering?

### 4. Create recipe file

- Template: `vault/_templates/recipe-formula.md`
- Save to: `vault/50_formulas/recipes/<slug>/v1.md`
- กรอกจาก user input + context
- **ต้องกรอก:** selling point, key technique, content angle, target buyer, kill condition
- **ปล่อยว่าง:** trial log (ยังไม่มีข้อมูลจริง)

### 5. Research check (ถ้า key technique ยังไม่ชัด)

ถ้า user ไม่รู้ mechanism ที่ทำให้สูตรนี้ได้ผล → แนะนำ:
```
/paper-survey <mechanism> — เช่น "Maillard reaction high-heat stir fry"
                          หรือ "fermentation lactic acid flavor development"
```
ไม่บังคับ — แต่สูตรที่ขายได้ต้องอธิบาย *ทำไม* ได้ ไม่ใช่แค่ *อะไร*

### 6. Extract insight atom (ถ้า key technique ชัดเจน)

ถ้า key technique อ้างอิง mechanism ที่ตรวจสอบได้:
- สร้าง atom ใน `vault/Knowledge/insight-atoms/recipe-<slug>-v1-<date>.md`
- Tag: `domain:recipe`, `theme cluster: sector/food`
- Append ใน `vault/Knowledge/INDEX_insights.md`

### 7. Report back

```
สร้างแล้ว: vault/50_formulas/recipes/<slug>/v1.md

กรอกแล้ว: Selling point ✓ | Key technique ✓ | Content angle ✓ | Target buyer ✓
ต้องกรอกเพิ่ม: Ingredients (ปริมาณที่แม่นยำ), Method (step by step)

Insight atom: [สร้างหรือไม่ + เหตุผล]

ขั้นต่อไป:
→ ทำสูตรจริง → กรอก trial log ทันทีหลังชิม
→ เปลี่ยนทีละ 1 อย่างต่อ version เท่านั้น
→ Approved-baseline หลัง 3 iterations + รสชาติผ่าน 3 คน
```

### 8. Commit

```bash
git add vault/50_formulas/recipes/<slug>/v1.md
bash scripts/safe-commit.sh "vault: new-recipe <slug> v1"
```

---

## Constraints

- **ห้ามเขียน recipe ให้ user** ก่อนที่ user จะให้ข้อมูล ingredients จริง
- **ห้ามกรอก trial log** ก่อนทำจริง — ทุกอย่างใน log ต้องมาจาก actual test
- **Approved-baseline ต้องผ่าน 3 iterations** — ไม่ advance ก่อน
- **Content angle ต้องกรอก** — ถ้า user ไม่รู้ให้ช่วย brainstorm 2-3 ตัวเลือก
