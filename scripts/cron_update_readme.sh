#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

# Always run on master
git switch master >/dev/null 2>&1 || true

git pull --ff-only origin master

python3 scripts/auto_update_readme.py

if ! git diff --quiet -- README.md; then
  # Commit only when README actually changed
  NOW_CN=$(TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M')
  git add README.md
  git commit -m "chore: auto-update README (${NOW_CN} BJ)"
  git push origin master
fi
