#!/usr/bin/env bash
# weekly-review.sh — run every Sunday (or manually)
# Reports inbox, activity, git commits, section sizes, cost.
# Suggests condensations and analyst review. Never modifies.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INBOX="$ROOT/vault/00_inbox"
WEEK=$(date +%Y-W%V)

# Thresholds
CONDENSE_NOTE_COUNT=40
STALE_INBOX_DAYS=7

echo "═══════════════════════════════════════════"
echo "  Weekly Review — $WEEK"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════"
echo

# --- Inbox status ---
INBOX_COUNT=$(find "$INBOX" -type f -name "*.md" 2>/dev/null | wc -l)
echo "📥 Inbox: $INBOX_COUNT items"
if [[ "$INBOX_COUNT" -gt 0 ]]; then
  find "$INBOX" -type f -name "*.md" -printf "   - %f (modified %TY-%Tm-%Td)\n" 2>/dev/null | head -20
fi
echo

STALE=$(find "$INBOX" -type f -name "*.md" -mtime +$STALE_INBOX_DAYS 2>/dev/null | wc -l)
if [[ "$STALE" -gt 0 ]]; then
  echo "⚠️  $STALE inbox items >$STALE_INBOX_DAYS days old — sort or archive"
  echo
fi

# --- Recent activity per folder ---
echo "📝 Notes added in last 7 days:"
for folder in 10_research 20_investment 30_content 40_projects daily; do
  if [[ -d "$ROOT/vault/$folder" ]]; then
    count=$(find "$ROOT/vault/$folder" -type f -name "*.md" -mtime -7 2>/dev/null | wc -l)
    printf "   %-20s %d\n" "$folder" "$count"
  fi
done
echo

# --- Section size check (condensation candidates) ---
echo "📊 Section sizes (condensation threshold: $CONDENSE_NOTE_COUNT notes):"
CONDENSE_SUGGESTIONS=()
for folder in $(find "$ROOT/vault" -maxdepth 2 -type d -not -path "*/90_archive/*" -not -path "*/_*" -not -path "*/.obsidian*" 2>/dev/null); do
  count=$(find "$folder" -maxdepth 1 -type f -name "*.md" 2>/dev/null | wc -l)
  if [[ "$count" -ge "$CONDENSE_NOTE_COUNT" ]]; then
    rel="${folder#$ROOT/}"
    printf "   ⚠️  %-35s %d notes — consider /condense\n" "$rel" "$count"
    CONDENSE_SUGGESTIONS+=("$rel")
  elif [[ "$count" -ge 20 ]]; then
    rel="${folder#$ROOT/}"
    printf "   %-35s %d notes\n" "$rel" "$count"
  fi
done
echo

# --- Oversized individual notes ---
echo "📏 Oversized notes (>2000 words):"
LARGE_NOTES=$(find "$ROOT/vault" -type f -name "*.md" -not -path "*/90_archive/*" -not -path "*/_moc/*" -exec sh -c 'wc -w "$1" 2>/dev/null | awk -v f="$1" "{if (\$1 > 2000) print \$1, f}"' _ {} \; 2>/dev/null | head -10)
if [[ -n "$LARGE_NOTES" ]]; then
  echo "$LARGE_NOTES" | while read -r count path; do
    rel="${path#$ROOT/}"
    printf "   %5d words  %s\n" "$count" "$rel"
  done
  echo "   → Consider splitting with wikilinks"
else
  echo "   (none)"
fi
echo

# --- Git activity ---
echo "📜 Git commits this week:"
cd "$ROOT"
git log --since="7 days ago" --pretty=format:"   %h %s" 2>/dev/null | head -15 || echo "   (no commits)"
echo
echo

# --- Handoff state ---
if [[ -f "$ROOT/.claude/handoff.md" ]]; then
  HANDOFF_AGE_DAYS=$(( ($(date +%s) - $(stat -c %Y "$ROOT/.claude/handoff.md")) / 86400 ))
  if [[ "$HANDOFF_AGE_DAYS" -gt 2 ]]; then
    echo "⚠️  Stale handoff: .claude/handoff.md (age: ${HANDOFF_AGE_DAYS}d)"
    echo "   Either resume it or delete it"
    echo
  fi
fi

