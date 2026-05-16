---
role: optimist
council_topic: Recipe + Fertilizer Workflow Design
date: 2026-05-17
---

# Optimist Proposal: One Pipeline, Two Speeds

## Core idea (1 sentence)

Build a single "formula lab" pipeline inside LTD-OS where research flows in first, formulas version-control themselves like code, and the system compounds knowledge across both food and fertilizer — because the underlying science loop is identical even if the test cycles differ by orders of magnitude.

## Workflow (step by step)

**Phase 0 — Research intake (shared, runs before any new formula)**

1. User finds a paper, article, video, or source about flavor chemistry, soil science, NPK ratios, fermentation, etc.
2. Run `/paper-survey <topic>` — researcher agent finds papers, summarizes, tags by domain (`food` or `fertilizer`) and mechanism (e.g., `nitrogen-fixation`, `maillard-reaction`, `NPK-ratio`, `organic-carbon`).
3. Researcher saves atomic insight cards to `vault/Knowledge/insight-atoms/` with tags `domain:food` or `domain:fertilizer`. These feed the same KB that powers Nick and trading theses — no new infrastructure.
4. Long PDFs (> 30 pages): NotebookLM first, paste summary back via `/import-notebooklm`. File lands in `vault/10_research/formulas/`.

**Phase 1 — Formula creation**

5. User says: "สร้างสูตรปุ๋ย palm v1" or "สร้างสูตรผัดกะเพรา v1".
6. Executor creates formula file from template: `vault/50_formulas/<domain>/<slug>/v1.md`. Contains: ingredients + ratios, hypothesis (why this combination), source citations linking to insight-atoms, intended outcome metric (taste score / leaf color / bunch weight).
7. Researcher cross-checks insight-atoms KB for contradictions or prior iterations before committing v1.

**Phase 2 — Testing and observation logging**

8. After each test, user says "log ผลสูตร <name> v<N>". Claude prompts 3 questions: result, problems, proposed change for next version.
9. Log appends to `vault/50_formulas/<domain>/<slug>/log.md` with ISO date + result + sensory or measured data. For fertilizer: plot location, palm ID, date applied, photo filename.
10. Photos go to `vault/_assets/formulas/<slug>/YYYY-MM-DD.jpg`.

**Phase 3 — Version advance (speed-gated by domain)**

11. Food: user self-approves after any test. "อร่อย, advance to v2" → executor copies v1.md to v2.md, carries forward what worked, marks what changed, links back. Safe-commit creates immutable record.
12. Fertilizer: Claude blocks advance until 60 days from last application log entry. At day 60, Claude prompts user for observation and approval. Hard minimum — not negotiable because one-variable-per-season is the only way to read signal from a slow system.
13. Every version advance = one git commit. If a palm formula causes yield problems at v3, user can diff v2 and v3 to find what changed.

**Phase 4 — Production declaration**

14. User runs `/formula-ready <name>`. Claude checks: (a) minimum 3 test iterations logged, (b) at least 1 research source cited, (c) no unresolved contradictions in log. Pass → `status: production`. Fail → Claude lists exactly what's missing.
15. Production formulas indexed in `vault/50_formulas/INDEX.md` — one line each: name | domain | current version | status | date declared.

## Folder structure

```
vault/
  50_formulas/
    INDEX.md                        — master list of all formulas
    food/
      pad-krapao/
        v1.md                       — hypothesis, ingredients, sources
        v2.md                       — incremental change, links v1
        log.md                      — all test sessions, chronological
    fertilizer/
      palm-organic-base/
        v1.md
        log.md
  10_research/
    formulas/                       — NotebookLM imports, paper summaries
  Knowledge/
    insight-atoms/                  — existing; add domain:food, domain:fertilizer tags
  _assets/
    formulas/                       — photos, dated
```

## Slash commands proposed

Start with zero new commands — first 2 weeks everything is manual. Commands built only after manual workflow proves stable.

After 2 weeks, build two:
- `/formula-log <name> <version>` — prompts 3 questions, appends to log.md, safe-commit
- `/formula-ready <name>` — runs readiness checklist, sets status, updates INDEX.md, safe-commit

`/paper-survey` already handles research intake for both domains without modification.

## Research integration

Research flows in **before** formula creation, not just after failure.

- Before v1: `/paper-survey` seeds the hypothesis. The v1.md template has a required `sources:` field — reviewer warns if empty, light friction without a hard block.
- Between versions: if a test produces unexpected results, researcher queries insight-atoms with the relevant mechanism tag.
- Cross-domain serendipity: organic chemistry atoms tagged `domain:fertilizer` may surface patterns relevant to fermentation in food. Microbial decomposition in compost and lacto-fermentation share biochemical mechanisms. A shared KB with mechanism tags makes this discoverable.

## Iteration / version control

| | Food | Fertilizer |
|---|---|---|
| Min test time before v-advance | None — taste is instant | 60 days minimum |
| Who approves | User self-approves any time | User approves after 60-day gate |
| Iterations before `production` | 3 minimum (days-weeks) | 3 minimum (~6 months total) |
| Log format | Date + taste notes + change hypothesis | Date + plot ID + visual obs + photo path |

Git is the version control. `safe-commit.sh` after every version advance = immutable checkpoint.

## Why this wins long-term

**Compounding knowledge, not compounding effort.** The insight-atoms KB grows with every `/paper-survey`. By formula 10, the researcher agent has a dense local KB to cross-reference. Formula 11 benefits from formulas 1-10. Without this, each new formula starts from zero.

**The 60-day fertilizer gate is a feature.** The hardest failure mode in agricultural iteration is acting on insufficient signal. Changing two variables per season makes data unreadable. A mandatory gate enforces one-variable discipline so user doesn't rely on willpower alone.

**Zero infrastructure debt.** No new platform, no new tool, no new agent. `vault/50_formulas/` is one new folder. Two lightweight slash commands, built only after manual workflow proves useful. The existing pipeline handles everything else.

**Realistic 12-month upside:** 2-3 validated palm formulas at `status: production`, each with full iteration history and science citations. 5-8 food formulas at production. A `/paper-survey` habit established. The reinvention problem solved — user never starts from zero again.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| User skips research, creates formula from intuition | `sources:` field required in v1.md; reviewer warns if empty at commit |
| 60-day fertilizer gate bypassed | Gate is a checklist prompt, not code lock — relies on habit; food workflow first builds discipline |
| Both domains started simultaneously → overload | Launch food only for first 2 weeks; fertilizer enters only after food feels natural |
| Food and fertilizer insight-atoms pollute each other | `domain:` tags make filtering clean — same pattern as trading theses |
| Fertilizer causes real yield loss | Version control means failure is documented, not hidden; loss becomes the most valuable data |
