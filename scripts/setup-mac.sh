#!/bin/bash
# ============================================================================
# setup-mac.sh — one-shot per-Mac setup
#
# Runs after mds-sync.sh has pulled all repos. Creates the per-machine
# stuff that doesn't sync via git: pre-dated folders, credentials skeleton,
# and reminder for manual UI steps (Finder sidebar pin).
#
# Run this ONCE per Mac:
#   bash ~/MDS/mds-diversified/scripts/setup-mac.sh
# ============================================================================

set -u

echo ""
echo "=========================================="
echo "  MDS — per-Mac setup"
echo "=========================================="
echo ""

# 1. Create the credentials directory if missing
mkdir -p "$HOME/.mds"
chmod 700 "$HOME/.mds"

if [ ! -f "$HOME/.mds/credentials.json" ]; then
  cat > "$HOME/.mds/credentials.json" <<'EOF'
{
  "_NOTE": "Copy actual values from your other Mac's ~/.mds/credentials.json (AirDrop the file across). Or rebuild each key by re-signing up at the relevant developer console.",
  "github_pat": "",
  "render_api_key": "",
  "unsplash_access_key": "",
  "pexels_api_key": "",
  "gemini_api_key": ""
}
EOF
  chmod 600 "$HOME/.mds/credentials.json"
  echo "[1] CREATED skeleton ~/.mds/credentials.json — fill in keys from other Mac (AirDrop the real file across)"
else
  echo "[1] OK  ~/.mds/credentials.json already exists"
fi

# 2. Pre-create 32 dated folders for tracknow client (today + 31 days)
TARGET="$HOME/MDS/tracknow-site/social-assets/_raw/tracknow"
mkdir -p "$TARGET"
created=0
for i in $(seq 0 31); do
  d=$(date -v +${i}d "+%Y-%m-%d")
  [ -d "$TARGET/$d" ] || { mkdir "$TARGET/$d"; created=$((created+1)); }
done
echo "[2] OK  Pre-created $created dated folders under $TARGET"

# 3. Install LaunchAgents (calls existing install script)
INSTALL_SH="$HOME/MDS/mds-diversified/scripts/install-mds-sync.sh"
if [ -x "$INSTALL_SH" ]; then
  bash "$INSTALL_SH" 2>&1 | sed 's/^/    /'
  echo "[3] OK  LaunchAgents installed (login-pull + 6pm-push)"
else
  echo "[3] SKIP  install-mds-sync.sh not found — install LaunchAgents later"
fi

# 3b. Install TrackNow post monitor LaunchAgent (6pm weekdays)
MONITOR_SRC="$HOME/MDS/mds-diversified/scripts/com.mds.tracknow-monitor.plist"
MONITOR_DEST="$HOME/Library/LaunchAgents/com.mds.tracknow-monitor.plist"
if [ -f "$MONITOR_SRC" ]; then
  sed "s|__HOME__|$HOME|g" "$MONITOR_SRC" > "$MONITOR_DEST"
  launchctl unload "$MONITOR_DEST" 2>/dev/null || true
  launchctl load "$MONITOR_DEST" 2>/dev/null
  echo "[3b] OK  TrackNow post monitor armed (runs 6pm AEST weekdays)"
fi

# 4. Manual reminders
cat <<'EOF'

[4] MANUAL STEPS — only you can do these (UI / secret transfer):

   a) Pin _raw to Finder sidebar
      • Open Finder, navigate to ~/MDS/tracknow-site/social-assets/
      • Drag the "_raw" folder into the left sidebar (Favourites section)
      • Click-and-hold for ~1 sec on drop so macOS registers it

   b) Copy credentials from other Mac (one-time)
      • On the OTHER Mac: AirDrop ~/.mds/credentials.json to this Mac
      • Move it into place: mv ~/Downloads/credentials.json ~/.mds/credentials.json
      • Lock it: chmod 600 ~/.mds/credentials.json

   c) Verify the workflow:
      python3 ~/MDS/mds-diversified/scripts/find-images.py "transport fleet"
      (Should open browser with 12 stock candidates.)

EOF
echo "Setup complete."
