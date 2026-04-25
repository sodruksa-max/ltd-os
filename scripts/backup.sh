#!/usr/bin/env bash
# backup.sh — backup ltd-os to: (1) git remote, (2) local zip snapshot
# Does NOT push to public repo. Warns if no remote configured.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

echo "═══════════════════════════════════════════"
echo "  LTD-OS Backup"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════"
echo

# 1. Verify we're in a git repo
if [[ ! -d .git ]]; then
  echo "❌ Not a git repo. Run bootstrap.sh first."
  exit 1
fi

# 2. Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "⚠️  Uncommitted changes detected."
  git status --short
  echo
  read -rp "Continue backup anyway? (y/N): " reply
  [[ "$reply" =~ ^[Yy]$ ]] || exit 1
fi

# 3. Push to git remote (if configured)
echo "→ [1/2] Git remote push..."
if git remote | grep -q .; then
  REMOTE=$(git remote | head -1)
  BRANCH=$(git branch --show-current)
  echo "  Pushing to $REMOTE/$BRANCH..."
  if git push "$REMOTE" "$BRANCH" 2>&1; then
    echo "  ✓ Pushed to $REMOTE"
  else
    echo "  ⚠️  Push failed (may need auth / no changes / conflict)"
  fi
else
  echo "  ⚠️  No git remote configured."
  echo "     Add one with: git remote add origin git@github.com:USER/REPO.git"
  echo "     (Use PRIVATE repo — vault may contain personal data)"
fi
echo

# 4. Local zip snapshot
echo "→ [2/2] Local zip snapshot..."
BACKUP_ROOT="${LTD_BACKUP_DIR:-$HOME/ltd-os-backups}"
mkdir -p "$BACKUP_ROOT"

STAMP=$(date +%Y%m%d-%H%M%S)
ZIP_FILE="$BACKUP_ROOT/ltd-os-$STAMP.zip"

# Exclude secrets + temporary files + node_modules + venv
cd "$(dirname "$ROOT")"
zip -rq "$ZIP_FILE" "$(basename "$ROOT")" \
  -x "*/.secrets/.env" \
  -x "*/.secrets/*.key" \
  -x "*/.secrets/*.pem" \
  -x "*/node_modules/*" \
  -x "*/venv/*" \
  -x "*/.venv/*" \
  -x "*/__pycache__/*" \
  -x "*/.next/*" \
  -x "*/.git/objects/pack/*" \
  -x "*/90_archive/*"  # archive not in regular backup (size)

SIZE=$(du -h "$ZIP_FILE" | cut -f1)
echo "  ✓ Snapshot: $ZIP_FILE ($SIZE)"
echo

# 5. Cleanup old backups (keep last 14)
echo "→ Cleanup old snapshots..."
cd "$BACKUP_ROOT"
COUNT=$(ls -1 ltd-os-*.zip 2>/dev/null | wc -l)
if [[ "$COUNT" -gt 14 ]]; then
  ls -1t ltd-os-*.zip | tail -n +15 | while read -r f; do
    rm "$f"
    echo "  Removed: $f"
  done
fi
REMAINING=$(ls -1 ltd-os-*.zip 2>/dev/null | wc -l)
echo "  Kept $REMAINING snapshots in $BACKUP_ROOT"

echo
echo "═══════════════════════════════════════════"
echo "  ✓ Backup complete"
echo "═══════════════════════════════════════════"
echo
echo "Storage locations:"
echo "  - Git remote: $(git remote -v | head -1 || echo 'NOT CONFIGURED')"
echo "  - Local zips: $BACKUP_ROOT"
echo
echo "For offsite backup, sync $BACKUP_ROOT to:"
echo "  - OneDrive (symlink or rclone)"
echo "  - Google Drive (rclone)"
echo "  - External drive"
echo
echo "Next: see docs/DISASTER_RECOVERY.md for restore steps"
