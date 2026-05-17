---
council_topic: nick-news-integration
expertise_lens: engineer
date: 2026-05-18
---

# Engineer Evaluation — Nick News Integration

## Code inspection findings

**news-snapshot.py (verified):**
- `ALL_SYMBOLS = GEO_SYMBOLS + BROAD_SYMBOLS` — 11 hardcoded ETF proxies, no per-ticker stocks
- `fetch_news()` passes `",".join(ALL_SYMBOLS)` as a single `symbols=` string — Alpaca accepts comma-joined multi-symbol in one call (not sequential)
- When Alpaca returns zero results: `resp.json().get("news", [])` returns empty list — **no exception, no warning printed. Silent empty result is confirmed behavior.**
- `dedup()` deduplicates by exact headline string — fragile if headline wording differs slightly

**nick-monitor.py (verified):**
- `load_current_holdings()` exists. Glob sorts `*_weekly-rec.md` alphabetically (not by date prefix) — works correctly in practice with YYYY-MM-DD prefix but fragile if naming drifts.
- Regex matches `### TICKER — Intact` or `### TICKER — Evolving` only. Tickers with status "Trimmed," "Closed," or any other label are **silently excluded** from holdings list. Proposers assume "all holdings" — incorrect.
- `vault/20_investment/nick/` folder exists with weekly/ and alerts/ subdirectories. No `news-digest.md` or `news/` subfolder yet.
- **Optimist's `vault/nick/news-digest.md` path is wrong.** That folder does not exist. Correct path is `vault/20_investment/nick/news-digest.md`.

**Critical: news-snapshot.py writes to stdout only — no cache file exists.**
Optimist's proposal says "reuse cached macro output if already run that session." There is no file cache. Any proposal referencing "reading the cached news-snapshot.py output" references something that does not exist.

**Critical: yfinance ticker.news ≠ what nick-monitor.py already uses.**
nick-monitor.py uses `/v8/finance/chart/` for price data with retry/backoff. `ticker.news` is an undocumented scrape endpoint. Proposers treating yfinance as "already integrated" for news are wrong — adding `ticker.news` is a new dependency with different failure characteristics.

---

## Per-proposal evaluation

### Optimist
- **Implementation effort:** ~60-80 lines added to nick-monitor.py. Feasible, but the path bug (`vault/nick/` vs `vault/20_investment/nick/`) will cause first-run failure. The "cached macro output" assumption is incorrect — needs replacement with a direct news-snapshot.py call (adds 15-30s latency).
- **Key failure mode:** 7-day fixed lookback resurfaces last week's headlines again this week. No cross-run dedup implemented.
- **Maintenance cost:** Medium — two call paths (Alpaca primary, yfinance fallback), both must be maintained separately.
- **Engineer verdict:** Feasible with caveats. Fix the path bug and the cache assumption before shipping.

### Pragmatist
- **Implementation effort:** ~40 lines added to news-snapshot.py. Genuinely the smallest code surface. Reuses entire existing pipeline (classify, dedup, print).
- **Key failure mode:** When `article["symbols"]` is an empty list (Alpaca omits symbols on broad market articles), holdings intersection returns zero — no company-specific section, no error. Nick infers "no news" when the fetch succeeded but returned untagged articles.
- **Maintenance cost:** Low. Exception isolation risk: if the new code path raises an unhandled exception, it aborts the macro output too. ~5 lines of try/except fixes this.
- **Engineer verdict:** Feasible. Most defensible technically. Three fixes needed (see recommendation below).

### Skeptic
- **Implementation effort:** ~15 lines for the fetch extension. Kill condition audit is unquantified (2 hours to 2 weeks).
- **Key failure mode:** Manual macro web searches (2-3 per session) burn 13-20% of search budget before kill condition work starts — the exact waste Skeptic says it wants to prevent.
- **Maintenance cost:** Low for the fetch extension. High if kill-condition-first is treated as a hard blocker with no completion criterion.
- **Engineer verdict:** Feasible. Kill-conditions and news fetch are parallel workstreams with no technical dependency — the sequencing argument is a preference, not a constraint.

