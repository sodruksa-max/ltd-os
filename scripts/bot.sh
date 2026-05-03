#!/usr/bin/env bash
# Auto-buy bot launcher
# Usage:
#   bash scripts/bot.sh                            # momentum mode, live paper
#   bash scripts/bot.sh --dry-run                  # preview only
#   bash scripts/bot.sh --reversal --bracket       # Option B (beginning-of-trend + bracket exits)
#   bash scripts/bot.sh --reversal --bracket --dry-run
#   bash scripts/bot.sh --top 3 --size 0.03

ROOT="$(git rev-parse --show-toplevel)"
PYTHON="$ROOT/code/python/.venv/Scripts/python"
exec "$PYTHON" "$ROOT/scripts/auto-buy.py" "$@"
