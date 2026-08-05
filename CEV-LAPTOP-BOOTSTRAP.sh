#!/usr/bin/env bash
# ==========================================================================
# CEV LAPTOP BOOTSTRAP
#
# Run this on the LAPTOP (the CEV global trading account machine).
# It is safe to run again any time. Nothing is deleted, nothing is guessed.
#
#   bash ~/MDS/mds-diversified/CEV-LAPTOP-BOOTSTRAP.sh
#
# From cold, with nothing on the machine:
#   mkdir -p ~/MDS && cd ~/MDS \
#     && git clone https://github.com/jamesglobalac007/mds-diversified.git \
#     && bash ~/MDS/mds-diversified/CEV-LAPTOP-BOOTSTRAP.sh
#
# What it does:
#   1. Clones or pulls every MDS repo, including cev-desk and cev-ibkr
#   2. Installs the skills into ~/.claude/skills (so /cev works)
#   3. Writes the CEV identity block into ~/.claude/CLAUDE.md on THIS machine
#      only, between markers, leaving everything else in that file alone
#   4. Verifies vault, credentials, VPS access, node
#   5. Prints a present / missing table with the fix for each gap
# ==========================================================================

set -uo pipefail

VPS_HOST="46.224.54.167"
VPS_NAME="cev-engine"
VAULT="$HOME/Obsidian/MDS Vault"
GLOBAL_MD="$HOME/.claude/CLAUDE.md"
BEGIN="<!-- BEGIN CEV LAPTOP BLOCK - managed by CEV-LAPTOP-BOOTSTRAP.sh -->"
END="<!-- END CEV LAPTOP BLOCK -->"

ok=(); missing=()
pass() { ok+=("$1|$2"); }
fail() { missing+=("$1|$2|$3"); }

echo ""
echo "=============================================="
echo " CEV LAPTOP BOOTSTRAP"
echo "=============================================="
echo ""

# --------------------------------------------------------------------------
# 1. Repos
# --------------------------------------------------------------------------
echo "--- 1. Repos ---"
if [ -f "$HOME/MDS/mds-diversified/LAPTOP-SETUP.sh" ]; then
  ( cd "$HOME/MDS/mds-diversified" && git pull --ff-only -q 2>/dev/null )
  bash "$HOME/MDS/mds-diversified/LAPTOP-SETUP.sh"
  pass "MDS repos" "cloned/pulled"
else
  echo "[FAIL] ~/MDS/mds-diversified/LAPTOP-SETUP.sh not found."
  fail "MDS repos" "mds-diversified not cloned" \
       "cd ~/MDS && git clone https://github.com/jamesglobalac007/mds-diversified.git"
fi
echo ""

for r in cev-desk cev-ibkr; do
  if [ -d "$HOME/MDS/$r/.git" ]; then
    pass "$r" "present"
  else
    fail "$r" "missing" "cd ~/MDS && git clone https://github.com/jamesglobalac007/$r.git"
  fi
done

# --------------------------------------------------------------------------
# 2. Skills
# --------------------------------------------------------------------------
echo "--- 2. Skills ---"
if [ -f "$HOME/MDS/_skills/install.sh" ]; then
  bash "$HOME/MDS/_skills/install.sh"
else
  echo "[SKIP] skills repo not present yet"
fi
if [ -f "$HOME/.claude/skills/cev/SKILL.md" ]; then
  pass "/cev skill" "installed"
else
  fail "/cev skill" "not installed" "bash ~/MDS/_skills/install.sh"
fi
echo ""

# --------------------------------------------------------------------------
# 3. CEV identity block in this machine's global CLAUDE.md
# --------------------------------------------------------------------------
echo "--- 3. Machine identity ---"
mkdir -p "$HOME/.claude"
touch "$GLOBAL_MD"
cp "$GLOBAL_MD" "$GLOBAL_MD.bak-$(date +%Y%m%d-%H%M%S)"

