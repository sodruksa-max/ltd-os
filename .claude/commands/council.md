---
description: Multi-agent debate workflow. 4 mindset proposers + 1 expertise lens generate independent input, cross-critique, synthesizer combines, devil's advocate challenges. Output = decision framework, NOT recommendation. Use for high-stakes decisions or project planning.
---

# /council <topic> [--expertise=<lens>]

Orchestrate 6-phase multi-agent debate with mindset proposers + expertise lens.

## Usage

```
/council <topic>
/council <topic> --expertise=engineer       (default if omitted)
/council <topic> --expertise=strategist
/council <topic> --expertise=financial_risk
```

## Expertise lens selection

If user doesn't specify, AUTO-PICK based on topic keywords:
- topic mentions "build", "code", "tool", "system" → `engineer` (default)
- topic mentions "ROI", "career", "business", "monetize", "audience" → `strategist`
- topic mentions "trading", "invest", "money", "capital", "ทุน", "เทรด" → `financial_risk`
- ambiguous → `engineer` (most generally useful)

Show user the auto-picked lens at start: "Using expertise lens: <X>. Override with --expertise=<other>."

## When to use

✅ **GOOD use:**
- "ผมจะเลือก trading strategy แบบไหน" → financial_risk lens
- "ผมจะทำ trading bot scrape news ดีไหม" → engineer lens
- "ลงทุน 30K อังเปาในอะไรดี" → financial_risk lens
- "เริ่มลง content TikTok หรือ YouTube ก่อน" → strategist lens

❌ **BAD use** (overkill):
- "Python list คืออะไร" → just ask
- "เลือก library อะไร" → too small

Cost: ~$1.50-3.50 per /council. Time: 10-16 min.

## Pre-checks

1. If user runs /council with vague topic → ASK clarification first
2. If well-formed → proceed
3. Create folder: `vault/_council/<YYYY-MM-DD>-<slug>/`

## Phase 1: Brief (1 turn)

Read `vault/_memory/PREFERENCES.md`, `DECISIONS.md`, user-provided context.

**OUTCOMES.md example selection (arXiv:2506.08607 CASE principle):** อย่าโหลด OUTCOMES.md ทั้งหมด — ดึงเฉพาะ 3 entries ที่ relevant ที่สุดต่อ topic นี้ (score by keyword similarity: domain + decision type + stakes level) แล้วใส่ใน brief เป็น "Prior decisions context"; ถ้าไม่มี entry ที่ match → ระบุ "no relevant prior decisions"

Write `brief.md` (context, goal, constraints, stakes, open questions, prior decisions context).

Show user: "Brief done. Auto-picked expertise lens: <X>. Starting parallel proposals..."

## Phase 1.5: Brief Clarity Stack (always — ก่อน spawn proposers)

### Schizophrenia — Wrong Problem Detector

> "ถ้า topic นี้เป็น symptom — root cause ที่แท้จริงคืออะไร?"

Force-generate 2 alternative framings:
- **Reframe 1:** [topic จาก angle ที่ใหญ่กว่า — ปัญหาระดับ system]
- **Reframe 2:** [topic จาก angle ที่เล็กกว่า / ลึกกว่า — root constraint ที่แท้จริง]

ถ้า alternative framing ทำให้ proposals ที่จะเกิดเปลี่ยนทิศทางอย่างมีนัย → flag `[SCHIZO: WRONG PROBLEM?]` และแสดงให้ user ก่อนดำเนินต่อ — user ยืนยัน topic เดิมหรือ reframe ก่อน spawn
ถ้าไม่ → ดำเนินต่อเงียบๆ

### Autism — Prior Council Cross-check

```bash
grep -i "<topic-keyword>" vault/_memory/COUNCIL_LOG.md | head -5
```

ถ้าพบ similar decision:
- แสดง: "เคย council เรื่องนี้เมื่อ [date] — outcome: [result]"
- ถาม: "มีอะไรที่เปลี่ยนไปจากครั้งก่อนที่ทำให้ต้อง council ใหม่?" (รอ user confirm ก่อนดำเนิน)

ถ้าไม่พบ → ดำเนินต่อเงียบๆ

## Phase 2: Proposals (5 parallel)

Invoke 5 mindset proposers IN PARALLEL with same brief:
- `optimist`
- `pragmatist`
- `skeptic`
- `caveman`
- `hypomania`

Each writes `proposal-<role>.md` independently. Don't share between agents.

