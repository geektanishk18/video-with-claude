#!/usr/bin/env bash
# FiguredOutAI reel workflow: one-time setup for macOS / Linux.   Run from the repo root:  bash setup/setup.sh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
have() { command -v "$1" >/dev/null 2>&1; }

echo "1/5  System tools"
if [[ "$(uname)" == "Darwin" ]]; then
  have brew || { echo "Install Homebrew first: https://brew.sh"; exit 1; }
  for p in python node ffmpeg git; do have "$p" || have "${p}3" || brew install "$p"; done
else
  sudo apt-get update -qq && sudo apt-get install -y -qq python3 python3-pip ffmpeg git nodejs npm fontconfig
fi

echo "2/5  Python packages"
python3 -m pip install -r "$REPO/setup/requirements.txt"

echo "3/5  Brand fonts"
if [[ "$(uname)" == "Darwin" ]]; then FD="$HOME/Library/Fonts"; else FD="$HOME/.local/share/fonts"; fi
mkdir -p "$FD" && cp "$REPO"/skills/figuredout-reel/assets/fonts/*.ttf "$FD"/ && (have fc-cache && fc-cache -f >/dev/null || true)

echo "4/5  Claude Code skills -> ~/.claude/skills"
mkdir -p ~/.claude/skills
for s in figuredout-reel figuredout-reel-rick-morty; do rm -rf ~/.claude/skills/$s; cp -r "$REPO/skills/$s" ~/.claude/skills/; done

echo "5/5  Remotion for the example reel"
(cd "$REPO/reels/unified-ai-inbox/video" && npm install)

python3 "$REPO/setup/check.py" || true
echo "Restart Claude Code to load the skills."
