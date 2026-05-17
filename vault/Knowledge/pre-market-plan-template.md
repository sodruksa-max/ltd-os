---
type: plan-template
updated: 2026-05-18
source: arXiv:2506.14852 (Agentic Plan Caching — NeurIPS 2025)
purpose: skeleton plan สำหรับ /pre-market — load ต้น session แทน re-plan ทุกรอบ; fill {{slots}} ด้วย data จริง
---

# Pre-Market Plan Template

*Load ไฟล์นี้ที่ Step 0.1 พร้อมกับ pre-market-behaviors.md — ใช้ template นี้เป็น execution skeleton*

---

## Execution Order (คงที่ทุกวัน)

```
STATIC LOAD (ก่อนเสมอ):
  [1] TRADING_RULES.md        → rules + thresholds
  [2] pre-market-behaviors.md  → behavior codes A1-D3
  [3] pre-market-plan-template.md → this file (execution skeleton)
  [4] pre-market-reasoning-skills.md → reasoning shortcuts

DYNAMIC FETCH (หลัง static เสมอ):
  [5] date + weekday bash
  [6] yesterday review (optional)
  [7] scripts: macro + news + sr-levels + universe + sector + catalyst + etf (parallel)
  [8] web searches: news + polymarket + earnings (ถ้า news-snapshot ล้มเหลว)

ANALYSIS (ใช้ static + dynamic ที่โหลดแล้ว):
  [9]  Layer A (pre-data instinct): A1·MISOPHONIA → A2·TOURETTE → A3·SYNESTHESIA → A4·HSP
  [10] Layer B (data-parallel): B1·APHANTASIA → B2·PTSD → B3·AURA
  [11] Write brief sections: Futures → Macro → Conflicts → Catalyst → Sector → ETF → S/R
  [12] Layer C (scenario qual): C1·TACHYPSYCHIA → C2·DR → C3·SPLIT-BRAIN → C4·SATIATION → C5·AIWS → C6·PARANOID → C7·TLE
  [13] Write scenario playbook + setups
  [14] Layer D (per setup): D1·DOPAMINE → D2·GAD → D3·SA
  [15] Save brief + ask decision tree

OUTPUT FORMAT (คงที่):
  File: vault/20_investment/_journal/{{DATE}}-premarket.md
```

---

## Slot Map

| Slot | Source | Static/Dynamic |
|---|---|---|
| `{{DATE}}` | bash `date` | dynamic |
| `{{WEEKDAY_TH}}` | bash `date` | dynamic |
| `{{TRADING_RULES}}` | vault/_memory/TRADING_RULES.md | static |
| `{{BEHAVIORS}}` | vault/Knowledge/pre-market-behaviors.md | static |
| `{{REASONING_SKILLS}}` | vault/Knowledge/pre-market-reasoning-skills.md | static |
| `{{MACRO_SCRIPT}}` | macro-snapshot.py output | dynamic |
| `{{NEWS_SCRIPT}}` | news-snapshot.py output | dynamic |
| `{{SR_LEVELS}}` | sr-levels.py output | dynamic |
| `{{UNIVERSE}}` | universe-screen.py output | dynamic |
| `{{SECTOR}}` | sector-flow.py output | dynamic |
| `{{CATALYST}}` | catalyst-calendar.py output | dynamic |
| `{{ETF}}` | etf-discovery.py output | dynamic |
| `{{WEB_NEWS}}` | web search result | dynamic |
| `{{POLYMARKET}}` | web search result | dynamic |

---

## Layer Output Targets (ลด verbose — compressed output per layer)

| Layer | Max output ถ้าไม่ triggered | Output ถ้า triggered |
|---|---|---|
| A1·MISOPHONIA | `A1: clear ✅` | `[MISOPHONIA: MARKET TRIGGER] <name> — escalate` |
| A2·TOURETTE | `A2: clean ✅` | `[REFLEX] <signal>` × N bullets |
| A3·SYNESTHESIA | `[GESTALT] T:X | TX:X | W:X | P:X | Wt:X` | same |
| A4·HSP | `A4: clear ✅` | `[HSP: <type>] — Implication: <1 line>` |
| B1·APHANTASIA | `B1: no visual labels ✅` | `[APHANTASIA: VISUAL LABEL] <label> → <criteria>` |
| B2·PTSD | `B2: clear ✅` | `[PTSD: AMBIENT THREAT] <channel> — <signal>` × N |
| B3·AURA | `B3: no signals ✅` | `[AURA: EARLY SIGNAL] <signal> — watch: X weeks` |
| C1·TACHYPSYCHIA | `C1: clear ✅` | `[TACHYPSYCHIA: SLOW DOWN] Level X — no entry until HH:MM` |
| C2·DR | `C2: clean ✅` | `[DR: UPSIDE ANCHORED] <item>` |
| C3·SPLIT-BRAIN | `C3: aligned ✅` | `[SPLIT-BRAIN: CONFLICT] — reconcile: <1 line>` |
| C4·SATIATION | `C4: fresh ✅` | `[SATIATION: NUMBNESS] "<narrative>" → AURA weight ×1.5` |
| C5·AIWS | `C5: proportional ✅` | `[AIWS: OVER/UNDER-REACTION] <event> — signal: <trade implication>` |
| C6·PARANOID | `C6: clear ✅` | `[PARANOID: ADVERSARIAL ACTOR / CONSENSUS TRAP]` |
| C7·TLE | `C7: no match ✅` | `[TLE: PATTERN MATCH] similar to <date> — prior: <outcome>` |
| D1·DOPAMINE | `D1: NORMAL ✅` | `[DOPAMINE: ELEVATED] — size -50%` |
| D2·GAD | table 3 rows mandatory | table 3 rows mandatory |
| D3·SA | `D3: proportional ✅` | `[SA: OVERREACTION] — mean-revert opportunity` |
