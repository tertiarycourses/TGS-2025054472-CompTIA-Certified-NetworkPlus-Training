#!/usr/bin/env bash
# Lab 9 — reverse everything setup.sh created (README Step 6).
# Tolerant: keep going even if a sub-interface is already gone.
set -uo pipefail

echo "== Deleting VLAN sub-interfaces =="
for i in eth0.10 eth0.20; do
  ip link del "$i" 2>/dev/null && echo "deleted $i" || echo "$i already gone"
done

# eth0 itself is never touched — the playground needs it.
echo "Cleanup done — eth0 is untouched and the box is back to its pre-lab state."
