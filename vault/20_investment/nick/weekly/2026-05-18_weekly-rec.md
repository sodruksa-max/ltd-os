---
type: nick-weekly
date: 2026-05-18
version: nick-v3
nav_usd: 2320.00
nav_inception: 2320.00
nav_change_pct: +0.00%
spy_inception_price: 737.71
benchmark_qqqm_inception: null
benchmark_soxx_inception: null
holdings: 0
cash_pct: 100.0
session_tier: 3
vix: 18.43
spy_5d_pct: -1.40
---

# Nick Weekly — 2026-05-18 (v3 Inception)

**[PORTFOLIO RESTART — Nick v3, fresh $2,320 account, 0 positions]**

NAV: $2,320.00 | SPY: $737.71 (inception locked) | Delta: N/A (Day 1) | Cash: 100%

---

## Session Classifier

```
[NARCOLEPSY: ACTIVE WEEK] Tier 3
Reason: SPY -1.40% 5d + NVDA earnings post-close May 20 (2 days) = thesis-defining T1/T2 event
Steps 5.29-5.43: RUN (Tier 3)
```

```
[DERMO: ACTIVE WEEK] — Tier 3 confirmed
SPY: -1.40% | VIX: 18.43 (+6.78%) | Earnings: NVDA May 20 in universe
```

## Cognitive Gates

| Flag | Value | Reason |
|---|---|---|
| is_monthly_first_week | FALSE | May 18 — day 18 of month |
| has_buy_candidate | TRUE | IONQ scored viable (EARLY★ RS↑↑) |
| has_recent_earnings | FALSE | No current holdings |

Steps gated ON: 5.5, 5.6, 5.7, 5.8, 5.10, 5.11, 5.17, 5.18, 5.19, 5.20
Steps SKIPPED: 5.9 (MONTHLY), 5.12 (no holdings with earnings), 5.13, 5.14, 5.15, 5.16 (MONTHLY)

---

## Step 0 — Score Previous Week's Recs

**[SKIP]** v3 inception — no prior recs to score. Previous outcome entries in nick-soul.md are from the old $10K portfolio.

---

## Step 1 — Market Context (from scripts)

| Metric | Value | Signal |
|---|---|---|
| SPY | $737.71 | -1.40% (5d) |
| VIX | 18.43 | +6.78% — EARLY tier, all buys allowed |
| 10Y Yield | 4.595% | +3.00% — mildly elevated |
| S&P Futures | -0.64% | pre-market weakness |
| VIX-Rank | 66th pct | Day-trade multiplier 0.47x (not applied to Nick — conviction sizing used) |
| Regime | EARLY | VIX <20 — buys allowed; trending toward EXTENDED if VIX spikes post-NVDA |

**VIX tier note:** Currently EARLY. If NVDA disappoints May 20 and VIX spikes to 20–28, regime shifts to EXTENDED (HIGH conviction only). If VIX ≥28, no new entries until it clears.

---

## Step 2 — Universe Signals (universe-screen.py)

| Ticker | Price | Signal | RS | Earnings Gate |
|---|---|---|---|---|
| NVDA | $225.32 | [EARLY★] | RS↑↑ | ⛔ May 20 (2d) — SKIP |
| IONQ | $51.95 | [EARLY★] | RS↑↑ | ✅ Clear |
| AVGO | $425.19 | [EARLY] | RS↓ | ⚠️ Check date |
| ASML | $1,501.81 | [EARLY★] | RS↑ | ✅ Clear — but impractical ($1,502/sh) |
| PLTR | $133.99 | [-] | RS↓ vol-div | ✅ Clear — but RS bearish |

---

## Step 3 — NAV Calculation

**NAV = $2,320.00 (inception, 100% cash)**
Inception SPY locked: $737.71
Benchmark inception prices (QQQM/SOXX): [EXACT UNAVAILABLE — not fetched this session; will lock next week]

---

## Step 3.5 — Tourette Price Reflex

```
[REFLEX] ASML $1,501.81 — EARLY★ RS↑ signal but single share = 65% NAV for $2,320 portfolio. Size mismatch is extreme. The signal is real, the allocation unit is impractical.
[REFLEX] AVGO RS↓ while price $425 — contradicts the EARLY signal. Needs explanation.
[REFLEX CLEAN] IONQ and NVDA signals consistent with thesis.
```

Reflex ASML: [REFLEX EXPLAINED] — ASML signal valid, but v3 capital too small. Skip until NAV > $5K.
Reflex AVGO: [REFLEX EXPLAINED] — AVGO large-cap retracement from highs, RS declining vs SPY is consistent with sector rotation. Not a buy here.

