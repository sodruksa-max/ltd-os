---
type: memory-index
updated: by-user-and-ai
---

# WORKFLOWS.md — Reusable Patterns

**Why this file exists:**
- Workflows that you've found work well — encoded so any AI can replicate them
- Different from agent prompts (Claude-specific format) — these are LANGUAGE-AGNOSTIC patterns
- ChatGPT, Gemini, Claude, future tools — all can read + apply

## How to use

### As a user
- When you discover a workflow that works → add here
- When you start a new session in ANY AI → ask "read WORKFLOWS.md and follow patterns relevant to this task"

### As an AI
- Read this file when starting work that has an established pattern here
- DON'T deviate from a documented workflow without telling user "I'm doing X differently because Y — proceed?"
- If a pattern doesn't exist for a task type, follow user's lead and offer to ADD a new pattern after

## Format

Each workflow:

```markdown
## <Workflow name>

**When to use**: <trigger or task type>
**Steps**:
1. ...
2. ...
**Done when**: <criteria>
**Common pitfalls**: <what can go wrong>
**Last refined**: YYYY-MM-DD
```

---

## Workflows

### Stock research (single ticker)

**When to use**: User wants thesis-level research on one stock
**Steps**:
1. Search vault first: `rg "<TICKER>" vault/20_investment/` — if exists, update don't duplicate
2. Read vault context: macro notes, sector notes, related companies
3. Fetch (cap 5 sources): 10-K (latest), latest earnings call, 2-3 articles for bear case
4. Use template `vault/_templates/stock-research.md`
5. Save to `vault/20_investment/<TICKER>-YYYY-MM-DD.md`
6. Fill all sections EXCEPT "Thesis" — that's the user's call
7. Suggest `/challenge <file>` after if user plans to act on it
**Done when**: All sections filled with `❓ verify` markers on uncertain data
**Common pitfalls**: 
- Fabricating numbers when source unclear (use ❓ instead)
- Writing thesis for user (defeats the point)
- Re-researching when good vault note already exists
**Last refined**: 2026-04-25

### Content draft (any format)

**When to use**: User wants publishable content (post/thread/longform/newsletter)
**Steps**:
1. Confirm format + topic + source material + target length
2. Read `vault/_memory/PREFERENCES.md` for voice rules
3. Read 3-5 recent files in `vault/30_content/` for voice in practice
4. Read source material (research notes, vault links)
5. Apply format-specific rules from `.claude/writing-formats/` (or equivalent)
6. Draft with self-critique section at bottom
7. Save to `vault/30_content/YYYY-MM-DD-<slug>.md`
**Done when**: Draft + self-critique complete, NOT published
**Common pitfalls**: 
- AI-telltale phrases ("let's dive in", "in today's world")
- Padding to hit word count
- Voice drift from user's actual style
**Last refined**: 2026-04-25

### NotebookLM import

**When to use**: User has summary from NotebookLM to file in vault
**Steps**:
1. Ask: source type (pdf/article/video/book), source URL/title, rough topic
2. Search vault for related existing notes (`rg`-based)
3. Use template `notebooklm-import.md`
4. Save: `vault/10_research/<subfolder>/YYYY-MM-DD-<slug>.md`
5. Paste user's NotebookLM output VERBATIM in TL;DR/Key points/Quotes sections
6. Add 2-5 wikilinks to genuinely related vault notes
7. Suggest tags
8. **Do NOT re-summarize** — defeats the cost-saving purpose
**Done when**: File saved, linked, tagged. User fills "My take" later.
**Last refined**: 2026-04-25

### Daily brief generation

