#!/usr/bin/env bash
# Lab 34 — restore the ORIGINAL default route saved by break.sh, and remove the
# 10.99.0.0/24 test route added in README Step 3.
# Tolerant: keep going even if one step has already been undone.
set -uo pipefail

BAK=/tmp/default-route.bak

echo "== Removing the 10.99.0.0/24 test route (README Step 6) =="
ip route del 10.99.0.0/24 2>/dev/null && echo "deleted 10.99.0.0/24" || echo "10.99.0.0/24 already gone"

echo
echo "== Restoring the default route =="
if ip route show default | grep -q .; then
  echo "A default route is already present:"
  ip route show default
elif [ -f "$BAK" ]; then
  DEF=$(head -1 "$BAK")
  # shellcheck disable=SC2086
  ip route add $DEF && echo "Restored: ip route add $DEF" || echo "Could not restore '$DEF' — add it by hand"
else
  echo "No backup at $BAK and no default route present."
  echo "Re-add it by hand, e.g.:  ip route add default via <gateway> dev eth0"
fi

echo
echo "Current routing table:"
ip route

echo
echo "Cleanup done — run ./verify.sh to confirm connectivity is restored."
