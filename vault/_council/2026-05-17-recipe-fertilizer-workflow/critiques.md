---
phase: 3-cross-critique
council_topic: Recipe + Fertilizer Workflow Design
date: 2026-05-17
---

# Cross-Critiques (12 total)

Format per critique: **Steelman → Weakness → Hard question**

---

## Optimist critiques

### Optimist → Pragmatist

**Steelman:** The 8-week hard gate is the right instinct. One variable per test cycle is genuine agricultural science discipline. Manual-first before slash commands is well-grounded in the trading system precedent.

**Weakness:** 8 weeks is arbitrary for palm oil. Published response timelines suggest 3-6 months for meaningful yield signals. An 8-week gate gives the user a false sense of enough data — they approve v2 at week 9 on leaf color alone, still with insufficient evidence. The gate needs to be calibrated to the specific outcome metric, not a fixed number.

**Hard question:** If the observation at week 8 is ambiguous ("trees look about the same"), does the user advance anyway because the gate says 56 days? Or does the system require a *positive* observation, not just a *minimum elapsed time*? The proposal doesn't distinguish between time-based and evidence-based gating.

---

### Optimist → Skeptic

**Steelman:** The pre-mortem is the strongest section of any proposal. Naming the 60% failure mode (observation data never filled in at 3 months) is realistic and the calendar reminder mitigation is correct. The conservative alternative (recipes only first) is genuinely the lowest-risk path.

**Weakness:** Sequential domain start ("fertilizer first, then recipes after it's stable") will likely produce zero recipes for 6+ months because fertilizer is never "stable" — it is always in the middle of a test cycle. In practice, sequential means "recipes deferred indefinitely." The Skeptic's own pre-mortem should include "domain sequencing causes permanent deferral of the second domain."

**Hard question:** What is the explicit condition that would signal "fertilizer system is stable enough to start recipes"? Without a concrete trigger, the Skeptic proposal collapses into infinite sequential deferral.

---

### Optimist → Caveman

**Steelman:** The 2-minute write rule is the most actionable insight in any proposal. The physical gut check — food failure costs one meal, fertilizer failure costs a season — is exactly the right way to frame asymmetric stakes for a non-technical user. "One specific change per version" is scientifically correct one-variable discipline.

**Weakness:** The caveman template has no research integration step. "Base reference: where you learned it" is not the same as citing a mechanism from a paper. A formula that tastes good but has no understanding of why it tastes good cannot be improved systematically — user is back to guessing every version.

**Hard question:** If the user cooks v1 and it tastes great, what happens next? The caveman proposal says "What to try next: one specific change" — but why change something that worked? The template implies you always need to iterate, which is wrong. A formula that is already good should be declared finished, not perpetually iterated.

---

## Pragmatist critiques

### Pragmatist → Optimist

**Steelman:** The cross-domain KB with mechanism tags is the strongest architectural insight in any proposal. Microbial decomposition and fermentation chemistry overlap — a shared insight-atom layer genuinely surfaces this. The `/formula-ready` production gate is the correct accountability mechanism: minimum iterations, minimum citations, no unresolved contradictions.

**Weakness:** The optimist proposes "Phase 0 — research intake before every new formula." This will kill iteration velocity. A user who must do a `/paper-survey` before they can start any recipe will stop starting recipes. Research-first is the "analysis paralysis" failure mode the Skeptic names correctly. Research should be optional-before and triggered-by-failure, not mandatory-before.

**Hard question:** The v1.md template has a required `sources:` field with a reviewer warning if empty. But what if the user's hypothesis is "I think more fish sauce will help" — a valid culinary intuition that does not require a paper? Does an empty sources field block them? If yes, you've made the tool hostile to tacit knowledge. If no, the "required field" is toothless.

---

### Pragmatist → Skeptic

