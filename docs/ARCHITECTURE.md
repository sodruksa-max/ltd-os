# Architecture Notes

Why LTD-OS is built this way. Read this when you're tempted to add complexity.

---

## Design constraints (the user)

- Doesn't write code
- Wants research + investing + content + small coding projects
- Runs Windows + AMD GPU (RX 9070 XT) + 9800X3D + 48GB RAM
- Uses Claude Code as primary interface
- Inspired by longtundiary's LTD OS but didn't want full 9-agent version

## Why these choices

### Why WSL2 (not native Windows)
Tooling assumes Linux. npm, pip, git, bash scripts, Claude Code workflows from tutorials — all work better on Linux. Windows native works but every step has edge cases. WSL2 is a one-time install that removes a thousand future paper cuts.

### Why Obsidian + git (not just markdown + grep)
The user has 4 distinct knowledge domains (research, investing, content, projects) that will cross-reference each other. Obsidian's wikilinks + graph + Dataview turn that into a navigable web. Plain markdown + ripgrep works for code projects but not for evolving knowledge bases where structure emerges over time.

Git on top because: rollback, version, future sync, and the safe-commit hook is where security gates live.

### Why 3 agents (not 9)
- **planner**: separates "thinking" from "doing" — cheaper to iterate on a plan than on broken code
- **executor**: focused, follows plan, no scope creep
- **reviewer**: gate before commit, catches secrets + dangerous patterns

The other 6 from original spec map to:
- `manager` = redundant with planner
- `librarian` = a script + Obsidian Dataview, not an agent
- `toolmaker` = executor with python skill
- `researcher` = executor with web_search
- `analyst` = a monthly script reading Claude Code's logs, not a live agent
- `ghost_guard` = the safe-commit script + .gitignore + secret-rotate script
- `visual_dashboard` = Obsidian itself

Agents that idle 90% of the time still cost context and slow handoffs.

### Why no Docker sandbox
The user only runs their own code, on their own machine, in WSL2. Docker adds:
- Image management overhead
- File mount complexity
- 5-30s startup per command
- Tooling that runs differently inside vs outside

When the user starts running untrusted code (scraped scripts, agent-generated tools that touch external APIs broadly), revisit. Until then, WSL2 itself is the sandbox boundary.

### Why no local LLM fallback
The user's GPU is AMD RDNA 4. As of April 2026, ROCm support on consumer RDNA 4 is workable but not first-class. Vulkan backend in llama.cpp works but is slower than CUDA equivalents. More importantly: a 7B-70B local model is qualitatively far below Claude/GPT-4 class. Falling back to it during an outage produces output the user can't trust.

If outage tolerance becomes critical, add a second API provider (Anthropic ↔ OpenAI), not local LLM.

### Why no auto Self-Evolution
"Analyst rewrites other agents' prompts based on token cost" sounds smart. In practice:
- Reward signal (cost) doesn't correlate with quality
- Silent prompt drift = silent capability loss
- No way to A/B test without a real eval set

Replace with: monthly human review of token logs + manual prompt edits.

### Why safe-commit (not raw `git commit`)
Single point in the workflow where security checks happen synchronously. Hook-based pre-commit is fragile (different shells, easy to bypass with `--no-verify`). A wrapped script is explicit, auditable, easy to extend.

Checks (in order):
1. Staged diff doesn't match secret patterns
2. No `.env` (without `.example`) staged
3. No file under `.secrets/` staged
4. If pytest/npm test exists, runs and must pass
5. Conventional commit format check (warn, not block)

---

## When to evolve

| Symptom | Add this |
|---|---|
| Token bills surprise you | `analyst` script (read Claude Code logs, summarize weekly cost by project) |
| Searching vault slow | Add Dataview MOC files; if still slow, embeddings + a vector DB |
| Same prompt copy-pasted often | Promote to a slash command in `.claude/commands/` |
| Need to share vault with someone | Push to private git remote; never to public |
| Weekly review feels like a chore | Automate the obvious parts (auto-archive >30d inbox); don't automate the thinking |
| Agents conflict on what to do | First check: is the task ambiguous? Usually fix the ask, not the agents |
| Hit context limits on big tasks | Memory condensation — summarize old vault sections into 1 high-level note + archive originals |

---

## What stays manual on purpose

- Sorting inbox (you decide what matters)
- Investment thesis writing (delegating thinking defeats the point)
- Final commit messages (force a moment of "what did I just do")
- Adding new agents (don't let agents add agents)
