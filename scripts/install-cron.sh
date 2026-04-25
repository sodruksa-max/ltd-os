#!/usr/bin/env bash
# install-cron.sh — set up cron schedule for daily-brief.sh
# Usage: install-cron.sh [--remove]

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
BRIEF_SCRIPT="$ROOT/scripts/daily-brief.sh"

# --- Pre-checks ---
if [[ ! -f "$BRIEF_SCRIPT" ]]; then
  echo "❌ daily-brief.sh not found at $BRIEF_SCRIPT"
  exit 1
fi

if [[ ! -x "$BRIEF_SCRIPT" ]]; then
  chmod +x "$BRIEF_SCRIPT"
fi

# --- Warning ---
cat <<'EOF'
═══════════════════════════════════════════
  CRON SETUP FOR DAILY BRIEF
═══════════════════════════════════════════

⚠️  BEFORE YOU PROCEED — read this:

Cron will invoke Claude Code automatically at scheduled times.
This means:
  - Claude API will be called without you watching
  - Each invocation costs tokens (~$0.05-0.30 per brief)
  - If API is down, job fails silently (check logs)
  - If there's a bug, it runs every day until you notice

Safety measures built in:
  ✓ Max 3 invocations per day (cost cap)
  ✓ 3-minute timeout per invocation
  ✓ Requires direnv-loaded ANTHROPIC_API_KEY
  ✓ Logs to /tmp/daily-brief-YYYY-MM-DD.log
  ✓ Auto-commits result (or fails loudly)

RECOMMENDATION: Run manually via `bash scripts/daily-brief.sh` for 1-2 weeks first.
Only schedule cron if you ACTUALLY read the brief every day.

EOF

read -rp "Proceed with cron setup? (yes/no): " reply
[[ "$reply" == "yes" ]] || { echo "Aborted."; exit 0; }

# --- Handle removal ---
if [[ "${1:-}" == "--remove" ]]; then
  echo
  echo "→ Removing cron entry for daily-brief..."
  (crontab -l 2>/dev/null | grep -v "$BRIEF_SCRIPT") | crontab -
  echo "✓ Removed. Verify with: crontab -l"
  exit 0
fi

# --- Schedule selection ---
echo
echo "When should the brief run? (cron uses 24-hour time, WSL2 local timezone)"
echo "  1) 7:00 AM weekdays"
echo "  2) 7:00 AM every day"
echo "  3) 8:30 AM every day"
echo "  4) Custom"
read -rp "Choice [1-4]: " choice

case "$choice" in
  1) CRON_TIME="0 7 * * 1-5" ;;
  2) CRON_TIME="0 7 * * *" ;;
  3) CRON_TIME="30 8 * * *" ;;
  4)
    read -rp "Enter cron expression (minute hour day month weekday): " CRON_TIME
    ;;
  *) echo "Invalid choice"; exit 1 ;;
esac

# --- Build cron line ---
# direnv won't work in cron by default — need to source .envrc manually
CRON_CMD="cd $ROOT && /bin/bash -c 'source .envrc 2>/dev/null; bash $BRIEF_SCRIPT' >> /tmp/ltd-os-cron.log 2>&1"
CRON_LINE="$CRON_TIME $CRON_CMD"

# --- Check if already present ---
if crontab -l 2>/dev/null | grep -q "$BRIEF_SCRIPT"; then
  echo
  echo "⚠️  Cron entry for daily-brief already exists:"
  crontab -l 2>/dev/null | grep "$BRIEF_SCRIPT"
  echo
  read -rp "Replace it? (yes/no): " reply
  [[ "$reply" == "yes" ]] || { echo "Aborted."; exit 0; }
  (crontab -l 2>/dev/null | grep -v "$BRIEF_SCRIPT") | crontab -
fi

# --- Add ---
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

echo
echo "✓ Cron entry added:"
echo "  $CRON_LINE"
echo
echo "Verify: crontab -l"
echo "Logs:   tail -f /tmp/ltd-os-cron.log"
echo "Remove: bash scripts/install-cron.sh --remove"
echo
echo "⚠️  WSL2 note: cron only runs when WSL2 is running."
echo "    If you close the WSL2 terminal window, cron STOPS."
echo "    Solutions:"
echo "    1. Keep a WSL2 terminal open"
echo "    2. Use Windows Task Scheduler to run the script (see docs/AUTOMATION.md)"