**Steelman:** The "build no slash commands yet" position is correct. The "one domain first" sequencing argument is also correct in principle — the user's attention bandwidth is not infinite. The "10 iterations before justifying a command" threshold is a reasonable empirical bar.

**Weakness:** The Skeptic's proposal requires getting a soil test before starting any fertilizer work. This adds a prerequisite that may take weeks to months to arrange in rural Thailand. Waiting for a soil test before starting any knowledge system means zero progress for the first quarter. The system can log incumbent practices (current formula if any, current cost, current leaf condition) right now — that IS the baseline, even without a formal soil test.

**Hard question:** The Skeptic says "if by month 3 there is no observation data → retire the system." But the system is just markdown files. "Retiring" it means deleting 3 markdown files. What's the cost of NOT retiring it? The stop condition framing suggests high infrastructure cost when the actual cost of an inactive vault folder is zero.

---

### Pragmatist → Caveman

**Steelman:** The "do not start both on day one" conclusion is empirically correct. The 2-minute friction rule is the most realistic constraint any of the proposals imposes. The "when to stop" section (5 versions still bad = wrong base recipe) is useful heuristic knowledge that none of the other proposals includes.

**Weakness:** The caveman proposal has no version numbering for fertilizer. "palm-formula.md" with an append log means the file becomes a single long document with no way to roll back to a specific application state. When yield drops in season 3 and the user wants to know what they applied in season 1, a flat append log is not a reliable record. The Caveman rejects version files but they exist precisely to solve this problem.

**Hard question:** "Write what you put in. Write what happened. Stop." — what does "happened" mean for fertilizer? New frond count? Bunch weight? Leaf color? "What happened" is too ambiguous for a domain where the observation requires defining the measurement. Without defining what you're measuring before you apply the formula, the observation is unfalsifiable.

---

## Skeptic critiques

### Skeptic → Optimist

**Steelman:** The shared insight-atoms KB with domain tags is technically elegant and avoids duplicating infrastructure. The 60-day gate for fertilizer is the right instinct. Production status gate (`/formula-ready` with 3-iteration minimum and source citation check) is the kind of accountability mechanism that prevents premature declaration.

**Weakness:** The Optimist proposes zero new commands for "2 weeks" then immediately proposes 2 commands (`/formula-log`, `/formula-ready`). But the trading system precedent (DECISIONS.md) shows that commands built at week 2 get iterated through 3+ council rounds before stabilizing. Two weeks of manual workflow is not sufficient validation for command design. The 2-week threshold is optimistic — it should be at minimum 5-10 real iterations with real data, which is 4-8 weeks for the food domain alone, and 4-6 months for fertilizer.

**Hard question:** The cross-domain KB with mechanism tags sounds compelling, but who defines the tag taxonomy? `maillard-reaction` and `NPK-ratio` are obvious. But what about `fermentation` (applies to both domains), `microbial-balance` (applies to both), `heat-transfer` (applies to food only?). Without a controlled vocabulary defined upfront, the tags will fragment organically and cross-domain search will surface false positives. Who maintains the taxonomy?

---

### Skeptic → Pragmatist

**Steelman:** The shared status vocabulary (`draft`, `active-trial`, `approved-baseline`, `superseded`, `failed`) is the strongest operational contribution in any proposal. Consistent status across domains makes the system queryable. The "research never merged into formula files" separation is correct — cross-contamination of evidence and hypothesis is a common failure in personal knowledge systems.

**Weakness:** The Pragmatist claims "one new top-level folder" for `vault/50_formulas/`. But the proposal also adds `vault/10_research/recipes/` and `vault/10_research/fertilizer/` — two new subdirectories inside an existing folder. And insight-atoms get new `domain:` tags. And `_assets/formulas/` gets created. The "minimal infrastructure" framing understates what is actually being added. This matters because CLAUDE.md has a hard rule: "Don't create new top-level folders without asking."

