---
description: Unified quality gate — vault content checklist + code security review + PR review. Auto-triggered by PostToolUse hook when vault content files are created.
---

# /review

Unified reviewer. Three modes dispatched automatically:

| Trigger | Mode |
|---|---|
| `VAULT_REVIEW_REQUIRED` hook output | Vault content checklist |
| `/review` before commit (no arg) | Code security + QA |
| `/review <PR#>` | GitHub PR review |

---

## Dispatch logic

1. ถ้ามี `VAULT_REVIEW_REQUIRED` ใน context → **Vault mode** (อ่าน file path จาก trigger output)
2. ถ้า argument เป็นตัวเลข (PR number) → **PR mode**
3. ถ้าไม่มี argument → **Code mode** (ตรวจ staged files)
4. ถ้า argument เป็น file path → **Vault mode** (ใช้ path นั้น)

---

## Vault Mode

### Step 1 — Identify content type

อ่านไฟล์ → detect type จาก path:

| Path pattern | Type |
|---|---|
| `*/_journal/*-review.md` | post-market-review |
| `*/10_research/*.md` | research-doc |
| `*/20_investment/*.md` (ไม่อยู่ใน `_journal/`, `nick/`, `_templates/`) | stock-research |
| `*/30_content/ideas/*.md` | idea-card |
| `*/30_content/*.md` (ไม่ใช่ ideas/) | content-draft |
| อื่นๆ | generic-vault-note |

### Step 2 — Run checklist

ตรวจทีละ item ใน checklist → mark ✅ หรือ ❌

### Step 3 — Fix immediately

ทุก ❌ ที่แก้ได้จาก context → แก้ทันที ไม่รอให้ user ถาม
ถ้าแก้ไม่ได้ (ต้องการข้อมูลภายนอก) → mark `[needs-user-action: <สิ่งที่ต้องการ>]`

### Step 4 — Final verdict

เมื่อทุก item ✅ หรือ `[needs-user-action]` → พิมพ์:
```
Review passed. File: <path>
Items fixed: X | Needs user action: Y

Commit when ready:
  bash scripts/safe-commit.sh "notes: <description>"
```

(ใช้ `vault:` แทน `notes:` ถ้าเป็น KB sync เท่านั้น เช่น stock-content, insight-atoms batch; ใช้ `memory: ... (approved YYYY-MM-DD)` สำหรับ _memory/ files)

---

## Checklists

### §A — Post-Market Review

**Structure (Full mode — มี premarket):**
- [ ] `## Most Likely Scenario verdict` — Predicted + Actual + Match + เหตุผล
- [ ] `## Calibration Score` — Direction, Confidence verdict, Brier Score (formula shown)
- [ ] Rolling 10-day BS noted (หรือ "ข้อมูลไม่พอ" ถ้า < 3 entries)
- [ ] `## Setup Outcomes` — table ครบ 3 setups, PEAD note present (แม้จะ "ข้าม")
- [ ] `## Pre-Commit Rules Triggered` — present (แม้จะ "ไม่มี rule trigger")
- [ ] `## What Was Missed (Blind Spots)` — ≥ 2 items หรือ "ไม่พบ"
- [ ] `## Council Recommendation` — present (แม้จะ "ไม่มี")
- [ ] `## Lessons for Next Brief` — ≥ 2 lessons
- [ ] `## Sentiment Proxy Accuracy` — present
- [ ] `## Market Data` — table ≥ 13 rows: SPY, QQQ, DIA, VIX, XLE, XLK, XLP, XLU, XLY, GLD, TLT, Brent, WTI

**Data quality:**
- [ ] Sources line มี URLs จริง — `[Alpaca](https://...)` ไม่ใช่แค่ `Alpaca historical bars`
- [ ] ถ้า footnote มี % จากหลาย basis → ระบุ basis ให้ชัด (vs prior close / vs open)
- [ ] ไม่มี `[unverified]` ใน Market Data table (OK ในส่วนอื่น)

