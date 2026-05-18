#!/usr/bin/env bash
# healthcheck.sh — automated system checks for LTD-OS
# Prints: PASS / WARN / FAIL per check

set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
VENV="$ROOT/code/python/.venv/Scripts/python"
SECRETS="$ROOT/.secrets/.env"
PASS=0; WARN=0; FAIL=0

p() { echo "PASS  $1"; ((PASS++)); }
w() { echo "WARN  $1"; ((WARN++)); }
f() { echo "FAIL  $1"; ((FAIL++)); }

echo "=== LTD-OS Health Check ==="
echo ""

# ── Python venv ──────────────────────────────────────────────────────────────
echo "-- Python"
if [[ -f "$VENV" ]]; then
  p "venv exists ($VENV)"
else
  f "venv missing — run: python -m venv code/python/.venv"
fi

for pkg in alpaca yfinance requests; do
  if "$VENV" -c "import $pkg" 2>/dev/null; then
    p "package: $pkg"
  else
    f "package missing: $pkg — pip install $pkg"
  fi
done

# ── Secrets ──────────────────────────────────────────────────────────────────
echo ""
echo "-- Secrets"
if [[ -f "$SECRETS" ]]; then
  p ".secrets/.env exists"
  for key in ALPACA_API_KEY ALPACA_SECRET_KEY; do
    if grep -q "^${key}=" "$SECRETS" 2>/dev/null; then
      val=$(grep "^${key}=" "$SECRETS" | cut -d= -f2)
      if [[ -n "$val" ]]; then
        p "$key is set"
      else
        f "$key is empty"
      fi
    else
      f "$key missing from .env"
    fi
  done
else
  f ".secrets/.env not found — create it with ALPACA keys"
fi

# ── Scripts ───────────────────────────────────────────────────────────────────
echo ""
echo "-- Scripts (core)"
for script in \
  "scripts/macro-snapshot.py" \
  "scripts/sr-levels.py" \
  "scripts/eod-report.py" \
  "scripts/stats-real-trade.py" \
  "scripts/context-check.sh" \
  "scripts/healthcheck.sh" \
  "scripts/safe-commit.sh" \
  "scripts/safe-push.sh" \
  "scripts/daily-brief.sh" \
  "scripts/bootstrap.sh" \
  "scripts/cost-report.sh" \
  "scripts/weekly-review.sh" \
  "scripts/alpaca-paper.py" \
  "scripts/screener.py" \
  "scripts/auto-buy.py" \
  "scripts/watchlist-manager.py" \
  "scripts/watchlist.json"
do
  if [[ -f "$ROOT/$script" ]]; then
    p "$script"
  else
    f "$script not found"
  fi
done

echo ""
echo "-- Scripts (data pipelines)"
for script in \
  "scripts/nick-monitor.py" \
  "scripts/nick-score.py" \
  "scripts/nick-kill-monitor.py" \
  "scripts/weekly-snapshot.py" \
  "scripts/post-snapshot.py" \
  "scripts/news-snapshot.py" \
  "scripts/catalyst-calendar.py" \
  "scripts/sector-flow.py" \
  "scripts/etf-discovery.py" \
  "scripts/universe-screen.py" \
  "scripts/brier-score.py" \
  "scripts/thesis-convergence.py" \
  "scripts/nick-daily.sh" \
  "scripts/nick-signals-update.py"
do
  if [[ -f "$ROOT/$script" ]]; then
    p "$script"
  else
    f "$script not found"
  fi
done

echo ""
echo "-- Scripts (CCR / automation)"
for script in \
  "scripts/ipo-scanner.py" \
  "scripts/build_dashboard.py" \
  "scripts/weekly-audit.py" \
  "scripts/junk_filter.py" \
  "scripts/_llm.py" \
  "scripts/outcomes-index.py" \
  "scripts/vault-review-trigger.sh" \
  "scripts/usage-tracker.py" \
  "scripts/bubble-risk-monitor.py"
do
  if [[ -f "$ROOT/$script" ]]; then
    p "$script"
  else
    f "$script not found"
  fi
done

# ── Slash commands ────────────────────────────────────────────────────────────
echo ""
echo "-- Slash commands (trading)"
for cmd in pre-market post-market market-log eod paper-trade screen bot weekly-calibration weekly-market; do
  if [[ -f "$ROOT/.claude/commands/${cmd}.md" ]]; then
    p "/${cmd}"
  else
    f "/${cmd} command missing"
  fi
