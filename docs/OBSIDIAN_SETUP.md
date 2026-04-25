# Obsidian Setup Guide

Getting Obsidian ready for LTD-OS workflow.

---

## Install

Download from https://obsidian.md — free for personal use.

## Open vault

1. Obsidian → "Open folder as vault"
2. Path: `\\wsl$\Ubuntu\home\<your-ubuntu-user>\projects\ltd-os\vault`
3. Click "Open"

> **Why this path**: Vault lives inside WSL2 so Claude Code can read/write it. Obsidian reads it from Windows side via the WSL2 UNC path.

---

## Essential plugins

### Core plugins (enable in Settings → Core plugins)

| Plugin | Why |
|---|---|
| **Templates** | Use the 7 templates in `_templates/` |
| **Daily notes** | Auto-create `vault/daily/YYYY-MM-DD.md` |
| **Outgoing links / Backlinks** | Navigate wikilinks |
| **Tag pane** | Browse by tag |
| **Graph view** | See how notes connect |
| **File recovery** | Local undo on top of git |

### Community plugins (Settings → Community plugins → Browse)

| Plugin | Why |
|---|---|
| **Dataview** | Query frontmatter — live dashboards in markdown |
| **Templater** | Powerful templates (dates, variables, prompts) |
| **Tasks** | Cross-note task management with `- [ ]` checkboxes |
| **Obsidian Git** | Auto-pull/push vault on a schedule (optional) |
| **Kanban** | Visual board view for projects |
| **Smart Connections** | Semantic search + related notes (see section below) |
| **Omnisearch** | Fuzzy + fast full-text search (complements Smart Connections) |

Install order: Dataview → Templater → Smart Connections → (others as needed)

---

## Recommended settings

### Daily notes
Settings → Daily notes:
- **Date format**: `YYYY-MM-DD`
- **New file location**: `daily/`
- **Template file**: `_templates/daily-note.md`
- **Open daily note on startup**: on

### Templates
Settings → Templates:
- **Template folder**: `_templates`

### Templater (after install)
Settings → Templater:
- **Template folder**: `_templates`
- **Trigger on file creation**: on
- **Folder templates**:
  - `10_research/papers/` → `_templates/paper-summary.md`
  - `10_research/videos/` → `_templates/video-note.md`
  - `20_investment/` → `_templates/stock-research.md`
  - `20_investment/_journal/` → `_templates/trade-journal.md`
  - `30_content/` → `_templates/content-draft.md`
  - `90_archive/failures/` → `_templates/failure.md`
  - `daily/` → `_templates/daily-note.md`

### Files & Links
- **Default location for new notes**: `00_inbox/`
- **Default location for new attachments**: "In the folder specified below" → `_assets`
  - This routes drag-dropped images to `vault/_assets/` instead of scattering across vault
  - See `vault/_assets/README.md` for subfolder structure + git policy
- **Default link format**: Relative path to file
- **Use [[Wikilinks]]**: on (rename-safe links)

---

## Dataview dashboards

Create `vault/README.md` sections with live queries. Examples below.

### Active projects (in vault/README.md or _memory/PROJECTS-DASHBOARD.md)

````markdown
## Active projects

```dataview
TABLE status, file.mtime as "Last edit"
FROM "40_projects"
WHERE status = "active"
SORT file.mtime DESC
```
````

### Recent research

````markdown
## Research this week

```dataview
LIST
FROM "10_research"
WHERE file.ctime > date(today) - dur(7 days)
SORT file.ctime DESC
```
````

### Investment watchlist

````markdown
## Stock theses (active)

```dataview
TABLE ticker, thesis_short as "Thesis", position as "Position"
FROM "20_investment"
WHERE type = "stock-research" AND !contains(file.path, "_journal")
SORT file.mtime DESC
```
````

### Content pipeline

````markdown
## Content status

```dataview
TABLE format, platform, status, target_publish as "Target"
FROM "30_content"
WHERE status != "published"
SORT target_publish ASC
```
````

### Trade journal summary

````markdown
## Recent trades

```dataview
TABLE ticker, action, price, outcome
FROM "20_investment/_journal"
SORT file.ctime DESC
LIMIT 20
```
````

### Inbox to sort

````markdown
## Inbox

```dataview
LIST file.ctime
FROM "00_inbox"
SORT file.ctime ASC
```
````

---

## Useful hotkeys (customize in Settings → Hotkeys)

| Action | Suggested key |
|---|---|
| Open command palette | `Ctrl+P` |
| Quick switcher (jump to note) | `Ctrl+O` |
| Search in all files | `Ctrl+Shift+F` |
| Create new note in inbox | `Ctrl+N` (default) |
| Insert template | `Ctrl+T` |
| Open daily note | `Ctrl+D` |
| Graph view | `Ctrl+G` |
| Toggle edit/preview | `Ctrl+E` |

---

## Folder view settings

Right-click each top-level folder → Collapse by default EXCEPT:
- `00_inbox/` — keep expanded (needs attention)
- `daily/` — keep expanded (current entry)
- `_memory/` — keep expanded (reference)

---

## Git + Obsidian

**Option A (recommended)**: git commits happen from Claude Code side via `safe-commit.sh`
- Obsidian shows the files; you never use git from inside Obsidian
- Pro: commit checks (secret scan, tests) always run
- Con: you commit manually by running the script

