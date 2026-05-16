---
description: Dyslexia-mode jigsaw thinking — find non-obvious connections between vault pieces that look unrelated on the surface. Use when you sense two ideas are related but can't articulate how.
---

# /connect <topic> [--scope=<scope>]

มองทั้งหมดพร้อมกัน แล้วหาว่า piece ไหนของ jigsaw เป็นชิ้นเดียวกัน

## Usage

```
/connect <topic>
/connect <topic> --scope=vault          (search all of vault — default)
/connect <topic> --scope=knowledge      (KB only: atoms + theses + tracker)
/connect <topic> --scope=research       (10_research/ + 50_formulas/)
/connect <topic> --scope=investment     (20_investment/ + nick/)
```

## When to use

✅ GOOD:
- "รู้สึกว่า AMF กับ microbiome thesis น่าจะเชื่อมกัน แต่ไม่รู้ยังไง" → `/connect AMF microbiome`
- "อยากรู้ว่า insight atoms เกี่ยวกับ palm oil มีชิ้นไหนเชื่อมกับ investment thesis บ้าง" → `/connect palm oil --scope=knowledge`
- "รู้สึกว่า umami synergy กับ fermentation น่าจะเป็น jigsaw เดียวกัน" → `/connect umami fermentation --scope=research`
- "อยากเห็นว่า theses ใน portfolio overlap กันยังไง" → `/connect hyperscaler capex --scope=investment`

❌ WRONG USE:
- "อยากรู้รายละเอียดเรื่อง X" → `/deep-dive` แทน
- "อยากได้ไอเดียใหม่" → `/brainstorm` แทน

---

## Dyslexia mode rules

1. **มองภาพรวมก่อนเสมอ** — อ่านทุกไฟล์ที่เกี่ยวข้องแบบ scan ก่อน ไม่ deep-read ทีละไฟล์
2. **หา underlying principle ไม่ใช่ keyword** — สอง piece อาจใช้ภาษาต่างกันแต่พูดเรื่องเดียวกัน
3. **ความเชื่อมที่ดีที่สุดคือที่ไม่ obvious** — ถ้า connection ชัดเกินไปคือทุกคนรู้แล้ว ไม่ต้อง map
4. **ระบุ "shape" ของ connection** — ไม่แค่ "เกี่ยวกัน" แต่ เกี่ยวกันยังไง: reinforce? contradict? incomplete without each other?
5. **หา missing piece** — ถ้า jigsaw ยังไม่สมบูรณ์ ระบุว่าขาดชิ้นไหน

---

## Steps

### 1. Gestalt scan (อ่านทั้งหมดพร้อมกัน ไม่ deep-read)

```bash
grep -ri "<topic_keywords>" vault/ --include="*.md" -l
```

- List ไฟล์ทั้งหมดที่เกี่ยวข้อง (ทุก level ของ vault ตาม scope)
- อ่านแต่ละไฟล์แบบ skim — จับ underlying principle ของแต่ละไฟล์ใน 1-2 ประโยค
- ยังไม่วิเคราะห์ connection ขณะนี้

ประกาศ: "กำลังสแกน [N] ไฟล์ที่เกี่ยวข้อง..."

### 2. Principle extraction (สกัด underlying principle ต่อไฟล์)

ต่อแต่ละไฟล์ที่ found — ระบุ:
- **Surface topic:** ไฟล์นี้พูดถึงอะไร (keyword level)
- **Underlying principle:** ไฟล์นี้จริงๆ พูดถึงอะไร (concept level)

ตัวอย่าง:
```
vault/Knowledge/insight-atoms/fertilizer-palm-npk-baseline.md
  Surface: palm oil NPK requirements, EFB/POME compost
  Underlying: microbial intermediaries increase nutrient bioavailability beyond raw NPK

vault/10_research/papers/soil-microbiome-survey.md  
  Surface: soil bacteria in agriculture
  Underlying: microbial intermediaries increase nutrient bioavailability beyond raw NPK
  
→ SAME underlying principle — jigsaw match
```

### 3. Connection mapping (ประกอบ jigsaw)

