# Nick Weekly — 2026-05-16

*Blinded portfolio manager — reads KB + prices only | ไม่ใช่คำแนะนำลงทุน*

---

## NAV Update

| | Since inception |
|---|---|
| Nick NAV | $10,063.15 (+0.63%) |
| SPY benchmark (proxy) | $739.17 vs $737.83 inception (+0.18%) |
| Delta vs SPY | **+0.45pp** |

**Position breakdown:**
| Ticker | Shares | Price | Value | vs Entry |
|---|---|---|---|---|
| NVDA | 13.95 | $225.32 | $3,143.22 | +4.80% |
| AVGO | 5.81 | $425.19 | $2,470.35 | -1.12% |
| ASML | 1.32 | $1,501.81 | $1,982.39 | -1.00% |
| PLTR | 10.95 | $133.99 | $1,467.19 | -2.19% |
| Cash | — | — | $1,000.00 | — |
| **TOTAL** | | | **$10,063.15** | **+0.63%** |

*Note: 50% QQQM + 50% SOXX inception prices not logged at init — using SPY as proxy. Flag for /nick-quarterly to establish clean benchmark baseline.*

---

## Holdings Review

### NVDA — Intact

- **Thesis:** CUDA moat + Blackwell ramp = irreplaceable AI training infrastructure for 18-24 months
- **Kill conditions check:**
  - ASIC displacement >15% hyperscaler training spend: No evidence — custom ASICs (Google, Meta) still share GPU capacity, not replacing
  - Capex collapse 2 consecutive quarters: NOT triggered — hyperscalers guiding >$200B AI capex FY2026
  - Export control >20% revenue: Existing restrictions only, no new material ones this week
- **nick-signals:** NEUTRAL RSI | MID vs MA20 | NEUTRAL RS
- **Rec:** **Hold**
- **Note:** Down -4.42% today in sector selloff — not thesis-driven. ⚠️ NVDA Q1 FY2026 earnings expected ~May 28 — watch for guidance on Blackwell allocation and hyperscaler demand trajectory.

---

### AVGO — Intact

- **Thesis:** Hyperscaler custom ASIC design wins (Google XPU, Meta MTIA) + AI networking = contracted, predictable revenue
- **Kill conditions check:**
  - Google/Meta cancel ASIC program: No evidence
  - Top 2 customers revenue -20% YoY: No evidence
  - AI networking revenue -15% YoY: No evidence
- **nick-signals:** NEUTRAL RSI | NEAR vs MA20 | NEUTRAL RS
- **Rec:** **Hold**
- **Note:** NEAR vs MA20 = ideal entry zone signal. If thesis strengthens post-earnings (est. ~June 5), add could be warranted. -1.12% from entry = noise.

---

### ASML — Intact

- **Thesis:** EUV monopoly + High-NA upgrade cycle = no viable competitor 5-10 years
- **Kill conditions check:**
  - Export ban forced by Netherlands/US: No new material restrictions this week
  - Guidance -20% YoY for 2 consecutive quarters: Not triggered
  - New lithography tech (DSA/e-beam) volume production: Not triggered
- **nick-signals:** NEUTRAL RSI | MID vs MA20 | **STRONG RS**
- **Rec:** **Hold**
- **Note:** STRONG RS despite -1.00% from entry = smart money rotating in while tech sells off. Highest-conviction hold in portfolio.

---

### PLTR — Intact (monitoring)

- **Thesis:** AIP platform = LLMs into actionable gov + enterprise workflows; 20+ years classified integration advantage
- **Kill conditions check:**
  - 2+ large gov contracts lost: No evidence
  - Commercial AIP ARR growth <20% YoY for 2 quarters: Not triggered
  - Stock -40% without earnings deterioration: -2.19% from entry = nowhere near
- **nick-signals:** NEUTRAL RSI | NEAR vs MA20 | **WEAK RS**
- **Rec:** **Hold — monitor**
- **Note:** WEAK RS (underperforming SPY >3% over 10d) = sector rotation out. Not a kill condition but pattern to watch. If WEAK RS persists 3+ weeks without thesis news, flag for trim discussion.

---

### Cash ($1,000 — 10%) — Hold, no deployment this week

