# Disaster Recovery

What to do when things break. Run through scenarios **before** they happen so you're not panic-reading during a crisis.

---

## Backup strategy (what's protecting you)

You have 3 layers of backup:

1. **Local git** — every commit via `safe-commit.sh` preserves history
2. **Git remote** (if configured) — `backup.sh` pushes to remote
3. **Local zip snapshots** — `backup.sh` creates `~/ltd-os-backups/ltd-os-YYYYMMDD-HHMMSS.zip` (last 14 kept)

**Run `bash scripts/backup.sh`**:
- Daily if heavy work
- Weekly minimum
- Before major refactor / risky experiment
- Before OS updates

---

## Scenarios + recovery steps

### 1. Accidentally deleted a file (not yet committed)

**Chance of recovery**: high

```bash
# If you deleted it with rm and haven't committed:
git checkout -- path/to/file    # restores from last commit

# If truly gone and not in git yet:
# Check Obsidian's "File recovery" (core plugin) — keeps short history
# Check WSL2 filesystem snapshots if enabled
```

### 2. Accidentally committed a secret

**Chance of recovery**: high, but **act fast**

```bash
# 1. REVOKE THE KEY FIRST (go to provider)
#    Don't just delete from git — history still has it
bash scripts/secret-rotate.sh    # guides you through this

# 2. Remove from history (rewrites history)
#    Use git-filter-repo (better than filter-branch):
pip install --break-system-packages git-filter-repo
git filter-repo --invert-paths --path path/to/leaked/file

# Or use BFG:
#   java -jar bfg.jar --delete-files filename.txt

# 3. Force push (if remote exists)
git push --force --all

# 4. Update any other clones of the repo
# 5. Check cloud provider audit logs for unauthorized use
```

### 3. Git repo corrupted

**Chance of recovery**: medium

```bash
# Symptoms: "object ... is corrupt"
# Try:
git fsck --full
git gc --aggressive --prune=now

# If still broken:
# 1. Clone fresh from remote (if remote is good)
git clone <remote-url> /tmp/ltd-os-recovered

# 2. Move current broken .git aside
mv ~/projects/ltd-os/.git ~/projects/ltd-os/.git-broken

# 3. Copy fresh .git
cp -r /tmp/ltd-os-recovered/.git ~/projects/ltd-os/

# 4. Verify
cd ~/projects/ltd-os && git status
```

### 4. WSL2 Ubuntu won't start

**Chance of recovery**: high (your data is on NTFS-accessible WSL VHDX)

```powershell
# In Windows PowerShell:
wsl --shutdown
wsl -d Ubuntu    # try restarting

# If still broken:
wsl --unregister Ubuntu
wsl --install -d Ubuntu   # fresh install

# BEFORE unregister: backup WSL2 data
wsl --export Ubuntu C:\backup\ubuntu-backup.tar

# After reinstall, restore:
wsl --import Ubuntu C:\WSL\Ubuntu C:\backup\ubuntu-backup.tar
```

### 5. SSD/drive failure

**Chance of recovery**: depends on backups