**Option B**: Obsidian Git plugin auto-commits every N minutes
- Pro: zero thought, always backed up
- Con: bypasses safe-commit checks — can commit secrets!
- **If you use this**: configure it to NEVER auto-push and ALWAYS require manual push after human review

**Do not mix**: pick one workflow and stick with it.

---

## Mobile (optional)

Obsidian mobile can sync via:
- **Obsidian Sync** (paid, $4/mo) — official, easy
- **Self-hosted git** — set up on phone's Obsidian + Git plugin
- **Syncthing** — P2P sync, free but fiddly

Warning: if vault contains sensitive investment/personal notes, be careful with cloud sync services.

---

## CSS snippets (optional polish)

Settings → Appearance → CSS snippets — drop custom `.css` files in `vault/.obsidian/snippets/`.

Popular ones:
- Hide frontmatter in reading mode
- Color-code folders in sidebar
- Bigger inline code

Search "Obsidian CSS snippets" — many available.

---

## When Obsidian feels slow

- Exclude `vault/90_archive/` from search (Settings → Files & Links → Excluded files)
- Disable Graph view for vaults > 1000 notes
- Turn off "Use relative paths" in image settings if it causes lag

---

## Don't do

- ❌ Install every popular plugin — each one is context + slowdown
- ❌ Use Obsidian Sync if your vault has financial/personal data (use self-hosted git)
- ❌ Edit files in Obsidian while Claude Code is also editing — conflicts
- ❌ Let Obsidian Git auto-commit secrets (configure to exclude `.secrets/` even though `.gitignore` should catch it)

---

## Semantic Search (Smart Connections)

As your vault grows, keyword search (grep) misses notes that discuss the same concept with different words. Example: searching `"inflation"` won't find notes that wrote `"ราคาสูงขึ้น"`, `"เงินเฟ้อ"`, or `"CPI rise"`.

**Smart Connections** plugin adds semantic search on top of Obsidian — without building a RAG pipeline yourself.

### When to enable

Install on day 1 if you expect to accumulate > 100 notes within a few months. Otherwise, enable when:
- Vault > 100 notes AND `rg` searches start missing relevant results
- You find yourself thinking "I know I wrote about this somewhere..."
- Claude Code is reading large vault sections to answer questions (token expensive)

### Setup

1. Settings → Community plugins → Browse → search "Smart Connections"
2. Install + Enable
3. Settings → Smart Connections:
   - **Model**: start with free local model (`TaylorAI/bge-micro-v2` or similar small model)
   - **Folders to exclude**: `.secrets`, `90_archive/security-log`, `_templates` (no need to embed these)
   - **Auto-embed on save**: ON (keeps index fresh)
4. First embed: may take 5-15 minutes if vault has 100+ notes
5. Use via:
   - Right-side panel "Smart View" — see related notes to currently open note
   - Command palette → "Smart Search" — semantic query

### Cost considerations

- **Free local model**: runs on your machine, no cost, slightly lower quality
- **OpenAI embeddings**: `$0.02 / 1M tokens` via Smart Connections config — cheap but cumulative
- **Budget tip**: local model is fine for most use cases; switch to OpenAI only if local recall feels weak

### Privacy

Local model = nothing leaves your machine. Good for sensitive investment notes / trade journal.
OpenAI model = notes get sent to OpenAI for embedding. Read their retention policy before enabling on financial data.

### Integration with Claude Code

Claude Code doesn't use Smart Connections directly (it's an Obsidian plugin). But when Smart Connections helps YOU find the right notes, you can then pass them to Claude:

```
อ่าน vault/10_research/paper-X.md และ vault/10_research/paper-Y.md แล้วเปรียบเทียบ
```

Over time, your own semantic search (via Smart Connections) complements Claude's reading — you find the relevant context, Claude synthesizes it.

---

## When Smart Connections isn't enough

If you hit these walls, consider building a proper RAG layer (ChromaDB / sqlite-vec):

### Trigger conditions for full RAG

1. **Vault > 500 notes** AND Smart Connections' recall drops (misses obvious relevant notes)
2. **Queries need filters** — e.g. "find investment notes from 2025 that mention semiconductors" — Smart Connections doesn't compose metadata filters well
3. **You want Claude Code to programmatically query vault semantics** (not just Obsidian UI)
4. **Custom embedding models** matter — e.g. need Thai-specific embeddings, domain-tuned models
5. **Structured retrieval** — need top-K chunks across documents for RAG-into-Claude workflows

### Rough build estimate (for future reference)

If triggers hit, budget:
- sqlite-vec or ChromaDB setup: 2-4 hours
- Embedding script + file watcher: 2-3 hours
- Claude Code skill/command to query vector DB: 1-2 hours
- Testing + tuning: 2-4 hours
- Total: 1-2 days

Embedding cost (Voyage or OpenAI):
- 1000 notes × 1KB avg = 1MB = ~$0.02 first embed
- Re-embed on changes: negligible

**Do not pre-build this.** Smart Connections covers 80% of use cases at 5% of the cost.

---

## Note size for semantic search

Embedding quality depends on note size:

- **Too small (< 50 words)**: not enough context for meaningful embedding
- **Sweet spot (200-1500 words)**: embeddings capture coherent concepts
- **Too large (> 2500 words)**: single embedding loses local detail → split

The 2000-word limit enforced by the writer/reviewer agents aligns with this sweet spot. Another reason to keep notes focused.
