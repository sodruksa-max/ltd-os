---
description: Invoke the devils_advocate agent on a specific note or decision. Use before committing to high-stakes decisions — investment thesis, content publish, architecture choices. Expensive — only for decisions that matter.
---

# /challenge

Invoke `devils_advocate` agent against the file specified by the user.

## Usage examples
- `/challenge vault/20_investment/NVDA.md` — challenge stock thesis
- `/challenge vault/30_content/2026-04-20-ai-agents-thread.md` — pre-publish red team
- `/challenge vault/40_projects/trading-bot/decisions/use-polygon-api.md` — challenge tech decision

## Steps

1. **Confirm file exists** — if not, ask user for correct path
2. **Read the target note fully** so you understand what's being challenged
2.5 **Psychopathy Emotional Reasoning Audit** — strip emotional language, test if argument survives

ก่อน invoke devils_advocate: scan target note หา language pattern ต่อไปนี้:

| Pattern | Flag | ตัวอย่าง |
|---|---|---|
| Hope ที่ไม่มี evidence | `[HOPE]` | "น่าจะดีขึ้น", "I believe it will recover" |
| Loss aversion drive decision | `[LOSS AVERSION]` | "Already down 30%, can't sell now" |
| Sunk cost in thesis | `[SUNK COST]` | "I've spent months researching this" |
| Social proof ไม่มี own analysis | `[SOCIAL PROOF]` | "Everyone is bullish on X" |
| Narrative attachment (รัก story มากกว่า data) | `[NARRATIVE]` | Logic ignores contradicting numbers |

**Emotional strip test:**
ลบ emotional language ออกทั้งหมด — เหลือแต่ metrics, data, conditions ที่วัดได้
แล้วถาม: argument ยังแข็งแกร่งไหม?
- ถ้า **ยังแข็งแกร่ง** → emotion เป็นแค่ style ไม่กระทบ core
- ถ้า **อ่อนลงมาก** → argument depends on emotional framing → flag ให้ devils_advocate focus ตรงนี้

แจ้งผล audit ก่อน proceed:
```
Psychopathy audit: [N] patterns found
- [FLAG] "<excerpt>" — impact: core / style only
Strip test: argument [holds / weakens significantly after stripping]
```

3. **Warn on cost** if this is the user's first `/challenge` today:
   ```
   Heads up: /challenge uses devils_advocate which runs 5+ web searches + deep vault scan.
   Proceed? (yes/no)
   ```
   Skip the warning if user has already used /challenge today (check recent git log or vault/90_archive/challenges/log.md).
4. **Invoke devils_advocate** with the file path
5. **Save output** to `<same-folder>/<original-basename>-challenge.md`
6. **Append log entry** to `vault/90_archive/challenges/log.md`:
   ```
   - YYYY-MM-DD <original-path> → severity: <level>
   ```
7. **Tell user** the summary verdict (severity + recommendation) and where full challenge is saved.

## Constraints

- **Do NOT auto-revise the original** — user decides what to do with the challenge
- **Do NOT combine with publish/commit** — challenge is informational only
- If user disagrees with the challenge: that's fine, the point is to make them think, not to override them
