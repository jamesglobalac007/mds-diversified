#!/usr/bin/env python3
"""Push script — copies worktree changes into main repo, commits, and pushes."""
import subprocess, os, sys, shutil

# HARD RULE: the repo is ALWAYS under ~/MDS/{project-slug}/
REPO = os.path.expanduser("~/MDS/mds-diversified")
WORKTREE = os.path.join(REPO, ".claude/worktrees/nice-lumiere")

if not os.path.isdir(os.path.join(REPO, ".git")):
    print(f"\033[91m✗ {REPO} is not a git clone. Run live-link rescue flow first.\033[0m")
    sys.exit(1)

if not os.path.isdir(WORKTREE):
    print(f"\033[91m✗ Worktree not found at {WORKTREE}\033[0m")
    sys.exit(1)

os.chdir(REPO)

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode == 0, r.stdout + r.stderr

def status(msg, ok=True):
    sym = "\033[92m✓\033[0m" if ok else "\033[91m✗\033[0m"
    print(f"  {sym} {msg}")

print("\n\033[1m🚀 Pushing MDS Diversified upgrade to GitHub\033[0m\n")

# 1. Pull latest from origin (stay in sync with the other Mac).
# --autostash temporarily shelves any uncommitted local changes during the rebase
# and re-applies them afterwards, so the script doesn't fail on a dirty working tree.
ok, out = run("git pull --rebase --autostash origin main")
status("Pulled latest from origin", ok)
if not ok:
    print(out)
    sys.exit(1)

# 2. Copy the upgraded index.html from the worktree into main repo
src_index = os.path.join(WORKTREE, "index.html")
dst_index = os.path.join(REPO, "index.html")
shutil.copy2(src_index, dst_index)
status("Copied index.html from worktree")

# 3. Copy the new dark-theme logo SVG from the worktree
src_logo = os.path.join(WORKTREE, "assets/logo/mds-diversified-horizontal-light.svg")
dst_logo = os.path.join(REPO, "assets/logo/mds-diversified-horizontal-light.svg")
shutil.copy2(src_logo, dst_logo)
status("Copied new dark-theme logo SVG")

# 4. Stage, commit, and push
CHANGED_FILES = [
    "index.html",
    "assets/logo/mds-diversified-horizontal-light.svg",
    "admin/MDS-parent-CLAUDE.md",
    "LAPTOP-SETUP.sh",
]
COMMIT_MSG = "Site polish + add parent ~/MDS/CLAUDE.md entry point for cross-machine routing"

ok, _ = run(f"git add {' '.join(CHANGED_FILES)}")
status("Staged files", ok)

# Check if there's anything to commit (no-op safe)
ok, out = run("git diff --cached --quiet")
# git diff --cached --quiet returns 0 if no changes, 1 if there are changes
# run() returns True for returncode 0, so:
if ok:
    print("\n\033[93m  ! No staged changes — nothing to commit.\033[0m")
    sys.exit(0)

ok, out = run(f'git commit -m "{COMMIT_MSG}"')
status("Committed", ok)
if not ok:
    print(out)
    sys.exit(1)

ok, out = run("git push origin main")
status("Pushed to GitHub", ok)

if ok:
    print(f"\n\033[92m{'='*50}")
    print(f"  ✓ PUSHED — Render is auto-deploying now")
    print(f"  Live in ~2 min: https://mds-diversified.onrender.com")
    print(f"{'='*50}\033[0m\n")
else:
    print(f"\n\033[91m✗ Push failed:\033[0m\n{out}")
    sys.exit(1)
