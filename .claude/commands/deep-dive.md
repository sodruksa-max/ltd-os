---
description: Autism-mode deep research — one topic, maximum depth, follow every reference, don't stop until nothing is left to find. Opposite of /brainstorm (wide). Use when you need the mechanism, not the surface.
---

# /deep-dive <topic> [--domain=<domain>]

ขุดลึกสุดในสิ่งเดียว — ไม่กว้าง ไม่หยุดเร็ว ไม่ข้ามสิ่งที่น่าสนใจ

## Usage

```
/deep-dive <topic>
/deep-dive <topic> --domain=fertilizer
/deep-dive <topic> --domain=food
/deep-dive <topic> --domain=trading
/deep-dive <topic> --domain=thesis
```

## When to use

✅ GOOD:
- "อยากรู้จริงๆ ว่า AMF ช่วยปาล์มยังไงในระดับ mechanism" → `/deep-dive AMF palm oil --domain=fertilizer`
- "อยากเข้าใจ umami synergy ลึกสุด ไม่ใช่แค่ summary" → `/deep-dive umami IMP GMP synergy --domain=food`
- "อยากรู้ว่า hyperscaler capex cycle ทำงานยังไงจริงๆ" → `/deep-dive hyperscaler capex cycle --domain=thesis`

❌ WRONG USE:
- "อยากได้ไอเดียหลายๆ อย่าง" → ใช้ `/brainstorm` แทน
- "อยากรู้ concept ทั่วไป" → ถามตรง ไม่ต้อง deep-dive

---

## Autism mode rules (ใช้ตลอด session นี้)

1. **ไม่ข้ามสิ่งที่น่าสนใจ** — ถ้าอ่านแล้วเจอ term ที่ไม่รู้หรือ mechanism ที่ยังไม่ชัด → ขุดต่อ ไม่ผ่านไป
2. **ไม่หยุดที่ "พอแล้ว"** — หยุดเมื่อ 3 search ติดต่อกันไม่ได้ข้อมูลใหม่จริงๆ
3. **จำทุกอย่างที่อ่าน** — สร้าง connection web: ทุก fact ต้องเชื่อมกับอย่างน้อย 1 fact อื่น
4. **ไล่ทุก reference** — ถ้า paper อ้าง study → หา study นั้น ถ้า claim อ้างผู้เชี่ยวชาญ → หาว่าเขาพูดอะไรจริงๆ
5. **ลงลึกกว่า summary** — surface = ทุกคนรู้, mechanism = น้อยคนรู้, root cause = แทบไม่มีใครรู้ → ไปให้ถึง root cause

---

## Steps

### 1. Vault check (autism: ตรวจก่อนเสมอ — ไม่ re-research สิ่งที่มีอยู่แล้ว)

```bash
grep -ri "<topic_keywords>" vault/Knowledge/insight-atoms/ vault/10_research/ --include="*.md" -l
```

- ถ้าพบ → โหลดเป็น context ก่อน ระบุสิ่งที่รู้แล้วและสิ่งที่ยังไม่รู้
- สร้าง "known map": fact ที่มีอยู่แล้วใน vault

### 2. Identify the ONE mechanism

จากทุกอย่างที่รู้และไม่รู้ ระบุ **1 คำถามหลัก** ที่ถ้าตอบได้ จะ unlock ความเข้าใจทั้งหมด

ตัวอย่าง:
- "palm oil yield" ไม่ใช่คำถามหลัก
- "why does K deficiency reduce bunch weight faster than N deficiency in mature palm?" คือคำถามหลัก

ประกาศ: "กำลังขุด: [คำถามหลัก]"

### 3. Layer-by-layer descent

ขุดเป็นชั้น — ไม่ข้ามชั้น:

```
Layer 1: Surface (what everyone says)
Layer 2: Mechanism (how it actually works)
Layer 3: Root cause (why the mechanism works that way)
Layer 4: Implication (what this means that most people haven't realized)
Layer 5: Edge cases (when does this break down?)
```

**ต่อแต่ละ layer:**
- Search หาข้อมูล (budget ตาม scope — ดูด้านล่าง)
- ระบุว่า "อยู่ที่ layer ไหนแล้ว"
- ถ้าเจอ sub-mechanism → flag ไว้ขุดต่อ อย่าข้าม

### 4. Connection web (สร้างระหว่างขุด)

ระหว่าง research สร้าง connection map:

