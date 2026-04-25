---
description: Generate a morning briefing from vault context — recent notes, open projects, today's focus. Can be invoked manually or by scripts/daily-brief.sh. Phase 1: vault-only (no external data fetch yet).
---

# /daily-brief

Produce a short daily briefing that helps user start the day.

## When invoked

- Manually via `/daily-brief` in Claude Code
- Automatically via `scripts/daily-brief.sh` (if user enables cron)

## Steps

### 1. Gather context (vault-only in Phase 1)

Read:
- `vault/_memory/PROJECTS.md` — active projects + status
- `vault/daily/YYYY-MM-DD.md` (yesterday) — "Tomorrow first thing" if set
- Last 3 daily notes — what's been on user's mind
- Open items in `vault/00_inbox/` — count + age of oldest
- Last 5 commits (`git log --oneline -5`) — recent activity
- `vault/_memory/COST_LOG.md` — latest week's spend (if exists)

**Do NOT** fetch external data (news, market). That's Phase 2.
**Do NOT** re-read vault/10_research/ or large sections — stay lean.

### 2. Generate brief

Format (keep short, ≤ 400 words):

```markdown
# Daily Brief — YYYY-MM-DD (Day Name)

## Yesterday's open threads
(from last daily note "Tomorrow first thing" + uncommitted work)
- 

## Today's suggested focus
(based on active projects + yesterday's state)
1. 
2. 
3. 

## Inbox attention needed
- <count> items (<X> stale > 7d)
- Oldest: "<filename>" (X days old)

## Active projects at a glance
| Project | Status | Last touch | Next step |
|---------|--------|-----------|-----------|
| ...     | ...    | ...       | ...       |

## Budget check (if COST_LOG has data)
- This week so far: $X (last week: $Y, delta: +Z%)
- Status: ✓ on track / ⚠️ approaching limit / 🚨 over budget

## Small nudge (pick 1)
<one-line reminder that matches user's current state — not fake cheerful, just observant>
- "Inbox has 15 items >2 weeks old — maybe 30min to sort?"
- "No commits for 4 days — are projects stuck or just not touched?"
- "Daily notes missing for 3 days — capture today before it's lost"
- "Budget on track this week"
```

### 3. Save + display

- Save to: `vault/daily/YYYY-MM-DD.md` (append to existing, or create if not exists)
  - If daily note exists: add brief at TOP, under title, BEFORE user's existing content
  - Use HTML comment markers: `<!-- BRIEF:START -->` ... `<!-- BRIEF:END -->` so user can delete it easily
- Show brief in chat so user can read immediately

### 4. Reporting

End with:
```
Brief saved to: vault/daily/YYYY-MM-DD.md
Used: ~X tokens, Y vault reads
Next: open Obsidian to see it in context
```

## Constraints

- **Keep it short** — 400 words MAX. Brevity is the whole point.
- **Don't invent data** — if nothing interesting happened, say "quiet day, nothing stood out"
- **No fake urgency** — don't manufacture "3 critical items" if there's 1
- **Voice**: observational, not coaching. Match PREFERENCES.md if filled.
- **No emoji** unless user uses them in their notes
- **No moralizing** — "you should commit more" is not briefing, it's nagging
- **Token budget**: max 3K tokens for entire task

## Anti-patterns

- ❌ Long motivational openings ("Good morning! Today is going to be amazing!")
- ❌ Repeating yesterday's brief verbatim if nothing changed
- ❌ Making up statistics about "how productive you were"
- ❌ Adding external data (news, markets) — that's Phase 2
- ❌ Writing > 400 words — if tempted, you're padding

## When to return empty brief

If ALL of these are true:
- No daily note in last 7 days
- No commits in last 7 days
- Inbox empty
- PROJECTS.md unchanged

Then output minimal: "No signal this week. When you pick work back up, brief will have data to work with."

Don't fabricate things to fill the template.
