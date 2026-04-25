---
description: Run analyst agent for cost + performance review. Suggests improvements; user must approve each one. Safe to run anytime — read-only unless you approve changes.
---

# /analyst

Invoke `analyst` agent to review usage + suggest improvements.

## Usage
- `/analyst` — full weekly-style report
- `/analyst quick` — short version, cost + top 3 anomalies only
- `/analyst --focus <agent-name>` — deep-dive on one agent

## Steps

1. Run `scripts/cost-report.sh --period week` and capture output
2. Read `vault/_memory/COST_LOG.md` for historical context
3. Invoke `analyst` agent with the data
4. Display full report to user
5. For each suggested action, ask: "Approve? (yes/no/modify)"
6. If approved: make the change, commit with message `analyst: <change> (approved)`
7. Log all approvals + rejections to `vault/_memory/ANALYST_LOG.md`

## Constraints

- **Never auto-apply** suggestions — always wait for user yes
- **Always commit approvals separately** from other work (makes revert easy)
- **Respect rate limits** — don't run /analyst more than 1x per day unless user forces
