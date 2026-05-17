#!/usr/bin/env bash
# workflow-state.sh — read/write workflow execution state
# Usage:
#   workflow-state.sh init   <name>               → create state file for today
#   workflow-state.sh mark   <name> <step> <status>  → completed|skipped|failed
#   workflow-state.sh read   <name>               → print JSON state
#   workflow-state.sh resume <name>               → print last completed step ID
#   workflow-state.sh finish <name> <status>      → mark workflow done (completed|failed|aborted)
#   workflow-state.sh log    <name> <duration> <steps_done> <steps_total>  → append to WORKFLOWS.md auto-log

set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATE_DIR="$ROOT/vault/_workflows/.state"
WORKFLOWS_MEM="$ROOT/vault/_memory/WORKFLOWS.md"

cmd="${1:-}"
name="${2:-}"

if [[ -z "$cmd" || -z "$name" ]]; then
  echo "Usage: workflow-state.sh <init|mark|read|resume|finish|log> <workflow-name> [args]" >&2
  exit 1
fi

today=$(date '+%Y-%m-%d')
state_file="$STATE_DIR/${name}-${today}.json"

case "$cmd" in

  init)
    mkdir -p "$STATE_DIR"
    cat > "$state_file" <<EOF
{
  "workflow": "$name",
  "date": "$today",
  "started": "$(date '+%Y-%m-%dT%H:%M:%S')",
  "steps": {},
  "last_completed": null,
  "status": "in-progress"
}
EOF
    echo "State initialized: $state_file"
    ;;

  mark)
    step="${3:-}"
    status="${4:-}"
    if [[ -z "$step" || -z "$status" ]]; then
      echo "Usage: workflow-state.sh mark <name> <step> <completed|skipped|failed>" >&2
      exit 1
    fi
    if [[ ! -f "$state_file" ]]; then
      echo "No state file for $name today — run init first" >&2
      exit 1
    fi
    # Update step status using Python (available in venv or system)
    python3 - "$state_file" "$step" "$status" <<'PYEOF'
import sys, json
f, step, status = sys.argv[1], sys.argv[2], sys.argv[3]
with open(f) as fh: data = json.load(fh)
data["steps"][step] = status
if status == "completed":
    data["last_completed"] = step
with open(f, "w") as fh: json.dump(data, fh, indent=2)
PYEOF
    echo "Marked $step → $status"
    ;;

  read)
    if [[ -f "$state_file" ]]; then
      cat "$state_file"
    else
      echo "{}"
    fi
    ;;

  resume)
    if [[ -f "$state_file" ]]; then
      python3 - "$state_file" <<'PYEOF'
import sys, json
with open(sys.argv[1]) as f: data = json.load(f)
print(data.get("last_completed") or "")
PYEOF
    else
      echo ""
    fi
    ;;

  finish)
    final_status="${3:-completed}"
    if [[ ! -f "$state_file" ]]; then
      echo "No state file for $name today" >&2
      exit 1
    fi
    python3 - "$state_file" "$final_status" <<'PYEOF'
import sys, json
from datetime import datetime
f, status = sys.argv[1], sys.argv[2]
with open(f) as fh: data = json.load(fh)
data["status"] = status
data["finished"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
with open(f, "w") as fh: json.dump(data, fh, indent=2)
PYEOF
    echo "Workflow $name finished: $final_status"
    ;;

  log)
    duration="${3:-?}"
    steps_done="${4:-?}"
    steps_total="${5:-?}"
    status_label="${6:-completed}"
    # Append run to WORKFLOWS.md auto-log section
    log_line="| $(date '+%Y-%m-%d %H:%M') | $name | ~${duration} | ${steps_done}/${steps_total} | $status_label |"
    if grep -q "^## Auto-Log" "$WORKFLOWS_MEM" 2>/dev/null; then
      # Insert after the header row separator
      python3 - "$WORKFLOWS_MEM" "$log_line" <<'PYEOF'
import sys
path, line = sys.argv[1], sys.argv[2]
with open(path) as f: content = f.read()
marker = "| --- | --- | --- | --- | --- |"
if marker in content:
    content = content.replace(marker, marker + "\n" + line, 1)
with open(path, "w") as f: f.write(content)
PYEOF
    else
      # Create auto-log section at end of file
      cat >> "$WORKFLOWS_MEM" <<EOF

---

## Auto-Log

*Auto-appended by /workflow runs — do not edit manually*

| Date | Workflow | Duration | Steps | Status |
| --- | --- | --- | --- | --- |
$log_line
EOF
    fi
    echo "Logged run to WORKFLOWS.md"
    ;;

  *)
    echo "Unknown command: $cmd" >&2
    exit 1
    ;;
esac
