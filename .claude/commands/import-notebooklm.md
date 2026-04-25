---
description: Import a summary from NotebookLM into the Obsidian vault with proper structure, tags, and wikilinks. Use when user has pasted content from NotebookLM.
---

# /import-notebooklm

User just pasted a summary from NotebookLM. Your job: organize it, link it, save it — don't re-summarize.

## Steps

1. **Ask user briefly** (1 message, ALL at once):
   - What was the source? (URL, book title, paper, or "multiple")
   - What type? (pdf / article / video / book / audio / multi-source)
   - Rough topic / tags (so we can find related notes)
   - Optional: why are they reading this? (connects to which project)

2. **Scan vault for related notes** before writing:
   - Run `grep -ri "<keywords>" vault/ --include="*.md" -l` on topic keywords
   - Look at titles/frontmatter of matches
   - Pick 2-5 genuinely related notes to link

3. **Create the note**:
   - Use template `vault/_templates/notebooklm-import.md`
   - Filename: `vault/10_research/<subfolder>/YYYY-MM-DD-<slug>.md`
     - subfolder based on source_type: `papers/` / `articles/` / `videos/` / `books/`
   - Frontmatter filled in completely
   - Paste user's NotebookLM output verbatim into "TL;DR", "Key points", "Quotes" sections
     - DO NOT rewrite what NotebookLM said — preserve their work, you're just organizing
     - The point is to NOT spend tokens re-processing

4. **Your value-add** (short, don't pad):
   - Fill "My take" section ONLY if user gave you context about why they're reading
   - If no context: leave the section with placeholders for user to fill manually
   - Fill "Related" with the 2-5 wikilinks you found
   - Suggest 3-5 tags based on content + existing tag patterns in vault

5. **Save + report**:
   ```
   Saved: vault/10_research/<path>/<filename>.md
   Linked to: [[note1]], [[note2]], [[note3]]
   Tags suggested: #tag1 #tag2
   Token cost of this import: ~minimal (no re-summarization)
   ```

## Constraints

- **DO NOT re-summarize the NotebookLM content** — defeats the purpose
- **DO NOT fabricate wikilinks** — only link to notes that actually exist
- **DO NOT fill "My take" without user input** — that section is personal synthesis
- Keep your output short — you're a file clerk here, not an analyst

## After importing

Remind user (one line):
> This note is saved. Next time you want to write/research on this topic, I'll pick it up automatically from vault.
