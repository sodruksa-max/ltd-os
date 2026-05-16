---
description: Hypomania-mode idea generation — generate 15+ ideas fast, no filtering, then pick top 3 by energy. Use for content hooks, formula hypotheses, thesis angles, project ideas.
---

# /brainstorm <topic> [--output=<mode>]

Generate ideas in hypomania mode — fast, unfiltered, volume-first.

## Usage

```
/brainstorm <topic>
/brainstorm <topic> --output=hooks      (content hooks for video/post)
/brainstorm <topic> --output=ideas      (business/project/product ideas)
/brainstorm <topic> --output=angles     (research angles or thesis frames)
/brainstorm <topic> --output=formulas   (recipe or fertilizer hypotheses)
```

Default output mode if omitted: `ideas`

## When to use

✅ GOOD:
- "ไม่รู้จะทำ video อะไรเกี่ยวกับ umami" → `/brainstorm umami --output=hooks`
- "อยากหา angle ใหม่สำหรับสูตรปุ๋ย" → `/brainstorm palm fertilizer --output=formulas`
- "ไม่รู้จะทำ project อะไรต่อ" → `/brainstorm formula business ideas`
- "อยากได้ thesis ใหม่" → `/brainstorm AI infrastructure --output=angles`

❌ TOO SPECIFIC (just ask directly):
- "ควรใส่ปุ๋ยกี่กรัม" → ถามตรง ไม่ต้อง brainstorm

## Steps

### 1. Enter hypomania mode

ห้าม filter. ห้าม evaluate. ห้ามพูดว่า "but this might not work."

ทุกไอเดียที่เกิดขึ้น = ออกมาหมด

### 2. Load context (light read)

- Read `vault/_memory/PREFERENCES.md` — ใครคือ user, goal คืออะไร
- If `--output=formulas`: scan `vault/50_formulas/` — อะไรมีอยู่แล้ว (ไม่ต้องซ้ำ)
- If `--output=hooks`: scan `vault/30_content/` — tone/style ที่เคยใช้
- If `--output=angles`: check `vault/Knowledge/THESIS_TRACKER.md` — thesis ที่มีอยู่

### 3. Generate — minimum 15, no maximum

Generate ต่อเนื่องไปเรื่อยๆ — ไม่หยุดเพื่อ evaluate

Rules:
- ไอเดียที่ 1-5 = สิ่งที่ทุกคนคิดได้ ต้องผ่านไปให้เร็ว
- ไอเดียที่ 6-10 = เริ่มน่าสนใจ
- ไอเดียที่ 11-15 = ที่ดีที่สุดมักอยู่ตรงนี้
- ถ้ายังมีไอเดียค้างอยู่หลัง 15 → ใส่ต่อ ไม่ตัด

ให้แต่ละไอเดียสั้น — 1 ประโยคหรือ 1 วลี ไม่ต้อง expand ตอนนี้

### 4. Build connections

หลัง generate แล้ว — มองหา:
- ไอเดียไหนที่รวมกันแล้วน่าสนใจกว่าแยกกัน?
- ไอเดียไหนเป็น sub-idea ของอีกอันหนึ่ง?
- มีไอเดียจาก domain อื่นที่ขโมยมาได้ไหม?

### 5. Energy filter (ครั้งเดียว — ไม่ใช้ logic)

จาก list ทั้งหมด เลือก **3 ตัวที่มี energy มากที่สุด** — ไม่ใช่ safe ที่สุด, ไม่ใช่ practical ที่สุด — ตัวที่น่าตื่นเต้นที่สุด

### 6. Save + hand off

Save to: `vault/00_inbox/brainstorm-YYYY-MM-DD-<slug>.md`

แล้วแสดง:
```
Top 3 (by energy):
1. [idea] — why this one has energy
2. [idea] — ...
3. [idea] — ...

Full list: vault/00_inbox/brainstorm-YYYY-MM-DD-<slug>.md

ขั้นตอนต่อไป:
→ /council <top pick>     (ถ้าเป็น decision)
→ /writer hook=<top pick> (ถ้าเป็น content)
→ /new-formula <top pick> (ถ้าเป็นสูตรปุ๋ย)
→ /new-recipe <top pick>  (ถ้าเป็นสูตรอาหาร)
```

## Output format (saved file)

```markdown
---
type: brainstorm
topic: <topic>
output_mode: <mode>
date: YYYY-MM-DD
top_3: [idea1, idea2, idea3]
---

# Brainstorm: <topic>

## All ideas (unfiltered)

1. ...
2. ...
3. ...
[continue to 15+]

## Connections spotted
- [idea X] + [idea Y] = [something more interesting]
- [idea Z] is a sub-version of [idea W]

## Top 3 by energy
1. **[idea]** — [1-line why]
2. **[idea]** — [1-line why]
3. **[idea]** — [1-line why]
```

## Constraints

- **ห้าม evaluate ระหว่าง generate** — ทุก idea ออกมาก่อน กรองทีหลัง
- **ขั้นต่ำ 15 ไอเดีย** — ถ้าหยุดที่ 10 แปลว่าหยุดเร็วเกินไป
- **Energy filter ใช้ได้ครั้งเดียว** — เลือก top 3 แล้วหยุด ไม่ re-rank ไม่ second-guess
- **ห้าม expand ทุก idea** — แค่ 1 ประโยคต่อ idea ใน generate phase
- **ไม่ต้องสมบูรณ์แบบ** — brainstorm คือ draft ของ draft

## Anti-patterns

- ❌ "ไอเดียที่ 3 อาจจะไม่ work เพราะ..." → เขียนแล้วก็ใส่ต่อไป ห้าม self-censor
- ❌ หยุดที่ 8 ไอเดียเพราะ "พอแล้ว" → ไม่พอ ต้อง 15+
- ❌ เลือก top 3 โดยใช้ logic แทน energy → energy มาก่อน ความสมเหตุสมผลมาทีหลัง
- ❌ ทำ brainstorm แล้วไม่ save → ไอเดียที่ไม่ได้ถูก save = หายไปตลอดกาล
