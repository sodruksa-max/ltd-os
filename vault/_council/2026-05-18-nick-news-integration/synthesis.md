---
council_topic: nick-news-integration
phase: 4-synthesis
date: 2026-05-18
---

# Synthesis — Nick News Integration

## Phase 4.5 Audit

### [FALSE DIVERSITY]

Optimist, Pragmatist, Caveman, and Hypomania (Angle 2) are all betting on the same underlying mechanism: add holdings tickers to an Alpaca `symbols=` call + write output to a markdown file Nick reads. Framing differs but code footprint is nearly identical. These four collapse to one effective option.

Skeptic is genuinely different — it gates the build on kill condition readiness. Hypomania's cron path is architecturally different but engineer ruled it out for Windows laptop environment.

**Effective options: 2, not 5.**
- **Option A (Build):** Alpaca per-ticker extension + markdown output. Pragmatist's `--nick-news` flag architecture is preferred by engineer.
- **Option B (Gate):** Fix kill conditions first, then build — Skeptic's sequencing.

### [OCD: MATRIX CHECK]
All 5 proposals rated on all 8 dimensions. Unknowns marked explicitly — no empty cells.

### [DR: BASE RATE]

Reference class: news-feed integrations built for low-frequency automated review agents (weekly cadence). Estimated success rate at improving decision quality over 6 months: ~30-40%. Majority produce data that is read but not acted on.

Primary failure modes (confirmed by critique cluster):
- Silent empty result — agent infers "no news" when fetch failed silently (Alpaca confirmed to behave this way)
- Stale data confidence — agent reads old digest, treats it as fresh
- Noise normalization — 3-8 benign headlines weekly trains agent to discount the channel; material event missed in routine
- Kill condition mismatch — news arrives, no actionable framework to map it to a decision

Skeptic's pre-mortem is the most empirically grounded analysis in the debate.

---

## Where proposals AGREE (convergence)

- Alpaca News API `symbols=` parameter is the right tool for per-ticker company news — all accept this; engineer confirms documented behavior
- No new API keys needed
- No cron — on-demand at `/nick-weekly` start is correct trigger (4 of 5; engineer confirms cron on Windows laptop unreliable)
- Output should be a markdown file Nick reads as KB, not a web search — preserves all 15 search budget for kill condition verification
- yfinance `ticker.news` is NOT a clean fallback — engineer confirms it is an undocumented scrape endpoint, different from nick-monitor.py's existing yfinance usage
- Token cost of news digest: ~700-900 tokens per session (engineer estimate, not yet verified against actual context load)

## Where proposals DIVERGE (real disagreements)