**KB Sync — ตรวจด้วย grep:**
- [ ] OUTCOMES.md มี entry ของวันนี้: `grep "<date>" vault/_memory/OUTCOMES.md`
- [ ] insight-atoms file มีอยู่: `vault/Knowledge/insight-atoms/post-market-<date>.md`
  - [ ] ทุก lesson ที่ falsifiable ถูก extract เป็น atom (≥ 1)
  - [ ] ทุก atom มี tag [T#] หรือ [General]
- [ ] INDEX_insights.md มี entry ของ post-market-<date>: `grep "post-market-<date>" vault/Knowledge/INDEX_insights.md`

**Review-only mode (ไม่มี premarket):**
- [ ] `## Actual Scenario` present
- [ ] `## Key Observations` ≥ 3 items
- [ ] `## Market Data` table present
- [ ] OUTCOMES.md มี `[review-only]` tag ในวันนั้น

---

### §A-lite — Market Log (Lite Review)

ใช้เมื่อ file มี `[lite]` ใน title — checklist เบากว่า §A

- [ ] `## Actual Scenario` present — SPY %, QQQ %, VIX, TLT %
- [ ] Scenario label ถูกต้อง (Bullish / Base / Bearish ตาม SPY threshold)
- [ ] `## Catalyst` present (แม้จะ "[ไม่ได้ระบุ]")
- [ ] OUTCOMES.md มี `[lite]` entry ของวันนั้น: `grep "<date> \[lite\]" vault/_memory/OUTCOMES.md`

ไม่ต้องตรวจ: calibration score, setup outcomes, insight atoms, KB sync เพิ่มเติม

---

### §B — Research Doc (Reese)

- [ ] Central question stated ชัดเจนที่ต้น doc
- [ ] Bull case section present (≥ 2 points)
- [ ] Bear case section present (≥ 2 points)
- [ ] Kill conditions — ≥ 2 items, แต่ละอันวัดได้จริง (มี threshold เฉพาะ ไม่ใช่ vague)
- [ ] Data gaps flagged (แม้จะ "ไม่พบ")
- [ ] Source citations present (ไม่ใช่ [unverified] ทั้งหมด)
- [ ] KB sync: ถ้ามี falsifiable insight → extract ไป insight-atoms/ หรือ note ว่าทำไมไม่มี

---

### §C — Stock Research

- [ ] Frontmatter มี: ticker, date, tags
- [ ] Thesis summary (1-2 ประโยค)
- [ ] Price target พร้อม basis (ไม่ใช่ตัวเลขลอยๆ)
- [ ] Bull/bear case
- [ ] Kill conditions วัดได้ (ไม่ใช่ "ถ้าแย่ลง" แต่ต้องเป็น "ถ้า EPS ลด X% / ถ้า contract หาย")
- [ ] ไม่มีตัวเลขที่ไม่มี source (ทุกตัวเลขสำคัญต้องมี source หรือ [unverified])
- [ ] Contradiction registry check ทำแล้ว: `grep "<ticker>" vault/Knowledge/contradiction-registry.md`
- [ ] THESIS_TRACKER update ถ้า thesis ใหม่หรือเปลี่ยน

---

### §D — Idea Card (Minnie)

- [ ] Central question ชัดเจน (ไม่ใช่แค่ topic)
- [ ] Sub-questions ≥ 2
- [ ] Hook angles ≥ 2
- [ ] Blind spots noted (อย่างน้อย 1)
- [ ] Output format ระบุ (yt / substack / x / slides)

---

### §F — Content Draft (Rae output)

- [ ] Output format ระบุชัดใน filename หรือ frontmatter (yt / substack / x / slides)
- [ ] ไม่มี AI clichés — ตาม voice profile ใน PREFERENCES.md
- [ ] Disclaimer present — ไม่ใช่ investment recommendation (ถ้า content เกี่ยวกับ investment)
- [ ] ทุก factual claim traceable ไปยัง research doc หรือ vault source — ไม่มีตัวเลขลอยๆ
- [ ] Link กลับไปหา research doc: `vault/10_research/<slug>-reese-<date>.md` (ถ้ามี)
- [ ] Word count เหมาะกับ format: X thread < 2000 words, longform varies
- [ ] ไม่มี fabricated quotes หรือ invented data

---

### §G — Generic Vault Note

- [ ] Word count < 2000 (นับด้วย `wc -w`) — warn ถ้าใกล้
- [ ] ไม่เกิน 5000 words (block ถ้าเกิน ยกเว้น MOC)
- [ ] มี title หรือ frontmatter
- [ ] ไม่มี secrets / API keys ในเนื้อหา

---

## Code Mode

ตรวจ staged files ก่อน commit:

```bash
git diff --cached --name-only
```

**Security (block commit ถ้าพบ):**
- [ ] ไม่มี API key / token / password hardcoded
- [ ] ไม่มีไฟล์ `*.env`, `*secret*`, `*credential*` ใน staging
- [ ] ไม่มี SQL injection (user input → query concatenation)
- [ ] ไม่มี command injection (user input → shell exec)
- [ ] ไม่มี XSS (unsanitized input → HTML)

**Quality (warn ไม่ block):**
- [ ] ไม่มี global pip install (ต้องใช้ venv)
- [ ] ไม่มี hardcoded local path (`C:/Users/sodru/`) ใน shared code
- [ ] ไม่มี print() debug ใน production path
- [ ] ไม่มี TODO/FIXME ใน code ที่ commit เป็น complete

**Vault-specific:**
- [ ] ไม่มีไฟล์ vault > 5000 words โดยไม่มี user confirm
- [ ] OUTCOMES.md, INDEX_insights.md เปลี่ยนแบบ append ไม่ใช่ rewrite

ผ่านทั้งหมด → `Code review passed. Safe to commit.`
ไม่ผ่าน → list ปัญหา + แก้ + re-check

---

## PR Mode

```
/review <PR#>
```

```bash
gh pr view <PR#> --json title,body,files,additions,deletions,commits
```

1. ตรวจทุก changed file ผ่าน Code Mode checklist
2. อ่าน PR description — ชัดเจน? ระบุ why ไม่ใช่แค่ what?
3. Flag breaking changes
4. Verdict: `approved` / `changes-requested` + specific items

---

## Constraints

- **Fix ทันที อย่าแค่ report** — ถ้าแก้ได้จาก context ให้แก้เลย
- **ห้าม fabricate** — อย่าเติมข้อมูลที่ไม่มี ใช้ `[needs-user-action]` แทน
- **Fast** — checklist pass เท่านั้น ไม่วิเคราะห์ deep (ใช้ /challenge หรือ /council สำหรับนั้น)
- **Exit ชัดเจน** — จบเมื่อทุก item ✅ หรือ `[needs-user-action]` ห้าม loop ไม่จบ