**T3 status:**
- RKLB: $124.77 — above original $85-90 trigger. New insight: $2.2B backlog + Neutron contract signed May 2026 = thesis structurally stronger. BUT: nick-signals = NEUTRAL RSI | **EXTENDED vs MA20** | STRONG RS. EXTENDED MA20 → sizing rule says 0.5x or wait. Not deploying today.
- ASTS: $83.67 — FCC approved (removes regulatory kill condition), BUT Q1 miss $14.7M vs $36.6M est (60% miss) + contradiction-registry flag. Revenue timing risk elevated. Pass.
- KTOS: $52.09 — Real revenue ($1.35B), Valkyrie scaling to 40 units/year, $447M Space Force contract. WEAK RS this week in broader selloff. Interesting but not urgent.

**T5 emerging:**
- IONQ: $51.95 (-9.61% today) — T5 anchor per KB. FY2026 guidance $260-270M, Q1 beat by 30%, $470M RPO. Strong commercial momentum. nick-signals (May 11): NEUTRAL RSI | MID vs MA20 | STRONG RS. Today's -9.61% likely sector selloff (SOXX -4.06%), not thesis-driven.
- Preliminary conviction: **medium** (8% NAV = ~$800) — but don't deploy into a down day.
- Decision: **Watch IONQ next week**. If stabilizes above $48-50, evaluate $300-500 entry (3-5% NAV = low-med conviction sizing matching remaining cash).

**Revised T3 deploy trigger:**
- RKLB: New target $100-110 range (prior resistance now support after Neutron catalyst)
- KTOS: Entry at $48-52 range (current level is borderline — wait for RS stabilization)

---

## Earnings Watch (next 4 weeks)

| Ticker | Est. Date | Event | Nick priority |
|---|---|---|---|
| NVDA | ~May 28, 2026 | Q1 FY2026 earnings | HIGH — Blackwell demand + hyperscaler guidance |
| AVGO | ~June 5, 2026 | Fiscal Q2 earnings | HIGH — XPU design win updates + networking |
| RKLB | ~May 2026 (est.) | Q1 2026 earnings | MED — Neutron timeline confirmation |

*ASML Q2 est. July. PLTR Q2 est. August.*

---

## Changes recommended

- **No changes this week** — all 4 holdings intact, no kill conditions triggered
- **Cash: hold** — don't deploy into today's broad semiconductor selloff (-4% SOXX)
- **Watch list for next week:** IONQ stabilization, RKLB/KTOS pullback, NVDA pre-earnings positioning

---

## ORDERS

```json
[
  {"action": "NONE", "ticker": "NVDA", "conviction": "high", "reason": "Intact — hold through earnings May 28"},
  {"action": "NONE", "ticker": "AVGO", "conviction": "high", "reason": "Intact — NEAR MA20, wait for earnings add signal"},
  {"action": "NONE", "ticker": "ASML", "conviction": "high", "reason": "Intact — STRONG RS, highest conviction hold"},
  {"action": "NONE", "ticker": "PLTR", "conviction": "med", "reason": "Intact — monitoring WEAK RS, no action yet"},
  {"action": "NONE", "ticker": "CASH", "conviction": "med", "reason": "Hold $1,000 — don't deploy into down day; IONQ watch next week"}
]
```

---

## KB Gaps — Research requests

| Priority | Topic | Why needed | Suggested command |
|---|---|---|---|
| High | NVDA Q1 FY2026 earnings | Kill condition check: Blackwell guidance + hyperscaler demand | `/pre-market` on May 28 |
| High | IONQ current prices + Q2 2026 guidance | Cash deployment decision next week — need RPO trend confirmation | `/stock-research IONQ` |
| Med | RKLB Q1 2026 earnings + Neutron timeline update | Revised entry trigger ($100-110) needs earnings confirmation | `/stock-research RKLB` |
| Med | AVGO Q2 earnings preview | XPU revenue mix + AI networking growth | Await June 5 |
| Low | KTOS Valkyrie production ramp status | Potential T3 entry at current price range | `/research-idea KTOS defense drone` |

---

## Nick's note

Portfolio is +0.63% vs SPY +0.18% after 6 days — a thin but positive spread. The portfolio's core risk is concentration: NVDA (30%) + AVGO (25%) are both T1/AI infra plays that will correlate strongly in any AI sentiment reversal. ASML (20%) with STRONG RS provides partial non-correlation. Cash optionality ($1,000) is worth protecting through this earnings season — NVDA and AVGO reporting within 3 weeks makes this the wrong week to deploy into new positions.
