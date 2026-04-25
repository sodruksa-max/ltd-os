# LTD-OS v0.3.10

Personal knowledge + workflow OS for research, investing, content creation, and coding projects. Built around Claude Code + 8 agents + Obsidian vault on Windows + WSL2.

Inspired by [longtundiary's LTD OS](https://www.youtube.com/watch?v=2AAxQhv7644), adapted for a non-coder owner with strong memory protection and token economics discipline.

---

## Quick start

1. Read [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md) — full install walkthrough (Thai/English)
2. Install WSL2 + Ubuntu (`wsl --install -d Ubuntu`)
3. Drop this folder into `~/projects/ltd-os` inside Ubuntu
4. Run `bash scripts/bootstrap.sh`
5. Open `vault/` in Obsidian (Windows side)
6. Start: `claude` → *"เปิด daily note วันนี้"*

---

## What's inside

```
ltd-os/
├── .claude/
│   ├── CLAUDE.md                  # project memory + all rules
│   ├── agents/                    # 15 sub-agents
│   │   ├── planner.md
│   │   ├── researcher.md
│   │   ├── writer.md
│   │   ├── coder.md
│   │   ├── executor.md
│   │   ├── reviewer.md
│   │   ├── analyst.md
│   │   ├── devils_advocate.md
│   │   ├── optimist.md            # /council proposer
│   │   ├── pragmatist.md          # /council proposer
│   │   ├── skeptic.md             # /council proposer
│   │   ├── synthesizer.md         # /council combiner
│   │   ├── engineer.md            # /council expertise lens (default)
│   │   ├── strategist.md          # /council expertise lens
│   │   └── financial_risk.md      # /council expertise lens
│   │   ├── planner.md             # routes, reads memory, handoff-aware
│   │   ├── researcher.md          # vault-first, 5-search cap
│   │   ├── writer.md              # 4 formats, voice from vault
│   │   ├── coder.md               # Python + web, self-correction loop, dep mgmt
│   │   ├── executor.md            # generic doer, memory-aware
│   │   ├── reviewer.md            # secret scan + size limits + QA
│   │   ├── analyst.md             # cost + perf (manual via /analyst)
│   │   └── devils_advocate.md     # steelman (manual via /challenge)
│   ├── writing-formats/           # thread/longform/hook/newsletter
│   └── commands/                  # 10 slash commands
│       ├── onboard.md             # one-time setup interview
│       ├── council.md             # multi-agent debate
│       ├── import-notebooklm.md
│       ├── stock-research.md
│       ├── challenge.md
│       ├── analyst.md
│       ├── handoff.md
│       ├── condense.md
│       ├── weekly-learnings.md
│       └── daily-brief.md
│
├── vault/                         # Obsidian vault (+ git)
│   ├── _memory/                   # always-loaded memory index
│   │   ├── PROJECTS.md
│   │   ├── DECISIONS.md
│   │   ├── PREFERENCES.md
│   │   ├── COST_LOG.md
│   │   ├── ANALYST_LOG.md
│   │   ├── OUTCOMES.md            # decision outcomes (cross-AI learning)
│   │   ├── WORKFLOWS.md           # patterns for any AI tool
│   │   ├── COUNCIL_LOG.md         # /council session index
│   │   └── ARCHIVE.md             # NOT loaded default
│   ├── _council/                  # /council debate sessions
│   ├── _templates/                # 8 templates
│   ├── _assets/                   # images, PDFs (embedded)
│   │   ├── stocks/
│   │   ├── research/
│   │   ├── content/
│   │   ├── daily/
│   │   └── projects/
│   ├── 00_inbox/
│   ├── daily/                     # daily notes
│   ├── 10_research/
│   ├── 20_investment/
│   │   └── _journal/              # trade journal (actions)
│   ├── 30_content/
│   ├── 40_projects/
│   └── 90_archive/
│       ├── weekly-reviews/
│       ├── failures/              # failure journal
│       ├── challenges/            # devils_advocate outputs
│       ├── condensations/
│       └── security-log/
│
├── code/
│   ├── python/
│   └── web/
│
├── scripts/                       # 10 scripts
│   ├── bootstrap.sh               # one-time WSL2 install
│   ├── safe-commit.sh             # secret-scan + test → commit
│   ├── new-project.sh             # scaffold python/web
│   ├── weekly-review.sh           # status + condensation hints
│   ├── secret-rotate.sh           # leak checklist
│   ├── context-check.sh           # warn on context fill
│   ├── cost-report.sh             # token + USD breakdown
│   ├── backup.sh                  # git push + zip snapshots
│   ├── daily-brief.sh             # scheduled brief runner (Phase 1)
│   └── install-cron.sh            # guided cron setup
│
├── .secrets/                      # gitignored env vars
├── docs/                          # 9 docs
│   ├── GETTING_STARTED.md
│   ├── AGENT_ARCHITECTURE.md
│   ├── NOTEBOOKLM_WORKFLOW.md
│   ├── MEMORY_SYSTEM.md
│   ├── OBSIDIAN_SETUP.md
│   ├── DISASTER_RECOVERY.md
│   ├── AUTOMATION.md
│   ├── AI_PORTABILITY.md          # use vault with ChatGPT/Gemini/local
│   └── ARCHITECTURE.md
│
├── .gitignore
├── .envrc                         # direnv auto-load
└── README.md                      # this file
```

---

## Core workflow (default: pipeline)

```
You ask Claude → planner (reads memory + handoff, routes) 
               → specialist (researcher/writer/coder/executor) 
               → reviewer (QA) 
               → safe-commit
```

You don't write code. You give intent. Planner picks specialist, they work, reviewer gates commit.

## Manual workflows (opt-in)

- `/onboard` — one-time interview to fill PREFERENCES.md (run after install)
- `/council <topic> [--expertise=<lens>]` — multi-agent debate (3 mindset proposers + expertise lens) for high-stakes decisions
- `/challenge <note>` — devils_advocate steelmans your decision
- `/analyst` — cost + performance review with approval-gated suggestions
- `/handoff` — save session state before context fills
- `/condense <section>` — semi-auto vault pruning (user approves plan)
- `/weekly-learnings` — distill week's key learnings from daily notes + commits
- `/daily-brief` — morning briefing from vault context (manual or cron-scheduled)
- `/import-notebooklm` — file NotebookLM summary into vault
- `/stock-research <TICKER>` — research pipeline for stocks

## Token-optimized research workflow (NotebookLM + Claude Code)

```
Heavy PDFs/audio → NotebookLM (free) → summary 
                → /import-notebooklm → Obsidian vault 
                → Claude uses vault as context
```

NotebookLM does heavy summarization for free. Claude Code organizes, synthesizes, and uses growing vault as compound memory. See [`docs/NOTEBOOKLM_WORKFLOW.md`](docs/NOTEBOOKLM_WORKFLOW.md).

---

## 5 protections against "Claude ลืม"

1. **Vault** = long-term truth (markdown + git)
2. **Memory index** (`vault/_memory/`) = loaded every session
3. **Handoff** (`.claude/handoff.md`) = session-to-session bridge
4. **Context monitor** (`scripts/context-check.sh`) = warn 70%/90%
5. **Condensation** (`/condense`) = prune big vault sections, archive originals

See [`docs/MEMORY_SYSTEM.md`](docs/MEMORY_SYSTEM.md).

---

## Daily commands

```bash
# Start a session
claude

# Create new project
bash scripts/new-project.sh python my-bot
bash scripts/new-project.sh web my-site

# Commit (runs secret + test gate)
bash scripts/safe-commit.sh "feat: add foo"

# Weekly routine
bash scripts/weekly-review.sh
bash scripts/backup.sh

# Anytime: context check
bash scripts/context-check.sh

# Monthly: cost review
bash scripts/cost-report.sh --period month
```

---

## Principles

1. **Markdown-first** — no proprietary formats
2. **Git is source of truth** — but only commit what reviewer approves
3. **Secrets stay in `.secrets/`** — never echo, never commit, never paste in chat
4. **8-agent pipeline** — planner routes, specialist does, reviewer gates
5. **Owner doesn't code** — agents explain in plain Thai/English
6. **Vault = compound memory** — bigger vault = Claude gets better *for you*
7. **NotebookLM for heavy summarization** — Claude for synthesis + action

---

## What this is NOT (deliberately)

- ❌ No Self-Evolution (auto prompt rewriting) — silent quality drift
- ❌ No multi-provider day 1 — Claude-only, fallback when needed
- ❌ No Local LLM fallback — AMD GPU + quality gap
- ❌ No Ghost Protocol panic lockdown — over-engineered
- ❌ No Docker sandbox — runs your own code only
- ❌ No browser automation NotebookLM — ToS risk + fragile
- ❌ No 9+ agents — 8 ceiling, coordination overhead
- ❌ No voice input

Add only when real pain appears. See `docs/AGENT_ARCHITECTURE.md` → "Evolution triggers."

---

## Version

v0.3.10 — 2026-04-25
- `/council` enhanced with **expertise lens** (Phase 3.5)
- 3 expertise agents: `engineer` (default), `strategist`, `financial_risk`
- Auto-pick lens based on topic keywords; override with `--expertise=<lens>`
- Synthesizer integrates expertise findings into decision matrix
- Removed Mode A/B distinction — single workflow, lens is the variable

v0.3.9 — 2026-04-25
- **Multi-agent debate**: `/council [A|B] <topic>` command + 4 new agents (optimist, pragmatist, skeptic, synthesizer)
- 5-phase workflow: brief → 3 proposals → cross-critique → synthesis → devil's advocate
- Output = decision matrix + open questions, NEVER auto-decides
- `vault/_council/` folder for session artifacts
- `vault/_memory/COUNCIL_LOG.md` for tracking decisions over time
- AI council uses vault context (PREFERENCES, DECISIONS, OUTCOMES) — not generic advice

v0.3.8 — 2026-04-25
- `vault/_assets/` for images/PDFs/audio with subfolder structure
- Obsidian configured to route attachments to `_assets/` automatically
- Git policy documented (commit by default; switch to gitignore if vault grows > 500MB)
- Optional Git LFS instructions in `_assets/README.md`

v0.3.7 — 2026-04-25
- `vault/_memory/OUTCOMES.md` — log decisions + their actual outcomes (cross-AI learning data)
- `vault/_memory/WORKFLOWS.md` — language-agnostic patterns for any AI tool
- `docs/AI_PORTABILITY.md` — guide for using vault with ChatGPT / Gemini / local LLMs
- `/weekly-learnings` enhanced — scans for OUTCOMES candidates from old DECISIONS

v0.3.6 — 2026-04-25
- Added `/onboard` — one-time interview to fill PREFERENCES.md (5 groups, ~15-30 min)
- Replaces "manually edit PREFERENCES.md" friction — makes first run productive

v0.3.5 — 2026-04-25
- `docs/OBSIDIAN_SETUP.md` adds Smart Connections plugin (semantic search)
- Full RAG deferred — trigger conditions documented
- Note size limits aligned with embedding sweet spot (200-2000 words)

v0.3.4 — 2026-04-25
- **Phase 1 automation**: `/daily-brief` slash command (vault-only, no external fetch yet)
- `scripts/daily-brief.sh` — cron-compatible wrapper with cost cap + timeout + logging
- `scripts/install-cron.sh` — guided cron setup with safety warnings
- `docs/AUTOMATION.md` — automation safety rules + WSL2 cron caveats
- `vault/DASHBOARD.md` — Obsidian Dataview dashboard (open with Dataview plugin)
- **Phase 2** (market data + news) deferred until 2+ weeks of Phase 1 usage

v0.3.3 — 2026-04-25
- Coder: mandatory version pinning (`==X.Y.Z`) for all new deps
- Coder: `timeout` wrapper on all code execution (30s default, configurable)
- Coder: timeout exit 124 handled in self-correction loop (max 2 retries)

v0.3.2 — 2026-04-25
- Coder: self-correction loop (max 5 iterations, anti-cheating rules)
- Coder: dependency management (asks before pip/npm install, never sudo)
- 8 agents + 7 slash commands + 8 scripts + 8 templates + 7 docs

v0.3.1 — 2026-04-25
- Added `/weekly-learnings` command
- Reviewer checks new scripts for header docs
- Weekly review includes Key Learnings section

v0.3 — 2026-04-25
- 8 agents (added analyst with user-approval gate)
- Memory protection system (5 layers)
- NotebookLM workflow integrated
- Cost tracking + backup strategy baked in

## License

Personal use scaffold. No warranty. Investment notes in `vault/20_investment/` are personal research, not advice.