**When to use**: Morning, manually or via cron
**Steps**:
1. Read PROJECTS.md, last 3 daily notes, last 5 commits, inbox count, COST_LOG (if exists)
2. NO external data fetch (Phase 1)
3. Format ≤ 400 words: yesterday's open threads / today's focus / inbox status / project glance / budget / one observation
4. Append to today's daily note with `<!-- BRIEF:START -->` markers
5. Auto-commit with `notes: daily brief YYYY-MM-DD`
**Done when**: Brief saved, ≤ 400 words, no fabrication
**Common pitfalls**:
- Fake urgency ("3 critical items" when there's 1)
- Motivational fluff
- Inventing stats
**Last refined**: 2026-04-25

### Decision challenge (high-stakes)

**When to use**: User about to commit to investment thesis / publish content / lock architecture
**Steps**:
1. Read target note fully — understand thesis + claims + evidence
2. Find STRONGEST counter-argument (steelman, not strawman)
3. Search: vault notes that contradict + best web sources for opposing view
4. Verify cited data (cherry-picking check)
5. Output: counter-argument + evidence + questions to answer + severity (minor/moderate/major/fatal)
6. Save as `<original>-challenge.md` — NEVER modify original
7. Log to `vault/90_archive/challenges/log.md`
**Done when**: Severity rated, recommendation given, file saved separately
**Common pitfalls**:
- Strawmanning (artificial weakness) instead of steelmanning (best counter)
- Softening to be nice — defeats the point
- Editing the original
**Last refined**: 2026-04-25

### Inbox sort (weekly)

**When to use**: `vault/00_inbox/` has > 5 items
**Steps**:
1. List inbox items with creation date + first line preview
2. For each: ask user "where does this go?" or suggest based on content:
   - Article/paper → `10_research/articles|papers/`
   - Stock idea → `20_investment/`
   - Content idea → `30_content/`
   - Project task → `40_projects/<project>/`
   - Stale junk → `90_archive/`
3. Use `git mv` to preserve history
4. Commit batch: `chore: sort inbox (X items)`
**Done when**: Inbox count = 0 OR user says "save the rest for next week"
**Last refined**: 2026-04-25

### Weekly learnings distillation

**When to use**: End of week, daily notes + commits + content available
**Steps**:
1. Read last 7 daily notes, week's commits, new notes in research/investment/content
2. Pattern-hunt: themes / contradictions / open questions / decisions / surprises / lessons
3. Draft ≤ 500-word summary in 5 sections
4. Append to `vault/90_archive/weekly-reviews/<week>.md`
5. For each "candidate rule" → ask user to promote to DECISIONS.md or PREFERENCES.md
6. **Check OUTCOMES.md candidates**: any decisions from past weeks that now have observable outcomes? Suggest entry.
**Done when**: Saved + rules approved
**Common pitfalls**:
- Copying instead of distilling
- Inventing learnings (quiet weeks happen — say so)
**Last refined**: 2026-04-25

### Pre/Post Market daily cycle (US trading days)

**When to use**: วันที่วางแผน trade US markets (ไม่ใช่ทุกวัน)
**Steps**:
1. `07:00–08:00 TH` — `/post-market <yesterday>` อ่าน "Lessons for next brief"
2. ตัดสินใจแก้ command หรือไม่ → ดู DECISIONS.md rule: ห้ามแก้ /pre-market 1-2 สัปดาห์หลัง v5 เว้นแต่ lesson ชัดเจนจาก pattern 3+ ครั้ง
3. `/pre-market` วันใหม่ (สร้าง brief + decision tree รวมใน step เดียว)
4. ทำ Decision Confidence Check checklist ใน decision tree
5. ถ้า checkbox ติด → `/council <topic เฉพาะ>` ก่อนตลาดเปิด
6. `20:30 TH` — ตลาด US เปิด — trade ตาม pre-commit rules เท่านั้น ไม่ improvise
**Done when**: เข้า position (หรือตัดสินใจไม่เข้า) ตาม pre-commit rules ที่เขียนไว้ใน decision tree
**Common pitfalls**:
- แก้ command หลัง post-market ทุกวัน = tweaking on noise (ดู DECISIONS.md: command freeze rule)
- ข้าม Decision Confidence Check = เข้า position โดยไม่รู้ว่ามี dilemma ค้างอยู่
- Improvise ระหว่างตลาดเปิด แทนที่จะ follow pre-commit rules
- รัน /post-market แล้วข้ามไป /pre-market ทันทีโดยไม่อ่าน lessons
**Last refined**: 2026-04-28

**Command modification rules**:
- ห้ามแก้ command ทุกวัน — แก้เมื่อ pattern ซ้ำ ≥ 3 ครั้งเท่านั้น
- Encode lesson เป็น rule generalizable ไม่ใช่ fix เฉพาะกรณี
- หลังแก้ → commit + version bump (v6, v7…)

**Confidence calibration (mandatory ใน /pre-market)**:
- นับ event risks: FOMC/Powell, Mag7 earnings week, Major geopolitical unresolved, CPI/PCE/NFP, Major Fed speakers
- 0-1 events → ดุลพินิจ | 2+ events → cap low (ห้ามใช้ medium หรือ high)
- *Updated 2026-05-02: threshold เข้มขึ้นจาก "2 events → medium" → "2+ events → low" — evidence: Apr 28 over-confident ใน FOMC + Mag7 + Iran พร้อมกัน*

**Polymarket interpretation rule** *(approved 2026-05-11)*:
- Polymarket ผิดทิศทาง 4/5 reviews (Apr28: 67%Up→down, Apr29: 61%Up→flat, Apr30: 45%Up→+1%, May5: 84%Hormuz→oil-3.9%)
- ถ้า odds ≥80% ในทิศทางเดียว → ระบุ **contrarian interpretation** ด้วยใน brief ไม่ใช่แค่ consensus confirmation
- ใช้ Polymarket เป็น 1 ใน 3 เหตุผล scenario ได้ แต่ห้าม reinforce scenario ตรงๆ ถ้า odds extreme

**Presidential Action Risk** *(approved 2026-05-11)*:
- ถ้ามีเรื่อง Trump/executive action ที่ยัง active (Iran, tariff, ceasefire, blockade, sanction) → เพิ่ม row "Presidential Action Risk" ใน Risk Framework table แยกออกจาก Geopolitical
- Format: `**Presidential Action Risk:** [สรุปสถานการณ์] → trigger: [oil / USD / defense / equities] → magnitude: [ต่ำ/กลาง/สูง]`
- Evidence: Apr 29 Trump naval blockade กลางวัน oil +7%; May 4 Iran missile strike overnight → narrative พลิก 180°

**Oil crash → sector beneficiary** *(approved 2026-05-11)*:
- ถ้า WTI หรือ Brent ลง ≥3% → ระบุ XLK + QQQM/QQQ เป็น primary beneficiary ใน Bullish scenario เสมอ (double tailwind: cost pressure ลด + yield กด = growth unlocked)
- Evidence: May 5 oil -3.9% → XLK +2.2%, IWM +1.69%; Apr 30 oil pressure คลาย → AAPL + Nasdaq rally

**Trade setup discipline**:
- Forward-looking เท่านั้น — if-then ไม่ใช่ already-true
- Time-stop ทุก setup (Day = exact ET time, Swing = days)
- Profit-taking rules กำหนดก่อนเข้า — ไม่ใช่หลังกำไร
- ห้าม entry หลัง 3pm ET; lunch lull 11:30–13:30 ET = no entry
- **Earnings EPS criterion**: ทุก setup trigger ต้องระบุ GAAP หรือ adjusted ชัดเจน — ใช้ GAAP เป็น primary; ถ้า adjusted ต่างจาก GAAP ≥5% → flag divergence ใน setup ก่อน execute *(evidence: Apr 28 UPS GAAP miss vs adj beat — trigger ambiguous)*
- **QQQ/Mag7 setup trigger**: ≥3/4 Mag7 beat GAAP EPS AND ≥2/4 AH reaction เป็นบวก → full size; ถ้า AH ยังไม่มีข้อมูลหรือ AH split (<2/4 บวก) → size ครึ่งหรือรอ open วันถัดไปก่อน *(evidence: Apr 29 4/4 GAAP beat แต่ 3/4 AH ลง เพราะ AI capex overhang)*

**Pre-commit rules 5 ประเภท**:
1. Circuit breakers — ปิด position ทันที
2. Setup invalidation — thesis ตาย
3. Profit-taking — lock gains
4. Time-of-day — เวลาห้าม trade
5. Earnings/news triggers

**Source verification**:
- ทุกตัวเลขต้องมี source attribution
- Conflict ระหว่าง sources → flag ชัด, choose ด้วย methodology
- ห้าม fabricate — ใช้ `[unverified]` ถ้าหาไม่ได้
- Live data > cached > forecast model

**Weekly review**:
- `/weekly-learnings` → aggregate 5 reviews → หา pattern ที่ data แข็งพอ
- ถ้าเห็น improvement candidate → encode เข้า command
- ห้าม tweak จาก single data point

**Session continuity**:
- ก่อนปิด Claude Code session → `/handoff`
- Uncommitted files → commit หรือ revert ก่อนปิด — ห้าม orphan changes ข้ามวัน

**Claude.ai vs Claude Code roles**:
- Claude Code = workhorse (90% ของงาน)
- Claude.ai = consultant สำหรับ second opinion
- เริ่มแชท Claude.ai ใหม่ → paste handoff + relevant context (Claude.ai ไม่จำ)
- หลัง consultation → archive lessons กลับลง vault

---

## Adding a new workflow

When you discover a pattern that worked:

1. Run it 2-3 times to verify it's actually a pattern (not luck)
2. Add entry above using the format
3. Commit: `memory: add WORKFLOWS pattern for <task>`
4. Reference it in agent prompts if you want auto-application

## Removing a workflow

If a pattern stops working (tools changed, you outgrew it):

1. Don't delete — move to "## Deprecated" section at bottom
2. Add note: why it stopped working
3. Future-you / future-AI learns from the obsolescence too

---

## Deprecated

(empty)