---

## Step 4 — Kill Condition Check

**No existing holdings → no kill checks.**

Pre-buy kill check (psychopathy forward):
- IONQ: kill conditions (RPO stagnation, gov contract loss, VIX ≥28) → none triggered → CLEAR
- NVDA: earnings gate → HOLD, not a kill condition
- PLTR: RS↓ vol divergence → not a kill condition but RS is an ENTRY condition — fails entry

---

## Step 5 — KB Sweep

**thesis-convergence.md:**
- AI Capex Supercycle: STRONG (8 sources) → T1 thesis healthy, NVDA/AVGO conviction intact
- Semiconductor Moats: STRONG (4 sources) → T2 thesis healthy
- AI Networking: STRONG → benefits NVDA/AVGO ecosystem
- Valuation Compression Risk: STRONG — headwind for high-multiple names (PLTR 46x EV/Rev flagged)

**nick-signals.md (May 17):**
- NVDA: NEUTRAL/MID/STRONG★ → momentum healthy
- IONQ: NEUTRAL/MID/STRONG → clean entry
- PLTR: OVERSOLD/NEAR/WEAK? → bearish flag, no buy
- ASML: NEUTRAL/NEAR/NEUTRAL → watchlist

**contradiction-registry.md (last known):** No active contradictions affecting IONQ or T5 thesis.

**insight-atoms (PLTR):** PLTR trades 46x NTM EV/Rev, CEO insider selling $1.88B, DOGE risk Q3-Q4 2026 — reinforces NOT buying PLTR until RS recovers and valuation concerns ease.

---

## Cognitive Sub-steps

### 5.5 Autism Pattern Check
```
[CLEAN] No prior v3 positions to drift-check
[CLEAN] No cross-session kill condition contradiction
[CLEAN] No intra-session conflict
Note: v3 inherits soul.md bias-prevention rules. Fresh start.
```

### 5.6 Dyslexia Spatial View
```
Portfolio shape: EMPTY (100% cash)
Real exposures: none
Hidden overlaps: none
Natural hedges: none (no positions)
Missing jigsaw:
  - T1 (AI Capex): NO exposure — pending NVDA post-earnings
  - T2 (Semicon Moats): NO exposure — ASML impractical for v3
  - T5 (Quantum): IONQ = immediate candidate
  - T4 (AI Software): PLTR = conditional (needs RS recovery)
Target shape: 3-4 focused bets, 30-40% deployed, 60-70% cash for future contributions
```

### 5.7 Psychopathy Kill Check
```
No existing positions to kill.

Pre-buy tests (would I buy today?):
[CLEAR] IONQ — YES: EARLY★ RS↑↑, T5 thesis STRONG, earnings-free, MED conviction → BUY
[HOLD] NVDA — NO today: earnings May 20 (2d) — earnings-eve gate; thesis intact but timing wrong → BUY post-earnings
[WATCH] PLTR — NO: RS↓ vol divergence, 46x EV/Rev, $1.88B CEO insider selling → Wait for RS recovery
[SKIP v3] ASML — Would but can't: $1,502/share = 65% NAV, impractical allocation unit
[SKIP v3] AVGO — Would but low priority: RS↓, $425/share at v3 size = 18.3% NAV per share (exceeds MED cap)
```

### 5.8 Schizophrenia Cross-Domain Scan
```
Domain leap: "If the portfolio's real driver isn't AI, what is it?"
Hypothesis: Compute infrastructure scarcity (same structural pattern as 2020–2022 semicon shortage)
→ Quantum (IONQ) decorrelates because it competes for different physical resources (trapped ions ≠ fabs)
→ Observable: Confirmed May 17 — IONQ +1.2% on -1.24% market day
→ Implication for v3: IONQ as decorrelated anchor first, then semicon names (NVDA) after T1 event clarity

No [UNKNOWN DRIVER] flag needed — existing thesis explains the observable.
```

### 5.10 GAD Pre-mortem: IONQ

Scenario: IONQ -30% within 90 days of entry

| Path | Failure | Early Warning | Decision Rule |
|---|---|---|---|
| 1 | Q2 RPO stagnation / revenue scaling fails | Q2 earnings: RPO ≤ Q1 RPO | Sell all IONQ immediately |
| 2 | Federal quantum funding cut (DOD/DOE budget) | News: program cancellation, contract non-renewal | Sell all if >30% revenue at risk |
| 3 | Macro deterioration — VIX spike to DANGER (≥28) | VIX ≥28 sustained 2+ days | Do NOT sell on VIX alone; freeze new adds, hold existing |