**SelfBudgeter rule (arXiv:2505.11274) — ทุก proposer ต้องทำก่อน generate:**
> "This proposal will address [X core arguments] in max [N] words."
ห้ามเกิน budget ที่ declare — ถ้าเกิน = cut ทิ้ง ไม่ใช่ extend; ลด verbose output ~60% โดยไม่เสียคุณภาพ

After all 5 done → 1-line summary of each.

## Phase 2.5: Proposal Scan Stack (always — หลังรับ 5 proposals ก่อน critique)

### ADHD — Missing Angle Scan

อ่าน 5 proposals พร้อมกันเป็น gestalt (ห้าม read ทีละตัว) → ถาม:
> "มุมมองหรือ dimension อะไรที่ **ทั้ง 5 proposers ไม่มีใครพูดถึงเลย**?"

Angles ที่มักโดนข้ามโดย proposers ทุก mindset:
- Exit strategy / reversibility — ถ้าตัดสินใจแล้วผิด กลับได้ไหม?
- Opportunity cost — สิ่งที่จะ **ไม่ได้ทำ** เพราะเลือก option นี้คืออะไร?
- 3rd-party dependency — มีอะไรที่ควบคุมไม่ได้ แต่ทุก option ต้องพึ่งพา?
- Timeline asymmetry — อะไรที่ต้องทำตอนนี้ vs อะไรที่รอได้โดยไม่เสียเปรียบ?
- Regulatory / compliance — ถ้า domain มีกฎหมายเกี่ยวข้อง มีใครพูดถึงไหม?

```
[ADHD: MISSING ANGLES]
- [angle ที่ขาด 1] — ไม่มีใครพูดถึงใน 5 proposals
- [angle ที่ขาด 2] — ไม่มีใครพูดถึงใน 5 proposals
```

Synthesizer ต้องเพิ่ม missing angles เหล่านี้ใน "Open questions" section ของ synthesis.md — ห้ามข้าม
ถ้าไม่มี missing angles → `[ADHD: FULL COVERAGE] ✅`

## Phase 2.8: Proposal Compression (Trajectory Prune — arXiv:2509.23586 AgentDiet)

> **รันทันทีหลัง Phase 2.5 เสร็จ — ก่อน spawn Phase 3 critiques**

**จุดประสงค์:** หลัง 5 proposals ถูก received แล้ว raw proposal text ถือว่า "expired" — compress เป็น structured summaries ก่อนส่งต่อ ลด ~60% input token ของ Phase 3 + Phase 4

**สร้าง `proposal-summaries.md`** โดย compress แต่ละ proposal เป็น 3 บรรทัด:
```
[PROPOSER: optimist]
Core claim: <1 ประโยค — recommendation สุดท้ายคืออะไร>
Key mechanism: <1 ประโยค — ทำงานอย่างไร / ทำไมถึงจะสำเร็จ>
Fatal risk: <1 ประโยค — สิ่งที่ทำให้ proposal นี้พังได้>
```

**กฎ:**
- summaries ทั้งหมดรวมกัน < 200 words
- ห้ามใส่ supporting argument, background, หรือ nuance — 3 บรรทัดเท่านั้น
- Full proposal text = expired หลัง Phase 2.8 — ห้าม carry ไปยัง Phase 3, 3.5, หรือ 4
- Phase 3 critiquers อ่าน **full proposals** เพื่อ generate critique (ยังใช้งานอยู่) — แต่ Phase 4 synthesizer รับเฉพาะ proposal-summaries.md

```
Phase 2.8 complete: proposal-summaries.md created (<N> words, 5 proposals compressed)
Full proposal text: expired — not forwarded to Phase 4
```

## Phase 3: Cross-critique (MARS pattern — arXiv:2509.20502)

**MARS rule: reviewers work INDEPENDENTLY — ห้าม pass critique ระหว่าง agents**

Generate 20 critiques (each proposer critiques the other 4) โดยใช้ MARS pattern:
- แต่ละ proposer อ่านเฉพาะ **proposals อื่น** — ห้ามอ่าน critiques ของ agent อื่นที่กำลัง generate
- Critiques ทั้งหมด save ตรงไป `critiques.md` โดยไม่ share ระหว่าง proposers
- Synthesizer (Phase 4) เป็น meta-reviewer ที่รวม critiques ทั้งหมด — ไม่ใช่ proposers
- Format per critique: steelman + weakness + question
- Caveman critiques: direct + physical — no abstract framing
- Hypomania critiques: fast, multiple angles — at least 2 angles per proposal

