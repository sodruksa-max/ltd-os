---
description: Natural language interface to NotebookLM — list notebooks, query sources, create audio/slides/mindmap/report, download artifacts to vault. Use for any NotebookLM operation.
---

# /nlm

NotebookLM ผ่าน natural language — Claude แปลงคำสั่งเป็น MCP calls และ save artifacts ลง vault อัตโนมัติ

## Usage

```
/nlm <natural language command>
```

Examples:
- `/nlm what notebooks do I have?`
- `/nlm list sources in Academic Study Skills`
- `/nlm ask the Academic Study Skills notebook about active recall`
- `/nlm make a podcast on the AVGO notebook`
- `/nlm generate slides for Academic Study Skills`
- `/nlm make a mind map of the CPU thesis notebook`
- `/nlm add this URL to AVGO notebook: https://...`

---

## Steps

### 1. Load MCP tools (always first)

Call ToolSearch with:
```
select:mcp__notebooklm-mcp__notebook_list,mcp__notebooklm-mcp__notebook_query,mcp__notebooklm-mcp__studio_create,mcp__notebooklm-mcp__studio_status,mcp__notebooklm-mcp__download_artifact,mcp__notebooklm-mcp__source_add,mcp__notebooklm-mcp__source_describe
```

### 2. Parse intent → map to operation

| User says | Operation |
|---|---|
| "list notebooks", "what notebooks", "show all" | `notebook_list` |
| "list sources", "what sources", "sources in" | `source_describe` |
| "ask", "query", "what does…say about", "tell me about" | `notebook_query` |
| "podcast", "audio", "listen to" | `studio_create(artifact_type=audio)` |
| "slides", "presentation", "deck" | `studio_create(artifact_type=slide_deck)` |
| "mind map", "mindmap", "map of" | `studio_create(artifact_type=mind_map)` |
| "report", "briefing", "summary doc" | `studio_create(artifact_type=report)` |
| "add source", "add url", "add this" | `source_add` |
| "download", "get the audio", "save the slides" | `download_artifact` (existing artifact) |

### 3. Resolve notebook

- Call `notebook_list` once
- Fuzzy-match the notebook name user mentioned (case-insensitive, partial OK)
- If unambiguous match: proceed silently
- If ambiguous or no name given (for operations that need one): show the list and ask which notebook

### 4A. Query operation

```python
notebook_query(notebook_id=<id>, query=<user's question verbatim>)
```

- Return answer as-is with citations — do NOT re-summarize or paraphrase

### 4B. Artifact creation

```python
studio_create(notebook_id=<id>, artifact_type=<type>, confirm=True)
```

Note: `confirm=True` is valid here — user explicitly requested creation by invoking /nlm.

**Then poll until done:**
- Call `studio_status(notebook_id=<id>)` every 30 seconds
- Find the artifact matching the type just created (most recent)
- Stop when `status == "complete"` or after 10 polls (5 min) — if timeout, report current status and stop

**Then download:**
```python
download_artifact(
    notebook_id=<id>,
    artifact_type=<type>,
    output_path=<vault_path>   # see §5
)
```

### 4C. Source add

```python
source_add(notebook_id=<id>, source_type="url", url=<url>)
# or
source_add(notebook_id=<id>, source_type="text", text=<text>, title=<title>)
```

Report how many sources the notebook now has.

### 5. Vault paths for artifacts

Base: `C:\Users\sodru\ltd-os\vault\_assets\notebooklm\`

| Artifact type | Subfolder | Extension |
|---|---|---|
| `audio` | `audio/` | `.mp3` |
| `slide_deck` | `slides/` | `.pdf` |
| `mind_map` | `mindmaps/` | `.json` |
| `report` | `reports/` | `.md` |
| `infographic` | `infographics/` | `.png` |
| `video` | `video/` | `.mp4` |

Filename pattern: `<notebook-slug>-<artifact-type>-<YYYY-MM-DD>.<ext>`

Example: `academic-study-skills-audio-2026-05-10.mp3`

Full output_path example:
```
C:\Users\sodru\ltd-os\vault\_assets\notebooklm\audio\academic-study-skills-audio-2026-05-10.mp3
```

### 6. Report back

```
Done.
Notebook : <title>
Operation : <what was done>
Saved    : vault/_assets/notebooklm/<type>/<filename>
```

For queries: just return the answer — no report footer needed.

---

## Auth errors

If any tool returns auth/authentication error:
```
Token expired. Run:  ! nlm login
```

## Constraints

- Never re-summarize `notebook_query` results — show verbatim with citations
- Never fabricate notebook IDs — always verify via `notebook_list`
- Max 10 polls on `studio_status` (5 min total) — stop and report if exceeded
- Warn user if artifact file is > 50MB before saving (git size policy)
- Do NOT auto-commit after saving artifacts — user commits manually
