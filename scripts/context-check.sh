#!/usr/bin/env bash
# context-check.sh — rough estimate of tokens consumed in current Claude Code session
# Limitation: Claude Code doesn't expose exact token counts to scripts
# This is a ROUGH approximation based on file sizes read + known message patterns

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SESSION_DIR="${CLAUDE_SESSION_DIR:-$HOME/.claude/sessions}"

# Claude Sonnet 4.5 context window
MAX_TOKENS=200000
WARN_THRESHOLD=140000   # 70%
CRITICAL_THRESHOLD=180000  # 90%

# Rough char-to-token ratio (safe overestimate: 3 chars/token)
# Thai: ~2-3 chars/token, English: ~4 chars/token → use 3 as worst case
CHARS_PER_TOKEN=3

# Sum sizes of files "likely in context"
# Heuristic: files in .claude/, vault/_memory/, recent git-modified files
total_chars=0

add_chars() {
  local path="$1"
  if [[ -f "$path" ]]; then
    local size=$(wc -c < "$path")
    total_chars=$((total_chars + size))
  fi
}

# Always-loaded files (CLAUDE.md, memory)
add_chars "$ROOT/.claude/CLAUDE.md"
for f in "$ROOT"/vault/_memory/*.md; do
  add_chars "$f"
done

# If handoff exists, it's loaded
add_chars "$ROOT/.claude/handoff.md"

# Files modified in this session (last 1 hour, as proxy)
if command -v find > /dev/null; then
  while IFS= read -r -d '' f; do
    add_chars "$f"
  done < <(find "$ROOT" -type f -name "*.md" -mmin -60 -not -path "*/90_archive/*" -not -path "*/.git/*" -print0 2>/dev/null)
fi

estimated_tokens=$((total_chars / CHARS_PER_TOKEN))
pct=$((estimated_tokens * 100 / MAX_TOKENS))

echo "═══════════════════════════════════════════"
echo "  Context usage (rough estimate)"
echo "═══════════════════════════════════════════"
echo "  Chars tracked: $total_chars"
echo "  Est. tokens:   $estimated_tokens / $MAX_TOKENS"
echo "  Usage:         ${pct}%"
echo

if [[ $estimated_tokens -ge $CRITICAL_THRESHOLD ]]; then
  echo "🚨 CRITICAL: Context at ${pct}% — save handoff and start new session NOW"
  echo "   Run: /handoff"
  exit 2
elif [[ $estimated_tokens -ge $WARN_THRESHOLD ]]; then
  echo "⚠️  WARN: Context at ${pct}% — consider /handoff soon"
  echo "   Run: /handoff  (to save state)"
  echo "   Then: exit + claude (to start fresh session)"
  exit 1
else
  echo "✓ Context OK (${pct}%)"
  exit 0
fi