**If you have `scripts/backup.sh` run regularly**:
1. Get a new drive
2. Install Windows + WSL2 fresh (see `GETTING_STARTED.md`)
3. Extract latest zip from `~/ltd-os-backups/` (if on another drive) OR clone from git remote
4. Run `bash scripts/bootstrap.sh`
5. Restore `.secrets/.env` from your password manager (NOT from backup — secrets shouldn't be in zip)

**If backups were on the same failed drive**: 
- Git remote is your last hope (if you set one up)
- **Lesson**: always set up git remote + offsite zip copy

### 6. Ransomware / drive encrypted

**Chance of recovery**: git remote or offline zip

If encrypted locally:
1. Don't pay ransom — no guarantee
2. Wipe + reinstall Windows
3. Restore from git remote + offsite zip
4. Your secrets should be re-rotated (assume attacker saw them)

### 7. Claude Code gets confused / breaks workflow

**Chance of recovery**: immediate

```bash
# In Claude Code:
/clear            # clears conversation, keeps auth
exit              # exits
claude            # fresh session

# If agent behavior is weird:
# 1. Check git log for recent analyst-suggested prompt changes
git log --oneline .claude/agents/

# 2. If you approved a change that broke things:
git revert <commit-hash>

# 3. Emergency reset to last known good:
git checkout <good-commit> -- .claude/agents/
```

### 8. Vault note got corrupted

**Chance of recovery**: high (git)

```bash
# Find the last good version
git log -- vault/path/to/note.md

# Restore specific commit version
git show <hash>:vault/path/to/note.md > vault/path/to/note.md

# Or full revert of that file
git checkout <hash> -- vault/path/to/note.md
```

### 9. Direnv / env vars suddenly not working

**Chance of recovery**: immediate

```bash
direnv reload
direnv allow
env | grep <YOUR_VAR_NAME>

# If still empty:
cat .envrc        # check syntax
cat .secrets/.env # check file exists + has values

# Nuclear option:
unset $(env | grep YOUR_PREFIX | cut -d= -f1)
direnv reload
```

### 10. Claude API quota exceeded

**Chance of recovery**: wait or upgrade

```bash
# Check current usage
bash scripts/cost-report.sh

# Short-term:
# - Stop non-essential tasks
# - Use NotebookLM for summarization tasks
# - /clear more often (smaller contexts)

# Longer-term:
# - Upgrade Anthropic plan
# - Add fallback provider (Phase 2)
```

---

## Pre-disaster checklist (do NOW)

- [ ] Create private GitHub/GitLab repo: `git remote add origin <url>`
- [ ] Run `bash scripts/backup.sh` manually once to verify it works
- [ ] Schedule automatic backup (cron or Windows Task Scheduler)
- [ ] Copy latest zip from `~/ltd-os-backups/` to external drive monthly
- [ ] Write `.secrets/.env` values in password manager separately
- [ ] Verify you can restore: copy zip to `/tmp/`, extract, walk through recovery
- [ ] Document YOUR specific git remote URL somewhere recoverable

---

## Testing recovery (do quarterly)

A backup you haven't tested isn't a backup.

```bash
# 1. Copy latest backup to test location
cp ~/ltd-os-backups/ltd-os-latest.zip /tmp/
cd /tmp && unzip ltd-os-latest.zip -d recovery-test

# 2. Walk through the recovery:
cd /tmp/recovery-test/ltd-os
bash scripts/bootstrap.sh   # should install cleanly

# 3. Verify essential files exist:
ls vault/_memory/           # should have PROJECTS, DECISIONS, PREFERENCES
ls .claude/agents/          # should have 8 agents
cat vault/_memory/DECISIONS.md | wc -l   # should have content

# 4. Cleanup
rm -rf /tmp/recovery-test /tmp/ltd-os-latest.zip
```

If any step fails: fix it **before** you need recovery for real.

---

## What you CAN'T recover from

Be honest with yourself about these:

- **Secrets you didn't write down elsewhere** — if `.env` is lost and you didn't record API keys in a password manager, they're gone (you'll need to regenerate)
- **Uncommitted git work > 1 hour** — if you forgot to commit and WSL2 dies, work is lost
- **Obsidian workspace state** — if you had a specific window layout/unsaved note buffers, Obsidian's File Recovery might save it, but no guarantee

**Mitigation**: `safe-commit.sh` often, backup daily, secrets in password manager.

---

## Incident log template

When something breaks, log it in `vault/90_archive/failures/YYYY-MM-DD-<incident>.md`:

```markdown
---
type: failure-journal
severity: moderate
category: system
date: 2026-04-25
---

# Incident: <what broke>

## Timeline
- HH:MM — first noticed
- HH:MM — identified cause
- HH:MM — recovery steps started
- HH:MM — restored

## Root cause


## What I did to recover


## What I'll do to prevent recurrence

```

Over time, these entries become the best guide to YOUR specific failure modes.
