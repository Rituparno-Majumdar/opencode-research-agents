#!/usr/bin/env bash
# sync-from-private.sh — safely sync improved agent files from private repo to public repo.
#
# Usage:
#   PRIVATE_REPO=/path/to/private ./scripts/sync-from-private.sh           # preview diff
#   PRIVATE_REPO=/path/to/private ./scripts/sync-from-private.sh --commit  # commit changes
#
# After --commit, push manually:
#   git push origin main
#
# This script NEVER writes to the private repo. It reads from it.

set -euo pipefail

# ─── Paths ───────────────────────────────────────────────────────────────────

PRIVATE_REPO="${PRIVATE_REPO:-/path/to/your/private-research-repo}"
PUBLIC_REPO="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$PUBLIC_REPO/scripts/publicsync.manifest"
SCRUB="$PUBLIC_REPO/scripts/scrub-rules.txt"

# ─── Validate ────────────────────────────────────────────────────────────────

if [ "$PRIVATE_REPO" = "/path/to/your/private-research-repo" ]; then
  echo "ERROR: Set PRIVATE_REPO env var to your private repo path."
  echo "  Example: PRIVATE_REPO=\"/path/to/research\" ./scripts/sync-from-private.sh"
  exit 1
fi

[ -d "$PRIVATE_REPO" ] || { echo "ERROR: Private repo not found: $PRIVATE_REPO"; exit 1; }
[ -f "$MANIFEST" ]     || { echo "ERROR: Manifest not found: $MANIFEST"; exit 1; }
[ -f "$SCRUB" ]        || { echo "ERROR: Scrub rules not found: $SCRUB"; exit 1; }

echo "Private:  $PRIVATE_REPO"
echo "Public:   $PUBLIC_REPO"
echo ""

# ─── Stage into temp dir (repo is untouched until scan passes) ────────────────

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# Walk manifest
while IFS='|' read -r mode src dest; do
  # Skip comments and blank lines
  [[ "$mode" =~ ^[[:space:]]*# ]] && continue
  mode=$(echo "$mode" | xargs)
  src=$(echo "$src"   | xargs)
  dest=$(echo "$dest" | xargs)
  [ -z "$mode" ] && continue

  SRC_PATH="$PRIVATE_REPO/$src"
  if [ ! -f "$SRC_PATH" ]; then
    echo "WARNING: source not found, skipping: $src"
    continue
  fi

  mkdir -p "$STAGE/$(dirname "$dest")"

  case "$mode" in
    copy)
      cp "$SRC_PATH" "$STAGE/$dest"
      ;;
    scrub)
      # Replace all personal path references:
      #   1. Hardcoded DEST= path → env-var form
      #   2. Print statement referencing vault name → generic form
      #   3. Any remaining /Users/pari absolute paths → placeholder
      sed \
        -e 's|DEST="/Users/[^"]*"|DEST="$OBSIDIAN_SECOND_BRAIN_PATH"|g' \
        -e 's|my-second-brain/raw/research|second-brain/raw/research|g' \
        -e 's|/Users/pari[^ "]*|/path/to/your/vault|g' \
        "$SRC_PATH" > "$STAGE/$dest"
      ;;
    review)
      # Never auto-overwrite dest. Stage as .staged for manual merge.
      cp "$SRC_PATH" "$STAGE/${dest}.staged"
      ;;
    *)
      echo "WARNING: unknown mode '$mode' for $src — skipping"
      ;;
  esac
done < "$MANIFEST"

# ─── HARD SECRET-SCAN GATE ───────────────────────────────────────────────────
# Scans every staged file. Any match aborts before the working tree is touched.

echo "Running secret scan..."
HITS=$(grep -rInf "$SCRUB" "$STAGE" 2>/dev/null | grep -v '\.staged$' || true)
if [ -n "$HITS" ]; then
  echo ""
  echo "ABORT: personal data / secret pattern found in staged files:"
  echo "$HITS"
  echo ""
  echo "Nothing was changed. Fix the scrub rule or manifest entry and retry."
  exit 2
fi
echo "Scan passed — no personal data detected."
echo ""

# ─── Drift report ────────────────────────────────────────────────────────────
# Warn about private prompt files that have no manifest entry (e.g. a new agent).

for f in "$PRIVATE_REPO"/.agents/prompts/*.md; do
  fname="$(basename "$f")"
  if ! grep -q "$fname" "$MANIFEST"; then
    echo "WARNING: $fname has no manifest entry — it will NOT be synced"
  fi
done

# ─── Promote staged files into the public working tree ───────────────────────

rsync -a "$STAGE/" "$PUBLIC_REPO/"

# ─── Show diff ───────────────────────────────────────────────────────────────

cd "$PUBLIC_REPO"
DIFF=$(git --no-pager diff --stat 2>/dev/null || true)

if [ -z "$DIFF" ]; then
  echo "Already in sync — no changes."
  exit 0
fi

echo "$DIFF"
echo ""
git --no-pager diff

# ─── Commit (only with --commit flag) ────────────────────────────────────────

if [[ "${1:-}" == "--commit" ]]; then
  # Add ONLY manifest dest paths — never git add -A
  while IFS='|' read -r mode src dest; do
    [[ "$mode" =~ ^[[:space:]]*# ]] && continue
    mode=$(echo "$mode" | xargs)
    dest=$(echo "$dest" | xargs)
    [ -z "$mode" ] && continue
    [[ "$mode" == "review" ]] && dest="${dest}.staged"
    [ -f "$PUBLIC_REPO/$dest" ] && git add "$PUBLIC_REPO/$dest"
  done < "$MANIFEST"

  git commit -m "sync: agent prompts from private system"
  echo ""
  echo "Committed. Push when ready:"
  echo "  git push origin main"
else
  echo ""
  echo "── Preview only. To commit:"
  echo "   PRIVATE_REPO=\"$PRIVATE_REPO\" ./scripts/sync-from-private.sh --commit"
  echo ""
  echo "── Then push manually:"
  echo "   git push origin main"
  echo ""
  echo "── Note: config.yaml.staged requires manual review before merging into config.yaml"
fi
