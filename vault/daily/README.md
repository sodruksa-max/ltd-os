# Daily notes

Auto-created via Obsidian's Daily notes plugin + Templater.

## Setup
See `docs/OBSIDIAN_SETUP.md` → Daily notes section.

## Filename format
`YYYY-MM-DD.md`

## Template
`vault/_templates/daily-note.md`

## Workflow
- **Morning**: open today's daily note, write `## Focus วันนี้`
- **Throughout day**: dump into `## Quick notes`
- **Before close**: write `## Tomorrow first thing` (tomorrow's first action)

## Claude Code integration
Ask Claude: *"เปิด daily note วันนี้"* → executor creates/opens
Ask: *"summarize สัปดาห์นี้จาก daily notes"* → researcher reads last 7 files
