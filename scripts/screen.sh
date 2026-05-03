#!/usr/bin/env bash
# Screener launcher
# Usage:
#   bash scripts/screen.sh                  # full momentum screen
#   bash scripts/screen.sh --reversal       # beginning-of-trend mode
#   bash scripts/screen.sh --top 5          # top 5 only
#   bash scripts/screen.sh NVDA AAPL        # specific tickers

ROOT="$(git rev-parse --show-toplevel)"
PYTHON="$ROOT/code/python/.venv/Scripts/python"
exec "$PYTHON" "$ROOT/scripts/screener.py" "$@"
