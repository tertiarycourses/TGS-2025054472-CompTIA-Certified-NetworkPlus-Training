#!/usr/bin/env bash
# Lab 34 — verify the routing table is healthy again after break.sh + cleanup.sh.
set -uo pipefail

fail=0

if ip route show default | grep -q 'default via'; then
  echo "PASS: a default route is present — $(ip route show default | head -1)"
else
  echo "FAIL: no default route — run ./cleanup.sh"
  fail=1
fi

if ip route get 8.8.8.8 >/dev/null 2>&1; then
  echo "PASS: ip route get 8.8.8.8 resolves — $(ip route get 8.8.8.8 2>/dev/null | head -1)"
else
  echo "FAIL: ip route get 8.8.8.8 says the network is unreachable"
  fail=1
fi

if ip route show 10.99.0.0/24 2>/dev/null | grep -q .; then
  echo "FAIL: the 10.99.0.0/24 test route from Step 3 is still installed — run ./cleanup.sh"
  fail=1
else
  echo "PASS: the 10.99.0.0/24 test route has been removed"
fi

if ping -c2 -W2 8.8.8.8 >/dev/null 2>&1; then
  echo "PASS: 8.8.8.8 is reachable — end-to-end connectivity restored"
else
  echo "FAIL: cannot ping 8.8.8.8 — the route is back but traffic still is not flowing"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — routing is restored and the box is back to its pre-lab state."
else
  echo "One or more checks failed."
fi
exit "$fail"
