#!/usr/bin/env bash
# safe-commit.sh — only commits if checks pass
# Usage: ./scripts/safe-commit.sh "feat: add new feature"

set -euo pipefail

MSG="${1:-}"
if [[ -z "$MSG" ]]; then
  echo "❌ Commit message required"
  echo "Usage: $0 \"<conventional commit message>\""
  exit 1
fi

cd "$(git rev-parse --show-toplevel)"

echo "→ Running pre-commit checks..."

# 1. Secrets scan on staged changes
echo "  [1/4] Secrets scan..."
if git diff --cached | grep -iE '(api[_-]?key|secret[_-]?key|password\s*=|token\s*=|sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN .* PRIVATE KEY-----)' > /dev/null; then
  echo "  ❌ BLOCKED: possible secret in staged changes"
  echo "     Run: git diff --cached | grep -iE 'api_key|secret|token|password'"
  exit 1
fi

# 2. Block .env files (except .example)
echo "  [2/4] Gitignore compliance..."
if git diff --cached --name-only | grep -E '(^|/)\.env($|\.)' | grep -v '\.example$' > /dev/null; then
  echo "  ❌ BLOCKED: .env file staged"
  exit 1
fi
if git diff --cached --name-only | grep -E '^\.secrets/' > /dev/null; then
  echo "  ❌ BLOCKED: file in .secrets/ staged"
  exit 1
fi

# 3. Run Python tests if present
echo "  [3/4] Tests..."
if [[ -f "pytest.ini" ]] || [[ -f "pyproject.toml" ]] && grep -q "pytest" pyproject.toml 2>/dev/null; then
  if command -v pytest > /dev/null; then
    pytest -q || { echo "  ❌ pytest failed"; exit 1; }
  fi
fi
if [[ -f "package.json" ]] && grep -q '"test"' package.json; then
  if command -v npm > /dev/null; then
    npm test --silent || { echo "  ❌ npm test failed"; exit 1; }
  fi
fi

# 4. Conventional commit format check
echo "  [4/4] Commit message format..."
if ! echo "$MSG" | grep -qE '^(feat|fix|docs|style|refactor|test|chore|perf|notes|vault|memory|analyst)(\(.+\))?: .+'; then
  echo "  ⚠️  Warning: message doesn't follow conventional commits"
  echo "     Expected: <type>(<scope>): <description>"
  echo "     Continue anyway? (y/N)"
  read -r REPLY
  [[ "$REPLY" =~ ^[Yy]$ ]] || exit 1
fi

echo "✓ All checks passed. Committing..."
git commit -m "$MSG"
echo "✓ Committed: $MSG"
