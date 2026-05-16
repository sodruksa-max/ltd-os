---
type: misophonia-triggers
description: Learned anomaly trigger patterns — fire immediately on pattern match, cannot be suppressed. Append-only.
updated: 2026-05-17
---

# Misophonia Trigger Registry

Patterns learned from experience that cannot be ignored when matched in any analysis, transcript, or market data. Read before every Vera audit and pre-market data scan.

## How to use

- **Vera (stock-content):** check every source document against this registry — any match → `[MISOPHONIA: TRIGGER] <pattern>` — must be addressed, cannot be explained away or skipped
- **pre-market:** check overnight data against market-level triggers — any match → `[MISOPHONIA: MARKET TRIGGER]` — escalate to primary concern regardless of other signals

## Format per entry

```
[CATEGORY] <trigger pattern> | First seen: <date> | Context: <why this is a trigger> | Action: <what to do on match>
```

---

## Company-Level Triggers (Vera / stock-content)

[MANAGEMENT] "exploring strategic alternatives" | First seen: — | Context: signals potential sale, distress, or major pivot — often precedes bad news | Action: flag as top-priority risk; verify context before proceeding
[MANAGEMENT] CFO departure before earnings | First seen: — | Context: CFO exits before earnings = elevated probability of negative surprise | Action: downgrade conviction; add to contradiction-registry
[ACCOUNTING] "revenue recognition change" | First seen: — | Context: accounting change that optically inflates revenue | Action: find unadjusted numbers; flag [HYPERLEXIA: ADJUSTED METRIC]
[ACCOUNTING] "material weakness" | First seen: — | Context: internal control failure — reported numbers may be unreliable | Action: immediate [MISOPHONIA: TRIGGER]; treat as potential kill condition
[ACCOUNTING] auditor change mid-cycle | First seen: — | Context: switching auditors mid-year signals accounting irregularities | Action: search for reason; flag as high-severity contradiction
[DILUTION] "at-the-market offering" | First seen: — | Context: company selling shares continuously into market — silent dilution | Action: calculate dilution rate; flag if > 5% of float in 6 months

---

## Market-Level Triggers (pre-market)

[STRUCTURE] VIX term structure inversion (front month > back month) | First seen: — | Context: near-term fear exceeds long-term — sharp directional move imminent | Action: [MISOPHONIA: MARKET TRIGGER]; force confidence = low regardless of scenario
[CREDIT] Credit spreads widening while equities flat or up | First seen: — | Context: bond market sees risk equities haven't priced yet | Action: flag divergence; bias toward Bearish or Base scenario
[MACRO] Oil decoupling — oil up while equities flat or down | First seen: — | Context: stagflation signal — cost-push inflation without growth | Action: flag; check Fed reaction probability; add to risk table
[FLOW] Major index gap-up on declining volume | First seen: — | Context: institutional distribution into retail buying — often precedes reversal | Action: flag; do not extend Bullish confidence

---

## How to append new triggers

After any post-market review or Vera audit that surfaces a pattern worth remembering permanently:

1. Identify the pattern precisely (exact phrase or measurable condition)
2. Append to the relevant section using the format above
3. Update `updated:` date in frontmatter

**Pruning rule:** If a trigger has produced ≥ 5 false positives and 0 true positives over 6+ months → remove and note why it was pruned.
