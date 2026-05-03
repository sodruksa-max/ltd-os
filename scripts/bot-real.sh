#!/usr/bin/env bash
# Bot launcher tuned for ~50,000 THB (~$1,400 USD) real budget
#
# Maps real budget onto $100k paper account:
#   $1,400 real / $100,000 paper = 1.4% base
#   25% of $1,400 per position = $350 -> size = 0.0035 on paper account
#   2 positions max = uses ~$700 total (~50% of real budget)
#
# Usage:
#   bash scripts/bot-real.sh               # momentum mode, dry-run by default
#   bash scripts/bot-real.sh --live        # remove --dry-run to place orders
#   bash scripts/bot-real.sh --reversal    # beginning-of-trend mode
#   bash scripts/bot-real.sh --reversal --bracket --live  # Option B live

ROOT="$(git rev-parse --show-toplevel)"
PYTHON="$ROOT/code/python/.venv/Scripts/python"

# Strip --live flag (our custom flag), pass rest to auto-buy.py
LIVE=0
ARGS=()
for arg in "$@"; do
  if [[ "$arg" == "--live" ]]; then
    LIVE=1
  else
    ARGS+=("$arg")
  fi
done

if [[ $LIVE -eq 0 ]]; then
  ARGS+=("--dry-run")
fi

exec "$PYTHON" "$ROOT/scripts/auto-buy.py" --size 0.0035 --top 2 "${ARGS[@]}"