done

echo ""
echo "-- Slash commands (formula system)"
for cmd in new-formula new-recipe; do
  if [[ -f "$ROOT/.claude/commands/${cmd}.md" ]]; then
    p "/${cmd}"
  else
    f "/${cmd} command missing"
  fi
done

echo ""
echo "-- Slash commands (research & content)"
for cmd in stock-research stock-content paper-survey import-notebooklm nlm; do
  if [[ -f "$ROOT/.claude/commands/${cmd}.md" ]]; then
    p "/${cmd}"
  else
    f "/${cmd} command missing"
  fi
done

echo ""
echo "-- Slash commands (nick portfolio)"
for cmd in nick; do
  if [[ -f "$ROOT/.claude/commands/${cmd}.md" ]]; then
    p "/${cmd} (nick-init / nick-weekly / nick-quarterly)"
  else
    f "/${cmd} command missing"
  fi
done

echo ""
echo "-- Slash commands (system)"
for cmd in review daily-brief handoff context condense weekly-learnings onboard analyst challenge council healthcheck token-audit; do
  if [[ -f "$ROOT/.claude/commands/${cmd}.md" ]]; then
    p "/${cmd}"
  else
    f "/${cmd} command missing"
  fi
done

echo ""
echo "-- Slash commands (cognitive trait)"
for cmd in brainstorm connect deep-dive wild-thesis; do
  if [[ -f "$ROOT/.claude/commands/${cmd}.md" ]]; then
    p "/${cmd}"
  else
    f "/${cmd} command missing"
  fi
done

echo ""
echo "-- Slash commands (workflow manager)"
for cmd in workflow new-workflow workflow-audit workflow-design; do
  if [[ -f "$ROOT/.claude/commands/${cmd}.md" ]]; then
    p "/${cmd}"
  else
    f "/${cmd} command missing"
  fi
done

# ── Workflow system ────────────────────────────────────────────────────────────
echo ""
echo "-- Workflow system"
if [[ -d "$ROOT/vault/_workflows" ]]; then
  p "vault/_workflows/ exists"
else
  f "vault/_workflows/ missing — workflow system not initialized"
fi
if [[ -d "$ROOT/vault/_workflows/.state" ]]; then
  p "vault/_workflows/.state/ exists"
else
  w "vault/_workflows/.state/ missing — state persistence will fail"
fi
if [[ -f "$ROOT/scripts/workflow-state.sh" ]]; then
  p "scripts/workflow-state.sh exists"
else
  f "scripts/workflow-state.sh missing — /workflow resume broken"
fi
wf_count=$(ls "$ROOT/vault/_workflows/"*.md 2>/dev/null | grep -v "\.state" | wc -l | tr -d ' ')
if [[ "$wf_count" -gt 0 ]]; then
  p "workflow definitions: $wf_count found"
else
  w "no workflow definitions in vault/_workflows/ — create with /new-workflow"
fi

# ── Vault structure ───────────────────────────────────────────────────────────
echo ""
echo "-- Vault"
for dir in \
  "vault/00_inbox" \
  "vault/daily" \
  "vault/10_research" \
  "vault/10_research/papers" \
  "vault/Knowledge" \
  "vault/Knowledge/insight-atoms" \
  "vault/20_investment/_journal" \
  "vault/20_investment/_journal/real-trades" \
  "vault/20_investment/nick/weekly" \
  "vault/20_investment/nick/alerts" \
  "vault/20_investment/nick/performance" \
  "vault/20_investment/nick/initial" \
  "vault/20_investment/nick/quarterly" \
  "vault/30_content" \
  "vault/40_projects" \
  "vault/50_formulas/fertilizer" \
  "vault/50_formulas/fertilizer/_research" \
  "vault/50_formulas/recipes" \
  "vault/50_formulas/recipes/_research" \
  "vault/_memory" \
  "vault/_templates" \
  "vault/_workflows" \
  "vault/90_archive"
do
  if [[ -d "$ROOT/$dir" ]]; then
    p "dir: $dir"
  else
    f "dir missing: $dir"
  fi
done