# --- Memory index sanity check ---
echo "🧠 Memory index:"
MEMORY_SIZE=$(du -ch "$ROOT/vault/_memory/"*.md 2>/dev/null | tail -1 | cut -f1)
echo "   Total size: $MEMORY_SIZE"
PROJECTS_LINES=$(wc -l < "$ROOT/vault/_memory/PROJECTS.md" 2>/dev/null || echo 0)
DECISIONS_LINES=$(wc -l < "$ROOT/vault/_memory/DECISIONS.md" 2>/dev/null || echo 0)
printf "   PROJECTS.md:   %d lines\n" "$PROJECTS_LINES"
printf "   DECISIONS.md:  %d lines\n" "$DECISIONS_LINES"
if [[ "$DECISIONS_LINES" -gt 100 ]]; then
  echo "   ⚠️  DECISIONS.md long — consider pruning oldest decisions into vault/90_archive/"
fi
echo

# --- Cost report (if available) ---
if [[ -x "$ROOT/scripts/cost-report.sh" ]]; then
  echo "💸 Cost report (last 7 days):"
  "$ROOT/scripts/cost-report.sh" --period week 2>/dev/null | grep -E "(Total|Estimated|Top)" | sed 's/^/   /' || echo "   (no data)"
  echo
fi

# --- Save review log ---
LOG_DIR="$ROOT/vault/90_archive/weekly-reviews"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$WEEK.md"

{
  echo "---"
  echo "type: weekly-review"
  echo "week: $WEEK"
  echo "generated: $(date -Iseconds)"
  echo "tags: [weekly-review]"
  echo "---"
  echo
  echo "# Weekly Review — $WEEK"
  echo
  echo "## Inbox"
  echo "- Items: $INBOX_COUNT"
  echo "- Stale (>${STALE_INBOX_DAYS}d): $STALE"
  echo
  echo "## Activity"
  for folder in 10_research 20_investment 30_content 40_projects daily; do
    if [[ -d "$ROOT/vault/$folder" ]]; then
      count=$(find "$ROOT/vault/$folder" -type f -name "*.md" -mtime -7 2>/dev/null | wc -l)
      echo "- $folder: $count notes"
    fi
  done
  echo
  if [[ ${#CONDENSE_SUGGESTIONS[@]} -gt 0 ]]; then
    echo "## Condensation suggestions"
    for s in "${CONDENSE_SUGGESTIONS[@]}"; do
      echo "- \`/condense $s\`"
    done
    echo
  fi
  echo "## Commits"
  echo '```'
  git log --since="7 days ago" --pretty=format:"%h %s" 2>/dev/null | head -30 || echo "(none)"
  echo
  echo '```'
  echo
  echo "## Memory index"
  echo "- Size: $MEMORY_SIZE"
  echo "- PROJECTS.md: $PROJECTS_LINES lines"
  echo "- DECISIONS.md: $DECISIONS_LINES lines"
  echo
  echo "## Key learnings"
  echo
  echo "<!-- Run /weekly-learnings in Claude Code to have Claude distill this"
  echo "     from daily notes + commits + new content this week.                -->"
  echo "<!-- Or fill in manually. Keep to ~1 page, ≤500 words.                   -->"
  echo
  echo "### Themes I kept coming back to"
  echo "- "
  echo
  echo "### What I learned"
  echo "- "
  echo
  echo "### What surprised me"
  echo "- "
  echo
  echo "### Mistakes / what didn't work"
  echo "- "
  echo
  echo "### Open questions"
  echo "- "
  echo
  echo "## Next week — TODO"
  echo "- [ ] (fill in manually)"
} > "$LOG"

echo "✓ Saved log: vault/90_archive/weekly-reviews/$WEEK.md"
echo

# --- Suggestions ---
echo "═══════════════════════════════════════════"
echo "  Suggested actions"
echo "═══════════════════════════════════════════"

if [[ "$INBOX_COUNT" -gt 5 ]]; then
  echo "📥 Sort inbox: open Claude Code → \"sort my inbox notes\""
fi

if [[ ${#CONDENSE_SUGGESTIONS[@]} -gt 0 ]]; then
  echo "📂 Condense sections:"
  for s in "${CONDENSE_SUGGESTIONS[@]}"; do
    echo "   /condense $s"
  done
fi

# Suggest /weekly-learnings if daily notes exist
DAILY_COUNT=$(find "$ROOT/vault/daily" -type f -name "*.md" -mtime -7 2>/dev/null | wc -l)
if [[ "$DAILY_COUNT" -ge 3 ]]; then
  echo "📝 Distill this week: /weekly-learnings  (Claude harvests key learnings from daily notes)"
fi

echo "🧐 Deep review: /analyst  (cost + performance insights)"
echo "💾 Backup: bash scripts/backup.sh"
echo
