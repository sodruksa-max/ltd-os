# Healthcheck Warning Log

*(auto-updated by /healthcheck — keeps last 5 runs)*
*(used by OCD persistent WARN escalation layer)*

## 2026-05-19 (current run — after session improvements)
- PASS: 151 | WARN: 1 | FAIL: 0 — OK WITH WARNINGS
- [WARN] DECISIONS.md header stale — `updated: 2026-05-18` but git last touch 2026-05-19 → FIXED inline (header updated to 2026-05-19)
- [OPEN] Metadata-contextual vault embedding (arXiv:2510.24402) — medium complexity, deferred, 3rd carry
- [DEFERRED] outcomes-index.py — OUTCOMES.md only 114 lines, index not useful yet; revisit when > 300 lines
- [KNOWN] 9 unregistered scripts: backup.sh, dashboard.py, dashboard.sh, discovery.py, install-cron.sh, key-rotate.sh, new-project.sh, update-sectors.py, update-universe.py — all intentional
- youtube-transcript.py newly registered this session ✓
- daily-brief Phase 2 (macro-snapshot + news-snapshot) wired this session ✓
- DECISIONS.md stale header fixed inline → no carry to next run

## 2026-05-19 (resolution update)
- All items from 2026-05-18 รอบ 2 resolved:
- [FIXED] commits pushed to origin/main ✓
- [FIXED] untracked files committed or gitignored ✓
- [FIXED] nick-daily.sh + nick-signals-update.py registered in healthcheck.sh ✓
- [FIXED] /token-audit registered in healthcheck.sh ✓
- [FIXED] nick/daily/ added to .gitignore ✓
- [FIXED] IR paper improvements (ExpandSearch/FinSearch/Coverage) already in stock-content.md ✓
- [OPEN] Metadata-contextual vault embedding (arXiv:2510.24402) — medium complexity, not yet built
- [OPEN] TODO-MED from 2026-05-17: outcomes-index.py script approved but not yet built (ANALYST_LOG 2026-05-16)
- Current state: PASS 146 | WARN 0 | FAIL 0 — ALL SYSTEMS GO (as of last full run 2026-05-18)

## 2026-05-18 (รอบ 2)
- PASS: 141 | WARN: 1 | FAIL: 1 — DEGRADED
- [FAIL] 17 commits ahead of origin/main — CCR runs stale nick-v3 code → Fix: safe-push.sh
- [WARN] 3 untracked files: ipo-radar-2026-05-18.md, nick-v3-sizing-exits-survey.md, nick/daily/2026-05-18.json
- [NEW] nick-daily.sh + nick-signals-update.py on disk, not in healthcheck.sh
- [NEW] /token-audit command not in healthcheck.sh
- [DECISION NEEDED] vault/20_investment/nick/daily/ — add to .gitignore (runtime output) or commit
- [KNOWN] dashboard.py, dashboard.sh, discovery.py, update-sectors.py, update-universe.py — CCR/Streamlit utilities, intentionally not in healthcheck
- [KNOWN] backup.sh, new-project.sh, install-cron.sh — general utilities, kept

## 2026-05-18 (รอบ 1)
- PASS: 141 | WARN: 0 | FAIL: 1 — DEGRADED
- [FAIL — FIXED] 8 commits unpushed → pushed origin/main ✓
- [FIXED] Orphan scripts cluster: deleted bot.sh, bot-real.sh, screen.sh, eod.sh, stats-paper-trade.py; archived stock-screener.py, screener-performance.py, crypto-screener.py → vault/90_archive/scripts-archive/
- [FIXED] secret-rotate.sh untracked → renamed key-rotate.sh + committed
- [FIXED] /healthcheck not in healthcheck.sh → added to system commands list
- [KNOWN] dashboard.py, dashboard.sh, discovery.py, update-sectors.py, update-universe.py — CCR/Streamlit utilities, intentionally not in healthcheck
- [KNOWN] backup.sh, new-project.sh, install-cron.sh — general utilities, kept

## 2026-05-17 (รอบ 3)
- PASS: 125 | WARN: 0 | FAIL: 0 — ALL SYSTEMS GO
- [ACCEPTED] scripts/trade-log.json — runtime-generated, accepted prior run, no change
- [KNOWN] 17 unregistered scripts — unchanged, all known utility/wrappers
- [KNOWN] 8 templates not in symmetry audit — active templates, no orphans
- [TODO-HIGH] ExpandSearch + FinSearch + Coverage matrix — IR paper survey improvements not yet in stock-content.md
- [TODO-MED] Metadata-contextual vault embedding — new feature from IR survey
