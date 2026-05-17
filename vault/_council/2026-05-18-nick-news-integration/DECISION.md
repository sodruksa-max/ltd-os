---
council_topic: nick-news-integration
expertise_lens: engineer
date: 2026-05-18
status: open
---

# Council Decision: Nick Real-Time News Integration

## TL;DR
5 proposers collapsed to 2 real options. Engineer verified Pragmatist's architecture as most sound. Devil's advocate raised the central question: are Nick's kill conditions written to receive news input? The debate cannot answer this — the user can. This document frames the decision without making it.

---

## MD Alternative History

### Option A — Ship `--nick-news` flag now (Pragmatist / Hybrid 1)
- **Month 1-3:** Flag works. Nick gets 3-5 headlines per holding per week. Kill conditions don't change — they're still written as qualitative triggers. Headlines arrive but don't map to kill condition thresholds. Nick notes positive/negative and moves on.
- **Month 4-9:** A CEO unexpectedly resigns at a holding. The headline arrives. Nick flags position "Evolving." Would have caught it via kill condition verification web search anyway. Net contribution of news feed: unclear.
- **Month 10-18:** Nick has read 500+ headlines. 490 required no action. The digest is background noise. The one material event that WAS headline-triggerable fires correctly — but was it 6 days after the event was already priced in? The feed added latency awareness but not decisional speed.

**Key divergence:** News feed adds value only when (a) kill condition is precise enough that a headline satisfies it AND (b) Nick would not have found it via kill condition verification search. Both must hold simultaneously.

### Option B — Gate on kill conditions first (Skeptic / Hybrid 2)
- **Month 1-3:** Kill condition audit runs (2-week timebox). 6 of 8 kill conditions rewritten to be metric-based and headline-triggerable. "CEO resigned" → kills. "Revenue miss > 10%" → kills. 2 structural kills (competitive moat, thesis validity) remain requiring web search — accepted.
- **Month 4-9:** News feed ships. Nick has 6 of 8 kill conditions that actually fire on headlines. System works as designed.
- **Month 10-18:** CEO event fires correctly. Nick exits before gap-down. System delivers ceiling scenario.

**Key divergence:** The 2-6 week gate at start produces a meaningfully better system because kill conditions and news input were co-designed, not built independently and hoped to interface.

---

## Decision matrix

| Dimension | Optimist | Pragmatist | Skeptic | Caveman | Hypomania |
|---|---|---|---|---|---|
| Implementation effort | ~70 lines, nick-monitor.py | **~40 lines, news-snapshot.py** | ~15 lines + kill-condition audit | ~40-50 lines, two-source stitch | Highest — cron + 2 files + healthcheck |
| Failure mode severity | Medium — path bug, no cross-run dedup | Medium — silent empty result, macro = price echo | Low for code; high if gate never clears | High — two-source incoherence | High — cron silent miss, stale digest |
| Maintenance cost | Medium | **Low** | Low for fetch | High | High |
| Macro coverage quality | ETF proxy price echo | ETF proxy price echo | 2-3 manual searches | ETF proxy price echo | New Alpaca endpoint required |
| Cron dependency | None | None | None | None | Yes — fatal on Windows laptop |
| Token/context impact | ~700-900 tokens (unverified) | ~700-900 tokens (unverified) | 0 | ~700-900 tokens (unverified) | ~700-900 tokens (unverified) |
| Kill condition alignment | No bridge built | No bridge built | Gates on bridge | No bridge built | No bridge built |
| Engineer verdict | Feasible with caveats | **Recommended** | Feasible | Not recommended | Not recommended |

---

## Expertise warnings

**Every option must address before shipping:**
1. `news-snapshot.py` has no cache file — "reuse cached output" references a non-existent artifact
2. Silent empty result is confirmed Alpaca behavior — must print "no news found for [TICKER]" explicitly
3. `load_current_holdings()` excludes Trimmed/Closed positions silently
4. Lookback must be dynamic (since last weekly-rec.md date), not fixed 7-day
5. Correct output path is `vault/20_investment/nick/news-digest.md` — not `vault/nick/`
6. Verify Alpaca's max symbols per call before combining 11 ETFs + ~10 holdings = ~21 symbols

---

## Caveman gut signal