```
[Fact A] → เพราะ → [Mechanism B] → นำไปสู่ → [Implication C]
[Mechanism B] ← ขัดแย้งกับ ← [Claim D จาก source X]
[Fact A] ← confirmed by ← [Independent source Y]
```

จุดประสงค์: เห็นว่า claim ไหนมี independent verification และ claim ไหนเป็น echo

### 5. Echo detection (autism: จำแหล่งที่มาทุกตัว)

ก่อน accept claim ใดๆ ว่าเป็นความจริง:
- Trace กลับว่า source ที่อ้างถึงกันมาจาก source เดิมไหม?
- ถ้า 3 sources อ้างเรื่องเดียวกัน แต่ทั้งหมด cite paper เดียว → flag `[ECHO — 1 original source]`
- ถ้า independent replication → flag `[CONFIRMED — independently replicated]`

### 6. Stopping condition

หยุดเมื่อ **3 เงื่อนไขใดเงื่อนไขหนึ่ง:**
1. 3 search ติดกันไม่ได้ข้อมูลใหม่จริงๆ (ไม่ใช่ข้อมูลซ้ำ)
2. ถึง Layer 5 และ edge cases ชัดเจนแล้ว
3. Search budget หมด

### 7. Save

Save to: `vault/10_research/deep-dive-<slug>-<date>.md`

---

## Search budget (ปรับตาม domain)

| Domain | Budget | เหตุผล |
|---|---|---|
| fertilizer | 8 searches | มีกลไกชีวเคมีลึก — ต้องตามหลายชั้น |
| food | 8 searches | flavor chemistry + receptor mechanism |
| trading/thesis | 10 searches | macro + micro + sector + company |
| general | 6 searches | default |

---

## Output format (saved file)

```markdown
---
type: deep-dive
topic: <topic>
domain: <domain>
date: YYYY-MM-DD
core_question: <the ONE question that unlocked everything>
depth_reached: surface | mechanism | root_cause | implication | edge_cases
---

# Deep Dive: <topic>

## Core question
*(The single question that determined the direction of this dive)*

## Known map (from vault — before research)
*(What was already in vault — not re-researched)*

## Layer descent

### Layer 1 — Surface
*(What everyone says)*

### Layer 2 — Mechanism
*(How it actually works)*

### Layer 3 — Root cause
*(Why the mechanism works that way)*

### Layer 4 — Implication
*(What this means that most people haven't realized)*

### Layer 5 — Edge cases
*(When does this break down? Under what conditions is the mechanism wrong?)*

## Connection web
*(Diagram-style: [A] → [B] ← [C])*

## Echo audit
- [CONFIRMED] <claim> — independently replicated by: <sources>
- [ECHO] <claim> — all roads lead to: <single original source>
- [UNVERIFIED] <claim> — no independent source found

## What this changes
*(What did you believe before this dive that turned out to be wrong or incomplete?)*

## Implications for [domain]
*(Specific: what should change in vault/Knowledge/ or formulas or thesis based on this?)*

## Dead ends (ขุดแล้วไม่มีอะไร)
*(Directions that seemed promising but yielded nothing — so future dives don't repeat)*

## Searches used: X/<budget>
```

---

## Constraints

- **1 topic per invocation** — ถ้าอยากขุดหลาย topic → รัน /deep-dive หลายรอบ
- **ห้ามกว้าง** — ถ้าเริ่มรู้สึกว่ากำลังทำ /brainstorm อยู่ → หยุด กลับมาที่ core question
- **Echo detection บังคับ** — ทุก claim ที่จะใส่ใน Layer 3-4 ต้องผ่าน echo check
- **Connection web บังคับ** — ถ้าไม่มี web = ยังไม่ได้ขุดลึกพอ
- **ห้าม fabricate** — ถ้าหาไม่ได้ → บันทึกเป็น dead end ไม่ใช่เดา

## Anti-patterns

- ❌ หยุดที่ Layer 2 เพราะ "น่าจะพอแล้ว" — ไม่พอ ไปต่อ
- ❌ Accept claim โดยไม่ trace source — อาจเป็น echo
- ❌ ขุดกว้างออกแทนที่จะขุดลึกลง — กลับมาที่ core question
- ❌ ไม่บันทึก dead ends — future session จะ repeat งานเดิม
- ❌ Connection web ที่เป็นแค่ list — ต้องเป็น relationship จริงๆ
