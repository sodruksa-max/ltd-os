#!/usr/bin/env bash
# secret-rotate.sh — interactive checklist for when a secret leaks
# This doesn't rotate keys for you (provider-specific) — it walks you through

set -euo pipefail

cat <<'EOF'
═══════════════════════════════════════════
  🚨 SECRET ROTATION CHECKLIST
═══════════════════════════════════════════

If a secret leaked (committed, pasted, exposed):

[ ] 1. REVOKE the key NOW at the provider
       - Anthropic:  https://console.anthropic.com/settings/keys
       - OpenAI:     https://platform.openai.com/api-keys
       - GitHub:     https://github.com/settings/tokens
       - AWS:        IAM console → delete access key
       - Other:      go to provider's API/security settings

[ ] 2. Generate a new key

[ ] 3. Update .secrets/.env with new value (NEVER commit)

[ ] 4. If the leak was in git history:
       - DON'T just delete and commit — history still has it
       - Use BFG or git-filter-repo to scrub history
       - Force-push (coordinate if shared repo)
       - See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

[ ] 5. Audit logs at the provider
       - Check for unauthorized usage between leak and revocation

[ ] 6. Update direnv: cd into project, run `direnv reload`

[ ] 7. Verify: `env | grep <KEY_NAME>` shows new value

EOF

read -rp "Type 'done' when checklist complete: " confirm
if [[ "$confirm" == "done" ]]; then
  echo "✓ Logged rotation at $(date)"
  mkdir -p vault/90_archive/security-log
  echo "$(date '+%Y-%m-%d %H:%M') — secret rotated" >> vault/90_archive/security-log/rotations.md
fi
