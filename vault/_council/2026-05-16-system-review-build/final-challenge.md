---
type: council-final-challenge
---
# Devil's Advocate: The Consensus Is a False Middle

## Core challenge
"Extend /analyst" inherits worst of both worlds: cost-audit mode + system-review mode in one command = user mentally filters every run. Cognitive overhead compounds. Serves neither purpose cleanly.

## Steelmanned case for DO NOTHING
Fix inputs before touching output layer. If OUTCOMES.md and COST_LOG.md are sparsely populated, synthesis wrapper produces confident-sounding nonsense. Correct sequencing: fix data quality first.

## Steelmanned case for /system-review
Synthesis is genuinely valuable → it deserves its own scope, trigger, and output format. Bolting onto /analyst is a technical debt decision dressed as pragmatism.

## Hard questions before deciding
1. What specific files will synthesis section read that /analyst doesn't already? Name them.
2. If underlying data is sparse, what makes you confident synthesis produces signal not hallucinated patterns?
3. Who decided "3-5 items"? What is that based on?
4. If synthesis proves valuable, what's the migration path — or will you refactor again in 3 months?
5. "No scheduling" = never runs unless triggered manually. How is this different from user just reading logs themselves?
