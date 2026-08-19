#!/usr/bin/env bash
# Lab 8 — reverse everything setup.sh created (README Step 7).
# Tolerant: keep going even if a namespace is already gone.
set -uo pipefail

echo "== Deleting namespaces a, r1, b =="
for n in a r1 b; do
  ip netns del "$n" 2>/dev/null && echo "deleted netns $n" || echo "netns $n already gone"
done

# Deleting a namespace destroys the veth pairs it held. Sweep any leftover
# halves that never made it into a namespace.
for i in a-r r-a b-r r-b; do
  ip link del "$i" 2>/dev/null && echo "deleted leftover link $i" || true
done

echo "Cleanup done — the box is back to its pre-lab state."
