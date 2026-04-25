# _assets/

Images, PDFs, audio, video — anything that's NOT markdown but gets embedded in vault notes.

## Subfolder structure

```
_assets/
├── stocks/      # stock charts, screenshots, IR slides
├── research/    # diagrams from papers, infographics
├── content/     # thumbnails, hero images for posts
├── daily/       # screenshots dropped into daily notes
└── projects/    # mockups, diagrams for project notes
```

Add subfolders as needed — but keep < 10 top-level subdirs to stay scannable.

## How to embed in notes

Drag image into Obsidian → it copies to `_assets/<current folder context>/` automatically (if Obsidian is configured per OBSIDIAN_SETUP.md).

Markdown link:
```markdown
![[stocks/NVDA-chart-2026-04.png]]
```

For sizing:
```markdown
![[NVDA-chart.png|400]]
```

## Git policy (IMPORTANT)

By default, **`_assets/` IS committed to git**. Pros and cons:

**Pros:**
- Full version control on images
- Sync across devices via git remote
- Restore from any commit

**Cons:**
- Vault repo grows fast (1MB images × 100 = 100MB → slow git operations)
- GitHub free repo limit = 1GB warning at 750MB
- Backups become heavy

### When to switch to gitignore (don't commit)

Edit `.gitignore` and add:
```
vault/_assets/**
!vault/_assets/**/.gitkeep
!vault/_assets/README.md
```

This keeps folder structure but excludes binary files. Use when:
- Vault `_assets/` exceeds 500MB
- You're hitting GitHub LFS quota
- You don't need image history

### Better: Git LFS (advanced)

For long-term: Git Large File Storage handles binaries efficiently
```bash
brew install git-lfs   # or apt install git-lfs
git lfs install
git lfs track "vault/_assets/**/*.png"
git lfs track "vault/_assets/**/*.pdf"
```

GitHub free tier: 1GB LFS storage, 1GB bandwidth/month. Sufficient for personal use.

## Naming conventions

Filename pattern: `<topic>-<date>-<descriptor>.<ext>`

Good:
- `NVDA-2026-04-Q1-earnings-chart.png`
- `attention-paper-architecture-diagram.png`
- `weekly-brief-2026-W17-thumbnail.jpg`

Bad:
- `image.png`
- `Screenshot 2026-04-25 at 14.32.51.png` (default Mac)
- `Pasted image 20260425143251.png` (default Obsidian)

**Rename after dropping** if Obsidian gives generic name. Wikilinks update automatically.

## Don't commit

Even if `_assets/` is committed:
- Personal photos (use separate vault)
- Screenshots that contain secrets/tokens (redact first)
- Copyrighted material you don't have rights to (papers PDFs, magazine scans)
- Anything > 10MB single file (consider compressing or external link)

## Smart Connections doesn't see images

Smart Connections (Obsidian semantic search plugin) only embeds **text**. To make images findable:
- Add caption text in note: `Caption: NVDA Q1 revenue by segment`
- Add filename context: image title becomes part of note's embedding
- Don't rely on visual content for retrieval — describe in text
