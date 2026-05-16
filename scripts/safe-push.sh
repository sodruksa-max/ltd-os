#!/usr/bin/env bash
# safe-push.sh — pull with rebase then push to origin/main
# Usage: ./scripts/safe-push.sh
# Run after safe-commit.sh to sync local commits to GitHub (required for CCR)

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

unpushed=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
if [[ "$unpushed" -eq 0 ]]; then
  echo "✓ Already in sync with origin/main — nothing to push"
  exit 0
fi

echo "→ Pulling remote changes (rebase)..."
git pull --rebase origin main

echo "→ Pushing $unpushed commit(s) to origin/main..."
git push origin main

echo "✓ Pushed. Remote is now up to date."
echo "  CCR routines will use the latest code on next run."
