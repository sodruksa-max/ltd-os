#!/usr/bin/env bash
# bootstrap.sh — one-time setup for fresh WSL2 Ubuntu
# Run from inside ltd-os/ folder

set -euo pipefail

echo "═══════════════════════════════════════════"
echo "  LTD-OS Bootstrap"
echo "═══════════════════════════════════════════"

# Check we're on Linux
if [[ "$(uname)" != "Linux" ]]; then
  echo "⚠️  This script is for Linux/WSL2. On Windows native, install manually."
  exit 1
fi

# 1. System packages
echo
echo "→ [1/6] Installing system packages (sudo required)..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
  git curl wget build-essential \
  python3 python3-venv python3-pip \
  ripgrep fd-find direnv jq

# 2. Node.js (via nvm) — required for Claude Code
echo
echo "→ [2/6] Installing Node.js via nvm..."
if [[ ! -d "$HOME/.nvm" ]]; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  # shellcheck disable=SC1091
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
  nvm install --lts
  nvm use --lts
else
  echo "   nvm already installed, skipping"
fi

# 3. Claude Code
echo
echo "→ [3/6] Installing Claude Code..."
if ! command -v claude > /dev/null; then
  npm install -g @anthropic-ai/claude-code
else
  echo "   claude already installed, skipping"
fi

# 4. Git config check
echo
echo "→ [4/6] Git config..."
if [[ -z "$(git config --global user.name 2>/dev/null || true)" ]]; then
  echo "   ⚠️  Git user.name not set."
  read -rp "   Enter your name: " NAME
  git config --global user.name "$NAME"
fi
if [[ -z "$(git config --global user.email 2>/dev/null || true)" ]]; then
  read -rp "   Enter your email: " EMAIL
  git config --global user.email "$EMAIL"
fi
git config --global init.defaultBranch main
git config --global pull.rebase false

# 5. Make scripts executable
echo
echo "→ [5/6] Making scripts executable..."
chmod +x scripts/*.sh

# 6. Init git repo + first commit
echo
echo "→ [6/6] Initializing git repo..."
if [[ ! -d ".git" ]]; then
  git init -q
  git add .
  git commit -q -m "chore: initial LTD-OS scaffold"
  echo "   ✓ Initial commit done"
else
  echo "   git repo already exists"
fi

# .envrc for direnv (per-folder env vars)
if [[ ! -f ".envrc" ]]; then
  cat > .envrc <<'EOF'
# direnv: load .secrets/.env if present
if [[ -f .secrets/.env ]]; then
  dotenv .secrets/.env
fi
EOF
  echo "   ✓ Created .envrc — run 'direnv allow' to enable"
fi

# Add direnv hook to bashrc if not present
if ! grep -q "direnv hook bash" "$HOME/.bashrc" 2>/dev/null; then
  echo 'eval "$(direnv hook bash)"' >> "$HOME/.bashrc"
  echo "   ✓ Added direnv to .bashrc"
fi

echo
echo "═══════════════════════════════════════════"
echo "  ✓ Bootstrap complete"
echo "═══════════════════════════════════════════"
echo
echo "Next steps:"
echo "  1. Open new terminal (or: source ~/.bashrc)"
echo "  2. Run: direnv allow"
echo "  3. Authenticate Claude Code: claude"
echo "  4. Read: docs/GETTING_STARTED.md"
echo
echo "To open this folder in Obsidian:"
echo "  - In Windows Obsidian, 'Open folder as vault'"
echo "  - Path: \\\\wsl\$\\Ubuntu\\home\\$USER\\projects\\ltd-os\\vault"
