---
description: Condense a vault section that's grown too large. Moves originals to 90_archive/ (never deletes), creates summary + MOC. User must approve plan before execution.
---

# /condense

Summarize a large vault section → archive originals → save condensed version.

## Usage
- `/condense vault/10_research/papers/`
- `/condense vault/20_investment/` (full section)

## Steps

1. **Analyze target section**
   - Count notes, total word count
   - Group by tag/topic (rough clusters)
   - Identify "stale" notes (no edit > 30 days, no inbound links)
   - Find notes that are already summaries vs raw material

2. **Propose plan** (do NOT execute yet):
   ```
   CONDENSATION PLAN for <section>:
   
   Current state:
   - Notes: X
   - Total words: XX,XXX
   - Stale (>30d, no links): Y
   
   Proposed action:
   1. Keep as-is: <list of N active notes>
   2. Group + summarize into MOC:
      - Topic A: notes X, Y, Z → vault/<section>/_moc/topic-a.md (new)
      - Topic B: notes P, Q, R → vault/<section>/_moc/topic-b.md (new)
   3. Archive (move, not delete):
      - Stale notes → vault/90_archive/<section>/YYYY-MM/
      - Originals of summarized notes → same
   
   Result:
   - Active notes: X → Y (-Z%)
   - MOC files created: N
   - Archived: M notes (recoverable)
   
   Proceed? (yes / modify / abort)
   ```

3. **On user "yes"**:
   - Create MOC files (Map of Content — index + summary + wikilinks to archived originals)
   - `git mv` originals to archive (preserves history)
   - Commit with message: `chore: condense <section> (archived N, created M MOC files)`

4. **On user "modify"**:
   - Ask what to change (keep more, archive less, different grouping)
   - Produce revised plan, re-ask

5. **On user "abort"**:
   - Do nothing, log to `vault/90_archive/condensations/log.md`:
     ```
     YYYY-MM-DD — proposed condense <section> — aborted by user
     ```

## MOC file format

```markdown
---
type: moc
section: <section name>
created: YYYY-MM-DD
covers: <topic>
source_count: N
---

# MOC: <topic>

## Summary
<3-5 sentence synthesis of what these notes collectively say>

## Key themes
1. <theme> — see [[archived-note-1]]
2. <theme> — see [[archived-note-2]]
3. <theme> — see [[archived-note-3]]

## Archived source notes
All originals are in `vault/90_archive/<section>/YYYY-MM/`:
- [[archived/.../note-1]] — <1 line summary>
- [[archived/.../note-2]] — <1 line summary>
- ...

## Why this MOC exists
<1-2 sentence: why these notes were grouped>
```

## Hard rules (NEVER violate)

1. **Never delete files** — always move to archive
2. **Never auto-condense** — always propose + wait for "yes"
3. **Always preserve git history** — use `git mv` not `cp + rm`
4. **Never condense `vault/_memory/`** — that's the memory index, special handling only
5. **Never condense `vault/_templates/`** — templates are permanent
6. **Keep MOC + archive linked** — MOC must wikilink to archived notes so they remain findable
7. **Log every condensation** to `vault/90_archive/condensations/log.md`

## When to refuse

- Section has < 20 notes (not big enough to need this)
- Section is actively being worked on (recent commits in last 3 days)
- User hasn't set up weekly-review habit yet (condense prematurely = lose context)

## Output after completion

```
✓ Condensed <section>
  Notes before: X
  Notes after: Y (active) + Z (archived)
  MOC files: N
  
  Recoverable: yes — all originals at vault/90_archive/<section>/YYYY-MM/
  Commit: <hash>
  
  Log: vault/90_archive/condensations/log.md
```