### Caveman
- **Implementation effort:** Described as "one script call" but is actually ~30-50 new lines to stitch two different APIs (news-snapshot.py ETF output + yfinance ticker.news per holding) into one file with no dedup or source label.
- **Key failure mode:** Two-source merge with no provenance label. yfinance schema changes without notice. yfinance ticker.news is undocumented — different endpoint from what nick-monitor.py already handles.
- **Maintenance cost:** High relative to apparent simplicity. Adding yfinance ticker.news is a new undocumented dependency.
- **Engineer verdict:** Not recommended as described. Reduce to one source (Alpaca only) and the proposal converges with Pragmatist or Skeptic.

### Hypomania
- **Implementation effort:** Highest surface area. New cron job + extended nick-monitor.py + extended news-snapshot.py + two output files + healthcheck extension.
- **Key failure mode (confirmed):** Windows Task Scheduler does not run tasks while machine is sleeping. A laptop that sleeps at midnight and wakes at 8AM silently misses the 6AM cron. The stale-file healthcheck fires only at `/nick-weekly` start — no proactive alert. Nick reads 5-day-old digest thinking it is fresh.
- **Keyword search on Alpaca:** Hypomania proposes querying Alpaca with keywords like "Iran conflict" — but the existing endpoint filters by `symbols=`, not by keyword. Client-side `classify()` handles categorization post-fetch. Server-side keyword queries require a different endpoint (`/v1beta1/news?query=`) — this is a new integration, not an extension of what exists.
- **Maintenance cost:** High — two output files, two staleness clocks, cron dependency, new API endpoint pattern.
- **Engineer verdict:** Not recommended for this environment (Windows laptop). On-demand fetch at `/nick-weekly` start eliminates cron failure mode at the cost of 15-30s latency — worthwhile trade for a once-weekly paper portfolio.

---

## Hidden costs none proposed addressed

1. **Token cost of news digest in /nick-weekly context.** Estimate: 10 holdings × 3 headlines × ~60 tokens per headline + metadata = ~700-900 tokens added per session. Within safe range but should be verified against actual weekly-rec.md context load.

2. **Lookback window vs. weekly cadence mismatch.** Fixed 7-day lookback resurfaces last week's headlines. Correct implementation: read date of most recent weekly-rec.md and use that as dynamic lookback start.

3. `load_current_holdings()` silently excludes non-Intact/Evolving positions. A "Trimmed" position (still partially held) receives no news monitoring.

4. **Empty-result silent failure is the central operational risk.** Every proposal using Alpaca for per-ticker stocks will encounter empty results for small/mid-cap tickers. Current macro script handles this gracefully; per-ticker path must explicitly implement the same.

5. **Alpaca symbol count limit.** Current script sends 11 symbols. Adding 10 holding tickers = 21 symbols total. Need to verify Alpaca's max `symbols` count per call.

---

## Recommended implementation path

Pragmatist's `--nick-news` flag architecture with three fixes:

1. **Exception isolation:** wrap holdings-merge logic in try/except so failure in company-news path does not abort macro output
2. **Empty-result UX:** explicitly print "Holdings-Specific News: [TICKER] — no news found" when Alpaca returns zero matching articles for that ticker
3. **Dynamic lookback:** replace hardcoded `LOOKBACK_HOURS` for the `--nick-news` path with date-diff from the most recent weekly-rec.md file (accessible via existing `NICK_WEEKLY` path in nick-monitor.py)

Output location: `vault/20_investment/nick/news-digest.md` (not `vault/nick/`).

---

## Red flags

1. **`vault/nick/news-digest.md` path in Optimist proposal is wrong.** Folder does not exist. Creating it violates CLAUDE.md policy ("Don't create new top-level folders without asking").
2. **news-snapshot.py has no cache file.** "Reuse cached output" references a non-existent artifact.
3. **yfinance ticker.news is a new undocumented dependency** — not the same as nick-monitor.py's existing yfinance usage.
4. **Cron on Windows laptop is unreliable.** The fix is removing the cron dependency, not improving healthchecking.
5. **load_current_holdings() filename sort is alphabetical** — latent fragility if naming conventions drift.
