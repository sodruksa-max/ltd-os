---
proposer: pragmatist
---
# Pragmatist: Extend /analyst, Not a New Command

Base rate on solo-owner meta-review commands: 70%+ abandonment within 4 weeks. Extending a command already in habit loop has 2-3x higher sustained use.

DECISIONS.md precedent: "ไม่สร้าง librarian agent — redundant กับ reviewer ที่มีอยู่." /system-review wrapping healthcheck + analyst + paper-survey = command equivalent of the librarian agent.

**Proposal:** Add `--roadmap` flag to `/analyst`. Pulls last healthcheck output + last analyst cost run + paper-survey index → synthesis block, max 5-item prioritized action list. Checks DECISIONS.md before recommending anything already vetoed.

**Realistic outcome:** Used once/month, 2-3 items acted on per quarter. vs new /system-review: used 3-4x month 1, drops to once every 6-8 weeks by month 3.

**Rejected:** /weekly-calibration extension — violates trading scope boundary. /system-review new command — new habit required, librarian precedent applies. Do nothing — gap is real (14 papers unimplemented).

**Key question:** Would you run `/analyst --roadmap` monthly if it appeared in CLAUDE.md session-start checklist?
