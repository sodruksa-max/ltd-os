# AI Portability Guide

How to use LTD-OS vault with AI tools other than Claude Code. **The vault is the asset — the AI is replaceable.**

---

## Core principle

Everything important is in `vault/` as plain markdown. AI tools are interchangeable interfaces over this knowledge.

If Claude Code disappears tomorrow, you take your vault to the next tool. ~70% of the system works immediately. The other 30% (orchestration, slash commands) gets rebuilt on the new tool's primitives.

---

## What's portable (works on ANY AI)

| Asset | Where | Works with |
|---|---|---|
| Vault content | `vault/**/*.md` | Anything that reads markdown |
| Memory index | `vault/_memory/` | Any AI given file access |
| Templates | `vault/_templates/` | Universal markdown |
| Frontmatter conventions | All vault notes | Standard YAML |
| Wikilinks | `[[note-name]]` | Obsidian + many AI tools |
| Workflows | `vault/_memory/WORKFLOWS.md` | Language-agnostic patterns |
| Outcomes log | `vault/_memory/OUTCOMES.md` | Cross-AI learning data |
| Documentation | `docs/` | Plain markdown |
| Git history | `.git/` | Any git client |

---

## What's Claude Code-specific

| Asset | Where | Migration approach |
|---|---|---|
| Agent prompts | `.claude/agents/*.md` | Copy prompt body → ChatGPT custom GPT / Gemini Gem / Cursor rules |
| Slash commands | `.claude/commands/*.md` | Convert to prompt templates user pastes manually |
| `CLAUDE.md` | `.claude/CLAUDE.md` | Copy to ChatGPT custom GPT "Instructions" / Gemini system prompt |
| Tool integration | Built into Claude Code | Use Aider / Cursor / Continue / Codex CLI |

---

## Tool-specific migration recipes

### → ChatGPT (Plus / Custom GPTs / Codex CLI)

**For chat use:**
1. Create custom GPT with Instructions = content of `CLAUDE.md`
2. Upload `vault/_memory/*.md` files as knowledge
3. For each Claude agent: create separate custom GPT with that agent's prompt body
4. Use Codex CLI for terminal coding work

**Limitations:**
- No automatic vault read every session — must re-upload or paste context
- No subagent delegation — manual switching between custom GPTs
- Slash commands → manual prompt templates

**Strengths gained:**
- Better image generation (DALL-E)
- Voice mode for daily-brief narration
- o1 series for math-heavy reasoning

### → Gemini (Pro / Gems / Code Assist)

**For chat use:**
1. Create Gem with system instructions = content of `CLAUDE.md`
2. Connect Google Drive containing vault for file access
3. For each Claude agent: separate Gem
4. Use Gemini Code Assist in VS Code for coding

**Limitations:**
- Less mature ecosystem for agent workflows
- Different prompt style (more verbose works better)

**Strengths gained:**
- Better video understanding (analyze YouTube directly)
- Long context window (1M+ tokens) — fewer condensation needs
- Built into Google Workspace

### → Local LLM (Ollama / LM Studio + Aider)

**For coding:**
1. Install Aider: `pip install aider-chat`
2. Run with local model: `aider --model ollama/qwen2.5-coder:32b`
3. Aider reads vault as project context
4. Git workflow same as Claude Code

**Limitations:**
- Requires beefy GPU (your RX 9070 XT works but slower than NVIDIA equivalent on ROCm)
- Quality below GPT-4 / Claude Opus class for complex tasks
- No multi-agent orchestration out of box

**Strengths gained:**
- Zero API cost
- Full privacy (nothing leaves machine)
- No quota limits

### → Multi-tool / hybrid (recommended long-term)

**Pattern:**
- Claude Code: vault management, agent orchestration, content writing
- ChatGPT/Codex: math reasoning, image gen, voice
- Gemini: video summarization, long-context analysis
- NotebookLM: heavy PDF summarization (already integrated)
- Local LLM: privacy-sensitive prototyping, offline work

**How vault enables this:**
Each tool reads same vault. OUTCOMES.md tracks which tool worked best for what. WORKFLOWS.md provides cross-tool consistent patterns.

---

## Pre-migration checklist

Before switching primary AI tool, do these:

- [ ] Backup vault: `bash scripts/backup.sh`
- [ ] Push to git remote (if not already): ensure all commits sync
- [ ] Export `vault/_memory/PREFERENCES.md` content — the new tool needs this
- [ ] Test new tool with 1-2 small tasks before committing
- [ ] Run `/analyst` first to capture baseline cost on Claude
- [ ] Plan 1-2 weeks of dual-running before fully switching

---

## What "AI learns about you" actually means

Not memory in the AI's brain — that's session-bound. Real learning lives in:

1. **PREFERENCES.md** — your voice, style, hard no's
2. **DECISIONS.md** — locked choices to avoid re-asking
3. **OUTCOMES.md** — what worked / didn't with reasoning
4. **WORKFLOWS.md** — patterns that produce good results
5. **Vault content** — the substrate of your thinking

Any AI given access to these 5 things can be productive with you in minutes, not months.

This is by design. Anthropic / OpenAI / Google can't lock you in if your "AI memory" is plain markdown in your folder.

---

## Hybrid usage tips

### Track which tool did what
In commit messages: `feat: add bot (claude-code) — fix tested with codex`

### Same vault, different sessions
- Don't have multiple AI tools edit same file simultaneously (git conflicts)
- One tool owns "active editor" per session
- Commit + push before switching tools

### Cost tracking across tools
`cost-report.sh` parses Claude logs only. For multi-tool:
- Track each tool's cost in `COST_LOG.md` manually:
  ```
  ## 2026-04-25
  - Claude Code: $X
  - ChatGPT API: $Y
  - Gemini: free tier
  ```

### Cross-tool prompt portability
Workflows in `WORKFLOWS.md` should be written in plain English, NOT tool-specific syntax. Bad:
```
Use Read tool to grep the vault, then Write to save
```
Good:
```
Search vault using grep-equivalent tool. Save result to specified path.
```

---

## When NOT to migrate

- You're tempted by "the new shiny" without a real pain Claude can't solve → stay
- Migration cost (time + relearning) > savings → stay
- New tool is < 6 months old, ecosystem unstable → wait

Migration is for solving real problems, not collecting tools.

---

## When to definitely migrate

- Claude Code becomes paywalled beyond your budget AND alternatives have parity
- Your work shifts to a domain another AI handles much better (e.g. heavy video → Gemini)
- You hit reliability/quota walls that block real work daily
- Privacy/compliance forces local-only

In those cases, the vault and this guide will get you running on the new tool in 1-3 days.

---

## Maintenance

Review this doc quarterly:
- Are tool capabilities listed still accurate? (AI moves fast)
- Did you actually use multi-tool, or stay on Claude? Update accordingly
- Any new portable assets you've created? Document them

Last updated: 2026-04-25