Pre-mortem: ✅ BUY IONQ confirmed — 3 clear failure paths identified, all measurable

### 5.11 DR Conviction Audit: IONQ

| Check | Result |
|---|---|
| Evidence for MED conviction | EARLY★ RS↑↑ (price data), T5 STRONG (convergence tracker 3+ sources), decorrelated behavior (May 17 confirmed) |
| Narrative-only? | NO — data-backed |
| Conviction level | MED — validated |
| ROI base rate | Pre-revenue quantum names: median 1-year ±30%, high variance → MED sizing (not HIGH) appropriate |
| Upside-anchored? | NO — base case used |

```
DR Conviction Audit: IONQ → MED conviction: PASS
DR clean: Y
```

### 5.17 Alexithymia Stake Inventory
Stakes today:
1. v3 inception buy — sets anchor for multi-year tracking discipline
2. NVDA May 20 = binary T1/T2 event in 2 days; cash preservation for that decision matters
3. VIX 18.43 trending up — if post-NVDA miss spikes VIX to EXTENDED, only HIGH conviction buys allowed

### 5.18 Aphantasia — Exact Numbers

| Trade | Shares | Price | Amount | % NAV |
|---|---|---|---|---|
| IONQ BUY | 4 | $51.95 | $207.80 | 8.96% |
| Cash remaining | — | — | $2,112.20 | 91.04% |
| Post-NVDA NVDA (plan) | 1 | $225.32 | $225.32 | 9.71% |
| Post-NVDA PLTR (conditional) | 2 | $133.99 | $267.98 | 11.55% |
| Total if all deployed | — | — | ~$701.10 | ~30.2% |

### 5.19 BPD Stability Check
```
IONQ: T5 thesis STRONG in convergence, no kill conditions triggered → STABLE BUY
NVDA: T1 thesis STRONG, pre-earnings gate only (not thesis break) → STABLE HOLD-FOR-BUY
PLTR: RS bearish, valuation compressed, insider selling → NOT stable enough to buy today
No FOMO detected — buying into down market (SPY -1.40%) on merit, not momentum
```

### 5.20 CIP (Contribution Investment Plan)
```
Monthly contribution: $110/mo
Next contribution date: 2026-06-18
Current cash after IONQ: $2,112.20
Minimum reserve rule: ≥$400 cash always (floor = 4× monthly contribution)
Today's deployment: $207.80 → leaves $2,112.20 (well above $400 floor) ✅
```

---

## Step 6 — Recommendation

### Immediate Action (May 18, today)

| Action | Ticker | Shares | Price | Amount | % NAV | Conviction |
|---|---|---|---|---|---|---|
| **BUY** | IONQ | 4 | $51.95 | $207.80 | 8.96% | MED |
| HOLD | CASH | — | — | $2,112.20 | 91.04% | — |

**Rationale:** IONQ is the only viable v3 anchor today. EARLY★ RS↑↑, T5 Quantum thesis STRONG (thesis-convergence 3+ sources), earnings-free, decorrelation from semicon narrative confirmed (May 17). MED conviction sizing (8.96% NAV) appropriate for pre-revenue quantum company with high uncertainty.

**Kill conditions for IONQ (v3):**
1. Q2 2026 RPO ≤ Q1 RPO → SELL ALL
2. Federal quantum funding cut / contract loss >30% revenue → SELL ALL
3. VIX ≥28 for 2+ days → FREEZE adds only (do not sell on macro alone)
Hold horizon: 12+ months

---

### Post-NVDA Decision Tree (execute May 21+)

**Scenario A — NVDA beats + raises (Blackwell demand strong, hyperscaler capex guidance ↑):**
- BUY NVDA: 1 share × ~$225 = ~$225 (9.71% NAV, MED conviction anchor)
- If earnings call confirms strong guidance: optional 2nd share = ~$450 total, 19.4% NAV (approaching HIGH cap)
- T1 thesis validated → proceed to Week 2 additions

**Scenario B — NVDA in-line (meets consensus, neutral guidance):**
- BUY NVDA: 1 share only = 9.71% NAV (MED conviction)
- No adds until Q2 FY2026 data confirms trajectory

**Scenario C — NVDA miss / guidance cut:**
- HOLD ALL REMAINING CASH — T1/T2 thesis at risk
- Do NOT buy AVGO, CRDO, or any AI capex name until NVDA thesis re-verified
- Re-run /nick-weekly immediately after earnings with fresh kill condition check

