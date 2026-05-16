---
description: Schizophrenia-mode cross-domain thesis generator — forces investment/research theses from unexpected domain combinations. Use when all obvious angles feel exhausted or when you need a thesis nobody else has seen.
---

# /wild-thesis <topic> [--domains=<d1>,<d2>]

สมองที่ไม่มีตัวกรอง domain — บังคับ generate thesis จากจุดที่ไม่มีใครมอง

## Usage

```
/wild-thesis <topic>
/wild-thesis <topic> --domains=biology,logistics
/wild-thesis <topic> --domains=military,fashion,agriculture
```

- `topic`: investment angle, research question, หรือ business model ที่ต้องการมุมใหม่
- `--domains`: 2-4 seed domains ที่ดูเหมือนไม่เกี่ยวข้องกับ topic เลย
  - ถ้าไม่ระบุ → auto-pick 3 domains ที่ห่างจาก topic มากที่สุด

## When to use

✅ GOOD:
- "ทุก angle ใน AI infrastructure ดูเหมือน priced in แล้ว" → `/wild-thesis AI infrastructure`
- "อยากหา thesis ที่คนอื่นยังไม่เห็น" → `/wild-thesis hyperscaler capex --domains=biology,water`
- "อยากรู้ว่า palm oil เชื่อมกับ supply chain crisis ยังไงในแบบที่ไม่มีใครเห็น" → `/wild-thesis palm oil --domains=semiconductor,siege warfare`

❌ WRONG:
- "อยากรู้ thesis ที่ obvious" → ถามตรง หรือ `/brainstorm` แทน
- "อยากเข้าใจกลไก X" → `/deep-dive` แทน
- "อยากหา connection ระหว่าง vault pieces" → `/connect` แทน

---

## Schizophrenia mode rules (ใช้ตลอด command นี้)

1. **ห้ามถามว่า "มันเกี่ยวกันไหม?"** — assume everything is connected, then find how
2. **Cross-domain = required** — ถ้า thesis ไม่ข้าม domain ≥ 2 = ยังไม่ wild พอ
3. **ไม่มี "that makes no sense"** — ความไม่ make sense ขั้นต้น = สัญญาณว่าถูกทิศทาง
4. **ยิ่ง distant ยิ่งดี** — connection ที่ obvious ไม่ใช่ schizophrenia thinking
5. **1 leap = 1 thesis** — แต่ละ thesis ต้องมี 1 unexpected domain leap ที่ชัดเจน

---

## Steps

### 1. Auto-generate seed domains (ถ้าไม่ระบุ --domains)

เลือก 3 domains จาก pool ที่ **ห่างจาก topic มากที่สุด** (ไม่ใช่ใกล้ที่สุด):

Pool: biology, military strategy, fashion trends, agriculture, music theory, architecture, linguistics, religious practice, sports physiology, anthropology, geology, cooking chemistry, medieval history, marine biology, urban planning, epidemiology, game theory (board games), textile manufacturing, ancient trade routes

ประกาศ: "Seed domains: [D1], [D2], [D3] — forcing connections from maximum distance..."

### 2. Cross-domain forcing (generate ทั้งหมดก่อน — ห้าม evaluate ระหว่างนี้)

ต่อแต่ละ seed domain → สร้าง 3 theses โดย apply framework:

> "[Topic] คือ [concept จาก seed domain] ที่แฝงตัวอยู่ — ถ้าจริง แปลว่าอะไร?"

ตัวอย่าง:
- topic = "hyperscaler capex", domain = "biology"
  → "hyperscaler capex cycle = predator-prey population wave — ถ้าจริง: peak capex = prey overshoot → collapse ใน 18 เดือน"
- topic = "hyperscaler capex", domain = "medieval siege warfare"
  → "data center build-out = castle moat strategy — ถ้าจริง: ยิ่งสร้างเร็ว = ยิ่ง lock out challengers = winner-take-all ชัดขึ้น"
- topic = "palm oil supply", domain = "epidemiology"
  → "palm oil boom-bust = epidemic curve — ถ้าจริง: adoption S-curve + crash ตามมาเสมอ = ควร short หลัง peak adoption 18 เดือน"

Total: 3 domains × 3 theses = 9+ theses ขั้นต่ำ

### 3. Implausibility ranking (กลับด้าน logic ปกติ)

จัด rank โดย: **ยิ่งฟังดู implausible มากกว่า = ยิ่งดี**

Reason: thesis ที่ smart money ยังไม่เห็น = ยิ่งฟัง implausible ในหูคนทั่วไป
ถ้า thesis ฟัง obvious = คนอื่นเห็นแล้ว = edge หาย

### 4. Evidence test (ขั้นตอนเดียวที่ใช้ logic)

ต่อแต่ละ thesis เริ่มจาก most implausible:
> "ถ้า thesis นี้จริง — อะไรจะต้อง observable ได้ในโลกจริงตอนนี้?"

- ระบุ observable prediction ได้ → **ALIVE — thesis ยังมีชีวิต**
- ระบุไม่ได้เลย → **DISCARD — เป็นแค่ metaphor ไม่ใช่ thesis**

### 5. Save

Save to: `vault/00_inbox/wild-thesis-<slug>-<date>.md`

---

## Output format (saved file)

```markdown
---
type: wild-thesis
topic: <topic>
seed_domains: [d1, d2, d3]
date: YYYY-MM-DD
theses_generated: N
theses_alive: M
---

# Wild Thesis: <topic>

## Seed domains
[D1], [D2], [D3] — selected for maximum distance from topic

## Generated theses (unfiltered)

### Domain: [D1]
1. **Leap:** "[topic] = [concept from D1]"
   → ถ้าจริง: [implication สำหรับ investment/research]
   Observable prediction: [อะไรต้องเป็นจริงในโลกจริงถ้า thesis นี้ถูก]
   Status: ALIVE / DISCARD

2. ...

### Domain: [D2]
...

## Alive theses (ranked: most implausible first)

| Rank | Thesis | Domain leap | Observable prediction |
|---|---|---|---|
| 1 (most wild) | | [D?]→[topic] | |
| 2 | | | |

## Most promising wild thesis
**[thesis]**
Why it might be real: [evidence หรือ weak signal จากโลกจริงที่ consistent กับ thesis นี้]
What to research next: `/deep-dive <X>` หรือ `/paper-survey <Y>`
```

---

## Constraints

- **Domain leap บังคับ** — ทุก thesis ต้องข้าม domain อย่างน้อย 1 ครั้ง
- **ห้าม obvious** — thesis ที่คนอื่นคิดอยู่แล้ว = ไม่ใช่ wild thesis
- **Evidence test บังคับ** — ทุก thesis ที่ ALIVE ต้องมี observable prediction
- **ห้าม fabricate evidence** — ถ้า observable prediction หาไม่ได้ = DISCARD
- **Maximum distance rule** — seed domains ต้องห่างจาก topic ให้มากที่สุด

## Anti-patterns

- ❌ Cross-domain ที่ obvious ("AI + semiconductor" = ทุกคนเห็นแล้ว ไม่ wild)
- ❌ Thesis ที่ไม่มี observable prediction = metaphor ไม่ใช่ thesis
- ❌ Seed domain ที่ใกล้ topic ("tech thesis + finance domain" = ไม่พอ)
- ❌ Discard thesis เพราะ "ฟังดูบ้า" = นั่นคือสัญญาณถูกทิศทาง

## Commit

หลัง /review ผ่าน → รัน:
```bash
bash scripts/safe-commit.sh "notes: wild-thesis <topic>"
```
