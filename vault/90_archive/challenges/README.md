# Challenges

Outputs from `/challenge` command — devils_advocate steelmanned counter-arguments to your decisions.

## How these files get here
1. You write a thesis/plan in `vault/20_investment/` or `30_content/` or `40_projects/`
2. You run `/challenge <path>` 
3. devils_advocate produces counter → saved as `<original-name>-challenge.md` in the SAME folder as the original (NOT here)
4. A log entry appended to `vault/90_archive/challenges/log.md`

## Why the challenge files live NEXT to originals, not here
Keeping them adjacent makes the relationship obvious in Obsidian. This folder is just the LOG.

## Log file
`log.md` has one line per `/challenge` invocation:
```
YYYY-MM-DD <original-path> → severity: <level>
```

## Review pattern
Quarterly: read `log.md`, look for:
- Which decisions I proceeded with despite "major" severity — were they right?
- Am I running `/challenge` before important decisions? Or skipping?
- Patterns in what devils_advocate flags

## When to delete old challenges
Never auto-delete. If a decision+challenge pair is truly ancient (> 1 year) and irrelevant, you can manually archive by moving to a dated subfolder here.
