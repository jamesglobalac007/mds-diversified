#!/usr/bin/env bash
# mdspush — push every git repo under ~/MDS/ that has unpushed commits.
#
# Safe by design:
#   - Pushes only what's already COMMITTED. Never auto-stages, never auto-commits.
#   - If a repo has uncommitted changes, it warns (so you don't silently leave
#     work behind) but does not push them.
#   - If a repo has diverged from origin, it refuses and tells you.
#
# Use the per-project `push` skill (via Claude) when you want a real commit
# message and review. Use `mdspush` as the end-of-evening sweep to confirm
# nothing's stuck unpushed.

cd ~/MDS 2>/dev/null || { echo "no ~/MDS folder"; exit 1; }

shopt -s nullglob 2>/dev/null
repos=(*/)
shopt -u nullglob 2>/dev/null

printf "%-32s  %s\n" "REPO" "RESULT"
printf "%-32s  %s\n" "----" "------"

pushed=0
sync=0
warned=0
failed=0

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

  if [ "$behind" != "0" ] && [ "$ahead" != "0" ]; then
    printf "%-32s  DIVERGED behind=%s ahead=%s -- run mdspull first\n" "$name" "$behind" "$ahead"
    failed=$((failed + 1))
    continue
  fi

  if [ "$behind" != "0" ]; then
    printf "%-32s  BEHIND %s -- run mdspull first  (dirty=%s)\n" "$name" "$behind" "$dirty"
    failed=$((failed + 1))
    continue
  fi

  if [ "$ahead" != "0" ]; then
    if push_out=$(git push 2>&1); then
      printf "%-32s  PUSHED %s commit(s)  (dirty=%s)\n" "$name" "$ahead" "$dirty"
      pushed=$((pushed + 1))
    else
      printf "%-32s  PUSH FAILED -- %s\n" "$name" "$(echo "$push_out" | head -1)"
      failed=$((failed + 1))
    fi
  else
    if [ "$dirty" != "0" ]; then
      printf "%-32s  in sync, but %s uncommitted file(s) NOT pushed\n" "$name" "$dirty"
      warned=$((warned + 1))
    else
      printf "%-32s  in sync (nothing to push)\n" "$name"
      sync=$((sync + 1))
    fi
  fi
done

echo ""
echo "summary: $pushed pushed, $sync clean+synced, $warned in-sync-but-dirty, $failed failed"

if [ "$warned" -gt 0 ]; then
  echo ""
  echo "NOTE: repos marked 'uncommitted file(s) NOT pushed' have local changes that"
  echo "      mdspush deliberately did NOT auto-commit. If you want those on GitHub,"
  echo "      use the per-project 'push' skill via Claude (it commits + pushes with"
  echo "      a real commit message after you review the diff)."
fi

if [ "$failed" -gt 0 ]; then
  exit 1
fi
