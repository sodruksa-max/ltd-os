---
council_topic: nick-news-integration
proposer: pragmatist
date: 2026-05-18
---

# Pragmatist Proposal: Extend Existing Scripts, Don't Build New Infrastructure

## TL;DR
Bolt a `--nick-news` flag onto news-snapshot.py that adds holding-specific symbols to the existing Alpaca fetch. Nick calls it directly at session start — no new APIs, no new scripts, no new failure modes.

## Approach
1. Add `load_current_holdings()` import (already exists in nick-monitor.py) into news-snapshot.py, or duplicate the 3-line file-read logic inline — simpler than a shared module
2. Add `--nick-news` flag: when set, merge holding tickers into `ALL_SYMBOLS` before the fetch call; existing fetch, parse, categorize logic unchanged
3. Add one new print section: "### Holdings-Specific News" — filters articles where `article["symbols"]` intersects with holdings; everything else falls into existing macro sections
4. Nick's `/nick-weekly` prompt prefixes with: `python scripts/news-snapshot.py --nick-news` output, then reads KB as before — blinded mandate intact (news is input, not a trade signal override)
5. Macro coverage (Iran, Fed, Trump-China) is already working via GEO_SYMBOLS + BROAD_SYMBOLS — no change needed there

## Base rate evidence
Alpaca News API `symbols` parameter already filters by ticker — this is documented behavior, not an assumption. The existing news-snapshot.py successfully fetches and categorizes 12h news in production. Extending a working fetch with additional symbols has ~0% chance of breaking the macro layer and high chance of surfacing company-specific headlines (earnings, FDA, contract wins) that yfinance.news misses on weekends/pre-market.

## Realistic outcome (50th percentile)
Nick gets 3-8 holding-specific headlines per weekly session, catches 1 material event (earnings miss, CEO change) per month that would otherwise arrive as a price gap with no context. Macro coverage stays identical.

## Time to first feedback
First `/nick-weekly` run after the patch — same day as implementation.

## Required skills/resources
No new API keys. No new dependencies. ~40 lines of Python added to an existing script.

## Comparison: alternatives I rejected
- **Separate nick-news.py script**: duplicates fetch logic, two scripts to maintain, no gain
- **yfinance ticker.news**: rate-limit unpredictable, weekend data stale, already have Alpaca
- **Web search per holding inside Nick's session**: burns 5-10 of the 15-search budget before KB read even starts — wrong priority order

## Open questions for user
Does Nick run `--nick-news` every weekly session regardless of KB freshness, or only when a kill condition is near trigger? Answer changes whether I add a `--quick` mode that skips company news and only runs macro.
