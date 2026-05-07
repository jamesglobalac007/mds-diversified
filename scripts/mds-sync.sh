#!/bin/bash
# ============================================================================
# mds-sync.sh — daily sync helper for ~/MDS
#
#   pull   : git pull every repo under ~/MDS (clones any missing canonical ones)
#   push   : git push every repo with committed-but-unpushed work
#   status : summary of dirty / ahead / behind across all repos
#
# Lives at ~/MDS/mds-diversified/scripts/mds-sync.sh on both machines.
# Run via the install-mds-sync.sh LaunchAgents (login = pull, 6pm = push).
# ============================================================================

set -u

MDS_ROOT="$HOME/MDS"
LOG_DIR="$MDS_ROOT/.logs"
mkdir -p "$LOG_DIR"

ts() { date "+%Y-%m-%d %H:%M:%S"; }

# Canonical repo list. Format: "URL" or "URL|custom-folder".
# Mirror this in LAPTOP-SETUP.sh — same source of truth.
REPOS=(
  "https://github.com/jamesglobalac007/mds-diversified.git"
  "https://github.com/jamesglobalac007/mds-conversations.git|conversations"
  "https://github.com/jamesglobalac007/deal-vault.git"
  "https://github.com/jamesglobalac007/LC-AI-Portal.git"
  "https://github.com/jamesglobalac007/Manson--Invest.git"
  "https://github.com/jamesglobalac007/radius-ndis-sda-platform.git"
  "https://github.com/jamesglobalac007/sb-empire-portal.git"
  "https://github.com/jamesglobalac007/tracknow-portal.git"
  "https://github.com/jamesglobalac007/tracknow-site.git"
  "https://github.com/jamesglobalac007/mds-social-hub.git|social-hub"
  "https://github.com/jamesglobalac007/mds-content.git"
)

cmd_pull() {
  echo "[$(ts)] === mds-sync pull ==="
  cd "$MDS_ROOT" || exit 1

  for entry in "${REPOS[@]}"; do
    if [[ "$entry" == *"|"* ]]; then
      url="${entry%%|*}"
      folder="${entry##*|}"
    else
      url="$entry"
      folder=$(basename "$url" .git)
    fi

    if [ ! -d "$folder" ]; then
      echo "[$(ts)] CLONE  $folder"
      git clone "$url" "$folder" 2>&1 | sed "s/^/  /"
      continue
    fi

    if ! [ -d "$folder/.git" ]; then
      echo "[$(ts)] SKIP   $folder (not a git repo)"
      continue
    fi

    dirty=$(git -C "$folder" status --porcelain | wc -l | tr -d ' ')
    if [ "$dirty" -gt 0 ]; then
      echo "[$(ts)] DIRTY  $folder ($dirty uncommitted) — skipping pull to avoid conflict"
      continue
    fi

    out=$(git -C "$folder" pull --ff-only 2>&1)
    if echo "$out" | grep -q "Already up to date"; then
      echo "[$(ts)] OK     $folder (up to date)"
    else
      echo "[$(ts)] PULL   $folder"
      echo "$out" | sed "s/^/  /"
    fi
  done

  # Refresh parent CLAUDE.md / AGENTS.md from canonical mds-diversified copies.
  for fname in CLAUDE.md AGENTS.md; do
    src="$MDS_ROOT/mds-diversified/admin/MDS-parent-$fname"
    [ -f "$src" ] && cp "$src" "$MDS_ROOT/$fname"
  done

  echo "[$(ts)] === pull done ==="
}

cmd_push() {
  echo "[$(ts)] === mds-sync push ==="
  cd "$MDS_ROOT" || exit 1

  for d in */; do
    folder="${d%/}"
    [ -d "$folder/.git" ] || continue

    dirty=$(git -C "$folder" status --porcelain | wc -l | tr -d ' ')
    branch=$(git -C "$folder" rev-parse --abbrev-ref HEAD 2>/dev/null)
    ahead=$(git -C "$folder" rev-list --count "@{u}..HEAD" 2>/dev/null || echo "0")

    if [ "$dirty" -gt 0 ]; then
      echo "[$(ts)] DIRTY  $folder ($dirty uncommitted on $branch — NOT auto-committing)"
    fi

    if [ "$ahead" -gt 0 ]; then
      echo "[$(ts)] PUSH   $folder ($ahead commits)"
      git -C "$folder" push origin "$branch" 2>&1 | sed "s/^/  /"
    elif [ "$dirty" -eq 0 ]; then
      echo "[$(ts)] OK     $folder (clean, in sync)"
    fi
  done

  echo "[$(ts)] === push done ==="
}

cmd_status() {
  echo "[$(ts)] === mds-sync status ==="
  cd "$MDS_ROOT" || exit 1
  printf "%-32s  %-8s  %-6s  %-7s\n" "REPO" "BRANCH" "AHEAD" "DIRTY"
  printf "%-32s  %-8s  %-6s  %-7s\n" "----" "------" "-----" "-----"
  for d in */; do
    folder="${d%/}"
    [ -d "$folder/.git" ] || continue
    branch=$(git -C "$folder" rev-parse --abbrev-ref HEAD 2>/dev/null)
    ahead=$(git -C "$folder" rev-list --count "@{u}..HEAD" 2>/dev/null || echo "?")
    dirty=$(git -C "$folder" status --porcelain | wc -l | tr -d ' ')
    printf "%-32s  %-8s  %-6s  %-7s\n" "$folder" "$branch" "$ahead" "$dirty"
  done
}

case "${1:-}" in
  pull)   cmd_pull ;;
  push)   cmd_push ;;
  status) cmd_status ;;
  "")     echo "Usage: $0 {pull|push|status}"; exit 1 ;;
  *)      echo "Unknown command: $1"; echo "Usage: $0 {pull|push|status}"; exit 1 ;;
esac