# Nick signals freshness
nick_signals="$ROOT/vault/Knowledge/nick-signals.md"
if [[ -f "$nick_signals" ]]; then
  # Check if file was modified in last 2 days (172800 seconds)
  if find "$nick_signals" -mmin +2880 | grep -q .; then
    w "nick-signals.md exists but >48h old — run nick-monitor.py"
  else
    p "nick-signals.md recent"
  fi
else
  f "nick-signals.md missing — run nick-monitor.py"
fi

# ── Knowledge Base files ──────────────────────────────────────────────────────
echo ""
echo "-- Knowledge Base files"
for kb in \
  "vault/Knowledge/THESIS_TRACKER.md" \
  "vault/Knowledge/topic-map.md" \
  "vault/Knowledge/INDEX_insights.md" \
  "vault/Knowledge/contradiction-registry.md" \
  "vault/Knowledge/thesis-convergence.md" \
  "vault/Knowledge/nick-soul.md" \
  "vault/Knowledge/ptsd-threat-patterns.md" \
  "vault/Knowledge/paranoid-threat-signatures.md" \
  "vault/Knowledge/tle-memory-index.md" \
  "vault/Knowledge/misophonia-triggers.md"; do
  if [[ -f "$ROOT/$kb" ]]; then
    p "$kb"
  else
    f "$kb missing"
  fi
done

# Nick core files
echo ""
echo "-- Nick core files"
for f in \
  "vault/20_investment/nick/performance/nav_log.md" \
  "vault/20_investment/nick/nick_state.json"; do
  if [[ -f "$ROOT/$f" ]]; then
    p "$f"
  else
    w "$f missing — nick system may be uninitialized"
  fi
done

# ── Memory files ──────────────────────────────────────────────────────────────
echo ""
echo "-- Memory files"
for mem in PROJECTS DECISIONS PREFERENCES OUTCOMES WORKFLOWS COUNCIL_LOG TRADING_RULES ANALYST_LOG COST_LOG HYPERTHYMESIA_LOG USAGE_LOG healthcheck-log; do
  fpath="$ROOT/vault/_memory/${mem}.md"
  if [[ -f "$fpath" ]]; then
    size=$(wc -c < "$fpath")
    if [[ $size -gt 50 ]]; then
      p "_memory/${mem}.md (${size} bytes)"
    else
      w "_memory/${mem}.md exists but nearly empty (${size} bytes)"
    fi
  else
    f "_memory/${mem}.md missing"
  fi
done

# ── Templates ─────────────────────────────────────────────────────────────────
echo ""
echo "-- Templates"
for tpl in real-trade-template fertilizer-formula recipe-formula content-draft daily-note failure notebooklm-import paper-summary paper-trade-template stock-research trade-journal; do
  if ls "$ROOT/vault/_templates/${tpl}"* 2>/dev/null | grep -q .; then
    p "template: $tpl"
  else
    w "template not found: $tpl"
  fi
done

# ── Git ───────────────────────────────────────────────────────────────────────
echo ""
echo "-- Git"
dirty=$(git -C "$ROOT" status --porcelain 2>/dev/null | grep -v "handoff.md" | wc -l | tr -d ' ')
if [[ "$dirty" -eq 0 ]]; then
  p "working tree clean"
else
  w "${dirty} uncommitted change(s) (excluding handoff.md)"
fi

# Check unpushed commits
unpushed=$(git -C "$ROOT" rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
if [[ "$unpushed" -eq 0 ]]; then
  p "in sync with origin/main"
elif [[ "$unpushed" -le 5 ]]; then
  w "${unpushed} commit(s) ahead of origin/main — run: git push origin main"
else
  f "${unpushed} commits ahead of origin/main — CCR will run stale code until pushed"
fi

stale_handoff=""
if [[ -f "$ROOT/.claude/handoff.md" ]]; then
  if find "$ROOT/.claude/handoff.md" -mmin +1440 | grep -q .; then
    stale_handoff="yes"
    w "handoff.md exists and is >24h old — may be stale"
  else
    p "handoff.md recent"
  fi
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "=== Summary ==="
echo "PASS: $PASS  |  WARN: $WARN  |  FAIL: $FAIL"
if [[ $FAIL -gt 0 ]]; then
  echo "Status: DEGRADED — fix FAIL items before next session"
  exit 2
elif [[ $WARN -gt 0 ]]; then
  echo "Status: OK with warnings"
  exit 1
else
  echo "Status: ALL SYSTEMS GO"
  exit 0
fi
