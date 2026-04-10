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

# List of all repos to clone
repos=(
  "https://github.com/jamesglobalac007/mds-diversified.git"
  "https://github.com/jamesglobalac007/mds-conversations.git:conversations"
  "https://github.com/jamesglobalac007/deal-vault.git"
  "https://github.com/jamesglobalac007/LC-AI-Portal.git"
  "https://github.com/jamesglobalac007/Manson--Invest.git"
  "https://github.com/jamesglobalac007/radius-ndis-sda-platform.git"
  "https://github.com/jamesglobalac007/tracknow-portal.git"
  "https://github.com/jamesglobalac007/tracknow-site.git"
)

for entry in "${repos[@]}"; do
  # Handle custom folder names (url:foldername)
  if [[ "$entry" == *":"* ]]; then
    url="${entry%%:*}"
    folder="${entry##*:}"
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

echo "=== Done! ==="
echo ""
echo "Your ~/MDS/ folder now contains:"
ls -1 ~/MDS/
echo ""
