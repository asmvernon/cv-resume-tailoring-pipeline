#!/bin/sh
# Upstream guardrail: fails if personal data is committed to this repo.
#
# Your own private copy is meant to hold your inventory, job descriptions and
# résumés, so CI runs this only on the upstream repo (see
# .github/workflows/ci.yml). It allows only the scaffolding below.

set -eu
cd "$(dirname "$0")/.."

ALLOWED='
inventory/schema.md
inventory/roles/.gitkeep
job_descriptions/.gitkeep
resumes/.gitkeep
'

bad=$(git ls-files inventory job_descriptions resumes | while read -r f; do
  case "$ALLOWED" in
    *"
$f
"*) ;;
    *) echo "$f" ;;
  esac
done)

# docs/tasks.md ships as an empty stub; the skills fill it with your open
# items. Upstream it must stay the stub.
if ! grep -qx -- '- \[ \] (nothing yet)' docs/tasks.md ||
   [ "$(grep -c -- '^- \[' docs/tasks.md)" -ne 1 ]; then
  bad="$bad
docs/tasks.md (should be the empty stub)"
fi

bad=$(printf '%s\n' "$bad" | sed '/^$/d')
if [ -n "$bad" ]; then
  echo "Personal data must not be committed to the upstream repo:" >&2
  printf '  %s\n' "$bad" >&2
  exit 1
fi
echo "No personal data committed."
