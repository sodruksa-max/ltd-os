#!/usr/bin/env bash
# cost-report.sh — estimate Claude API costs from Claude Code usage
# Usage: cost-report.sh [--period day|week|month] [--format text|json]

set -euo pipefail

PERIOD="${2:-week}"
FORMAT="text"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --period) PERIOD="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Claude Sonnet 4.5 pricing (as of 2026-04) — UPDATE if pricing changes
# https://docs.claude.com/en/docs/about-claude/pricing
INPUT_COST_PER_MTOK=3.00   # $3 / 1M tokens
OUTPUT_COST_PER_MTOK=15.00 # $15 / 1M tokens

# Claude Code logs location (may vary)
LOG_CANDIDATES=(
  "$HOME/.claude/projects"
  "$HOME/.config/claude-code/logs"
  "$HOME/.claude-code"
)

LOG_DIR=""
for candidate in "${LOG_CANDIDATES[@]}"; do
  if [[ -d "$candidate" ]]; then
    LOG_DIR="$candidate"
    break
  fi
done

if [[ -z "$LOG_DIR" ]]; then
  echo "⚠️  Claude Code log directory not found at standard locations."
  echo "    Tried: ${LOG_CANDIDATES[*]}"
  echo "    Set CLAUDE_LOG_DIR env var to override."
  echo
  echo "Showing TEMPLATE output — no real data available:"
  echo
fi

LOG_DIR="${CLAUDE_LOG_DIR:-$LOG_DIR}"

# Period to seconds
case "$PERIOD" in
  day)   SECS=86400 ;;
  week)  SECS=604800 ;;
  month) SECS=2592000 ;;
  *)     SECS=604800 ;;
esac

CUTOFF=$(($(date +%s) - SECS))

if [[ "$FORMAT" == "text" ]]; then
  echo "═══════════════════════════════════════════"
  echo "  Claude Code Cost Report"
  echo "  Period: last $PERIOD"
  echo "═══════════════════════════════════════════"
  echo
fi

# Parse JSONL logs if available
total_input=0
total_output=0
declare -A agent_input
declare -A agent_output
declare -A agent_count

if [[ -n "$LOG_DIR" && -d "$LOG_DIR" ]]; then
  # Find session files modified within period
  while IFS= read -r -d '' file; do
    # Parse JSONL if jq available
    if command -v jq > /dev/null; then
      while IFS= read -r line; do
        # Extract usage from assistant messages
        input_tok=$(echo "$line" | jq -r '.message.usage.input_tokens // 0' 2>/dev/null || echo 0)
        output_tok=$(echo "$line" | jq -r '.message.usage.output_tokens // 0' 2>/dev/null || echo 0)
        agent=$(echo "$line" | jq -r '.subagent // "main"' 2>/dev/null || echo main)
        
        total_input=$((total_input + input_tok))
        total_output=$((total_output + output_tok))
        agent_input[$agent]=$((${agent_input[$agent]:-0} + input_tok))
        agent_output[$agent]=$((${agent_output[$agent]:-0} + output_tok))
        agent_count[$agent]=$((${agent_count[$agent]:-0} + 1))
      done < "$file"
    fi
  done < <(find "$LOG_DIR" -type f \( -name "*.jsonl" -o -name "*.log" \) -newer /tmp/.cutoff_marker 2>/dev/null -print0 || true)
fi

# Calculate costs (using bc for float math)
if command -v bc > /dev/null; then
  input_cost=$(echo "scale=2; $total_input * $INPUT_COST_PER_MTOK / 1000000" | bc 2>/dev/null || echo "0.00")
  output_cost=$(echo "scale=2; $total_output * $OUTPUT_COST_PER_MTOK / 1000000" | bc 2>/dev/null || echo "0.00")
  total_cost=$(echo "scale=2; $input_cost + $output_cost" | bc 2>/dev/null || echo "0.00")
else
  input_cost="0.00"
  output_cost="0.00"
  total_cost="0.00"
fi

if [[ "$FORMAT" == "json" ]]; then
  cat <<EOF
{
  "period": "$PERIOD",
  "total_input_tokens": $total_input,
  "total_output_tokens": $total_output,
  "input_cost_usd": $input_cost,
  "output_cost_usd": $output_cost,
  "total_cost_usd": $total_cost,
  "by_agent": {
EOF
  first=true
  for agent in "${!agent_input[@]}"; do
    [[ "$first" == "false" ]] && echo ","
    first=false
    printf '    "%s": {"input_tokens": %d, "output_tokens": %d, "invocations": %d}' \
      "$agent" "${agent_input[$agent]}" "${agent_output[$agent]}" "${agent_count[$agent]}"
  done
  echo
  echo "  }"
  echo "}"
else
  echo "Total tokens:    $(printf "%'d" $((total_input + total_output)))"
  echo "  Input:         $(printf "%'d" $total_input)"
  echo "  Output:        $(printf "%'d" $total_output)"
  echo
  echo "Estimated cost:  \$$total_cost USD"
  echo "  Input:         \$$input_cost"
  echo "  Output:        \$$output_cost"
  echo
  
  if [[ ${#agent_input[@]} -gt 0 ]]; then
    echo "By agent:"
    for agent in "${!agent_input[@]}"; do
      in_tok=${agent_input[$agent]}
      out_tok=${agent_output[$agent]}
      count=${agent_count[$agent]}
      printf "  %-20s %10s tokens  %s invocations\n" \
        "$agent" "$(printf "%'d" $((in_tok + out_tok)))" "$count"
    done
    echo
  fi
  
  # Append to cost log
  LOG_FILE="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/vault/_memory/COST_LOG.md"
  if [[ -f "$LOG_FILE" ]]; then
    {
      echo ""
      echo "## $(date '+%Y-%m-%d') — $PERIOD report"
      echo "- Total: \$$total_cost ($(printf "%'d" $((total_input + total_output))) tokens)"
      echo "- Input: \$$input_cost, Output: \$$output_cost"
    } >> "$LOG_FILE"
    echo "Logged to: vault/_memory/COST_LOG.md"
  fi
fi
