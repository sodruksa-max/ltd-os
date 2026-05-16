---
type: council-expertise
lens: engineer
---
# Engineer Lens: Technical Feasibility + Maintenance Cost

## What "building" actually means
Every proposal = writing a markdown prompt file. File creation: 20 min. Real implementation risk is what the instructions ask Claude to DO during execution.

## Feasibility per proposal

**OPTIMIST (new command):** File trivial. Hidden cost: parsing healthcheck.sh output (exits 0/1/2), reading paper-survey files (no consistent schema across survey runs), /schedule integration (known pain point). "Reading paper-survey files" is most underestimated component — varies by session format, no consistent schema. → Stretch

**PRAGMATIST (--roadmap flag):** Most technically sound. /analyst already has established read paths. One conditional branch in markdown. DECISIONS.md well-structured = reliable. Degrades gracefully — roadmap stays coupled to /analyst format by design. → Recommended

**SKEPTIC (3-line note):** Lowest risk. Adds no new read sources. Synthesizes only what /analyst already loaded. Stop conditions defined. → Safe

**CAVEMAN (one section):** Mechanically identical to SKEPTIC. Same file, same sources, same degradation. → Safe

## Hidden complexity nobody named

1. **healthcheck.sh exits non-zero** on WARN/FAIL. Any command calling it as subprocess may short-circuit. /system-review would need to replicate error handling /healthcheck already does.

2. **Paper-survey files have no consistent schema** — written by researcher persona in varying formats. "Read paper-survey folder" means: all files (token-heavy), most recent (fragile on naming), grep for marker (requires marker to exist). None of the proposals name this.

3. **ANALYST_LOG.md will eventually exceed token economics** §7 threshold (>1000 words → read with offset+limit). A prompt that says "read ANALYST_LOG.md" without offset will read stale or truncated window silently.

## Maintenance cost ranking (lowest → highest)
1. CAVEMAN / SKEPTIC — one file, no new sources, no scheduling
2. PRAGMATIST — one conditional branch; DECISIONS.md schema change breaks silently
3. OPTIMIST — new file + docs + /schedule integration + healthcheck parser + paper-survey reader

## Engineer recommendation
SKEPTIC and CAVEMAN are mechanically equivalent, lowest risk. PRAGMATIST is the best of the ambitious options — reuses proven paths, stays within 5K analyst budget, degrades gracefully. OPTIMIST's "reading paper-survey files" feature is single most underestimated component and needs its own scoped design before committing.