BLOCK_BODY=$(cat <<'BLOCK'

# THIS MACHINE — CEV GLOBAL TRADING

This laptop and this Claude account exist for one job: the **CEV global trading portal**.
Assume every session is trading work unless James says otherwise. Other MDS work can
happen here, it is just not the default.

## Where things are

| Folder | What it is |
|---|---|
| `~/MDS/cev-desk` | The CEV global trading portal, follow-the-sun multi-asset desk. Sandbox: sandbox-cev-desk.onrender.com |
| `~/MDS/cev-ibkr` | The live trading engine that drives the Hetzner VPS `cev-engine` at 46.224.54.167 |
| `~/Obsidian/MDS Vault/40 Trading/` | The trading second brain. Read before any trade action, every time. |
| `~/MDS` | Everything else. Never work outside this folder. |

## Standing behaviour on this machine

- Run the `cev` skill at the start of a trading session. It is the full boot sequence.
- STEP 0 always: read `40 Trading/` in the vault before any trade logic or opinion.
- Read index futures and the current regime before recommending or arming anything.
- Learn aggressively, trade conservatively. High volume, small wins, low risk.
- No drastic one-day changes. Every proposed change states evidence, overfit risk,
  downside and disposition.
- Never execute a trade, arm a strategy or move money without James saying go.
- Surface only action-needed red alerts. Routine notices stay collapsed.
- `git pull` before touching either CEV repo. Both are live.
- If something is missing on this machine, name it and give the fix. Do not work around it.
  The repair command for almost everything is:
  `bash ~/MDS/mds-diversified/CEV-LAPTOP-BOOTSTRAP.sh`
BLOCK
)

python3 - "$GLOBAL_MD" "$BEGIN" "$END" <<PY
import sys, io
path, begin, end = sys.argv[1], sys.argv[2], sys.argv[3]
body = """$BLOCK_BODY"""
with io.open(path, encoding="utf-8") as f:
    txt = f.read()
new = begin + "\n" + body + "\n" + end + "\n"
if begin in txt and end in txt:
    pre = txt.split(begin)[0]
    post = txt.split(end, 1)[1]
    out = pre + new + post
    action = "updated"
else:
    out = (txt.rstrip() + "\n\n" if txt.strip() else "") + new
    action = "added"
with io.open(path, "w", encoding="utf-8") as f:
    f.write(out)
print("[OK] CEV identity block " + action + " in " + path)
PY

if grep -q "CEV GLOBAL TRADING" "$GLOBAL_MD"; then
  pass "Machine identity" "CEV block in ~/.claude/CLAUDE.md"
else
  fail "Machine identity" "block not written" "re-run this script"
fi
echo ""

# --------------------------------------------------------------------------
# 4. Verifications
# --------------------------------------------------------------------------
echo "--- 4. Verifications ---"

if [ -d "$VAULT/40 Trading" ]; then
  pass "Obsidian vault" "40 Trading/ found"
else
  fail "Obsidian vault" "40 Trading/ not found at $VAULT" \
       "Open the Obsidian app and let Obsidian Sync pull the vault down"
fi

if [ -f "$HOME/.mds/credentials.json" ]; then
  keys=$(python3 -c "import json;print(', '.join(sorted(json.load(open('$HOME/.mds/credentials.json')).keys())))" 2>/dev/null)
  pass "Credentials" "keys present: ${keys:-unreadable}"
else
  fail "Credentials" "~/.mds/credentials.json missing" \
       "Copy it across from the Mac mini, or re-add keys with the save-credential skill"
fi

if ssh -o BatchMode=yes -o ConnectTimeout=6 -o StrictHostKeyChecking=accept-new \
      root@"$VPS_HOST" 'systemctl is-system-running' >/dev/null 2>&1; then
  pass "VPS $VPS_NAME" "SSH OK"
  echo "  services:"
  ssh -o BatchMode=yes -o ConnectTimeout=8 root@"$VPS_HOST" \
    'systemctl list-units --type=service --state=running --no-legend --no-pager | grep -i cev || echo "  (no cev services matched)"' 2>/dev/null | sed 's/^/    /'
else
  fail "VPS $VPS_NAME" "no SSH from this machine" \
       "Add this laptop's SSH public key to root@$VPS_HOST (cat ~/.ssh/id_ed25519.pub)"
fi

if command -v node >/dev/null 2>&1; then
  pass "node" "$(node -v)"
else
  fail "node" "not installed" "brew install node"
fi
echo ""

# --------------------------------------------------------------------------
# 5. Report
# --------------------------------------------------------------------------
echo "=============================================="
echo " RESULT"
echo "=============================================="
echo ""
echo "PRESENT"
for e in "${ok[@]}"; do printf "  [ok]  %-18s %s\n" "${e%%|*}" "${e#*|}"; done
echo ""
if [ ${#missing[@]} -eq 0 ]; then
  echo "MISSING"
  echo "  nothing. This laptop is ready."
  echo ""
  echo "Next: cd ~/MDS && claude    then run:  /cev"
else
  echo "MISSING  (${#missing[@]})"
  for e in "${missing[@]}"; do
    n="${e%%|*}"; rest="${e#*|}"; why="${rest%%|*}"; fixcmd="${rest#*|}"
    printf "  [--]  %-18s %s\n" "$n" "$why"
    printf "        fix: %s\n" "$fixcmd"
  done
  echo ""
  echo "Fix those, run this script again, then: cd ~/MDS && claude  and  /cev"
fi
echo ""
