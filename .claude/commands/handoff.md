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

*(arXiv:2603.19935 Memori: ใช้ semantic triples + narrative summary แทน free-text prose — 67% fewer tokens เมื่อ resume; เขียน triples ก่อน narrative เสมอ)*

```markdown
---
created: YYYY-MM-DD HH:MM
context_usage: ~XX%
session_duration: ~XX hours
---

# Session Handoff

## Semantic Triples (resume เร็ว — อ่านส่วนนี้ก่อน)
<!-- format: (decided: X | about: Y | result: Z) -->
- (decided: <action/choice> | about: <topic/file> | result: <outcome/state>)
- (decided: <action/choice> | about: <topic/file> | result: <outcome/state>)
- (in-progress: <task> | about: <file/goal> | blocked-by: <blocker or "none">)

## Narrative Summary (context ที่ triples ไม่ capture)
<2-3 ประโยค — เหตุผลที่ decisions เหล่านั้นถูกทำ, constraint พิเศษ, หรือ context ที่สำคัญ>

## Next step
<exactly what to do first in the next session — 1 action>

## Files to read first next session
1. `<file>` — <why>
2. `<file>` — <why>

## Open questions
- <question 1>
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