**Hard question:** The proposal says "after 4 weeks and 5 real cycles, assess friction." But for fertilizer, 5 cycles means 5 separate applications on different trees over 8+ weeks each — that's 40+ weeks minimum. Does "5 real cycles" mean 5 recipe iterations + 1 fertilizer application? If fertilizer and recipe cycles count differently, the 4-week / 5-cycle threshold means something very different for each domain.

---

### Skeptic → Caveman

**Steelman:** "Start with ONE recipe. Track it perfectly for one month. Then add fertilizer." is the only proposal that explicitly sequences the habit formation before the high-stakes domain. This is correct. The gut signal UNEASY is honest — two domains, two speeds, one unproven tracking habit. The Caveman is the only proposer who is worried about the right thing.

**Weakness:** The Caveman template has the user fill in "What to try next: one specific change" at the end of every session. This implies the user always knows what to change. But for a new formula developer with no food science or soil science training, the bottleneck is not tracking — it is knowing WHAT to change. "Change one thing" is only useful if the user has a hypothesis. The Caveman assumes tacit knowledge that may not exist yet.

**Hard question:** The Caveman says "3 people eat it and say good" is the readiness test for food. But what if the 3 people like food that is not the flavor profile you are developing toward? If you're developing a Southern Thai recipe and your 3 tasters prefer Central Thai flavors, their positive feedback moves you in the wrong direction. Who defines the taste target before iteration begins?

---

## Caveman critiques

### Caveman → Optimist

**Steelman:** One pipeline makes sense. Don't build two caves. The research-before rule is good — you should know why you're putting each thing in before you put it in. The "approved-baseline" gate is a real thing: a formula that works should be locked and called done.

**Weakness:** Too many steps before you touch the formula. Phase 0 (research), Phase 1 (creation), Phase 2 (testing), Phase 3 (version advance), Phase 4 (production declaration) — that is 5 phases before the food reaches the table. A cook does not do 5 phases. A cook cooks. The system will feel like homework before the first bowl of food.

**Hard question:** The 60-day fertilizer gate. What does the user DO for 60 days? Check trees? Write notes? If there is no clear action for the user during the waiting period, they will forget the system exists. What is the concrete task for day 15, day 30, day 45?

---

### Caveman → Pragmatist

**Steelman:** 8-week hard block is right for fertilizer. Trees are slow. Changing formula every week is like changing your hunting spot every day — you never learn where the game is. The "manual first" rule is correct. Build nothing until you know you will use it.

**Weakness:** The shared status vocabulary (`draft`, `active-trial`, `approved-baseline`, `superseded`, `failed`) is five words that a person needs to remember and apply correctly. A caveman has two states: "still testing" and "this works." Five states is two too many. Complexity grows faster than value when systems have more states than a person naturally thinks in.

**Hard question:** "Research never merged into formula files" — where does the user put the thing they read that changed how they think about the formula? If they read that fish sauce needs 3 minutes of heat to bloom and change their recipe — that is both research AND part of the formula. Keeping them separate requires the user to maintain two references simultaneously. In practice, people write the thing they just learned next to the formula it affects.

---

### Caveman → Skeptic

**Steelman:** Starting with only one domain is the right call. The pre-mortem (60% chance of failing to fill in the 3-month observation) is honest and everyone else should read it. The conservative alternative (recipes only, prove habit, then fertilizer) is the safest bet.

**Weakness:** The Skeptic says "confirm you have a baseline before starting." Getting a soil test in rural Thailand takes time and cost. Meanwhile the trees are growing, the farmer is applying whatever they currently apply, and the clock is running. The Skeptic's requirement for a baseline before starting means the system might never start. The baseline IS the first observation of what you're currently doing — you do not need a lab test to begin tracking.

**Hard question:** The Skeptic wants stop conditions: "if by month 3 there is no observation data → retire the system." What does retiring the system mean concretely? Delete three markdown files? Tell Claude to stop asking about it? The stop condition sounds decisive but costs nothing to enforce or ignore.
