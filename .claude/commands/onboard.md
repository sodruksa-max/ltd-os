---
description: One-time interview to fill vault/_memory/PREFERENCES.md with user's voice, investment style, conventions. Run ONCE right after install. After completion, the command self-deprecates with a note.
---

# /onboard

Interview the user to fill `vault/_memory/PREFERENCES.md`. Run ONCE after install.

## When to run
- First thing after `bash scripts/bootstrap.sh` completes + API key is set
- Also: when user manually wants to re-interview (e.g. workflow changed substantially)
- NOT recurring — don't run weekly, don't auto-invoke

## Pre-check

1. Read `vault/_memory/PREFERENCES.md` — is it already filled?
2. If sections have real content (not placeholder `-` bullets):
   ```
   PREFERENCES.md already has content. Options:
   1. Skip — leave as-is
   2. Review + update existing — I'll ask, you decide what to change
   3. Full reinterview — replace everything
   
   Which? (1/2/3)
   ```
3. Proceed based on choice

## Interview flow

Ask in **5 groups**, ONE group at a time. After each group → write to PREFERENCES.md → ask user to confirm before moving to next group.

**Style for questions:**
- Conversational, not form-filling
- Ask follow-ups if answer is vague ("short sentences" → "how short? 5-10 words typical?")
- Accept "skip" / "not sure" — don't force answers
- Match user's language (Thai/English/mix)
- Max 5 questions per group

---

### Group 1: Background + communication

Ask:
1. What do you do for work/life? (1-2 sentences — context for all future tasks)
2. How did you hear about this workflow (longtundiary / other)? — sets expectations
3. Languages you work in (native + professional)?
4. How do you want me to communicate: short + direct, or explanatory? Push back or just agree?
5. Emoji: ok, no, only if you use first?

Write to PREFERENCES.md → `## Background` + `## How to communicate`

---

### Group 2: Depth + tone signals

Ask:
1. Give me examples of times you want DEEP explanations (debug / architecture / trade-offs?)
2. Examples of times you want SHORT (quick fact / already know topic / rushing?)
3. Any keywords you use that mean "go deeper" or "stay brief"? (e.g. "ลึก", "tldr")
4. Things I do that would annoy you (preambles? excessive caveats? asking obvious clarifications?)

Write to `## Depth signals`

---

### Group 3: Voice (for content writer)

Only ask if user will create content (Substack / X / YouTube etc.):

1. Platforms you'll publish to?
2. Recent posts/threads you wrote — paste 1-2 examples OR describe voice in your own words
3. Sentence length pattern (short punchy / long winding / varied)?
4. Formality (casual / professional / mix)?
5. Thai/English mix ratio — when do you use English vs Thai?
6. Phrases you love / phrases you'd never use?

Write to `## Voice (for content writer)` + `## Content platforms`

If user says "I'm not creating content" — skip this group, write "N/A — not creating content currently".

---

### Group 4: Investment style (if applicable)

Ask if user mentions investing:

1. Timeframe (day-trade / swing / long-term / buy-and-hold)?
2. Market focus (US / Thai / crypto / global)?
3. Risk tolerance in words (conservative / moderate / aggressive)?
4. Sectors you understand well / avoid?
5. Framework you follow (Buffett / Graham / Lynch / own)?
6. Things that would make you exit immediately (hard rules)?

Write to `## Investment style`

Skip if not investing.

---

### Group 5: Conventions + hard no's

Ask:
1. Code style preferences (tabs/spaces, naming, test patterns)?
2. Commit message style (conventional / descriptive / short)?
3. File naming conventions you prefer?
4. **Hard no's** — things I should NEVER do regardless of instructions:
   - Publish without approval? (default yes)
   - Delete files without asking? (default yes)
   - Execute trades? (default yes)
   - Create accounts on your behalf? (default yes)
   - Install system tools with sudo? (default yes)
   - Anything else?

Write to `## Project conventions` + `## Hard no's`

---

## After all groups done

1. Read back full PREFERENCES.md to user:
   ```
   Here's what I've captured — review and tell me what to change:
   <full content>
   ```

2. Wait for user: "looks good" / specific edits / "redo section X"

3. On approval:
   - Commit: `git add vault/_memory/PREFERENCES.md && git commit -m "memory: initial onboarding (approved YYYY-MM-DD)"`
   - Log to `vault/_memory/DECISIONS.md`:
     ```
     - YYYY-MM-DD — Onboarding complete, PREFERENCES.md filled
     ```
   - Tell user:
     ```
     ✓ Onboarding complete.
     PREFERENCES.md is filled — every future session I'll read this.
     
     This command is for one-time use. You can:
     - Re-run /onboard if workflow changes a lot (3-6 months)
     - Or just tell me "update PREFERENCES.md — <what changed>" anytime
     
     Suggested next: create your first daily note or try /daily-brief
     ```

## Constraints

- **Do NOT fabricate answers** — if user says "skip" or "not sure", write "(not specified)" in that field
- **Do NOT persist across sessions** — this is one-shot interview, not ongoing dialogue
- **Max 30 minutes total** — if running longer, user is overthinking, suggest "let's save what we have and refine later"
- **No token waste** — don't re-read vault/ during interview unless user references something specific
- **Respect hard no's** — if user answers "never delete files", add that verbatim, even if other rules say otherwise later
- **Confirmation before commit** — never commit without showing user the full file first

## Anti-patterns

- ❌ Asking 20 questions without writing anything (overwhelming)
- ❌ Auto-adding "common preferences" user didn't state
- ❌ Leaving sections filled with generic AI guesses ("prefers clean code") when user didn't say that
- ❌ Running this recurring — it's ONE-SHOT by design

## Time budget

~15-30 minutes total. Token usage ~10-20K. Justified because this file saves tokens every future session by letting Claude skip "getting to know you" overhead.
