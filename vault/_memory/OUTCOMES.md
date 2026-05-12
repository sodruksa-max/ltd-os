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

## 2026-05-11 — Command iteration freeze หลัง /pre-market v5

**Decision**: freeze /pre-market command 1-2 สัปดาห์หลัง v5 เพื่อ validate ก่อน iterate — ไม่แตะ command จนถึง /weekly-learnings ~4 พ.ค.
**Reasoning at the time**: บ่ออยากแก้ command ทุกวัน — validate ใน real use ก่อน ไม่งั้นไม่รู้ว่า v5 ดีจริงหรือแค่ดูดีในหัว
**Alternatives considered**: iterate ทันที (rejected: ไม่มี signal จาก real use); freeze ยาวกว่า 2 สัปดาห์ (rejected: overkill)
**Outcome (after 2 weeks)**: ✅ worked
**What I learned**:
  - freeze ช่วยให้ focus ไปที่ Nick system ได้เต็มที่โดยไม่กระจัดกระจาย
  - /pre-market ไม่ได้ใช้ตลอดสัปดาห์ WN19 — market focus เบาลง ทำให้ freeze ไม่รู้สึก painful เลย
  - 2 สัปดาห์เหมาะกับ command ที่ใช้ 3-4 ครั้ง/สัปดาห์ ถ้าใช้ทุกวันอาจต้องสั้นกว่า
**Would recommend to future-me / other AI**: yes — ทุกครั้งที่ ship command ใหม่ ให้ freeze 5-10 real uses ก่อน iterate
**Tags**: #process #workflow #pre-market #command-design

---

## Trading Calibration Log

*One-line per trading day — appended by /post-market*

2026-04-28 — Predicted: Base (medium), Actual: Bearish (-0.49%), Match: Partial, Calibration: over-confident, Top lesson: ลด confidence เป็น low เมื่อ event risk ≥ 2 ตัวพร้อมกัน (FOMC + Mag7 earnings + Iran)
2026-04-29 — Predicted: Base (low), Actual: Base (-0.04%), Match: Yes, Calibration: well-calibrated, Top lesson: Earnings beat ≠ stock up — AMZN +70% EPS beat → AH -3% เพราะ AI capex $200B overhang; เพิ่ม "what's priced in" check ใน QQQ setup
2026-04-30 — Predicted: Base (low), Actual: Bullish (+1.02%), Match: No, Calibration: wrong direction (appropriate uncertainty), Top lesson: PCE 4.5% triggered QQQ invalidation rule แต่ตลาดขึ้น +1% — month-end window dressing + AAPL beat override macro; revisit PCE hard invalidation criterion
[weekly-calibration 2026-05-02] 3 reviews analyzed — proposals: 3 approved, 0 skipped — top pattern: EPS beat ≠ stock up (Apr 28 UPS + Apr 29 Mag7); confidence threshold tightened (2+ events → cap low)

2026-05-04 — Predicted: Base (medium), Actual: Bearish (-0.41%), Match: No, Calibration: over-confident, Top lesson: Binary geopolitical events (Iran peace→missiles) = cap confidence Low; add 10Y yield rate-of-change tracker to brief
2026-05-05 — Predicted: Base (low), Actual: Bullish (SPY +0.78%), Match: No, Calibration: direction wrong / confidence appropriate (BS 0.09), Top lesson: Oil -3.90% crash = unlock XLK risk-on; Polymarket 84% crowd can be 180° wrong — extreme odds = potential contrarian signal
[weekly-calibration 2026-05-11] 5 reviews analyzed (2026-04-28 ถึง 2026-05-05) — proposals: 4 approved, 0 skipped — top pattern: geopolitical binary event = over-confidence trap (2/5 reviews)

2026-05-11 — Predicted: Base (medium), Actual: Base (SPY +0.23%), Match: Yes, Calibration: well-calibrated, BS: 0.25, Top lesson: XLE +2.68% ใน Base — WTI > $95 sustained = XLE ขึ้นตาม oil; ASTS miss 223% on EPS > expected magnitude; pre-market TLT +0.49% ≠ EOD

## Weekly Market Log

*One-line per week — appended by /weekly-market*

2026-W18 — Regime: Risk-On (Mild), S&P ~+1.07% (Mon-Fri, 7,173→7,250), Best sector: XLE (+3.19% — Iran geopolitical premium), Worst: XLK [unverified], Key event: FOMC 4 dissenting votes + Trump Iran naval blockade + Mag7 sell-the-news; April best month since 2020

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