จัดกลุ่ม pieces ที่มี underlying principle เหมือนกันหรือ complementary:

**Connection types:**
- `[REINFORCE]` — สอง piece บอกเรื่องเดียวกันจากมุมต่าง → ทำให้ claim แข็งแกร่งขึ้น
- `[COMPLETE]` — piece A อธิบาย mechanism, piece B อธิบาย application → รวมกันเป็น complete picture
- `[CONTRADICT]` — สอง piece ขัดแย้งกัน ทั้งที่ดูเหมือนอยู่คนละ domain
- `[UNLOCK]` — piece A เป็น precondition ของ piece B → ถ้าไม่มี A, B ใช้ไม่ได้เต็ม
- `[MISSING]` — เห็น shape ของ jigsaw ที่ควรมี piece X แต่ vault ยังไม่มี → flag gap

### 4. Spatial layout (วาด map)

แสดง connections เป็น relationship diagram:

```
[Piece A: AMF activation]
    ↕ COMPLETE
[Piece B: CEC+ mechanism]  
    ↕ REINFORCE
[Piece C: biochar soil carbon]
    ↕ UNLOCK
[Piece D: K bioavailability for palm yield]
    ⬜ MISSING: cost-effectiveness data for Thai context
```

### 5. Non-obvious insight (จุดที่ dyslexia เห็นแต่ linear reader ไม่เห็น)

ระบุ connection ที่ไม่ obvious ที่สุด 1-3 อัน — เหล่านี้คือ value จริงของ /connect:

> "Piece X จาก [domain 1] และ Piece Y จาก [domain 2] ดูไม่เกี่ยวกัน แต่จริงๆ ทั้งสองเป็น instance ของ [underlying principle] เดียวกัน — แปลว่า [implication ที่ไม่มีใครเห็น]"

### 6. Save

Save to: `vault/00_inbox/connect-<slug>-<date>.md`

---

## Output format (saved file)

```markdown
---
type: connect
topic: <topic>
scope: <scope>
date: YYYY-MM-DD
files_scanned: N
connections_found: N
---

# Connect: <topic>

## Files scanned
*(brief list — surface topic per file)*

## Principle map
*(underlying principle extracted per file)*

## Connections

### [REINFORCE] <Piece A> ↔ <Piece B>
Why: <underlying principle they share>
Implication: <what this means together that neither says alone>

### [COMPLETE] <Piece A> + <Piece B> = <complete picture>
Why: <how they fit>
Implication: <what becomes possible when you see them as one>

### [CONTRADICT] <Piece A> vs <Piece B>
Why: <the tension>
Resolution needed: <what would resolve it>

### [MISSING] <shape of gap>
What vault needs: <what piece would complete this jigsaw>
Suggested action: `/deep-dive <topic>` or `/paper-survey <topic>`

## Spatial layout
*(relationship diagram)*

## Non-obvious insights (dyslexia finds)
1. **[Piece X] + [Piece Y]:** <the surprising connection>
   Implication: <what this unlocks>

## What to do next
- [action] — because [connection found]
```

---

## Constraints

- **Gestalt first** — ห้าม deep-read ทีละไฟล์ก่อน scan ทั้งหมด
- **Underlying principle ไม่ใช่ keyword** — connection ที่ดีที่สุดคือ same principle, different language
- **ห้าม force connection** — ถ้าไม่มี connection จริง ให้บอก "ไม่พบ non-obvious connection"
- **Non-obvious บังคับ** — ถ้า insight ชัดเกินไปไม่ต้อง include
- **Missing piece บังคับ** — เสมอต้องระบุว่า jigsaw ยังขาดอะไร

## Anti-patterns

- ❌ Connection ที่ obvious ("palm oil และ fertilizer เกี่ยวกัน" — ทุกคนรู้แล้ว)
- ❌ List ไฟล์โดยไม่ระบุ underlying principle
- ❌ Spatial layout ที่เป็นแค่ list — ต้องเป็น relationship จริงๆ
- ❌ ไม่ระบุ missing piece — jigsaw ที่ไม่บอกว่าขาดอะไรคือยังไม่สมบูรณ์
