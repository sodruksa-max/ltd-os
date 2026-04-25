# Vault

Knowledge base for LTD-OS. Open this folder as a vault in Obsidian.

## Folders

| Folder | Purpose |
|---|---|
| `00_inbox/` | Drop new ideas, links, snippets here. Sort weekly. |
| `10_research/papers/` | Academic papers, deep articles |
| `10_research/articles/` | Blog posts, news, shorter reads |
| `10_research/videos/` | YouTube/podcast notes |
| `20_investment/` | Stock research, macro notes, trade journal |
| `30_content/` | Drafts: posts, scripts, newsletters |
| `40_projects/` | High-level project notes (code lives in `../code/`) |
| `90_archive/` | Old stuff, weekly review logs, security log |
| `_templates/` | Obsidian note templates |

## Conventions
- File names: `YYYY-MM-DD-slug.md` for time-stamped notes
- Use frontmatter (YAML at top) for metadata — Dataview can query it
- Link liberally with `[[wikilinks]]`
- Tag for cross-cutting themes; folder for primary location

## Suggested Obsidian plugins
- **Dataview** — query frontmatter, build dashboards
- **Templater** — date variables in templates
- **Periodic Notes** — daily/weekly notes
- **Git** — auto-pull/push the vault

## Workflow with Claude Code
1. Drop notes into `00_inbox/` raw
2. Weekly: ask Claude to sort inbox into right folders
3. Ask Claude to summarize/synthesize across notes when starting a new project
