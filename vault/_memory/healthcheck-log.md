# Healthcheck Warning Log

*(auto-updated by /healthcheck — keeps last 5 runs)*
*(used by OCD persistent WARN escalation layer)*

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

