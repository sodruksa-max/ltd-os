---
role: pragmatist
council_topic: Recipe + Fertilizer Workflow Design
date: 2026-05-17
---

# Pragmatist Proposal: One Spine, Two Speeds

## Core idea (1 sentence)

Use a single shared folder spine and one minimal set of templates for both domains, but enforce different iteration gates — food recipes can advance on same-day taste judgment, fertilizer can only advance after a documented minimum 8-week hold and at least 3 field observations.

## Workflow (step by step)

**Step 0 — Research intake (shared)**
New paper, article, or link lands in `vault/00_inbox/`. User tells Claude: "summarize this for recipe context" or "summarize this for fertilizer context." Researcher agent extracts key claims and saves to `vault/10_research/recipes/` or `vault/10_research/fertilizer/`. Research lives here, never directly inside formula files.

**Step 1 — Formula creation**
User says "start a new recipe — [dish name]" or "start a new fertilizer formula — [palm oil, cost-reduction goal]." Claude creates formula file using standard template: hypothesis, inputs with quantities, method, expected outcome, linked research refs, status: `draft`.

**Step 2 — Trial logging**

Food (fast loop, days): after cooking, user dictates 3 things — what changed from last time, what tasted different, what to adjust next. Claude appends to a `## Trial Log` section inside the same version file. 2-minute friction maximum or it will not happen.

Fertilizer (slow loop, weeks-months): after application, user logs date, area, quantity, method, weather. Intermediate observation at 4 weeks: leaf color, frond development, visible stress. **Hard gate at 8 weeks minimum before any formula change is permitted.** If user tries to create v2 before 8 weeks, Claude blocks: "v1 applied [X] days ago, minimum hold is 56 days, you have [N] observations logged, need 3 minimum."

**Step 3 — Version gate**

Food: user says "lock this version." Claude stamps `status: approved-baseline`, archives trial log into v1.md as final record, scaffolds v2.md starting from v1 parameters.

Fertilizer: user says "approve v1." Claude checks: (a) at least 56 days since application logged, (b) at least 3 observation entries, (c) at least one intermediate growth/leaf note. Any missing → blocked, Claude lists exactly what is missing.

**Step 4 — Knowledge extraction**
After approval, Claude extracts 2-3 insight atoms to `vault/Knowledge/insight-atoms/` with tag `domain:recipe` or `domain:fertilizer`. Indie-style extraction runs after approval only — keeping the trial loop fast.

## Folder structure

```
vault/
  10_research/
    recipes/         ← paper/article summaries
    fertilizer/      ← soil science, nutrient ratio notes
  50_formulas/
    recipes/
      [dish-slug]/
        v1.md        ← formula + trial log + status
        v2.md        ← branched after v1 approved
    fertilizer/
      palm-oil/
        v1.md
        v2.md
```

One new top-level folder. Git handles version diffs through normal safe-commit. No additional changelog file needed.

## Slash commands proposed

**Zero new slash commands for the first 4 weeks.** Use prose instructions to Claude for every step.

After 4 weeks and at least 5 real cycles, assess actual friction and propose at most 2 commands:
- `/new-formula [recipe|fertilizer] [name]` — scaffolds template, auto-links relevant inbox research
- `/formula-check [path]` — runs the version gate checklist (elapsed days, observation count, current status)

Do not build these before manual workflow has generated real data about where friction actually lives.

## Research integration

Research comes in **before** formula creation AND **after** formula failure — not one or the other.

Before creation: `/paper-survey` on specific topic produces 1-page synthesis. User pulls 2-3 testable hypotheses into formula hypothesis field.

After failed/unclear trial: user flags `## Why It Failed (hypothesis)` and asks for targeted research. More token-efficient than front-loading all research — you cannot know which mechanism matters until you see the failure.

Research is never merged into formula files. It stays in `10_research/` and gets cited by link. Formula notes stay lean; trial log is the single source of truth.

## Iteration / version control

Status vocabulary (same across both domains):
- `draft` — created, not yet tested
- `active-trial` — being tested now, do not branch
- `approved-baseline` — stable, safe to use at real scale
- `superseded` — replaced by newer version, kept for reference
- `failed` — documented failure with reason, do not reuse without major rethink

The `approved-baseline` status for fertilizer is the only one with real financial stakes. The 8-week gate before reaching it is not bureaucracy — it is the minimum data required to distinguish signal from noise on a slow biological system.

## Why this is the realistic bet

**Shared spine, domain-adjusted gates.** Two separate systems for one user doubles maintenance surface. The domains share 80% structure — hypothesis, inputs, method, observation, version. The 20% difference (iteration speed) is handled by the hold gate, not by separate architectures. One solo user maintaining two parallel systems abandons one within 6 weeks.

**Manual-first, then commands.** Trading-foundations precedent: journal before bots, iteration before automation. Building commands before habit exists = infrastructure cost against unvalidated workflow.

**The 8-week fertilizer gate is the system's most important control.** Published palm oil fertilizer trials show meaningful yield response takes 8-16 months; leaf tissue signal detectable at 3 months earliest. Without a hard minimum hold, user will change formula every 3-4 weeks based on "trees look the same" — accumulating zero valid observations while spending real input budget on confounded experiments.

**Median outcome:** 3-5 recipe iterations in the first month (fast enough to establish habit). One fertilizer cycle logged properly in the same period. By week 8, enough empirical grounding to know what slash commands are worth building. Complexity scales with proven need, not anticipated need.

## Open questions that would change this recommendation

- How many palm trees available for trial? Fewer than 20 → minimum hold should extend to 12 weeks, not 8.
- Is there existing fertilizer application history at the farm? If yes, that becomes v0 — the incumbent formula is the baseline from day one.
- Are recipes dishes you already cook regularly, or new from scratch? If former, v1 is documentation of current practice — first entry costs no testing effort.
- Current fertilizer cost per tree per cycle? Knowing the cost baseline determines how much savings is needed to make iteration overhead worthwhile.

## Sources

- Oil palm organic fertilizer transition study, PMC 2016-2022 smallholder data (Indonesia)
- Cambridge Experimental Agriculture: oil palm smallholder management practices, Krabi Thailand