---

### Week 2–3 Plan (May 22 – Jun 1) — Contingent on Scenario A/B

| Priority | Ticker | Shares | Price | Amount | % NAV | Conviction | Condition |
|---|---|---|---|---|---|---|---|
| 1 (if A) | NVDA | 1–2 | ~$225 | $225–$450 | 9.7–19.4% | HIGH/MED | Post-earnings confirmation |
| 2 (conditional) | PLTR | 2 | ~$134 | ~$268 | 11.5% | MED | RS must recover to NEUTRAL first |
| SKIP | AVGO | 0 | $425 | — | — | — | 1 share = 18.3% NAV, exceeds MED cap; impractical for v3 |
| SKIP | ASML | 0 | $1,502 | — | — | — | 1 share = 65% NAV; v3 rule — skip until NAV > $5K |

---

### Target Portfolio State (after 2–3 weeks, Scenario A)

| Ticker | Shares | Entry Price | Value | % NAV |
|---|---|---|---|---|
| IONQ | 4 | $51.95 | ~$208 | ~9% |
| NVDA | 1 | ~$225 | ~$225 | ~10% |
| PLTR (conditional) | 2 | ~$134 | ~$268 | ~12% |
| CASH | — | — | ~$1,619 | ~70% |

Cash reserve: ~$1,619 (70%) — preserves capital for May/June/July contributions + opportunistic adds.

---

## Step 7 — Candidate Sweep

No new candidates surfaced outside universe this session. ETF discovery script not run.

**Watchlist for next week:**
| Ticker | Thesis | Reason to Watch | Block |
|---|---|---|---|
| CRDO | T2 Semiconductor Moats | RS rising in previous signals, lower price point | Check price vs MED sizing |
| KTOS | T3 Space & Defense | Defense AI, more affordable than AVAV | Check earnings date |
| AVAV | T6 Robotics | Defense autonomy + space correlation | Check price |

---

## Step 8 — Research Pipeline Queue

Searches used this session: ~5 (via scripts)
Remaining budget: ~10 saved for post-NVDA session

---

## Step 8.5 — KB Update Requests

- **[2026-05-18] CRITICAL:** NVDA Q1 FY2026 earnings post-close May 20 — Blackwell demand + hyperscaler capex guidance = T1 thesis gate for v3. Run `/stock-content NVDA` the morning of May 21.
- **[2026-05-18] MED:** IONQ Q2 2026 guidance + RPO trend — first v3 position, kill condition monitoring begins immediately.
- **[2026-05-18] LOW:** CRDO current price + entry window — T2 Semiconductor Moats candidate for v3 Week 3+ expansion.

---

## Step 9 — Process Lesson

→ Appended to nick-soul.md separately.

---

*Session: Tier 3 | Searches used: ~5 (scripts) | NAV: $2,320.00 | Rec: BUY IONQ 4sh | Cash: $2,112.20*

---

## Update — 2026-05-18 Session 2 (post-system-check)

*State.json confirmed: positions = {} — IONQ buy above is still a pending recommendation.*

**Current prices (2026-05-18 live):**
- IONQ: $51.44 (vs $51.95 in rec above — lower = better entry ✅)
- NVDA: $222.93 | SPY: $740.31 | VIX: 18.63 (68th pct, multiplier 0.45x)

**NEW: Position size arithmetic — NVDA also impractical at current NAV:**
HIGH conviction cap = 15% × $2,320 × 0.45 = $156.60 < NVDA $222.93
→ NVDA joins ASML/AVGO on "v3 impractical" list. T1 exposure via NVDA requires NAV > ~$2,972 (~6 months)

**NEW candidates surfaced:**
- CBRS (Cerebras Systems) — T1 AI chips, IPO May 14, $5.5B deal → potential affordable T1 proxy. Price unknown. Research queue priority 1.
- BKSY (BlackSky) — T3 Space, EARLY★, $39.20 → affordable. Research queue priority 2.
- DCO (Ducommun) — T3 Space/Satellite, EARLY★, $145.18 → affordable. Research queue priority 3.

**ORDERS remain unchanged:**
```json
[
  {"action": "BUY", "ticker": "IONQ", "conviction": "med", "reason": "T5 quantum anchor, decorrelated from NVDA earnings risk, $51.44 confirmed live price"}
]
```

*Session 2 searches used: 5 | Total session: 10/15*
