---
role: skeptic
council_topic: Recipe + Fertilizer Workflow Design
date: 2026-05-17
---

# Skeptic Proposal: One Domain First, No New Slash Commands Yet

## Core idea (1 sentence)

Build the fertilizer tracking system manually in markdown for one full growth cycle before building any slash commands — the recipe system should not be built at all until the fertilizer system proves the pattern works.

## Workflow (step by step)

**Phase 0 — Before any system work (right now):**
1. Decide which domain to start. Not both. Pick one. The rest waits.
2. If fertilizer: confirm you have actual palm trees to test on and a baseline (current cost/yield numbers). Without a baseline, there is no way to know if a formula change helped or hurt.
3. If recipes: confirm you have at least 5 recipes you want to develop — not "might be interesting," actually cooking regularly now.

**Phase 1 — Fertilizer only (months 1-6), all manual:**
1. Create one file: `vault/50_formulas/fertilizer/palm-v0.1.md` using a fixed template.
2. Apply the formula. Record date, plot/tree ID, quantities, cost, weather condition.
3. Three months later: record observable results (leaf color, new frond count, bunch weight if measurable).
4. Create `palm-v0.2.md` only if results justify a change. If no change needed, do NOT create a new version — "no change" is information too.
5. After 2 complete cycles: only then assess whether a slash command would save real time.

**Phase 2 — Recipes (only after fertilizer system is stable, not before):**
1. Start with one recipe folder: `vault/50_formulas/recipes/`.
2. Use the same template pattern as fertilizer but with a taste-score field instead of yield-measure.
3. Test, cook, record — all manual, no commands.

**Phase 3 — Slash commands (only if Phase 1+2 prove demand):**
Only build `/new-formula` or `/new-recipe` if you have run the manual process 10+ times and felt friction from lack of automation. Friction = the signal. Build-first is not.

## Folder structure

```
vault/
  50_formulas/
    fertilizer/
      palm-v0.1.md        ← first formula + test record
      palm-v0.2.md        ← only if formula changes
      _research/          ← paper summaries, not the papers
    recipes/              ← create only after fertilizer phase is stable
      [dish-name]-v0.1.md
```

Formula template (same for both domains, different measurement fields):

```
---
domain: fertilizer | recipe
version: v0.X
status: draft | testing | stable | retired
created: YYYY-MM-DD
---

## Formula
[ingredients + ratios]

## Rationale
[why this — cite research note, not full paper]

## Test log
| Date | Plot/Batch | Change from last | Observation | Score/Measure |

## Kill condition
[what result would make me retire this version]

## Research basis
[[vault/50_formulas/fertilizer/_research/paper-name]]
```

## Slash commands proposed

**None yet.** The existing `/paper-survey` already handles research intake. The existing researcher + writer agents already handle drafting. A new slash command adds maintenance burden to CLAUDE.md before the workflow has been validated manually even once. Revisit after 2 completed test cycles.

## Research integration

Use `/paper-survey` for initial literature search. Output goes to `vault/50_formulas/fertilizer/_research/` as a 1-page summary per paper. The formula file cites the note, not the paper.

**Order of operations: formula hypothesis first, then research to confirm or challenge it.** Research-first leads to analysis paralysis and no formula ever gets tested.

Hard rule: formula must be drafted before the third research note is created.

## Iteration / version control

Git is already the version control. The only rule: **do not edit a version file after it has been applied to real trees.** If you want to change something, create a new version file. The old file stays untouched — it is evidence.

Version promotion gate (fertilizer only): v0.X → v0.X+1 requires one full observation cycle recorded + at least one measurable data point (cost delta or yield proxy). Never advance version based on "it looks okay" after 2 weeks — palm responds at 3-6 months minimum.

## Failure modes this prevents

**Failure 1 — Wrong formula applied at scale:** The version-lock-after-apply rule prevents retroactively editing test records. Git history is the audit trail.

**Failure 2 — System abandoned after 2 weeks (highest probability):** Every slash command, folder, and template added before the first real use increases abandonment threshold. Manual-first means usable on day 1 with zero setup. Complexity is earned by usage, not pre-built in anticipation.

**Failure 3 — Two domains cannibalize attention:** User already has 2 active unfinished projects (trading bot pending, LTD-OS iteration ongoing). Adding 2 new domains simultaneously = 4 active fronts. Sequencing (fertilizer first, recipes only after) is the only path where at least one domain gets a complete first cycle.

**Failure 4 — Research becomes the work instead of testing:** Paper-surveying is intellectually satisfying and produces vault files. It is not the same as applying a formula and measuring results.

---

## Pre-mortem: how this fails

1. **(60% probability):** User builds the folder, drafts palm-v0.1.md, applies the formula — then does not record the 3-month observation because life moved on. Mitigation: calendar reminder at application date +90 days. Nothing else works.

2. **(25% probability):** User starts both domains in month 1. Recipe system gets attention (fast feedback = dopamine), fertilizer tracking gets neglected exactly when it matters most (slow feedback = boring).

3. **(15% probability):** Research phase expands into 3+ `/paper-survey` runs with 0 formulas applied yet. Classic pre-action preparation loop.

## Hidden costs

**Baseline cost:** If you do not measure palm yield NOW (before any formula change), every observation after the first formula is meaningless. Baseline measurement must happen before any other step — and it requires physically going to the trees, counting, weighing, recording.

**Emotional cost of slow feedback:** Waiting 3-6 months to see if your formula worked, with real money at stake, is harder psychologically than system design suggests. Ambiguous results (was it the formula or the drought?) create doubt spirals.

**Survivorship bias:** Organic fertilizer success stories come from commercial stations with controlled plots, 10+ years of baseline data, and lab soil analysis. For palm specifically, literature suggests 6-18 months to see clear response to fertilizer regime changes. Most individual experimenters quit before seeing a real signal.

## Conservative alternative

Start with recipes only (zero financial risk, fast feedback). Track 10 recipes over 4 weeks. If you feel genuine value from the tracking, extend the same pattern to fertilizer. If you stop at 2 recipes, you have answered an important question cheaply.

## Stop conditions (define before starting)

Fertilizer: If by month 3 there is no observation data for the first application → retire the system. If soil test reveals confounding variable → pause until soil data is baseline-stable.

Recipe: If after 6 recipes you are not referencing old notes before cooking → tracking is not adding value, stop. If template takes more than 3 minutes to fill → simplify before continuing.