**ทำไม:** MARS ลด token ~50% vs MAD โดยตัด reviewer-to-reviewer interaction ออก (context ไม่ blow up ระหว่าง critique rounds)

## Phase 3.2: Critique Compression (Trajectory Prune — arXiv:2509.23586 AgentDiet)

> **รันทันทีหลัง Phase 3 critiques ทั้ง 20 ถูก generate เสร็จ — ก่อน Phase 3.3**

**จุดประสงค์:** raw critiques (steelman + weakness + question per critique = ~60 words × 20 = ~1,200 words) → extract เฉพาะส่วนที่ synthesizer ต้องการจริงๆ — ลด ~70% input token ของ Phase 4

**สร้าง `critique-extracts.md`** โดย drop steelman preamble ทั้งหมด — เก็บเฉพาะ:
```
[proposer-A → proposal-B]
Weakness: <1 ประโยค>
Question: <1 ประโยค>
```

**กฎ:**
- ห้ามเก็บ steelman section — synthesizer ไม่ต้องการ (proposals summaries ครอบคลุมแล้ว)
- ห้ามเก็บ preamble, rationale, หรือ positive framing
- critique-extracts ทั้งหมดรวมกัน ≤ 600 words (20 critiques × 2 บรรทัด + header)
- Full critiques text = expired หลัง Phase 3.2 — ห้าม carry ไปยัง Phase 3.5 หรือ Phase 4

```
Phase 3.2 complete: critique-extracts.md created (<N> words, 20 critiques → weakness+question only)
Full critique text: expired — not forwarded to Phase 4
```

## Phase 3.3: Stability Check (arXiv:2510.12697)

> **รัน immediately หลัง Phase 3 critiques เสร็จ — ก่อน spawn expertise agent**

ตรวจว่า debate converge แล้วหรือยัง — ประหยัด token และส่ง confidence signal ไปยัง synthesizer

**Directional alignment scan:**
อ่าน 5 proposals ด้วยสายตาเร็ว — classify แต่ละ proposal:
- `FAVOR` — proposal แนะนำ direction นั้น / สนับสนุน action
- `OPPOSE` — แนะนำตรงข้าม
- `NEUTRAL/CONDITIONAL` — ขึ้นกับเงื่อนไข ยังไม่ชัดเจน

นับ: `N_favor / N_oppose / N_neutral`

**Stability verdict:**
```
[STABILITY: HIGH CONFIDENCE — EARLY CONVERGENCE] ถ้า N_favor ≥ 4 หรือ N_oppose ≥ 4
[STABILITY: MODERATE CONFIDENCE — PROCEED NORMAL] ถ้า max(N_favor, N_oppose) = 3
[STABILITY: LOW CONFIDENCE — DEBATE UNRESOLVED] ถ้า N_neutral ≥ 3 หรือ N_favor = N_oppose
```

**ส่ง verdict ไปยัง Phase 4:**
- HIGH CONFIDENCE → synthesizer note "4/5 proposers converged" + สามารถ skip recap proposals ทีละตัว (สรุปรวมได้เลย) — ประหยัด ~30% token
- LOW CONFIDENCE → synthesizer escalate ไปยัง "Hard questions to answer first"

## Phase 3.5: Expertise lens (NEW — 1 turn)

Invoke chosen expertise agent (`engineer` / `strategist` / `financial_risk`).

Reads brief + 4 proposals + 12 critiques. Writes `expertise-<lens>.md` with:
- Lens-specific evaluation per proposal
- Hidden costs/risks proposers missed
- Concrete recommendations FROM THIS LENS ONLY

This is NOT a 4th proposal — it's a reality check from one specific angle.

## Phase 4: Synthesis (synthesizer agent)

**AgentDropout filter (arXiv:2503.18891) — รันก่อน synthesis:**
Synthesizer scan critiques ทั้งหมดก่อน process — ถ้า 2 critiques overlap >80% (paraphrase กัน) → mark duplicate → process เพียง 1 ไม่ทั้งคู่; บันทึก `[DUPLICATE DROPPED] proposer-A critique on X ≈ proposer-B critique on X` ใน synthesis.md header; ลด noise + synthesizer input token

Synthesizer reads brief + **proposal-summaries.md** + **critique-extracts.md** (after dedup) + **expertise findings**. Full proposals and full critiques are expired (Trajectory Prune — Phase 2.8 + 3.2). Produces `synthesis.md`:
- Decision matrix (now includes expertise dimensions)
- Where proposers AGREE / DIVERGE
- **Caveman gut signal** — did primal brain say SAFE, UNEASY, or DANGER? Note if gut contradicts sophisticates
- **Hypomania ceiling signal** — what's the highest-upside scenario identified? Did other proposers miss it or reject it?
- Critique patterns
- Expertise warnings highlighted
- Hybrid options
- Open questions

