---
type: reasoning-skills
updated: 2026-05-18
source: arXiv:2604.21764 (Thinking with Reasoning Skills — Apr 2026)
purpose: reusable reasoning shortcuts สำหรับ /pre-market — load พร้อม behaviors.md; ใช้ skills แทน re-derive logic ทุกวัน
---

# Pre-Market Reasoning Skills

*Load พร้อม pre-market-behaviors.md ที่ Step 0.1 — ใช้ skill code แทนการ reason จากศูนย์*

---

## Sizing Skills (Position Size Calculation)

**SK-SIZE-VIX:** VIX-Rank → multiplier
- Rank <30th pct → 1.0x | 30-50th → 0.75x | 50-70th → 0.47x | 70-85th → 0.30x | >85th → 0.15x
- Source: TRADING_RULES.md

**SK-SIZE-HSP:** HSP flags → multiplier
- 0 flags → 1.0x | 1 flag → 0.75x | 2+ flags → 0.50x (auto, no user confirm needed)

**SK-SIZE-PTSD:** PTSD threats → multiplier
- 0 threats → 1.0x | 1 threat → 0.85x | 2 threats → 0.70x | 3 threats → 0.55x | max -45%

**SK-SIZE-TACHY:** Tachypsychia level → multiplier
- Level 0 (clear) → 1.0x | Level 1 (NQ gap >1%) → 0.75x, no entry 9:30-9:45 | Level 2 (VIX >25) → 0.50x

**SK-SIZE-COMBINE:** Effective size = VIX × HSP × PTSD × TACHY (multiply all)
- ตัวอย่าง: 0.47 × 0.75 × 0.85 × 0.75 = ~0.22x base

---

## Oil-Energy Skills

**SK-OIL-XLE:** Brent threshold → sector call
- Brent >$95 ≥2 trading days → XLE primary outperformer (TRADING_RULES.md)
- Brent <$80 → XLE underweight; energy headwind

**SK-OIL-SPREAD:** Brent vs WTI spread interpretation
- Spread >$5 → global supply fear > domestic | Spread <$2 → US-specific driver
- Wide spread + Iran news → Hormuz risk premium; use Brent as primary signal

---

## Yield Skills

**SK-YIELD-TLT:** 10Y change → TLT reliability
- 10Y change ≥+5bps vs prior close → TLT pre-market unreliable (TRADING_RULES.md)
- 10Y change <5bps → TLT direction valid intraday

**SK-YIELD-GROWTH:** 10Y level → growth stock pressure
- 10Y >4.5% → growth/tech headwind; reduce XLK weight
- 10Y >5.0% → high pressure; avoid momentum longs unless RS very strong (>+15%)

---

## VIX-Scenario Skills

**SK-VIX-REGIME:** VIX level → market regime
- VIX <15 → low vol, momentum works, SMOOTH texture
- VIX 15-20 → elevated caution, ROUGH texture, reduce size moderately
- VIX 20-25 → CHOPPY, high false signals, day trade only
- VIX >25 → JAGGED, cash default, only high-RS EARLY★ if must trade

**SK-VIX-TERM:** VIX term structure → directional bias
- VIX9D/VIX <0.9 → backwardation (fear near-term) → bearish intraday
- VIX9D/VIX >1.1 → contango (calm near-term) → potential bounce

---

## Catalyst-Earnings Skills

**SK-EARN-NVDA:** NVDA earnings → sector cascade
- NVDA beats → semicon sector bid: AMD, AVGO, LRCX, UCTT, MU follow within 1-2 sessions
- NVDA misses → semicon sector dump; avoid all semicon longs earnings week
- Rule: ห้าม hold NVDA (or semicon) swing ข้ามวัน earnings

**SK-EARN-BINARY:** Binary event → confidence cap
- Unresolved binary (Iran deal, FOMC, major earnings) → confidence cap = Low always
- ถ้า binary resolves → re-assess scenario ทันที ไม่รอจบ session

---

## Sector-Flow Skills

**SK-SECTOR-PRIORITY:** Sector-flow label → long/avoid
- Leading + Improving → long bias ✅
- Fading → avoid new longs, monitor exits
- Lagging → avoid longs ❌; consider short (only high-conviction)

**SK-SECTOR-SPACE:** ROKT/ITA interpretation
- ROKT Leading + ITA Lagging → space stocks decouple from defense ETF → check RKLB/ASTS independently
- Both Lagging → risk-off in space theme; WATCH only, no entry

---

## Geopolitical Skills

**SK-GEO-OIL:** Geopolitical event → oil/defense implication
- Middle East escalation → Brent +X%, XLE up, defense (LMT/RTX/KTOS) bid
- Middle East resolution → Brent -X%, XLE down, tech/growth relief rally
- Magnitude scale: Low (<$3 Brent move), Mid ($3-8), High (>$8 or Hormuz risk)

**SK-GEO-BINARY:** Iran nuclear deal framework → trading rule
- Rejected/stalled → binary event active → confidence cap Low; check XLE
- Agreed → remove cap; re-assess VIX + futures direction

---

## Pattern-Recognition Skills (TLE Matches)

**SK-TLE-MAY2026:** May 2026 oil spike + Iran rejection context
- Prior similar: May 5, 2026 → outcome: oil eased D+2, XLK +2.2%
- Implication: if Iran softens → flip to XLK within 48h; XLE take profit

**SK-TLE-NVDAEARNS:** NVDA earnings pre-positioning week
- Pattern: RS strong week before earnings → often fades intraday earnings day regardless of beat/miss
- Rule: day trade only; exit by 2pm ET earnings day regardless of P&L
