---
council_topic: ควรเริ่ม project trading-foundations แบบไหนดี
expertise_lens: financial_risk
date: 2026-04-25
phase: expertise
---

# Financial Risk Lens: trading-foundations project start

---

## 1. Gate Metrics — Are Win Rate >= 40% + R-Multiple >= 1.5 Sufficient?

The skeptic's critique lands correctly but doesn't go far enough. The specific failure mode: paper trading removes the mechanism that causes most beginners to fail gates — the inability to hold a position through drawdown when real money is on the line. A paper trader sees a -12% position and holds comfortably; a real-money trader at -12% feels compulsion to exit before the -25% hard stop is hit. The result is a paper journal full of trades that respected the system, producing win rate 42% and R-multiple 1.6, while real-money behavior will clip winners early and ride losers longer.

The gate metrics are necessary but not sufficient as a readiness signal. What they measure is: "can this person execute a trading system on a spreadsheet?" They do not measure emotional execution under loss, decision quality at 3 concurrent losing positions, or discipline to sit flat when no setup qualifies.

**Minimum additional gate**: the paper journal must show at least 3 instances of a stop-loss being hit and honored (trade closed at stop, not held or modified). Exits-at-stop in paper trading are also easy to fake, but requiring documented stop hits creates a structural trace.

---

## 2. Capital at Risk in Month 7+ — Realistic Drawdown Scenarios

Starting capital deployed: 10,000 THB. Risk per trade: 500 THB (5%). Max concurrent: 4 positions = 2,000 THB at risk simultaneously.

Base rates for beginning momentum traders: retail momentum beginners underperform their paper results by 15–30 percentage points in the first 3 months of real trading. If paper R-multiple was 1.5, realistic first-quarter real R-multiple is likely 0.9–1.2.

**Scenario table (first 3 months real trading, ~24 trades):**

| Scenario | Win rate | Avg R | Net result |
|---|---|---|---|
| Best (paper performance holds) | 42% | 1.5R | +2,520 THB |
| Median (behavioral decay) | 33% | 1.1R | -660 THB |
| Worst (5th percentile) | 25% | 0.7R | -4,200 THB |

The worst case on a 10K deployment is -4,200 THB — 42% drawdown of the real-money tranche but only 4.2% of total 100K capital. The structural protection (keeping Month 7 capital at 10K) works correctly.

The risk is not the absolute numbers. The risk is the behavioral response to a -42% drawdown on the live tranche: pressure to "make it back," which is the classic trigger for rule violation.

---

## 3. Risks None of the Three Proposals Address Adequately

**USD/THB currency risk is entirely absent from all three proposals.** Trading US stocks means exposure in USD. A 500 THB risk-per-trade calculation is wrong at execution — the actual risk is denominated in USD and converted at exit, not entry. A position sized to risk 500 THB at 36 THB/USD could risk 520 THB if USD weakens to 34 THB/USD during the hold. The journal template must record USD amounts separately from THB equivalents.

**Brokerage costs against small position sizes.** At 10K THB deployed across positions, typical per-trade costs (IB minimum commissions, FX conversion spread) can be 0.1–0.3% per side. On a 2,500 THB position, round-trip cost is 50–150 THB. Against a 500 THB risk budget, fees alone represent 10–30% of the risk unit. Real R-multiple targets should be recalibrated: the 1.5R gate, net of fees, requires gross R closer to 1.7–1.8.

**No proposal specifies a "restart from paper" trigger.** If Month 7–9 real-money performance is poor, what is the structured protocol to revert? The proposals treat paper-to-real as a one-way gate. It needs to be bidirectional with a specific trigger: if real-money win rate falls below 30% over 15+ trades, return to paper-only and do not re-enter real money for 60 days.

---

## 4. Which Proposal Best Protects Capital During the Transition

The **Pragmatist's structure best protects capital**, specifically for one reason the proposal itself understates: the requirement to document stop price and target *before entry* is the single most important capital protection mechanism available before real money starts. It forces the R-multiple calculation to be honest at trade selection, not retroactively adjusted in the journal. This pre-trade documentation habit, built over 20+ paper trades, is the only way to make the R-multiple gate metric meaningful.

The Skeptic's sequencing is correct philosophically but the 3-month "no code, no content" lockout doesn't accelerate capital protection any more than the Pragmatist's module sequencing, and delays building the journal infrastructure that is the actual protection mechanism.

The Optimist's parallel-track approach introduces a specific capital risk: **identity investment in content before trading performance is established creates pressure to trade more actively to generate content, potentially increasing trade frequency beyond the 4-position-max rule.**

---

## 5. Critical Warning for DECISION.md

> **The paper-to-real gate is not a one-way door.** The gate metrics (win rate ≥40%, R-multiple ≥1.5) authorize *entry* into real trading — they do not authorize *staying there*. If real-money trading produces a win rate below 30% over any 15-trade window, the mandatory action is full return to paper-only for a minimum 60-day reset. This rule must be committed to before Month 7. The behavioral risk is that a losing real-money trader rationalizes continued trading because "I need more data" or "market conditions are unusual." The antidote is a pre-committed, non-negotiable reversion rule that does not require judgment at the moment it triggers.

---

## Hard Questions for User

1. When your first real-money position hits -20% (not if — when), what do you do at 11pm when you can't sleep and the US market opens in 10 hours?
2. The first 3-month median scenario is -660 THB net loss. Can you treat that as tuition and continue executing the system, or does any real-money loss feel like failure?
3. Why is USD/THB risk not in any of your existing PREFERENCES trading rules? Does your broker show P&L in USD or THB, and have you verified which is your accounting currency?
