#!/usr/bin/env bash
# usage: publish_results.sh <label> <file-or-dir>...   -> commits them to branch `results` under run-<id>/<label>/ and latest/<label>/
# Needs `permissions: contents: write` and GITHUB_TOKEN in env. Retries on push races (parallel jobs).
set -uo pipefail
LABEL="$1"; shift
ORIG="$PWD"; D="$(mktemp -d)"; cd "$D"
git init -q; git config user.name "finetune-bot"; git config user.email "finetune-bot@users.noreply.github.com"
git remote add origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
for attempt in 1 2 3 4 5; do
  if git fetch -q --depth 1 origin results 2>/dev/null; then git checkout -q -B results FETCH_HEAD; else git checkout -q --orphan results; fi
  rm -rf "latest/$LABEL"; mkdir -p "run-${GITHUB_RUN_ID}/$LABEL" "latest/$LABEL"
  for f in "$@"; do [ -e "$ORIG/$f" ] && cp -r "$ORIG/$f" "run-${GITHUB_RUN_ID}/$LABEL/"; done
  cp -r "run-${GITHUB_RUN_ID}/$LABEL/." "latest/$LABEL/"
  git add -A; git commit -q -m "results: $LABEL run ${GITHUB_RUN_ID}" || exit 0
  git push -q origin HEAD:results && exit 0
  sleep $((attempt * 5))
done
echo "publish failed"; exit 1