1. **Build now vs gate on kill conditions first** — Skeptic says kill conditions must be headline-triggerable before a news feed has value. Everyone else says build now. This is the only genuine fork.
2. **Macro coverage method** — ETF proxy news (price-reaction, not cause) vs manual web searches (burns budget) vs keyword Alpaca query (new endpoint). No proposal has a clean answer.
3. **Lookback window** — Fixed 7-day (resurfaces last week's headlines) vs dynamic since last weekly-rec.md date (correct, requires one extra implementation step).

---

## Decision matrix

| Dimension | Optimist | Pragmatist | Skeptic | Caveman | Hypomania |
|---|---|---|---|---|---|
| Implementation effort | ~70 lines, nick-monitor.py | ~40 lines, news-snapshot.py | ~15 lines + kill-condition audit (2h–2wk) | ~40-50 lines, two-source stitch | Highest — cron + 2 files + healthcheck |
| Failure mode severity | Medium — path bug, no cross-run dedup | Medium — silent empty result, macro = price echo | Low for code; high if gate never clears | High — two-source incoherence, no provenance | High — cron silent miss, stale digest |
| Maintenance cost | Medium — two call paths (Alpaca + yfinance fallback) | Low — one API, one script, exception-isolated | Low for fetch; unknown for kill-condition work | High — yfinance undocumented schema | High — two staleness clocks, cron dependency |
| Macro coverage quality | ETF proxy price echo (not cause) | ETF proxy price echo (not cause) | Manual 2-3 searches — burns budget | ETF proxy price echo (not cause) | Keyword query = new Alpaca endpoint |
| Cron dependency | None | None | None | None | Yes — confirmed fatal on Windows laptop |
| Token/context impact | ~700-900 tokens (unverified) | ~700-900 tokens (unverified) | 0 tokens (search budget used instead) | ~700-900 tokens (unverified) | ~700-900 tokens (unverified) |
| Kill condition alignment | Feeds kill conditions; no mapping bridge | Same — no mapping bridge | Blocks until bridge exists | Same — no mapping bridge | Same — no mapping bridge |
| Engineer verdict | Feasible with caveats (path bug, cache assumption broken) | **Feasible — most defensible; 3 named fixes** | Feasible; sequencing is preference not constraint | Not recommended as described | Not recommended for Windows laptop |

---

## Engineer warnings — every option must address these

1. `news-snapshot.py` has no cache file. Any proposal referencing "reuse cached output" references a non-existent artifact. Cold fetch adds 15-30s latency to every `/nick-weekly` that did not follow `/pre-market`.
2. Silent empty result is confirmed Alpaca behavior. Must implement explicit "no news found" print per ticker — not silence.
3. `load_current_holdings()` excludes Trimmed/Closed positions. Partially held positions receive no news monitoring.
4. Lookback must be dynamic. Fixed 7-day resurfaces last week's headlines. Use date-diff from most recent weekly-rec.md.
5. Correct output path is `vault/20_investment/nick/news-digest.md` — not `vault/nick/` (folder does not exist).
6. Alpaca symbol count: current 11 + ~10 holdings = ~21 total. Verify max symbols per call.

---

## Caveman gut signal

**SAFE** — and gut does not contradict the sophisticated proposals. "Nick reads news before deciding, same as every fund manager" is correct framing. Danger signals Caveman identified (noise, stale file, macro gap) are exactly the risks the engineer quantified. Gut and analysis converge on what to build. They disagree only on the two-source approach — reduce to Alpaca only and Caveman converges with Pragmatist.

---

## Hypomania ceiling signal

Best case: Nick catches an earnings warning 16h before weekly review, kill condition fires same day, position closed before gap-down, zero manual intervention. **This ceiling is reachable with Option A (on-demand Pragmatist path).** The cron architecture is not required to reach it. On-demand fetch achieves the same ceiling with lower operational risk.

---

## Missing angles from ADHD scan

1. **Kill condition → news query mapping bridge** — nobody built it. "CEO resigned" arrives; kill condition says "revenue miss > 10%." Nick has no framework to connect the headline to a decision. Without this bridge, news is informational but not decisional.
2. **Token cost unverified** — engineer estimates 700-900 tokens. Needs one live measurement against actual `/nick-weekly` context load before assuming it fits.
3. **Lookback window mismatch** — all proposals except Skeptic use fixed 7-day. Dynamic lookback is a 5-line fix but must be in v1, not deferred.
4. **Exit/rollback criteria** — only Skeptic defined stop conditions. Build path needs: "If Alpaca returns empty for 3 consecutive runs → log warning + fall back to 2 manual macro web searches."

---

## Hybrid options

**Hybrid 1 — Build + Parallel Audit:**
Ship the `--nick-news` flag (Pragmatist architecture, engineer's 3 fixes) immediately. Run kill condition audit in parallel — not as prerequisite. At 4-week review: assess whether headlines are mapping to kill condition actions. If not, reduce to macro-only.

**Hybrid 2 — Gate with 2-Week Timebox:**
Do kill condition audit first, hard deadline 2 weeks. If kill conditions are not headline-triggerable by then, ship minimal Alpaca extension anyway. Eliminates the "delay forever" failure mode while respecting Skeptic's logic.

---

## Recommendation framework

**IF lowest implementation risk matters most** → Pragmatist (engineer's recommended path, ~40 lines, 3 named fixes, one API, lowest failure surface)

**IF decision quality before shipping matters most** → Skeptic-first via Hybrid 2 (2-week timebox on kill condition audit, then Pragmatist architecture)

**IF shipping now and iterating matters most** → Hybrid 1 (build this week, parallel audit, 4-week review gate)

**IF macro news quality above all** → 2 manual web searches (Skeptic's fallback) are the most honest answer until keyword-query Alpaca endpoint is verified

---

## Open questions (user must answer before deciding)

1. Are Nick's current kill conditions expressed as measurable financial metrics — or qualitative triggers that a single headline could satisfy? This determines whether Option B's gate is meaningful or theatrical.
2. Is 15-30 seconds of cold fetch latency acceptable at every `/nick-weekly` start?
3. Should "Trimmed" positions still receive news monitoring — they are partially held and kill conditions may still apply?
4. For macro news (Iran, Fed pivot, Trump-China): is ETF price-echo (SPY/TLT movement) sufficient context for Nick, or does Nick need cause-level reporting?
5. What is the completion criterion for "kill conditions are headline-triggerable enough" — who sets the bar, and by when?
