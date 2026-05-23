#!/usr/bin/env bash
# setup-mds-sync.sh — install mdspull + mdspush helpers on THIS machine.
#
# Idempotent: safe to run repeatedly. Converts ~/MDS/_sync/{pull,push}-all.sh
# into symlinks pointing at the canonical version inside the mds-diversified
# repo, so a `git pull` in mds-diversified auto-updates the helpers everywhere.
#
# Usage:
#   cd ~/MDS/mds-diversified && git pull && bash scripts/setup-mds-sync.sh

set -e

REPO_SCRIPTS=~/MDS/mds-diversified/scripts/_sync
LOCAL_SYNC=~/MDS/_sync

# Sanity check — canonical scripts must exist
for f in pull-all.sh push-all.sh; do
  if [ ! -f "$REPO_SCRIPTS/$f" ]; then
    echo "FAIL: $REPO_SCRIPTS/$f missing. Did you `git pull` in mds-diversified first?"
    exit 1
  fi
done

# Make sure ~/MDS/_sync exists, then replace any existing file with a symlink
mkdir -p "$LOCAL_SYNC"
for f in pull-all.sh push-all.sh; do
  rm -f "$LOCAL_SYNC/$f"
  # Relative symlink so it works on both /Users/jameso AND /Users/jamesglobal
  ln -sf "../mds-diversified/scripts/_sync/$f" "$LOCAL_SYNC/$f"
done
echo "[OK] linked ~/MDS/_sync/{pull,push}-all.sh -> mds-diversified canonical"

# Make sure ~/.zshrc exists and has the aliases (idempotent)
touch ~/.zshrc
if ! grep -q "alias mdspull=" ~/.zshrc; then
  printf '\n# MDS multi-repo sync helpers\nalias mdspull='\''bash ~/MDS/_sync/pull-all.sh'\''\n' >> ~/.zshrc
  echo "[OK] added 'mdspull' alias to ~/.zshrc"
else
  echo "[SKIP] 'mdspull' alias already in ~/.zshrc"
fi
if ! grep -q "alias mdspush=" ~/.zshrc; then
  printf 'alias mdspush='\''bash ~/MDS/_sync/push-all.sh'\''\n' >> ~/.zshrc
  echo "[OK] added 'mdspush' alias to ~/.zshrc"
else
  echo "[SKIP] 'mdspush' alias already in ~/.zshrc"
fi

echo ""
echo "===================================================="
echo "  DONE -- mdspull / mdspush installed on this machine"
echo "===================================================="
echo ""
echo "Open a NEW terminal tab (or run 'source ~/.zshrc') and try:"
echo "  mdspull"
echo "  mdspush"
echo ""
echo "Both are safe by design: never auto-merge, never auto-commit,"
echo "never force-push. They report what they did and what they skipped."
