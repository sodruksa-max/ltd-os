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

Read `vault/_memory/PREFERENCES.md`, `DECISIONS.md`, `OUTCOMES.md`, user-provided context.

Write `brief.md` (context, goal, constraints, stakes, open questions).

Show user: "Brief done. Auto-picked expertise lens: <X>. Starting parallel proposals..."

## Phase 2: Proposals (5 parallel)

Invoke 5 mindset proposers IN PARALLEL with same brief:
- `optimist`
- `pragmatist`
- `skeptic`
- `caveman`
- `hypomania`

Each writes `proposal-<role>.md` independently. Don't share between agents.

After all 5 done → 1-line summary of each.

## Phase 3: Cross-critique (1 turn)

Generate 20 critiques (each proposer critiques the other 4):
- Format: steelman + weakness + question
- Save all 20 in single `critiques.md`
- Caveman critiques: keep language direct and physical — no abstract framing
- Hypomania critiques: fast, multiple observations per proposal — at least 2 angles per critique

## Phase 3.5: Expertise lens (NEW — 1 turn)

Invoke chosen expertise agent (`engineer` / `strategist` / `financial_risk`).

Reads brief + 4 proposals + 12 critiques. Writes `expertise-<lens>.md` with:
- Lens-specific evaluation per proposal
- Hidden costs/risks proposers missed
- Concrete recommendations FROM THIS LENS ONLY

This is NOT a 4th proposal — it's a reality check from one specific angle.

## Phase 4: Synthesis (synthesizer agent)

Synthesizer reads brief + 5 proposals + 20 critiques + **expertise findings**. Produces `synthesis.md`:
- Decision matrix (now includes expertise dimensions)
- Where proposers AGREE / DIVERGE
- **Caveman gut signal** — did primal brain say SAFE, UNEASY, or DANGER? Note if gut contradicts sophisticates
- **Hypomania ceiling signal** — what's the highest-upside scenario identified? Did other proposers miss it or reject it?
- Critique patterns
- Expertise warnings highlighted
- Hybrid options
- Open questions

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
