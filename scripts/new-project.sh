#!/usr/bin/env bash
# new-project.sh — scaffold a new project
# Usage: ./scripts/new-project.sh <python|web> <project-name>

set -euo pipefail

TYPE="${1:-}"
NAME="${2:-}"

if [[ -z "$TYPE" || -z "$NAME" ]]; then
  echo "Usage: $0 <python|web> <project-name>"
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

case "$TYPE" in
  python)
    DIR="$ROOT/code/python/$NAME"
    [[ -d "$DIR" ]] && { echo "❌ Already exists: $DIR"; exit 1; }
    mkdir -p "$DIR"/{src,tests}
    cd "$DIR"

    cat > README.md <<EOF
# $NAME

## Setup
\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
\`\`\`

## Run
\`\`\`bash
python -m $NAME
\`\`\`
EOF

    cat > pyproject.toml <<EOF
[project]
name = "$NAME"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
EOF

    mkdir -p "src/$NAME"
    cat > "src/$NAME/__init__.py" <<EOF
"""$NAME"""
__version__ = "0.1.0"
EOF
    touch "src/$NAME/__main__.py"

    cat > tests/test_smoke.py <<EOF
def test_imports():
    import $NAME
    assert $NAME.__version__
EOF

    cat > .env.example <<EOF
# Copy to .env (which is gitignored) and fill in real values
# EXAMPLE_API_KEY=
EOF

    echo "✓ Python project created: $DIR"
    echo "  Next: cd $DIR && python -m venv .venv && source .venv/bin/activate"
    ;;

  web)
    DIR="$ROOT/code/web/$NAME"
    [[ -d "$DIR" ]] && { echo "❌ Already exists: $DIR"; exit 1; }
    mkdir -p "$DIR"
    cd "$DIR"

    cat > README.md <<EOF
# $NAME

## Setup
\`\`\`bash
npm install
npm run dev
\`\`\`
EOF

    cat > package.json <<EOF
{
  "name": "$NAME",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "echo 'Configure your dev script'",
    "test": "echo 'No tests yet' && exit 0"
  }
}
EOF

    cat > .env.example <<EOF
# Copy to .env (gitignored)
EOF

    echo "✓ Web project created: $DIR"
    ;;

  *)
    echo "❌ Unknown type: $TYPE (use 'python' or 'web')"
    exit 1
    ;;
esac
