#!/bin/bash
# ============================================
# MDS Laptop Setup Script
# Run this on the Mac laptop to mirror the
# Mac mini's ~/MDS/ folder structure.
# ============================================

echo ""
echo "=== MDS Laptop Setup ==="
echo ""

# Create ~/MDS if it doesn't exist
mkdir -p ~/MDS
cd ~/MDS

# List of all repos to clone.
# Format: "URL"  OR  "URL|custom-folder-name"  (pipe separator to avoid clashing with https://)
repos=(
  "https://github.com/jamesglobalac007/mds-diversified.git"
  "https://github.com/jamesglobalac007/mds-conversations.git|conversations"
  "https://github.com/jamesglobalac007/deal-vault.git"
  "https://github.com/jamesglobalac007/LC-AI-Portal.git"
  "https://github.com/jamesglobalac007/Manson--Invest.git"
  "https://github.com/jamesglobalac007/radius-ndis-sda-platform.git"
  "https://github.com/jamesglobalac007/sb-empire-portal.git"
  "https://github.com/jamesglobalac007/tracknow-portal.git"
  "https://github.com/jamesglobalac007/tracknow-site.git"
)

for entry in "${repos[@]}"; do
  # Handle custom folder names (url|foldername). Pipe separator avoids the colon-in-URL bug.
  if [[ "$entry" == *"|"* ]]; then
    url="${entry%%|*}"
    folder="${entry##*|}"
  else
    # Extract folder name from URL (strip .git)
    folder=$(basename "$entry" .git)
    url="$entry"
  fi

  if [ -d "$folder" ]; then
    echo "[OK] $folder already exists — pulling latest..."
    (cd "$folder" && git pull)
  else
    echo "[CLONE] Cloning $folder..."
    git clone "$url" "$folder"
  fi
  echo ""
done

echo "=== Syncing parent ~/MDS/CLAUDE.md ==="
CANONICAL=~/MDS/mds-diversified/admin/MDS-parent-CLAUDE.md
if [ -f "$CANONICAL" ]; then
  cp "$CANONICAL" ~/MDS/CLAUDE.md
  echo "[OK] Updated ~/MDS/CLAUDE.md from canonical source"
else
  echo "[SKIP] Canonical file not found at $CANONICAL — pull mds-diversified first"
fi
echo ""

echo "=== Syncing parent ~/MDS/AGENTS.md ==="
CANONICAL=~/MDS/mds-diversified/admin/MDS-parent-AGENTS.md
if [ -f "$CANONICAL" ]; then
  cp "$CANONICAL" ~/MDS/AGENTS.md
  echo "[OK] Updated ~/MDS/AGENTS.md from canonical source"
else
  echo "[SKIP] Canonical file not found at $CANONICAL — pull mds-diversified first"
fi
echo ""

echo "=== Done! ==="
echo ""
echo "Your ~/MDS/ folder now contains:"
ls -1 ~/MDS/
echo ""
echo "Entry point: cd ~/MDS && claude or codex — then say 'work on <project name>'"
echo ""
