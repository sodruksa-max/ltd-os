---
description: Execute a named workflow from vault/_workflows/ — supports step sequencing, conditional branching, and resume from last completed step.
---

# /workflow

Run a pre-defined multi-step workflow with conditional branching and state persistence.

## Usage

```
/workflow <name>               — run workflow from start (or resume if in-progress today)
/workflow <name> --fresh        — ignore today's state, restart from step 1
/workflow list                 — show all available workflows
```

Examples:
- `/workflow morning`
- `/workflow weekly`
- `/workflow research`
- `/workflow list`

---

## Steps

### 0. Validate input

**If `/workflow list`:**
```bash
ls vault/_workflows/*.md | grep -v ".state" | sed 's|.*/||;s|\.md||'
```
For each file: read `name` + `description` from frontmatter → show table. Done.

**If `/workflow <name>`:**
- Check `vault/_workflows/<name>.md` exists — if not: list available + stop
- Read entire workflow definition file

---

### 1. Check state → offer resume

```bash
bash scripts/workflow-state.sh read <name>
```

- If state file exists and `status = "in-progress"`:
  - Show: `📋 Found in-progress run from today. Last completed: <step-id>. Resume from <next-step>? (yes / restart)`
  - If user says restart: `--fresh` mode, re-init state
  - If user says yes (or no input): resume from next step after `last_completed`
- If `--fresh` flag or no state: init fresh state
  ```bash
  bash scripts/workflow-state.sh init <name>
  ```
- If state exists and `status = "completed"`: notify "Workflow already completed today" → ask if user wants to run again with `--fresh`

---

### 2. Collect required inputs (before starting any step)

Scan all steps in workflow definition for `requires-input` fields.

For each input required:
- Ask user once, upfront, before execution begins
- Store answers for use during step execution

Example for `research` workflow:
> "Step-1 ต้องการ topic — รัน /paper-survey เรื่องอะไร?"

---

### 3. Execute steps in order

For each step in the workflow definition:

#### 3a. Check if step should be skipped (resume mode)
- If state shows this step as `completed` or `skipped` → skip with note `[ALREADY DONE: step-X]`
- Otherwise proceed

#### 3b. Evaluate condition (if step has one)
Read the `condition` field:
- **Output-based condition:** evaluate using content already in Claude's context from prior step output
  - VIX value from /pre-market → compare to threshold
  - Count of Evolving/Invalidated from /nick-weekly output → compare to threshold
  - EARLY★ tickers from universe-screen → check if any exist
- **Interactive condition:** ask user directly (e.g., "ต้องการ deep-dive หุ้นไหม?")

Condition result:
- `yes` → run `yes-cmd` (substitute collected inputs if needed)
- `no` → mark step as `skipped`, proceed to next

#### 3c. Execute step command

Follow the full instructions of the referenced command (e.g., `/pre-market` means execute everything in `.claude/commands/pre-market.md`).

Announce before execution:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ Step [N/Total]: <step-id>
   Command: <cmd>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 3d. Write state after step

```bash
bash scripts/workflow-state.sh mark <name> <step-id> <completed|skipped|failed>
```

#### 3e. Handle failure

Check `on-fail` field:
- `stop` → mark workflow failed, finish state, show error + resume instruction, stop
- `continue` → log warning, proceed to next step

---

### 4. Finish workflow

```bash
bash scripts/workflow-state.sh finish <name> completed
```

Calculate duration (started vs now). Count steps done vs total.

```bash
bash scripts/workflow-state.sh log <name> "<duration>m" <done> <total> completed
```

---

### 5. Report to user

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Workflow complete: <name>
Duration: ~<N> min | Steps: <done>/<total>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Steps summary:
  ✓ step-1: <name>        [completed]
  ⏭ step-2: <name>        [skipped — condition: <result>]
  ✓ step-3: <name>        [completed]

Run logged to vault/_memory/WORKFLOWS.md
```

---

## Constraint rules

- **ห้าม skip step โดยไม่แจ้ง** — ทุก skip ต้องระบุเหตุผล (condition false / resume)
- **ห้าม re-fetch data ที่ step ก่อนหน้าดึงมาแล้ว** — ใช้ context จาก prior step output ตาม ToolCaching rule
- **Condition evaluation ต้องอิงจาก evidence จริง** — ห้ามสมมติ condition result โดยไม่มี data
- **State file อัปเดตหลังทุก step** — ถ้า Claude crash กลางทาง ก็ resume จาก state ได้
- **Duration estimate:** ประมาณจาก estimated-time ใน workflow frontmatter + steps ที่รันจริง

## Failure resume message format

```
⚠️ Workflow interrupted at: <step-id>
State saved: vault/_workflows/.state/<name>-<date>.json
To resume: /workflow <name>
To restart: /workflow <name> --fresh
```

## Available workflows

ดู `vault/_workflows/*.md` สำหรับ list ทั้งหมด — เพิ่ม workflow ใหม่ด้วย `/new-workflow`
