#!/bin/bash
# ============================================================================
# install-mds-sync.sh — install the login-pull and 6pm-push LaunchAgents
#
# Run once per Mac:    bash ~/MDS/mds-diversified/scripts/install-mds-sync.sh
# Uninstall later:     bash ~/MDS/mds-diversified/scripts/install-mds-sync.sh uninstall
# ============================================================================

set -e

SRC_DIR="$HOME/MDS/mds-diversified/scripts"
DEST_DIR="$HOME/Library/LaunchAgents"
PLISTS=(com.mds.sync-pull.plist com.mds.sync-push.plist)

mkdir -p "$DEST_DIR" "$HOME/MDS/.logs"
chmod +x "$SRC_DIR/mds-sync.sh"

if [ "${1:-}" = "uninstall" ]; then
  for p in "${PLISTS[@]}"; do
    label="${p%.plist}"
    if [ -f "$DEST_DIR/$p" ]; then
      launchctl unload "$DEST_DIR/$p" 2>/dev/null || true
      rm "$DEST_DIR/$p"
      echo "[OK] removed $label"
    fi
  done
  exit 0
fi

for p in "${PLISTS[@]}"; do
  label="${p%.plist}"
  cp "$SRC_DIR/$p" "$DEST_DIR/$p"
  launchctl unload "$DEST_DIR/$p" 2>/dev/null || true
  launchctl load "$DEST_DIR/$p"
  echo "[OK] installed $label"
done

echo
echo "Login-pull and 6pm-push are armed."
echo "Logs: ~/MDS/.logs/sync-pull.log  ~/MDS/.logs/sync-push.log"
echo "Run a one-shot pull now:  bash $SRC_DIR/mds-sync.sh pull"
