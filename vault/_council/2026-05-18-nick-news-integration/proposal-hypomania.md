---
council_topic: nick-news-integration
proposer: hypomania
date: 2026-05-18
---

# Hypomania Proposal: Dual-Feed Intelligence Engine — Nick Becomes News-Aware Before You Wake Up

## TL;DR
Run a nightly news-fetch script that outputs two clean files — one per-ticker, one macro — and Nick reads them as immutable KB snapshots at session start. Zero new API keys. Zero search budget burned.

## Approach

**Angle 1 — The Automated Pre-Digest (ceiling scenario)**
- Extend `nick-monitor.py`: at cron trigger (6AM daily), call `load_current_holdings()` → feed tickers to Alpaca News API `symbols=` parameter → save `vault/Knowledge/nick-news-holdings.md` (last 24h, top 3 stories per ticker, kill-condition-flagged)
- Parallel: extend `news-snapshot.py` to also query 5 macro topic keywords ("Fed rate", "Iran conflict", "China trade", "Treasury yield", "dollar index") → save `nick-news-macro.md`
- Nick reads both files at `/nick-weekly` start as static KB — costs 0 search budget, arrives pre-filtered

**Angle 2 — The Zero-Build Path (fast ceiling)**
- yfinance `ticker.news` is free, no new key — scrape all holdings in 1 loop, output markdown digest
- For macro: reuse existing `news-snapshot.py` ETF proxies (TLT = Fed, GLD = crisis, USO = Iran) as macro signal proxies — news about TLT IS macro news, no keyword search needed
- Macro coverage is already 80% done with zero new code

## Best Case (ceiling)
Nick catches an earnings warning 16 hours before weekly review. Kill condition fires same day. Position closed before gap-down. Zero manual intervention.

## Key Assumptions
- Alpaca `symbols=` parameter works reliably per their docs (verified: yes)
- Cron runs even when user is offline (Windows Task Scheduler or GitHub Actions cron)
- Nick treats news digest as read-only KB — never as trade instruction

## Risks and Mitigations
| Risk | Mitigation |
|---|---|
| News noise overwhelms Nick's analysis | Cap: 3 headlines per ticker, summary only |
| Cron fails silently | healthcheck detects stale news file (> 30h old) → warn in weekly |
| Macro proxy mismatch (TLT ≠ Fed news) | Add 2 direct keyword queries as supplement |
