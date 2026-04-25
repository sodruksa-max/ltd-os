# 🏠 LTD-OS Dashboard

Open this in Obsidian (requires Dataview plugin).

---

## Today

```dataviewjs
const today = dv.date("today").toFormat("yyyy-MM-dd");
const daily = dv.pages('"daily"').where(p => p.file.name === today).first();
if (daily) {
  dv.paragraph("📅 [[daily/" + today + "|Today's daily note]]");
} else {
  dv.paragraph("📅 No daily note yet today. Run: `bash scripts/daily-brief.sh` or open Claude Code and create one.");
}
```

---

## Active projects

```dataview
TABLE WITHOUT ID
  file.link as "Project",
  status,
  last_touch as "Last touched",
  next_step as "Next"
FROM "_memory"
WHERE file.name = "PROJECTS"
```

(Note: the above is a placeholder — PROJECTS.md uses markdown headers not frontmatter. See `vault/_memory/PROJECTS.md` directly for the list.)

---

## Research this week

```dataview
LIST
FROM "10_research"
WHERE file.ctime > date(today) - dur(7 days)
SORT file.ctime DESC
```

---

## Content pipeline

```dataview
TABLE WITHOUT ID
  file.link as "Draft",
  format,
  platform,
  status,
  target_publish as "Target"
FROM "30_content"
WHERE status != "published"
SORT target_publish ASC
```

---

## Investment watchlist

```dataview
TABLE WITHOUT ID
  file.link as "Research",
  ticker,
  sector,
  status,
  position
FROM "20_investment"
WHERE type = "stock-research"
SORT file.mtime DESC
```

---

## Recent trades

```dataview
TABLE WITHOUT ID
  file.link as "Entry",
  ticker,
  action,
  price,
  outcome
FROM "20_investment/_journal"
SORT file.ctime DESC
LIMIT 10
```

---

## Inbox to sort

```dataview
LIST
FROM "00_inbox"
SORT file.ctime ASC
LIMIT 20
```

---

## Failures journal (review quarterly)

```dataview
TABLE WITHOUT ID
  file.link as "Incident",
  category,
  severity,
  date
FROM "90_archive/failures"
SORT file.ctime DESC
LIMIT 10
```

---

## Weekly reviews (last 4 weeks)

```dataview
LIST
FROM "90_archive/weekly-reviews"
SORT file.ctime DESC
LIMIT 4
```

---

## Upcoming (Phase 2)

This dashboard will grow with:
- **Market snapshot**: when market data integration is added (Phase 2)
- **News feed**: when RSS aggregation is enabled (Phase 2)
- **Cost tracker**: live spending vs. budget
- **Automation alerts**: if scheduled jobs failed

For now → the dashboard is vault-only. That's OK — you don't need real-time market data to start the day well.

---

## How to use

- **Morning**: open this note, scan daily brief + active projects
- **Before close**: jump to today's daily note, write "Tomorrow first thing"
- **Weekly**: check weekly review log + inbox state
- **Monthly**: scan failures journal, identify patterns
