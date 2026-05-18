#!/usr/bin/env bash
# Nick v3 daily routine — run every US trading day pre-market
# Usage: bash scripts/nick-daily.sh [--live]
#   default: signals update + dry-run preview only
#   --live:  signals update + dry-run + prompt before live scan

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="$REPO/code/python/.venv/Scripts/python"
DAILY_SCAN="$REPO/code/python/nick_trader/daily_scan.py"
SIGNALS_UPDATE="$REPO/scripts/nick-signals-update.py"

LIVE=false
for arg in "$@"; do
  [[ "$arg" == "--live" ]] && LIVE=true
done

echo ""
echo "=== Nick v3 Daily Routine — $(date '+%Y-%m-%d %H:%M') ==="
echo ""

# Step 1: Update nick-signals.md
echo "[1/3] Updating nick-signals.md..."
"$PYTHON" "$SIGNALS_UPDATE"
echo ""

# Step 2: Dry-run preview
echo "[2/3] Dry-run preview..."
"$PYTHON" "$DAILY_SCAN" --dry-run
echo ""

# Step 3: Live scan (only with --live flag)
if [[ "$LIVE" == true ]]; then
  echo "[3/3] Live scan..."
  read -r -p "  Review dry-run above. Execute live scan? [y/N] " confirm
  if [[ "${confirm:-N}" =~ ^[Yy]$ ]]; then
    "$PYTHON" "$DAILY_SCAN"
  else
    echo "  Live scan skipped."
  fi
else
  echo "[3/3] Skipped live scan (pass --live to enable)"
fi

echo ""
echo "Done."
