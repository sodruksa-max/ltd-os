#!/usr/bin/env bash
# daily-brief.sh — generate morning briefing by calling Claude Code
# Usage: daily-brief.sh [--dry-run]
#
# Can be run manually or from cron (see scripts/install-cron.sh).
# In Phase 1: uses vault data only. Phase 2 will add market data + news.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$HOME/projects/ltd-os")"
cd "$ROOT"

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

# --- Cost cap check (safety) ---
COST_CAP_FILE="$ROOT/.claude/daily-brief.cap"
TODAY=$(date +%Y-%m-%d)
INVOCATIONS_TODAY=0
if [[ -f "$COST_CAP_FILE" ]]; then
  LAST_DATE=$(head -1 "$COST_CAP_FILE" 2>/dev/null || echo "")
  if [[ "$LAST_DATE" == "$TODAY" ]]; then
    INVOCATIONS_TODAY=$(tail -1 "$COST_CAP_FILE" 2>/dev/null || echo 0)
  fi
fi

MAX_DAILY_INVOCATIONS="${DAILY_BRIEF_MAX:-3}"
if [[ "$INVOCATIONS_TODAY" -ge "$MAX_DAILY_INVOCATIONS" ]]; then
  echo "⚠️  Already ran $INVOCATIONS_TODAY daily briefs today (cap: $MAX_DAILY_INVOCATIONS)"
  echo "    Set DAILY_BRIEF_MAX env var to increase. Aborting to prevent cost runaway."
  exit 1
fi

# --- Check prerequisites ---
if ! command -v claude > /dev/null; then
  echo "❌ claude CLI not found. Install Claude Code first."
  exit 1
fi

if [[ ! -d .git ]]; then
  echo "❌ Not a git repo — are you in the right folder?"
  exit 1
fi

# --- Check direnv env loaded (needed for API key) ---
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  # Try to source .envrc
  if [[ -f .envrc ]]; then
    # shellcheck disable=SC1091
    source .envrc 2>/dev/null || true
  fi
  if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
    echo "❌ ANTHROPIC_API_KEY not set. Run 'direnv allow' in project root."
    exit 1
  fi
fi

echo "═══════════════════════════════════════════"
echo "  Daily Brief — $TODAY"
echo "═══════════════════════════════════════════"
echo

# --- Nick kill condition alerts (check before brief) ---
ALERTS_DIR="$ROOT/vault/20_investment/nick/alerts"
if [[ -d "$ALERTS_DIR" ]]; then
  recent_alert=$(find "$ALERTS_DIR" -name "*-alert.md" -mmin -2880 2>/dev/null | sort -r | head -1)
  if [[ -n "$recent_alert" ]]; then
    echo "*** NICK KILL CONDITION ALERT ***"
    echo "   File: $(basename "$recent_alert")"
    echo "   Run /nick-weekly to review triggered positions"
    echo "   ────────────────────────────────────────"
    grep "^\*\*" "$recent_alert" 2>/dev/null | head -5 || true
    echo "   ────────────────────────────────────────"
    echo
  fi
fi

if [[ "$DRY_RUN" == "true" ]]; then
  echo "(DRY RUN — would invoke: claude \"/daily-brief\")"
  echo "Current invocations today: $INVOCATIONS_TODAY/$MAX_DAILY_INVOCATIONS"
  exit 0
fi

# --- Update usage log before brief ---
if [[ -f "$ROOT/code/python/.venv/Scripts/python" ]]; then
  "$ROOT/code/python/.venv/Scripts/python" "$ROOT/scripts/usage-tracker.py" 2>/dev/null || true
elif command -v python3 > /dev/null; then
  python3 "$ROOT/scripts/usage-tracker.py" 2>/dev/null || true
fi

# --- Pull latest from remote first (if remote exists) ---
if git remote | grep -q .; then
  echo "→ Pulling latest from git remote..."
  git pull --quiet 2>&1 | head -5 || echo "  (pull failed or no upstream)"
fi

# --- Invoke Claude Code in non-interactive mode ---
echo "→ Running /daily-brief via Claude Code..."
echo "  (this takes 30-60 seconds)"
echo

# Use claude in "print" mode (non-interactive) — outputs response and exits
# Reference: claude --help for exact flags; this may need adjustment once CLI stabilizes
timeout 180 claude -p "/daily-brief" 2>&1 | tee "/tmp/daily-brief-$TODAY.log"

EXIT_CODE=${PIPESTATUS[0]}

if [[ $EXIT_CODE -eq 124 ]]; then
  echo
  echo "⚠️  Claude timed out after 3 minutes — check network / API status"
  exit 1
elif [[ $EXIT_CODE -ne 0 ]]; then
  echo
  echo "⚠️  Claude exited with code $EXIT_CODE"
  echo "    Log: /tmp/daily-brief-$TODAY.log"
  exit 1
fi

# --- Update invocation counter ---
{
  echo "$TODAY"
  echo "$((INVOCATIONS_TODAY + 1))"
} > "$COST_CAP_FILE"

# --- Commit the daily note if created/updated ---
DAILY_NOTE="vault/daily/$TODAY.md"
if [[ -f "$DAILY_NOTE" ]]; then
  if ! git diff --quiet "$DAILY_NOTE" 2>/dev/null; then
    echo
    echo "→ Auto-committing daily brief..."
    git add "$DAILY_NOTE"
    git commit -q -m "notes: daily brief $TODAY" || echo "  (no changes to commit)"
  fi
fi

echo
echo "═══════════════════════════════════════════"
echo "  ✓ Done"
echo "═══════════════════════════════════════════"
echo "  Brief: $DAILY_NOTE"
echo "  Invocations today: $((INVOCATIONS_TODAY + 1))/$MAX_DAILY_INVOCATIONS"
echo "  Log: /tmp/daily-brief-$TODAY.log"