**Confidence Score (arXiv:2604.07667 Conformal Social Choice) — synthesizer คำนวณหลังเขียน synthesis.md เสร็จ:**

| Factor | Score |
|---|---|
| Proposal alignment (Phase 3.3 stability) | HIGH=3 / MODERATE=2 / LOW=1 |
| Expert lens alignment | Confirms synthesis direction=2 / Partial=1 / Contradicts=0 |
| Devil's advocate severity (Phase 5 — ประเมิน pre-emptively ถ้ายังไม่รัน) | Mild expected=2 / Moderate expected=1 / Likely severe=0 |

**Total /7 → threshold:**
- 6-7 → `confidence: HIGH` — debate resolved, eligible for immediate decision logging
- 4-5 → `confidence: MEDIUM` — user review recommended before deciding
- 0-3 → `confidence: LOW` — open questions must be answered first

Output ใน synthesis.md และ DECISION.md frontmatter:
```yaml
confidence: HIGH / MEDIUM / LOW
confidence_score: N/7
confidence_factors: alignment=[H/M/L], expert=[C/P/X], da=[mild/mod/severe]
```

**Outcome tracking rule:**
- `confidence: HIGH` → append ใน `vault/_memory/COUNCIL_LOG.md`: `[HIGH_CONF] <date> <topic> — N/7 — track outcome 2-8wk`
- `confidence: LOW` → append: `[UNRESOLVED] <date> <topic> — open questions block decision`

## Phase 4.5: Synthesis Audit Stack (always — synthesizer รันก่อนเขียน decision matrix)

### Dyslexia — False Diversity Check

มองทั้ง 5 proposals พร้อมกันเป็น gestalt ไม่ใช่ทีละตัว:
> "proposals ไหนที่ดูเหมือนต่างกันแต่จริงๆ bet เดิม — driver เดียวกัน, risk เดียวกัน?"

ถ้าพบ pair ที่ underlying assumption overlap > 70% → flag `[FALSE DIVERSITY] proposal-A ≈ proposal-B — ทั้งคู่ bet on [driver]`
→ Synthesizer ต้อง merge เป็น 1 option ใน matrix ไม่แสดงเป็น 2 ทางเลือกปลอม — false diversity = ลวงว่ามีทางเลือกมากกว่าความจริง

### OCD — Matrix Symmetry Check

ก่อนเขียน decision matrix บังคับตรวจ:
- ทุก proposal ต้องถูกประเมินบน **dimension เดียวกันทุกข้อ** ห้ามมี cell ว่าง
- ถ้า dimension ไหนไม่มีข้อมูลสำหรับ proposal บางตัว → บังคับระบุ `[unknown — ต้องหาข้อมูล]` ไม่ใช่เว้นว่าง
- ถ้า matrix asymmetric → flag `[OCD: MATRIX GAP] proposal-X ขาด dimension Y` → แก้ก่อน finalize

### Depressive Realism — Base Rate Calibration

ก่อน synthesizer สรุป recommendation framework:
> "decisions ประเภทนี้ใน domain นี้ — historical success rate โดยทั่วไปคือเท่าไหร่?"

ตัวอย่าง calibration:
- "เปลี่ยน strategy ใหม่ทั้งหมด" → base rate success ~20-30%
- "ทำ incremental improvement บน system ปัจจุบัน" → base rate ~60-70%
- "รอก่อนแล้วค่อยตัดสินใจ" → delayed decision leading to better outcome ~40%

```
[DR: BASE RATE] decisions ประเภทนี้: success ~X% | failure mode ที่พบบ่อย: [Y]
```

Synthesizer ต้อง reference base rate นี้ใน recommendation framework — ห้าม ignore
ถ้าประเมิน base rate ไม่ได้ → `[DR: BASE RATE UNKNOWN]` — บันทึกเป็น open question

## Phase 5: Devil's advocate final

Devils_advocate challenges synthesis. Save `final-challenge.md`.

## Phase 5.5: Maladaptive Daydreaming — Alternative History Stress Test

ก่อนเขียน DECISION.md — รัน vivid alternative history simulation สำหรับ top 2 options

> "ย้อนกลับไป 18 เดือน ถ้าเลือก [Option X] วันนั้น — timeline ที่ concrete ที่สุดคืออะไร?"

