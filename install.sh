#!/usr/bin/env bash
# Installs cie-econ-essay and cie-econ-ppt into ~/.claude/skills/
# and installs Python dependencies for cie-econ-ppt.
#
# Usage:   bash install.sh
# Run from the root of the cloned A-Level-Econ-Marking-Sample repo.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo ""
echo "Installing CIE Economics skills"
echo "  Source: $REPO_ROOT"
echo "  Target: $SKILLS_DIR"
echo ""

mkdir -p "$SKILLS_DIR"

for skill in cie-econ-essay cie-econ-ppt; do
    src="$REPO_ROOT/$skill"
    dst="$SKILLS_DIR/$skill"
    if [[ ! -d "$src" ]]; then
        echo "[skip] $skill not found at $src"
        continue
    fi
    if [[ -d "$dst" ]]; then
        echo "[update] $skill (replacing existing install)"
        rm -rf "$dst"
    else
        echo "[install] $skill"
    fi
    cp -R "$src" "$dst"
done

echo ""
echo "Installing Python dependencies for cie-econ-ppt..."

PYTHON=""
for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1; then
        PYTHON="$(command -v "$c")"
        break
    fi
done

if [[ -z "$PYTHON" ]]; then
    echo ""
    echo "  No Python found. Install Python 3.10+ first, then re-run this script."
    echo "  macOS:  brew install python@3.12"
    echo "  Linux:  use your package manager (apt install python3 python3-pip, etc.)"
    echo ""
    echo "  The cie-econ-essay skill will still work without Python."
    exit 0
fi

echo "  Using Python: $PYTHON"
"$PYTHON" -m pip install --quiet --user python-pptx matplotlib pypdf scipy || {
    echo "  pip install failed. cie-econ-ppt may not work until you install:"
    echo "      $PYTHON -m pip install --user python-pptx matplotlib pypdf scipy"
    exit 1
}

echo "  Verifying diagram library..."
"$PYTHON" -c "import sys; sys.path.insert(0, '$SKILLS_DIR/cie-econ-ppt/scripts'); import diagrams; print('  OK -', len(diagrams.REGISTRY), 'diagrams available')"

echo ""
echo "Done."
echo ""
echo "Restart Claude Code, then try:"
echo "    cie: write a 12-mark sample answer on PED"
echo "    cie ppt: A-Level Topic 2.1 Demand and supply"
echo ""
echo "Note: cie-econ-ppt will need to know your Python path. It's at:"
echo "    $PYTHON"
