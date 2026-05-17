---
council_topic: nick-news-integration
proposer: optimist
date: 2026-05-18
---

# Optimist Proposal: Two-Layer News Feed — Script-First, Search-Last

## TL;DR
Extend nick-monitor.py with a `fetch_nick_news()` function that pulls company news via Alpaca symbols API for all holdings + reuses news-snapshot.py output for macro — zero new APIs, zero new scripts, and Nick gets a pre-digested news digest before every weekly review.

## Approach

1. **Extend nick-monitor.py** (not a new script) — add `fetch_nick_news()` that calls the Alpaca News API with `symbols=<holdings list>` (load_current_holdings() already gives us this), lookback 7 days, top 3 headlines per ticker.
2. **Reuse news-snapshot.py output for macro** — run news-snapshot.py first (or read its cached markdown output if already run that session), then pass that block to Nick as "macro context." No duplicate fetch, no new API.
3. **Write a `vault/nick/news-digest.md`** — nick-monitor.py writes a clean dated file: company headlines per holding + macro headlines block. Nick reads this file before weekly-rec reasoning, not raw API output.
4. **Nick consumes digest as KB read, not search** — news-digest.md is a vault file, not a web search. Preserves all 15 web search budget for kill condition verification where it matters.
5. **On-demand trigger** (not cron) — news-digest generates when `/nick-weekly` runs, immediately before Nick's review step. Avoids stale data and no maintenance overhead.

## Why this could work

- **Alpaca symbols API is already proven** — news-snapshot.py uses the exact same endpoint and auth. Adding a `symbols` parameter pointing to holdings list is one function, not a new integration.
- **DRY architecture wins** — teams that reuse infrastructure consistently report lower defect rates vs adding parallel pipelines.
- **Digest-as-vault-file preserves blinded mandate** — Nick reads a markdown file, same as reading THESIS_TRACKER.md. No price feeds, no trade history, no BLOCKLIST touching.

## Best case (top 20% outcome)
Nick catches a kill condition trigger from a headline before it shows in price — e.g., CEO resignation on Thursday triggers early sell recommendation in Friday weekly. Kill condition response time drops from 7 days (weekly cadence) to same-day. Nick's thesis integrity improves measurably over 3 months.

## Realistic case (median outcome)
Nick gets 3-5 relevant headlines per holding per week. Macro block surfaces 1-2 geopolitical signals. Nick's kill condition reasoning improves quality — fewer "no news available" hedges in weekly-rec, more specific "as of [date], no adverse company news" statements. Maintenance cost: near zero.

## Key assumptions
- Alpaca News API returns reasonable company-specific coverage for Nick's holdings (works well for US large/mid-cap; thinner for small-cap).
- news-digest.md stays under 300 lines — if holdings expand past 15 tickers, add a `max_articles_per_ticker=2` cap.
- nick-monitor.py can write to vault/nick/ (already does for other outputs).

## Risks

| Risk | Mitigation |
|---|---|
| Alpaca news sparse for small-cap holdings | Fallback: yfinance ticker.news for tickers with 0 Alpaca results — same session, no extra key |
| Digest grows noisy over time | Hard cap: top 2 headlines per ticker, dedup by URL hash |
| Macro digest overlaps company news (e.g., SPY news about AAPL) | Label section headers clearly: `## Company News` vs `## Macro Context` — Nick filters by section |
| /pre-market not run → no macro news cached | news-snapshot.py runs independently; nick-weekly calls it directly if no cache found |
