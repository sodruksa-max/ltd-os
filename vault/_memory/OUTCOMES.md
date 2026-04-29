---
type: memory-index
updated: by-user-and-ai
---

# OUTCOMES.md — Decision Outcomes Log

**Why this file exists:**
- Decisions in DECISIONS.md = "what I chose"
- Outcomes here = "how it actually turned out"
- AI tools (Claude / ChatGPT / Gemini / future) read this to learn YOUR patterns
- Future-you reads this to avoid repeating mistakes

**Cross-AI portability**: Plain markdown. Any LLM can ingest this and understand your reasoning.

## Format

Each entry follows this structure:

```markdown
## YYYY-MM-DD — <decision title>

**Decision**: <what you chose>
**Reasoning at the time**: <why — capture original thinking, don't sanitize later>
**Alternatives considered**: <what you almost picked instead>
**Outcome (after N weeks/months)**: ✅ worked / ⚠️ mixed / ❌ wrong
**What I learned**: <1-3 bullet points>
**Would recommend to future-me / other AI**: yes / no / with caveats
**Tags**: #tooling #investment #content #process
```

## Rules

- **Add entry when outcome is observable** (not at decision time — DECISIONS.md is for that)
- **Be honest about ❌ wrong** — sanitizing kills the learning
- **Include reasoning at the time** — easy to look smart in hindsight, hard to remember actual thinking
- **Tag liberally** — makes it findable across AI sessions
- **Keep entries short** — 100-200 words each, not essays

## Anti-patterns

- ❌ Auto-generating entries from chat logs (AI guesses outcomes wrong)
- ❌ Only logging successes (survivorship bias destroys value)
- ❌ Editing old entries to look smarter (defeats the whole point)
- ❌ Logging trivial decisions (entry should matter 6+ months later)

## When to add an entry

- After 2-4 weeks following a decision (enough time to see results)
- Triggered by `/weekly-learnings` if it surfaces an outcome
- Triggered by failure journal entry that links back to a decision
- Quarterly review: scan DECISIONS.md → which ones now have observable outcomes?

---

## Entries

(empty — entries will appear as you live with decisions long enough to see results)

---

## Trading Calibration Log

*One-line per trading day — appended by /post-market*

2026-04-28 — Predicted: Base (medium), Actual: Bearish (-0.49%), Match: Partial, Calibration: over-confident, Top lesson: ลด confidence เป็น low เมื่อ event risk ≥ 2 ตัวพร้อมกัน (FOMC + Mag7 earnings + Iran)

<!-- Example entry (delete when adding real ones):

## 2026-04-25 — Use NotebookLM for heavy summarization instead of Claude

**Decision**: Offload PDF/audio summarization to NotebookLM (free), import via /import-notebooklm
**Reasoning at the time**: Claude tokens expensive for 100-300 page docs; NotebookLM has generous free tier
**Alternatives considered**: 
  - Just use Claude (rejected: cost)
  - Browser automation NotebookLM (rejected: ToS + fragile)
  - Skip summarization, search raw PDFs (rejected: slow + huge context)
**Outcome (after 2 weeks)**: ✅ Token bill ↓60%, vault grew ~40 notes, workflow ~40s/import
**What I learned**: 
  - NotebookLM summary quality > my fear; needed ~5% manual cleanup
  - Manual copy/paste isn't a bottleneck at this volume
  - Vault-first lookup (CLAUDE.md policy) compounded the savings
**Would recommend to future-me / other AI**: yes
**Tags**: #tooling #cost-optimization #notebooklm #vault

-->
