#!/usr/bin/env bash
# dashboard.sh — launch the Streamlit trading bot dashboard
# Usage: bash scripts/dashboard.sh
ROOT="$(git rev-parse --show-toplevel)"
STREAMLIT="$ROOT/code/python/.venv/Scripts/streamlit"
exec "$STREAMLIT" run "$ROOT/scripts/dashboard.py" --server.headless true