**SAFE** — gut and analysis agree on what to build (Alpaca per-ticker extension + markdown output). They disagree only on the two-source approach. Reduce to Alpaca only and Caveman converges with Pragmatist. Gut does not flag this as a dangerous direction.

---

## Hypomania ceiling

The best-case scenario (Nick catches earnings warning 16h before weekly review, kill condition fires same day, exits before gap-down) is reachable with on-demand Pragmatist architecture. The cron is not required to reach the ceiling.

---

## Recommendation framework

**IF Nick's kill conditions are already measurable (metric-based, headline-triggerable):**
→ **Pragmatist architecture** with 3 engineer fixes. Ship this week. Total ~40-50 lines.

**IF Nick's kill conditions are qualitative (vague, not headline-triggerable):**
→ **Hybrid 2 (Skeptic-first with 2-week timebox).** Audit kill conditions first, hard deadline 2 weeks. Then ship Pragmatist architecture. Do not ship the feed into a system that cannot act on it.

**IF macro coverage is the primary concern (Iran war, Fed pivot, Trump-China):**
→ Neither option solves this cleanly. ETF proxy is price-echo, not cause. The honest answer is 2 manual web searches at `/nick-weekly` start for macro context — not automation. Build company-specific first; revisit macro separately.

**IF shipping speed is paramount:**
→ **Hybrid 1** — ship company-specific news now, run kill condition audit in parallel, review at 4 weeks whether headlines are mapping to actions. Accept the 60-70% base rate risk.

---

## GAD Pre-mortem on top recommendation (Pragmatist / Hybrid 1)

| Failure path | Probability | Early warning signal (30-60 days) | Decision rule |
|---|---|---|---|
| Kill condition mismatch — Nick reads news, cannot act on it, digest becomes noise | High | Nick's weekly-rec shows "news noted: [headline]" with no subsequent kill condition trigger or verdict change for 3+ consecutive weeks | Stop — audit kill conditions before continuing; do not add more news |
| Silent Alpaca failure — empty results mistaken for "no news" → false confidence | Medium | Nick notes "no relevant news this week" for holdings with obvious market events during that week | Stop — verify Alpaca is returning results; implement explicit empty-result logging |
| Token crowding — news digest fills context, Nick's kill condition reasoning becomes shallower | Low | Nick's weekly-rec analysis shortens in depth; fewer KB atom references; more surface-level verdicts | Reduce headlines cap from 3 to 1 per ticker; measure context before/after |

**Pre-mortem complete: ✅ — 3 failure paths identified.**

---

## Hard questions to answer first (from devil's advocate)

1. **Are Nick's current kill conditions headline-triggerable?** Read the most recent weekly-rec.md. For each kill condition, ask: "Would a single news headline satisfy or invalidate this condition?" If the answer is No for more than half — ship Hybrid 2, not Hybrid 1.

2. **Can Nick act faster than the market?** Nick's weekly cadence means a Monday event is reviewed Friday. Is there evidence that knowing about it on Wednesday (via headline) vs Friday (via price action) changes Nick's recommendation? If no — the ceiling scenario is rarer than Hypomania implies.

3. **What are the two prior open council decisions costing?** The Auto-Trader and thesis design councils are both open. Does news integration address either, or is it a third parallel priority competing for attention?

4. **For macro coverage: is ETF price-echo sufficient?** If Nick needs to know "WHY" the market moved (cause news), neither ETF proxy nor the recommended architecture delivers it. The honest answer is 2 web searches. Be explicit about this trade-off before shipping.

5. **Who monitors the news feed after the 4-week review?** Hybrid 1 assumes a review gate at 4 weeks. If the review finds the feed is not improving decisions, what is the explicit removal process? Don't build something without a confirmed exit path.

---

## All artifacts

- [[brief]]
- [[proposal-optimist]] / [[proposal-pragmatist]] / [[proposal-skeptic]] / [[proposal-caveman]] / [[proposal-hypomania]]
- [[critiques]] (20 critiques, MARS pattern, AgentDropout dedup applied)
- [[expertise-engineer]]
- [[synthesis]]
- [[final-challenge]]

---

## Outcome (fill later when known)

- Date decided:
- Choice: [Pragmatist / Hybrid 1 / Hybrid 2 / Skeptic-first / Hold]
- Specific implementation: [what was actually built]
- Outcome (after 4-8 weeks): [did headlines map to kill condition actions? what changed?]
