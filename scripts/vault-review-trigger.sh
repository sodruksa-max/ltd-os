#!/bin/bash
# PostToolUse hook — fires when Write tool creates/overwrites vault content files
# Outputs trigger message so Claude runs /review automatically

INPUT=$(cat)

# Extract file_path from Write tool JSON event
PYTHON=$(which python3 2>/dev/null || which python 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | $PYTHON -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(d.get('tool_input', {}).get('file_path', ''))
except:
    print('')
" 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

# Normalize to forward slashes for pattern matching
NORM=$(echo "$FILE_PATH" | tr '\\' '/')

# Detect content type — ordered from most specific to least
if echo "$NORM" | grep -qE "_journal/[^/]+-review\.md$"; then
    # Distinguish lite (market-log) from full post-market review
    FIRST_LINE=$(head -1 "$FILE_PATH" 2>/dev/null || echo "")
    if echo "$FIRST_LINE" | grep -q "\[lite\]"; then
        TYPE="market-log-lite"
    else
        TYPE="post-market-review"
    fi
elif echo "$NORM" | grep -qE "vault/10_research/[^/]+\.md$"; then
    TYPE="research-doc"
elif echo "$NORM" | grep -qE "vault/20_investment/[^/]+\.md$" && \
     ! echo "$NORM" | grep -qE "(_journal|_templates|nick)/"; then
    TYPE="stock-research"
elif echo "$NORM" | grep -qE "vault/30_content/ideas/[^/]+\.md$"; then
    TYPE="idea-card"
elif echo "$NORM" | grep -qE "vault/30_content/[^/]+\.md$" && \
     ! echo "$NORM" | grep -q "vault/30_content/ideas/"; then
    TYPE="content-draft"
else
    # Not a content file we review — exit silently
    exit 0
fi

echo "VAULT_REVIEW_REQUIRED: $TYPE"
echo "file: $FILE_PATH"
echo "→ รัน /review บน file นี้ทันที ก่อนทำอะไรต่อ"
exit 0
