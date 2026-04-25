# Agent Architecture (v0.3)

How the 7 agents work together, what each costs, and when to reach for which.

---

## The 7 agents

```
┌─────────────────────────────────────────────────────────────┐
│                        Tier 1: Core                         │
│  planner → executor → reviewer                              │
│  (planner also routes to specialists below)                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Tier 2: Specialists                        │
│  researcher  │  writer  │  coder                            │
│  (planner auto-invokes based on task)                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Tier 3: Deliberation                      │
│  devils_advocate                                            │
│  (ONLY via /challenge slash command — manual)               │
└─────────────────────────────────────────────────────────────┘
```

---

## Cost profile (relative)

| Agent | Typical cost | Why |
|---|---|---|
| planner | low | Reads context, writes plan.md. No heavy work. |
| researcher | medium | Web searches + vault scan. Cap: 5 searches / task. |
| writer | medium | Loads format rules + voice profile + source material. |
| coder | medium-high | Reads code context, writes/edits, possibly runs tests. |
| executor | low | File ops, simple scripts. |
| reviewer | low | Read-only scan + secret check. |
| devils_advocate | **high** | Deep research to build steelmanned counter. Cap: 5 searches + 10 vault reads. |

---

## Default flow (most tasks)

```
user prompt
    │
    ▼
planner
  │ ├─ trivial task? ─→ do it directly, done
  │ └─ non-trivial ─→ write plan.md, route
    │
    ▼
specialist (researcher / writer / coder / executor)
    │
    ▼
reviewer
    │ ├─ PASS ─→ user runs: bash scripts/safe-commit.sh "..."
    │ └─ FAIL ─→ back to specialist with reviewer's findings
    ▼
commit
```

---

## When debate happens

Debate is **opt-in**, not automatic. User invokes:

```
/challenge vault/20_investment/NVDA.md
/challenge vault/30_content/2026-04-20-thread.md
/challenge vault/40_projects/bot-v2/decisions/use-polygon.md
```

The challenge runs `devils_advocate` → saves `<file>-challenge.md` next to original → severity rating (minor/moderate/major/fatal).

User decides what to do with the challenge. Original is never modified.

**When to use `/challenge`:**
- Investment thesis before adding to position
- Content draft before publish (if audience is large or topic is contested)
- Architecture decision before locking in
- Research conclusion that will drive an action

**When NOT to use:**
- Small decisions (filename, routine tasks)
- Things you've already decided (challenge doesn't change your mind) — save tokens
- Daily content (weekly newsletter routine, etc.)

---

## Routing rules (what planner does)

Planner looks at the user's prompt and decides:

| User says... | Routes to |
|---|---|
| "research / find info / what's the latest on" | `researcher` |
| "draft / write a thread / post / newsletter" | `writer` (asks format if unclear) |
| "code / build a script / fix a bug / automate" | `coder` |
| "rename / move / sort / organize files" | `executor` |
| "summarize this vault note" | `executor` (or direct response) |
| anything combining above | chain: `researcher → writer`, `researcher → coder`, etc. |

**Planner will NOT auto-invoke `devils_advocate`** — that's on you.

---

## Pipeline vs debate (the two modes)

### Default mode: Specialist pipeline
Fast, cheap, linear. Each specialist does their job, hands off.

```
research → write → review → commit
```

Good for: daily work, content production, coding tasks, routine research.

### Debate mode: Adversarial check
Slow, expensive, adversarial. Used to pressure-test a conclusion.

```
your thesis ←→ devils_advocate's counter → you decide
```

Good for: high-stakes decisions, anything you'd regret being wrong about.

**Don't use both on every task.** Pipeline handles 95% of work; debate for the 5% that matters.

---

## Token discipline (per the CLAUDE.md policy)

- Planner checks vault first (grep/Read) before invoking researcher
- Researcher refuses to re-research topics already summarized in vault
- Writer uses vault/30_content/ for voice — doesn't re-derive voice every time
- Coder loads only relevant files, not whole project tree
- Reviewer is read-only — low cost by design
- Devils_advocate has hard caps (5 searches, 10 reads, 1500 words out)

End-of-task reports should say "used N web searches, M vault reads" — this makes cost visible.

---

## Evolution triggers (when to add more)

| Pain | Solution |
|---|---|
| Spend a lot on research that duplicates existing vault | Upgrade researcher's vault-first logic |
| Writer output doesn't match your voice | Maintain a dedicated `voice-profile.md` at `.claude/writing-formats/voice.md` |
| Specific platforms need specific rules (X vs LinkedIn) | Add platform-specific format files |
| Same decision pattern comes up a lot | Add slash command for it (like `/stock-research <ticker>`) |
| Reviewer misses a class of issue | Update reviewer.md with new check |

**Don't** add more agents. 7 is the ceiling for this setup. More agents = more coordination overhead + token burn.

---

## Future: multi-provider (Phase 2)

Currently everything runs on Claude. When you want to add fallback:

1. Add `scripts/llm-fallback.py` that wraps OpenAI/Gemini API
2. Add `.secrets/.env` entries for the fallback keys
3. Each agent's prompt stays the same — the fallback wrapper re-routes prompts when Claude API is down
4. Only triggered by detected failure, not by default

**Do not** pre-build this. Wait until you've actually hit an outage that blocked real work.
