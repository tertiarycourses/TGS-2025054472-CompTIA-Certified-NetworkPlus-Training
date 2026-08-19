#!/usr/bin/env bash
# One-time restructure: each lab gets its own folder (labs/lab-NN-slug/README.md).
# Legacy loose module labs are archived. Run from the repo root.
set -euo pipefail
cd "$(dirname "$0")/../../../.."   # repo root (build -> courseware-build -> skills -> .claude -> repo)
[ -d labs ] || { echo "labs/ not found"; exit 1; }

for f in labs/lab-*.md; do
  [ -f "$f" ] || continue
  base="$(basename "$f" .md)"
  mkdir -p "labs/$base"
  git mv "$f" "labs/$base/README.md" 2>/dev/null || mv "$f" "labs/$base/README.md"
  echo "moved $f -> labs/$base/README.md"
done

mkdir -p labs/_archive
for f in "labs/Explaining Application Services.md" "labs/Implementing Network Services.md" "labs/Network Management.md"; do
  [ -f "$f" ] || continue
  git mv "$f" "labs/_archive/$(basename "$f")" 2>/dev/null || mv "$f" "labs/_archive/$(basename "$f")"
  echo "archived $f"
done
echo "done"
