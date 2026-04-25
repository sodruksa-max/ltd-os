---
description: Save current session state to .claude/handoff.md so the next Claude Code session can pick up exactly where you left off. Use when context usage is high (>70%) or before closing a long work session.
---

# /handoff

Save session state → next session reads it first.

## When to use
- Context monitor warns 70%+ usage
- Ending a multi-hour coding/research session
- Switching computers
- About to close terminal after complex work

## Steps

1. **Read current work state** — what's the user doing right now?
   - Latest plan.md (if exists)
   - Files recently edited (check git status + diff)
   - Unfinished tasks mentioned in this session

2. **Create/overwrite `.claude/handoff.md`**:

```markdown
---
created: YYYY-MM-DD HH:MM
context_usage: ~XX%
session_duration: ~XX hours
---

# Session Handoff

## What I was doing
<1-3 sentences — the main task in progress>

## Current state
- **Active plan**: `path/to/plan.md` (step X of Y done)
- **Files modified**: 
  - `path/to/file1` — <what changed>
  - `path/to/file2` — <what changed>
- **Uncommitted changes**: yes/no
- **Tests status**: passing/failing/not run

## Decisions made this session (don't re-litigate)
- <decision 1 + 1-line reason>
- <decision 2 + 1-line reason>

## Open questions for next session
- <question 1>
- <question 2>

## Next step
<exactly what to do first in the next session>

## Context that matters
<key facts/constraints the next session needs to know — e.g. "API key is in .env", "project is for client X not Y">

## Files to read first next session
1. `<file>` — <why>
2. `<file>` — <why>
```

3. **Report to user**:
   ```
   Handoff saved to .claude/handoff.md
   
   Summary:
   - Task in progress: <X>
   - Next step: <Y>
   - Context captured: <what's in handoff>
   
   Safe to close session now.
   ```

4. **Do NOT commit handoff.md** — it's session scratch, regenerated each handoff

## Constraints

- **Don't summarize chat history verbatim** — extract decisions + state, not conversation
- **Don't include secrets** — if .env was modified, note "env updated" not the values
- **Keep it < 500 lines** — if longer, split into multiple focused handoffs
- **Overwrite, don't append** — old handoffs go stale fast

## Next session behavior

Planner reads `.claude/handoff.md` first if it exists:
```
📋 Found handoff from <timestamp>.
Last task: <summary>
Next step: <step>
Continue this? (yes/new task)
```

If user says "yes" → proceed from "Next step"
If user says "new task" → delete handoff.md, start fresh
