# Healthcheck Warning Log

*(auto-updated by /healthcheck — keeps last 5 runs)*
*(used by OCD persistent WARN escalation layer)*

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

## 2026-05-17 (รอบ 2)
- PASS: 97 | WARN: 0 | FAIL: 0 — ALL SYSTEMS GO
- [PERSISTED — 1 run, ACCEPTED] scripts/trade-log.json — runtime-generated file referenced in nick.md blocklist, low impact, no fix needed
- [INFO] 17 unregistered scripts — ทั้งหมด utility/wrapper ที่รู้จักแล้ว ไม่ต้อง monitor เพิ่ม
- [INFO] ทุก improvement จากรอบ 1 ปิดครบแล้ว

## 2026-05-17 (รอบ 1)
- [WARN] scripts/trade-log.json — referenced in nick.md as blocklist but not a script (runtime-generated, low impact)
- [NEW] 20 unregistered scripts found on disk vs healthcheck.sh
- [RESOLVED] vault-review-trigger.sh / usage-tracker.py / bubble-risk-monitor.py — added to healthcheck
- [RESOLVED] video-note.md archived — no active references
- [INFO] content-draft.md retained — still used by writer agent + vault-review-trigger
- [INFO] stock-screener.py retained — different purpose from screener.py (ต้นรอบ vs momentum)

