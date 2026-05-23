#!/usr/bin/env bash
# mdspull — fast-forward pull every git repo under ~/MDS/.
#
# Safe by design:
#   - --ff-only: refuses anything that's not a clean fast-forward (never auto-merges)
#   - never force-pushes, never resets, never loses uncommitted work
#   - reports diverged or dirty repos so you can handle them by hand
#
# Run at the start of every work session on either Mac mini or laptop.

cd ~/MDS 2>/dev/null || { echo "no ~/MDS folder"; exit 1; }

# Capture the repo list BEFORE the loop, so subsequent cd's don't affect glob expansion
shopt -s nullglob 2>/dev/null
repos=(*/)
shopt -u nullglob 2>/dev/null

printf "%-32s  %s\n" "REPO" "RESULT"
printf "%-32s  %s\n" "----" "------"

diverged=0
failed=0
pulled=0
upd=0

for d in "${repos[@]}"; do
  name="${d%/}"
  [ -d ~/MDS/"$name"/.git ] || continue
  cd ~/MDS/"$name" || continue

  if ! git fetch --quiet 2>/dev/null; then
    printf "%-32s  FETCH FAILED (check GitHub auth)\n" "$name"
    failed=$((failed + 1))
    continue
  fi

  ab=$(git rev-list --left-right --count "@{u}...HEAD" 2>/dev/null) || {
    printf "%-32s  no upstream tracked\n" "$name"
    continue
  }
  behind=$(echo "$ab" | awk '{print $1}')
  ahead=$(echo "$ab" | awk '{print $2}')
  dirty=$(git status --porcelain | wc -l | tr -d ' ')

  if [ "$behind" = "0" ] && [ "$ahead" = "0" ]; then
    printf "%-32s  up to date  (dirty=%s)\n" "$name" "$dirty"
    upd=$((upd + 1))
  elif [ "$ahead" != "0" ] && [ "$behind" = "0" ]; then
    printf "%-32s  AHEAD %s -- has unpushed commits  (dirty=%s)\n" "$name" "$ahead" "$dirty"
  elif [ "$ahead" != "0" ] && [ "$behind" != "0" ]; then
    printf "%-32s  DIVERGED behind=%s ahead=%s -- manual reconcile  (dirty=%s)\n" "$name" "$behind" "$ahead" "$dirty"
    diverged=$((diverged + 1))
  else
    if pull_out=$(git pull --ff-only 2>&1); then
      printf "%-32s  PULLED (was behind %s)  (dirty=%s)\n" "$name" "$behind" "$dirty"
      pulled=$((pulled + 1))
    else
      printf "%-32s  PULL FAILED -- %s\n" "$name" "$(echo "$pull_out" | head -1)"
      failed=$((failed + 1))
    fi
  fi
done

echo ""
echo "summary: $pulled pulled, $upd up-to-date, $diverged diverged, $failed failed"
if [ "$diverged" -gt 0 ] || [ "$failed" -gt 0 ]; then
  echo "review the lines above before editing anything"
  exit 1
fi
