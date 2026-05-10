---
council_topic: Nick Auto-Trader + Self-Improvement System
phase: cross-critique
date: 2026-05-10
---

# Cross-Critiques — 12 critiques (each proposer critiques the other 3)

Format per critique: **Steelman** (best argument FOR the target) | **Weakness** (specific flaw) | **Question** (one thing the proposal doesn't answer)

---

## OPTIMIST → PRAGMATIST

**Steelman:** The base-rate grounding (90% of retail algos overfit on thin data, 30-50 trades minimum for statistical validity) is the most empirically honest number in any proposal. The EXTENDED conflict resolution rule — "no entry, hold existing, queue for pullback" — is elegant precisely because it is binary. Binary rules don't have edge cases.

**Weakness:** "1-2 positions at a time" on a $10K paper NAV at 5% risk = $500 per position. At that size, Alpaca paper order fill prices and bid-ask spread noise dominate any P&L signal. The pragmatist raises the $500-vs-$5K sizing question but doesn't answer it. If paper trades are sized at $500 and real money trades will be sized at $5K+, the paper results are not comparable to live results — they measure a different regime of market impact.

**Question:** If Nick can only hold 1-2 positions at a time across 4 theses and 15 tickers, what is the explicit prioritization rule when 3 tickers are simultaneously EARLY with active theses? Highest conviction score? First EARLY in screen output? Random? This decision determines the learning signal more than any other parameter.

---

## OPTIMIST → SKEPTIC

**Steelman:** The 50-trade threshold before any proposals are generated is more honest than my N=20. The "Nick Observed" reframing is excellent — it names the system accurately (an observer, not a decision-maker) and removes the illusion of autonomy. The pre-mortem structure (what does failure look like, what is the worst case, survivorship bias check) is the right framework for designing any system that touches real capital decisions.

**Weakness:** The skeptic's three failure modes (KB corruption, thesis-vs-tier confusion, kill condition blindspot) are all identified in the brief itself — which means they are known risks preventable by design, not surprises. Naming the failure modes without specifying the design rules that prevent them converts a risk analysis into a list of warnings. The proposal ends at "don't do this yet" without answering "what exactly changes when you do."

**Question:** If Nick reaches 50 closed trades but 45 of them are T1 AI Capex (T3 Space had no EARLY setups in 4 months), what does the monthly proposal say about T3 Space conviction? You cannot update on zero trades. Does the skeptic's system flag thesis-level data gaps, or silently leave stale conviction scores unchanged while appearing to have "done calibration"?

---

## OPTIMIST → CAVEMAN

**Steelman:** The 30-day shadow mode before any execution is genuinely the lowest-risk first step possible. It costs nothing — no Alpaca orders fire, no KB is touched — and produces a validation dataset of 20-30 hypothetical picks that can be reviewed by a human before the machine runs live. If the picks look insane in shadow mode, you haven't lost anything.

**Weakness:** The caveman identifies what NOT to do but does not specify what the approved system looks like after the gates are passed. "Nick executes entries/exits, logs everything" is a description of a system that needs to be designed. After 30 shadow picks and 20 closed trades, what code runs, what does it read, what does it write, and where does it fail safely? The proposal stops at the point where the real design decisions start.

**Question:** If shadow mode logs 30 "would-have-traded" picks and 22 of them show hypothetical losses, what is the decision rule? Is that a signal that the system is broken, or that May 2026 was a bad momentum month? Shadow mode produces interpretable signal only if you establish the interpretation criteria before running it — not after seeing the results.

---

## PRAGMATIST → OPTIMIST

**Steelman:** The insight that the infrastructure gap is thin ("80% already built") is correct and important. The runner reads universe-screen output and translates it to Alpaca orders — that is genuinely a thin integration layer, not a research problem. The separation of concerns (runner vs exit watcher vs logger vs analyzer) makes each layer independently testable and replaceable.

**Weakness:** The exit watcher "runs intraday every 30 min" — this requires a persistent process running during US market hours (9:30 AM–4 PM ET). On a Windows machine with no cloud compute, that process will fail when the machine is asleep, rebooted, or the internet drops. The optimist proposal treats the exit watcher as a given but doesn't address the reliability problem: this is the most critical layer (missing an exit = uncapped loss), and it's also the layer most likely to fail in a home setup.

**Question:** When the exit watcher fails to run and a position hits -25% without triggering the hard stop, what is the recovery protocol? Does the daily morning runner detect missed exits and act on them? The proposal describes the exit watcher's function but not its failure mode — which for a risk-management layer is the most important design detail.

---

## PRAGMATIST → SKEPTIC

**Steelman:** Centering the worst-case scenario (KB degrades T1/T2 just before real money phase) is exactly correct. This is the highest-stakes failure because it is silent, slow, and only becomes visible after real money has been committed based on corrupted data. The skeptic is right to call this out loudly. The "survivorship bias check" — most algo systems fail quietly, not dramatically — is an important calibration on optimism.

**Weakness:** The skeptic identifies three failure modes that are all preventable by design (KB corruption → threshold rule; thesis-vs-tier confusion → conflict resolution rule; kill condition blindspot → human flag policy). Identifying preventable risks and recommending "freeze self-improvement" is a postponement, not a solution. The skeptic's conservative alternative ("Nick Observed") is identical to Phase 1 of every other proposal — the skeptic just calls it a permanent state instead of a phase.

**Question:** If the self-improvement loop is frozen until 50 trades and the human reviews monthly summaries but doesn't update THESIS_TRACKER (because the summaries are mixed and inconclusive), the KB stays static for 6-9 months while market regime shifts. How does the skeptic's system handle KB staleness — a failure mode that is arguably more dangerous than KB corruption, because stale data silently biases every decision without any update history to audit?

---

## PRAGMATIST → CAVEMAN

**Steelman:** "No KB writes until 20+ closed trades" is the strongest single operational rule in any proposal. It is specific, verifiable, requires no infrastructure to enforce, and it directly addresses the highest-risk failure mode (self-improvement on noise). This rule should appear verbatim in whatever system gets built.

**Weakness:** The caveman's shadow mode → human reviews picks → then execution structure has no design for what "execution" means. The proposal ends at the moment the real architecture decisions begin. It's strong on what not to do, silent on what to do after the gates are cleared. Shadow mode for 30 days is a reasonable validation step, but it doesn't produce a system — it produces a dataset that still needs a system designed around it.

**Question:** After shadow mode + 20 closed trades, the human gate approves KB updates proposed by Nick. What format are those proposals in? A markdown file? A Slack message? A diff of THESIS_TRACKER? The caveman's approval gate requires a proposal format to exist before the gate has any meaning — without that, "human blocks it" is a policy with no mechanism.

---

## SKEPTIC → OPTIMIST

**Steelman:** The proposal-only self-improvement design (human gate before any KB write) directly neutralizes the highest-risk failure mode. The 5-layer architecture maps cleanly to testable units. The risk table is honest about what can go wrong and provides specific mitigations rather than just acknowledging risk.

**Weakness:** N=20 closed trades per thesis as the threshold for enabling the weekly analyzer is too low. With 4 theses, 20 total closed trades could mean 5 per thesis — and 5 trades per thesis produces a confidence interval so wide that any conviction score update would be statistically unjustifiable. The optimist says the proposal file will include CI and trade count, but at N=5 per thesis, the honest CI-annotated proposal would read "insufficient data" every time. The threshold needs to be per-thesis, not total.

**Question:** The optimist says the analyzer "runs in read-only mode" below N=20 closed trades total. What does it log in read-only mode, and where does that log go? If the pre-threshold patterns are not surfaced to the user, there is zero learning for the first 3-4 months of operation — which removes the main argument for automation over manual trading.

---

## SKEPTIC → PRAGMATIST

**Steelman:** The EXTENDED conflict resolution rule ("no entry, hold existing, queue for pullback") is the most operationally precise decision rule in any proposal. A binary rule that handles the thesis-active-but-EXTENDED case with a clear output — do not enter, note it, wait — eliminates the ambiguity that would cause a code-level bug in any other proposal's handling of this case.

**Weakness:** "Runs 9:00 AM ET via GitHub Actions cron" introduces three external dependencies: GitHub's cron scheduler, the Actions runner pool, and Alpaca's paper API — all of which have latency or availability gaps at market open. GitHub Actions is not a real-time system; free-tier runners queue behind paid workloads and can start 2-8 minutes late. A 9:07 AM entry instead of 9:00 AM is fine for paper trading but locks in an infrastructure pattern that will need to be completely replaced for live trading. This is a technical debt the pragmatist doesn't acknowledge.

**Question:** The pragmatist's open questions section raises the most important design question: is 5% risk-per-trade on the $10K paper NAV ($500) or on the $100K experiment fund ($5,000)? This 10x sizing difference changes whether paper results have any predictive validity for live performance. If paper trades are $500 and live trades will be $5K, the slippage, spread, and behavioral dynamics are different enough that 6 months of paper data may not transfer. The proposal raises this question but leaves it open.

---

## SKEPTIC → CAVEMAN

**Steelman:** "Thesis bot acting daily = momentum bot in disguise" is the most important conceptual warning across all proposals. Frequency mismatch between signal cadence and action cadence is how thesis-based systems silently become something else. This should be a hard rule in the final design: Nick's action frequency must match the thesis holding period, not the screening frequency.

**Weakness:** The 20-trade rule for blocking KB updates is presented as the central guardrail, but the proposal doesn't say where 20 comes from. Is it 20 total, or 20 per thesis? A rule that can't be defended with a statistical rationale is a heuristic dressed as a threshold. The skeptic proposal uses 50 with a reference to statistical validity; the caveman uses 20 without grounding.

**Question:** The caveman's kill switch is "Nick proposes any KB conviction update before 20 closed trades = human blocks it." What happens to the blocked proposals? Are they stored, dated, and reviewed later to see whether the blocked update would have been correct? If blocked proposals disappear, you lose the ability to evaluate whether the 20-trade threshold was the right number — and you can never tighten or loosen it with evidence.

---

## CAVEMAN → OPTIMIST

**Steelman:** Five layers with clear jobs. Runner → exit watcher → logger → analyzer → human gate. Each layer does one thing. The human gate is at the end, not the beginning — that is right. Let the machine gather data; human touches only the update.

**Weakness:** Five layers = five things that can break. Exit watcher goes down, positions bleed. Analyzer misfires, bad proposal lands in human inbox, human rubber-stamps it, KB is poisoned. Too many moving parts. The optimist built a machine that trusts five sub-machines to work together without failure. Simpler machine, fewer breaks.

**Question:** Between trade 1 and trade 20, who watches the machine? The analyzer runs read-only and the human sees nothing. If the runner logic has a bug — say, it enters positions at ALERT tier on killed theses because THESIS_TRACKER wasn't updated — the bug runs for 20 trades before anyone reviews. What is the check between go-live and the first meaningful review?

---

## CAVEMAN → PRAGMATIST

**Steelman:** One job. Machine runs every morning. Does one thing. Stops. That is good survival design. One job is less likely to break quietly than five.

**Weakness:** GitHub Actions + Alpaca paper API = two walls between the signal and the action. If internet drops, cron misses. If GitHub has issues, runner skips. If Alpaca changes its paper API, positions are not updated. Three places where "everything looks fine" but nothing happened. Silence from a daily batch looks exactly like success.

**Question:** If the daily batch runner fails silently (no error, no log, just didn't run) and an open position hits its hard stop price, who catches it? The proposal doesn't define what happens to open positions when the executor goes dark. A machine with silent failure modes is more dangerous than one that fails loudly.

---

## CAVEMAN → SKEPTIC

**Steelman:** "Nick Observed" is the right name. It is honest. An observer that logs what it sees is safer than a trader that acts on what it guesses. Good name = clear thinking about what the machine actually is.

**Weakness:** 50 trades before proposals. That is 6-9 months at thesis cadence. During that time, the market regime will change. The theses may change. The conviction scores in THESIS_TRACKER may be stale by the time the first proposal is generated. Waiting too long for safety can create a different kind of wrong: KB that doesn't reflect what the machine actually learned.

**Question:** The skeptic wants monthly human review of proposals. But the human is also reviewing trades every week. How much time does this system cost the human each month — in minutes, specifically? If the review cost is more than 30 minutes per week total, the human will stop reviewing, the gate will become a rubber stamp, and the safety mechanism is theater.
