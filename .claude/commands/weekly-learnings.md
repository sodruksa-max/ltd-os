---
description: Distill this week's key learnings from daily notes + commits + content into a single page in the weekly review log. Runs Claude in summarizer mode, preserves originals, user approves before save.
---

# /weekly-learnings

Help user produce a "Key Learnings" section for this week's review. Not auto-archive — user must approve.

## When to use
- End of week (Sunday/Monday morning)
- After `bash scripts/weekly-review.sh` has generated the stats section
- When daily notes + commits feel rich enough to harvest patterns

## Steps

1. **Read the week's data:**
   - Last 7 daily notes from `vault/daily/`
   - Git commits from last 7 days: `git log --since="7 days ago" --pretty=format:"%h %s"`
   - New notes in `vault/10_research/`, `vault/20_investment/`, `vault/30_content/`
   - Failure journal entries this week: `vault/90_archive/failures/`
   - **DO NOT re-read old weekly reviews** — redundant

2. **Pattern-hunt (not content-copy):**
   Read looking for these patterns:
   - **Recurring themes**: same topic across 3+ different notes
   - **Contradictions**: something you wrote contradicts what you wrote earlier
   - **Questions raised but not answered**: still open
   - **Decisions that worked / didn't**: evidence from outcomes
   - **Unexpected surprises**: things that didn't go as expected
   - **Skills/tools learned**: new techniques, libraries, concepts

3. **Scan for OUTCOMES candidates:**
   - Read `vault/_memory/DECISIONS.md` — find decisions made 2-8 weeks ago
   - For each: is there now observable outcome based on this week's data?
   - If yes → flag as OUTCOMES.md candidate at end of brief
   - Format suggestion: paste exact entry skeleton with hypothesis filled in

3. **Draft key learnings** (max 1 page, ≤ 500 words):

```markdown
## Key learnings — Week YYYY-WNN

### Themes I kept coming back to
- 
- 

### What I learned (skills / facts / frameworks)
- 
- 

### What surprised me
- 

### Mistakes / what didn't work
- 

### Open questions for next week
- 

### Candidate rules (for DECISIONS.md or PREFERENCES.md)
<if any learning is a repeatable principle>
- [ ] Propose adding to DECISIONS.md: "<rule text>"

### OUTCOMES candidates (decisions ripe to log)
<if any DECISIONS.md entries from past 2-8 weeks now have observable results>
- [ ] DECISION: "<old decision>" → suggest entry in OUTCOMES.md
       Hypothesis on outcome: <✅ worked / ⚠️ mixed / ❌ wrong>
       Data supporting this: <pointer to vault notes / commits>
```

4. **Append to `vault/90_archive/weekly-reviews/<week>.md`** under a new `## Key learnings` section.
   - If section exists: ASK user before overwriting
   - If weekly review file doesn't exist: create with just the key learnings

5. **For each "Candidate rule"**, ask user:
   ```
   Promote to DECISIONS.md? (yes/no/modify)
   ```
   If yes: append to `vault/_memory/DECISIONS.md` with today's date.

6. **For each "OUTCOMES candidate"**, ask user:
   ```
   Add entry to OUTCOMES.md for "<decision>"? (yes/no/skip — too early)
   ```
   If yes: open `vault/_memory/OUTCOMES.md`, draft entry using template format, ASK user to fill "What I learned" + "Would recommend" before commit. Don't autocomplete those — they need user reflection.

7. **Report:**
   ```
   Key learnings saved: vault/90_archive/weekly-reviews/<week>.md
   Rules promoted: <n>
   Outcomes logged: <n>
   Source notes analyzed: <n>
   Tokens used: ~<estimate>
   ```

## Constraints

- **DO NOT delete or move** any daily notes / research / content — this is harvest, not archive
- **DO NOT fabricate learnings** — if the week was quiet, say "quiet week, nothing stood out"
- **DO NOT auto-add rules** to DECISIONS.md / PREFERENCES.md without explicit approval
- **Keep it 1 page** — if tempted to go longer, you're copying not distilling
- **Voice**: match user's voice in daily notes (they wrote them in their voice — learnings should feel like them, not you)

## When to skip

- User just ran this within 3 days — no new data to distill
- `vault/daily/` has < 3 entries this week — not enough signal
- User says "skip" — respect it

## Anti-patterns

- ❌ Summarizing each daily note separately (that's just a re-read, no distillation)
- ❌ Copying full sentences from daily notes (paraphrase pattern, not content)
- ❌ Adding rules user didn't explicitly approve
- ❌ Running this and also `/analyst` in same session (context bloat)

## Commit

หลัง user approve → รัน:
```bash
bash scripts/safe-commit.sh "notes: weekly-learnings <week>"
```
