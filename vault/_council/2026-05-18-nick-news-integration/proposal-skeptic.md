---
council_topic: nick-news-integration
proposer: skeptic
date: 2026-05-18
---

# Skeptic Proposal: Read Less, Trigger Better

## TL;DR
The real problem is not that Nick lacks news — it is that Nick's kill conditions are not measurable enough to act on news even if he had it. Fix the kill conditions first; build news infrastructure second.

## Approach
- Do not build a new news script. Extend nick-monitor.py with a single function: call Alpaca News API with symbols from load_current_holdings() — reuse what exists, add ~15 lines.
- Macro news: do not automate. Nick burns 2–3 web searches at the start of /nick-weekly to query broad macro. That is cheaper than building and maintaining a macro pipeline that will drift stale.
- Output goes to a flat .md file (nick-news-cache.md). Nick reads it, does not store it in KB. Disposable.
- No cron. On-demand only — runs when /nick-weekly calls it. Cron jobs for a paper portfolio are maintenance cost with no payoff.
- Cap: 5 headlines per ticker, 10 macro headlines max. Hard limit in code, not a guideline.

## Pre-mortem: how this fails
1. **Kill condition mismatch (probability: high)** — Nick sees "CEO resigned" but the kill condition says "revenue miss > 10%." Nick has no framework to act. The news arrives; nothing happens. The system produced noise, not signal.
2. **Headline hallucination drift (probability: medium)** — yfinance ticker.news returns scraped headlines of variable quality. Nick reads a misleading headline, flags a thesis as threatened, and wastes 3 web searches verifying something that was not real news. Net cost: search budget gone, no action taken.
3. **Macro query scope creep (probability: medium)** — "Iran war" and "Trump China visit" are not ticker-queryable events. Every attempt to automate macro via ETF proxies (SPY, GLD) returns market movement news, not cause news. The system fetches data that sounds relevant but requires human judgment to interpret — which Nick cannot do without burning searches.

## Hidden costs
- Maintenance: every time Alpaca changes rate limits or yfinance schema shifts, nick-monitor.py silently breaks. No one notices until Nick's weekly review has stale data.
- Search budget erosion: if macro auto-fetch fails silently, Nick falls back to web searches — now using 5 searches on macro instead of kill condition verification, which is the higher-value use.
- Blinded mandate creep: a news cache file that accumulates over time starts to look like a trade journal. One bad refactor and Nick is reading sentiment history, not thesis fundamentals.

## Survivorship bias check
Every "build a news feed for my portfolio" project assumes someone is actively monitoring the feed. The ones that work have a human reading and triaging. Nick is an AI that runs once per week. The gap between "news arrived Monday" and "Nick reviews Friday" means the news is already priced in before Nick can act.

## Worst case (5th percentile)
Nick-monitor.py adds news fetch. Alpaca returns 429 rate-limit errors silently. The script catches the exception and writes an empty news cache. Nick reads an empty file, assumes no relevant news, and holds a position through a material kill condition event. The system created false confidence — worse than having no system.

## Conservative alternative
Before building anything: audit Nick's current kill conditions. Are they measurable from a single headline? Rewrite kill conditions to be headline-triggerable first (e.g., "competitor named in earnings call as taking share"). Then the 15-line Alpaca extension has something to feed.

## Stop conditions
- If Alpaca returns empty results for 3 consecutive /nick-weekly runs: remove the fetch, use web searches instead.
- If Nick burns more than 5 of 15 search budget on macro interpretation: the macro layer is not working.
