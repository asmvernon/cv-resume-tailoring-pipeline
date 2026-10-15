#!/bin/sh
# Checks that this copy of the repo is private before personal data goes in.
#
# Your inventory, job descriptions and résumés get committed here, so this
# copy must be private. The assistant runs this before writing any of them
# (see CLAUDE.md). Exit codes:
#   0  private, or a local folder with no remote: go ahead
#   1  not private (the upstream repo itself, or a public repo): stop
#   2  can't tell: ask the user to confirm the copy is private

UPSTREAM="asmvernon/cv-resume-tailoring-pipeline"

cd "$(dirname "$0")/.." || exit 2

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "OK: not a git repository, so nothing is pushed anywhere."
  exit 0
fi

url=$(git remote get-url origin 2>/dev/null)
if [ -z "$url" ]; then
  if [ -n "$(git remote)" ]; then
    echo "UNKNOWN: this copy has remotes but none called origin: $(git remote | tr '\n' ' ')"
    exit 2
  fi
  echo "OK: no remote, so this copy stays on this computer."
  exit 0
fi

# owner/name from https://github.com/owner/name(.git) or git@github.com:owner/name(.git)
slug=$(printf '%s\n' "$url" |
  sed -n -E 's#^(https?://([^@/]+@)?|ssh://git@|git@)github\.com[:/]([^/]+/[^/]+)$#\3#p' |
  sed 's#\.git$##')

if [ -z "$slug" ]; then
  echo "UNKNOWN: origin is $url, which isn't on github.com, so its visibility can't be checked."
  exit 2
fi

if [ "$(printf '%s' "$slug" | tr 'A-Z' 'a-z')" = "$UPSTREAM" ]; then
  echo "NOT PRIVATE: origin is the public upstream repo ($UPSTREAM), not your own copy."
  echo "Make a private copy first: see the README's 'Before you start' section."
  exit 1
fi

# Prefer the GitHub CLI when it's signed in: it reports visibility directly.
if command -v gh >/dev/null 2>&1 &&
   vis=$(gh repo view "$slug" --json visibility --jq .visibility 2>/dev/null); then
  case "$vis" in
    PRIVATE) echo "OK: $slug is private."; exit 0 ;;
    *) echo "NOT PRIVATE: $slug is $(printf '%s' "$vis" | tr 'A-Z' 'a-z')."
       echo "Make it private in its GitHub settings, or make a private copy (see the README)."
       exit 1 ;;
  esac
fi

# Otherwise ask GitHub's API. Signed out, a private repo answers 404, the
# same as a repo that doesn't exist; when it answers 200 (a public repo, or
# a private one seen with credentials), its "private" field says which.
if command -v curl >/dev/null 2>&1; then
  body=$(curl -s --max-time 10 -w '\n%{http_code}' \
    "https://api.github.com/repos/$slug" 2>/dev/null)
  code=$(printf '%s\n' "$body" | tail -n 1)
  case "$code" in
    200)
      # The repo's own field comes first; a template or parent repo's
      # comes later in the response.
      private=$(printf '%s\n' "$body" | grep -Eo '"private": *(true|false)' |
        head -n 1 | grep -Eo 'true|false')
      if [ "$private" = true ]; then
        echo "OK: $slug is private."; exit 0
      elif [ "$private" = false ]; then
        echo "NOT PRIVATE: $slug is public (anyone can see it)."
        echo "Make it private in its GitHub settings, or make a private copy (see the README)."
        exit 1
      fi ;;
    404) echo "OK: $slug isn't publicly visible, so it's private (or not created on GitHub yet)."
         exit 0 ;;
  esac
fi

echo "UNKNOWN: couldn't reach GitHub to check whether $slug is private."
exit 2
