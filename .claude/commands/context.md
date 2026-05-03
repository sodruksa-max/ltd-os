---
description: Check current context/token usage — warns when approaching Claude's context window limit
---

# /context

Check how full the current context window is and whether to run /handoff.

## Steps

1. Run the context check script:

```bash
scripts/context-check.sh
```

2. Read the output and respond based on exit code:

| Exit | Usage | Action |
|------|-------|--------|
| 0 | < 70% | "Context OK — safe to continue" |
| 1 | 70–90% | "Context at ~X% — consider /handoff before next heavy task" |
| 2 | > 90% | "Context CRITICAL at ~X% — run /handoff NOW before losing work" |

3. If usage > 70%, remind user:
   - `/handoff` saves current session state
   - After handoff: exit Claude Code and restart to get a fresh context window
   - Next session will auto-load the handoff and offer to resume

## Output format

```
Context: ~XX% (est. ~XX,XXX / 200,000 tokens)
Status: [OK / WARN / CRITICAL]
[If WARN/CRITICAL]: Recommend running /handoff before continuing heavy tasks.
```

## Notes

- Estimate is based on file sizes (chars ÷ 3), not exact token count — actual usage may differ by ±20%
- Thai text uses ~2-3 chars/token vs English ~4 chars/token — script uses 3 as worst case
- This does NOT include the current conversation messages, only files read into context