ต่อแต่ละ top 2 options:
- **Month 1–3:** early signal แรกที่ proof หรือ disproof decision
- **Month 4–9:** inflection point — จุดที่รอดหรือพัง
- **Month 10–18:** outcome ที่ vivid ไม่ใช่ probability กลางๆ

บันทึก key divergence point: จุดที่ทั้ง 2 options เริ่มแยกทางกัน — นั่นคือ decision factor ที่แท้จริง

Save ใน `brief.md` section "MD Alternative History" และ reference ใน DECISION.md

## Phase 5.7: Pre-mortem Stack (always — ก่อนเขียน DECISION.md)

### GAD — Pre-mortem on Top Recommendation

สำหรับ option ที่ synthesizer rank ไว้สูงสุด (หรือ top 2 ถ้า synthesizer ไม่ rank):

> "สมมติเลือก option นี้แล้วล้มเหลวใน 12 เดือน — 3 failure paths ที่ concrete ที่สุด?"

| Path | Failure scenario | Early warning signal (ภายใน 30-60 วัน) | Decision rule เมื่อเห็น signal |
|---|---|---|---|
| 1 | [สิ่งที่ทำให้พัง] | [signal แรก] | [ทำอะไร] |
| 2 | [สิ่งที่ทำให้พัง] | [signal แรก] | [ทำอะไร] |
| 3 | [สิ่งที่ทำให้พัง] | [signal แรก] | [ทำอะไร] |

บันทึกใน DECISION.md section "Pre-mortem" — ห้ามข้าม
ถ้า synthesizer ไม่สามารถ enumerate 3 failure paths ได้ครบ → conviction ไม่พอ → downgrade recommendation เป็น "explore further" ใน DECISION.md

## Phase 6: Final document

Combine into `DECISION.md`:

```markdown
---
council_topic: <topic>
expertise_lens: <lens used>
date: YYYY-MM-DD
status: open
---

# Council Decision: <topic>

## TL;DR
<2-3 sentences: structure of decision, not the decision>

## Decision matrix
<from synthesizer — includes expertise dimensions>

## Expertise warnings
<critical findings from expertise lens>

## Caveman gut signal
<SAFE / UNEASY / DANGER — and whether gut contradicts the sophisticated proposals>

## Hypomania ceiling
<The highest-upside scenario identified — what becomes possible if the best conditions align?>

## Recommendation framework
<from synthesizer — IF dimension X matters → option Y>

## Hard questions to answer first
<from devil's advocate>

## All artifacts
- [[brief]]
- [[proposal-optimist]] / [[proposal-pragmatist]] / [[proposal-skeptic]] / [[proposal-caveman]] / [[proposal-hypomania]]
- [[critiques]]
- [[expertise-<lens>]]
- [[synthesis]]
- [[final-challenge]]

## Outcome (fill later when known)
- Date decided: 
- Choice: 
- Outcome (after N weeks): 
```

Update `vault/_memory/COUNCIL_LOG.md`.

## Output to user

```
✓ Council complete (~X tokens, $Y, Zm)
Expertise lens: <lens>

Files: vault/_council/<date>-<slug>/

Read in this order:
1. DECISION.md (start here)
2. expertise-<lens>.md (specific reality check)
3. synthesis.md (decision matrix + caveman gut + hypomania ceiling)
4. proposal-hypomania.md (ceiling check — read if proposals feel too conservative)
5. proposal-caveman.md (gut check — read if sophisticated proposals feel too abstract)
6. proposal-*.md (full proposals if curious)
7. final-challenge.md (questions YOU must answer)

The council does NOT decide for you.

When you decide → update DECISION.md frontmatter status to "decided: <choice>"
After 2-8 weeks → log outcome to OUTCOMES.md (use /weekly-learnings)
```

## Constraints

- Total token budget: 80-120K (6 phases, 5 proposers)
- Time budget: 10-16 minutes wall time
- If a proposer fails → continue with remaining, note in DECISION.md
- DO NOT skip phases
- DO NOT auto-decide for user
- DO NOT execute decision (only document it)

## Anti-patterns

- ❌ Synthesizer recommending single option
- ❌ Skipping expertise phase (loses concrete reality check)
- ❌ Council on trivial decisions
- ❌ Council that takes >15 min
- ❌ Forgetting to log outcome later

## Tips for users

- Be SPECIFIC in topic
- Council works best when you have hypothesis to test
- Outcome logging is what makes council COMPOUND in value over time
- Try different expertise lenses on same topic — different lens reveals different blind spots
