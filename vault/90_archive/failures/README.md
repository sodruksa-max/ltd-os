# Failure Journal

Project failures, bad investments, flopped content, broken systems. Writing them down = compounding wisdom.

## Rules
- **Filename**: `YYYY-MM-DD-<short-slug>.md`
- **Template**: `vault/_templates/failure.md`
- **Severity**: minor / moderate / major / catastrophic
- **Category**: project / investment / content / decision / system

## Review quarterly
Every 3 months, read this folder top-to-bottom. Look for patterns:
- Same mistake recurring? → add rule to `vault/_memory/DECISIONS.md`
- Category-specific blind spot? → update `vault/_memory/PREFERENCES.md`
- System-level issue? → file a `docs/` update or `.claude/` change

## Why this is in 90_archive/ not active folders
- Failures are for reflection, not active reference
- Not loaded by default in Claude session (save tokens)
- Searchable when needed: `rg "pattern" vault/90_archive/failures/`

## Dataview

````markdown
## Failures by category

```dataview
TABLE category, severity, date
FROM "90_archive/failures"
SORT file.ctime DESC
```

## Catastrophic failures (lest we forget)

```dataview
LIST
FROM "90_archive/failures"
WHERE severity = "catastrophic"
```
````
