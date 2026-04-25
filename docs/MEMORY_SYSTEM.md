# Memory System

How LTD-OS protects against "Claude ลืม" — 5 layers of defense.

---

## The problem

Claude has no persistent memory across sessions by default. Each time you run `claude`, it starts fresh. Plus, even within one session, context window fills up (~200K tokens) and old messages get truncated.

Without a memory system:
- Day 2: you re-explain what you're working on
- Day 30: you can't remember what you decided last month
- Session 10 hours in: Claude forgets how the session started
- Cross-session: Claude doesn't know your voice, preferences, or locked decisions

---

## 5-layer defense

```
Layer 1: Vault (long-term truth)
   ↑ referenced by
Layer 2: Memory index (always-loaded) 
   ↑ read by planner every session
Layer 3: Handoff (session-to-session bridge)
   ↑ created before context fills
Layer 4: Context monitor (in-session warning)
   ↑ triggers handoff when needed
Layer 5: Condensation (long-term pruning)
   ↑ prevents vault from exploding
```

### Layer 1: Vault = source of truth

Everything important lives in `vault/` as markdown + git. This is your actual memory. Claude reads from here.

- `vault/10_research/` — knowledge ingested
- `vault/20_investment/` — theses + trade journal
- `vault/30_content/` — drafts with voice profile
- `vault/40_projects/` — project notes
- `vault/90_archive/` — everything old (not loaded by default)

**Protection**: git commits every change. Nothing is ever really "lost."

### Layer 2: Memory index = always loaded

`vault/_memory/` contains 5 files Claude reads every session:

| File | Purpose |
|---|---|
| `PROJECTS.md` | Active projects + status |
| `DECISIONS.md` | Locked decisions — don't re-ask |
| `PREFERENCES.md` | User voice, conventions, hard no's |
| `COST_LOG.md` | Weekly cost history |
| `ARCHIVE.md` | Inactive projects (NOT loaded by default) |

**Protection from bloat**: 
- Items > 30 days inactive in PROJECTS.md → move to ARCHIVE.md
- DECISIONS.md format = one-line per decision (dense)
- COST_LOG.md trimmed every 3 months

**Rule**: if `vault/_memory/` total size > 20KB, something's wrong — condense.

### Layer 3: Handoff = session bridge

When a session gets long, run `/handoff` before closing:

1. Claude saves `.claude/handoff.md` with:
   - What you were working on
   - Files modified, decisions made
   - Next step
   - Context that matters for resuming

2. Next session: planner reads handoff first
3. Picks up exactly where you left off

**When to use**:
- Context at 70%+ (context-check.sh warns)
- Ending a multi-hour session
- Switching computers
- Interrupted by life — save state before losing it

### Layer 4: Context monitor

`scripts/context-check.sh` — rough estimate of tokens consumed in current session.

Output:
```
Context usage: 67% (134K / 200K tokens)
✓ OK
```

Or:
```
Context usage: 72% (144K / 200K tokens)
⚠️  WARN — consider /handoff soon
```

**Thresholds**: warn 70%, critical 90%

CLAUDE.md instructs planner to check this before long tasks. Can also run manually anytime.

### Layer 5: Condensation

When vault sections grow huge (say `10_research/papers/` has 47 notes), reading them all = expensive.

`/condense vault/10_research/papers/` command:
1. Groups notes by topic
2. Creates MOC (Map of Content) files summarizing each group
3. Moves originals to `vault/90_archive/` (not deleted — recoverable)
4. Future sessions read the MOC, not the raw notes

**Rules**:
- Semi-auto only — weekly-review.sh detects need, you run /condense
- Originals go to archive, not trash
- MOC wikilinks back to archived originals — findable
- Never condense `_memory/` or `_templates/`

---

## When "Claude ลืม" happens, which layer fixed it?

| Symptom | Fix |
|---|---|
| "Sorry, what project was I working on?" | Layer 2 (PROJECTS.md) |
| "We already decided this last week — why ask again?" | Layer 2 (DECISIONS.md) |
| "You were matching my voice, now you're not" | Layer 2 (PREFERENCES.md) + writer reads vault/30_content/ |
| "Session is slowing down / giving weird responses" | Layer 4 detected, Layer 3 bridges to new session |
| "I close terminal and start over — I lose context" | Layer 3 (handoff) + Layer 2 (memory index) |
| "Vault so big, Claude takes forever to search" | Layer 5 (condensation) |

---

## Anti-patterns

### ❌ Auto-updating memory without user approval
If Claude decides on its own what to add/remove from DECISIONS.md, drift is silent. Always require user approval for memory edits beyond simple appends.

### ❌ Over-loading PREFERENCES.md
If that file grows beyond ~5KB, you're prescribing too much. Trust Claude to infer from vault content.

### ❌ Skipping handoff "because I'll remember"
You won't. Either handoff or accept that the next session starts fresh.

### ❌ Full-auto condensation
Condensation bugs are silent quality loss. Always manual approval before archive.

### ❌ Writing diary-style in _memory/
DECISIONS.md is one-line per decision. PROJECTS.md is status, not narrative. Keep memory index dense.

---

## Monitoring

Run these weekly to check memory health:

```bash
# Memory index size
du -sh vault/_memory/

# Handoff files (old ones should be cleaned)
ls -la .claude/handoff.md 2>/dev/null

# Sections approaching condensation threshold
find vault/ -type d -exec sh -c 'echo "$(find "$1" -maxdepth 1 -name "*.md" | wc -l) $1"' _ {} \; | sort -rn | head

# Average note size (if growing, split notes)
find vault/ -name "*.md" -not -path "*/_memory/*" -not -path "*/_templates/*" -not -path "*/90_archive/*" -exec wc -w {} + | tail -1
```

Or just: `bash scripts/weekly-review.sh` — it reports all of these.

---

## Future additions (do NOT add yet)

- **Semantic search** (embeddings + vector DB) — when vault > 500 notes and grep feels slow
- **Graph analysis** — auto-detect orphan notes, hub notes, dead clusters
- **Cross-vault LLM summaries** — nightly `analyst` report of vault changes

These are all tempting. None are needed on day 1.
