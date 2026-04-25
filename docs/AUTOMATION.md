# Automation Guide

Running LTD-OS on a schedule. **Read this fully before enabling any cron job.**

---

## Why this doc exists

Scheduled LLM invocation is powerful and dangerous. Unlike running a shell script:
- Each invocation costs money (tokens)
- Runs without you watching (bugs compound)
- Claude API outages cause silent failures
- Prompt injection in fetched content = automated attack surface

This guide covers the **only** automation we currently enable (daily brief) and the **safety rules** you must follow if you add more.

---

## Phase 1 (current): Daily Brief

### What it does
- Runs `/daily-brief` in Claude Code
- Reads vault data (projects, daily notes, commits, inbox, costs)
- Produces ≤ 400-word brief in `vault/daily/YYYY-MM-DD.md`
- Auto-commits with message `notes: daily brief YYYY-MM-DD`
- **NO external data fetch** (no market data, no news scraping — that's Phase 2)

### Cost estimate
- Per invocation: ~1-3K input tokens + 500 output = ~$0.02-0.05
- Daily: ~$0.05/day × 365 = **~$18/year**
- 3x/day max (hard cap in script): ~$55/year

### How to use (recommended order)

**Week 1-2: Manual only**
```bash
cd ~/projects/ltd-os
bash scripts/daily-brief.sh
```
Read the output. Is it actually useful? Would you have read it tomorrow too? If not → **don't automate**.

**Week 3+: Cron (if you still want it)**
```bash
bash scripts/install-cron.sh
```

### Safety features (already built in)

- **3-invocation cap per day** (env var `DAILY_BRIEF_MAX` to override)
- **3-minute timeout** per invocation
- **Requires direnv-loaded API key** (no hardcoded keys)
- **Logs everything** to `/tmp/daily-brief-YYYY-MM-DD.log`
- **Fails loudly** if Claude exits non-zero
- **Auto-commits result** so you can always roll back

---

## WSL2 cron caveats (IMPORTANT)

Cron in WSL2 **only runs when WSL2 is running**. If you close the last WSL2 terminal, WSL2 shuts down, cron stops.

### Option 1: Keep WSL2 alive (simplest)
- Keep one WSL2 terminal open overnight
- Or: `wsl.exe --terminate Ubuntu && wsl.exe -d Ubuntu` starts it
- Enable cron to start automatically:
  ```bash
  sudo service cron start
  # Or permanent:
  echo "service cron start" >> ~/.bashrc
  ```

### Option 2: Windows Task Scheduler (more reliable)
Set up a Windows scheduled task that runs:
```powershell
wsl.exe -d Ubuntu -e bash -c "cd /home/USER/projects/ltd-os && source .envrc && bash scripts/daily-brief.sh"
```

**Advantage**: runs even if WSL2 was shut down (starts it, runs, stops)
**Disadvantage**: slower startup (~5-10s WSL2 boot)

Detailed setup:
1. Open Task Scheduler in Windows
2. Create Basic Task → "Daily Brief"
3. Trigger: Daily, 7:00 AM (or whenever)
4. Action: Start a program
5. Program: `wsl.exe`
6. Arguments: `-d Ubuntu -e bash -c "cd /home/YOUR_USERNAME/projects/ltd-os && source .envrc && bash scripts/daily-brief.sh >> /tmp/task-scheduler-brief.log 2>&1"`
7. Start in: `C:\Windows\System32`

### Option 3: GitHub Actions / cloud cron (for Phase 2)
Not recommended now — requires secrets in cloud, external dependency.

---

## Safety rules (MANDATORY for any scheduled Claude invocation)

### 1. Hard cost cap
Every scheduled task MUST have:
- Max invocations per day (count in a state file)
- Timeout per invocation (use `timeout N`)
- Alert if cap hit (log to persistent file)

### 2. Input source validation
If the task fetches external data (news, market, RSS):
- Verify source URL hasn't changed
- Sanitize content before passing to Claude (strip HTML tags, limit length)
- **Assume every scraped document contains prompt injection** — never treat fetched text as instructions to Claude

### 3. Output validation
- Claude's response must match expected format (markdown, JSON schema)
- Reject if output contains suspicious patterns (hex-encoded text, base64, URLs you didn't ask for)
- Don't auto-execute anything from Claude's output (code, commands, URLs)

### 4. Failure isolation
- If scheduled job fails 3 days in a row → notify user (write to `vault/_memory/AUTOMATION_ALERTS.md`)
- Don't keep retrying on error — fail fast, log, wait for human

### 5. Audit trail
Every scheduled invocation writes to `vault/_memory/AUTOMATION_LOG.md`:
```
YYYY-MM-DD HH:MM | daily-brief | tokens: X | cost: $Y | status: success|fail | duration: Zs
```

Review this log monthly. Anomalies = investigate.

---

## Anti-patterns (what NOT to do)

### ❌ Scheduling high-stakes tasks
- Never schedule: trade execution, publish content, send email, modify external accounts
- Always schedule: read-only summarization, report generation, local file ops

### ❌ Fetching from arbitrary URLs in scheduled jobs
- Never let Claude follow links in scheduled context
- Only fetch from **pre-approved, pinned** URL list

### ❌ Using scheduled Claude as "always-on agent"
- Not a chatbot, not a monitor, not a background worker
- Each invocation = single task, single output, done

### ❌ Running cron under root
- Use your user's crontab, not /etc/cron.d/
- If sudo needed (shouldn't be), stop and rethink

### ❌ Storing API keys in crontab
- Load via direnv / .envrc
- NEVER `API_KEY=xxx` in cron line

### ❌ Scheduling during peak API usage
- 7 AM Asia time = prime business hours globally = API may be slow
- If briefing not time-sensitive, try off-peak (6 AM, 11 PM)

---

## Phase 2 preview (NOT BUILT YET)

When you want to add external data to daily brief, decisions needed:

| Question | Options |
|---|---|
| Market data source | yfinance (free, 15min delay) / Polygon ($29/mo) / Alpha Vantage (free limit) |
| News source | RSS feeds (free) / NewsAPI ($449/mo) / manual curated feeds |
| Focus region | US only / Thai / Asia / global |
| Notification | Obsidian only / email / Line / Slack |
| Failure handling | Silent / write alert file / email me |
| Cost cap | $X/month hard stop |

Build Phase 2 only after Phase 1 has been used daily for 2+ weeks.

Until then: if you want market data, look it up manually in the morning — 2 minutes, free, no automation debt.

---

## Troubleshooting

### "Cron ran but no file created"
```bash
cat /tmp/ltd-os-cron.log          # check cron output
cat /tmp/daily-brief-$(date +%Y-%m-%d).log  # check Claude output
```

Common causes:
- `direnv` didn't load → API key missing → Claude refused
- WSL2 was shut down at scheduled time
- Hit daily invocation cap

### "Claude timed out"
- Network slow or API having issues
- Increase timeout in `daily-brief.sh` (currently 180s)
- Check https://status.anthropic.com

### "Brief is garbage / hallucinated"
- Vault likely empty or near-empty → no signal
- Run manually with `--dry-run` first
- Check `PREFERENCES.md` / `PROJECTS.md` aren't empty

### "Cost higher than expected"
- Check `vault/_memory/COST_LOG.md` for patterns
- Reduce frequency (weekly not daily?)
- Disable cron: `bash scripts/install-cron.sh --remove`

---

## Remember

**Automation without feedback = waste at scale.**

If the daily brief goes unread in `vault/daily/` for a week: you're not getting value. Fix the content or disable the cron. Don't let it run silently forever.
