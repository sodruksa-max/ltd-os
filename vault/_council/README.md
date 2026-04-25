# _council/

Output ของ `/council` workflow — multi-agent debate sessions.

## Structure

```
_council/
├── README.md (this file)
├── 2026-04-25-trading-strategy/
│   ├── brief.md
│   ├── proposal-optimist.md
│   ├── proposal-pragmatist.md
│   ├── proposal-skeptic.md
│   ├── critiques.md
│   ├── synthesis.md
│   ├── final-challenge.md
│   └── DECISION.md  ← start here
└── 2026-05-01-content-platform/
    └── ...
```

## How to use a council session

1. Open `DECISION.md` first (TL;DR + decision matrix + hard questions)
2. If need detail → read `synthesis.md`
3. If need raw arguments → read individual `proposal-*.md`
4. After deciding → update DECISION.md frontmatter `status: decided: <choice>`
5. After 2-8 weeks → log outcome via `/weekly-learnings` → updates OUTCOMES.md

## When to /council

- Decisions involving money, time >1 week, hard to reverse
- Project planning with multiple viable approaches
- Strategy choices where you have hypothesis to test

NOT for:
- Quick factual questions
- Tool/library selection (too small)
- Things with obvious right answer
