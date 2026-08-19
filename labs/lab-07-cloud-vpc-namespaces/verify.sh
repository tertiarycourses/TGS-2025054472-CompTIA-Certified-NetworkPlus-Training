#!/usr/bin/env bash
# Lab 7 — verify the simulated VPC works (README Step 5).
# Checks both namespaces exist, the bridge is up, both addresses are assigned,
# and that web can ping db across the bridge.
set -uo pipefail

fail=0

for ns in web db; do
  if ip netns list | grep -qw "$ns"; then
    echo "PASS: namespace '$ns' exists"
  else
    echo "FAIL: namespace '$ns' not found — run ./setup.sh or README Step 1"
    fail=1
  fi
done

if ip link show br0 >/dev/null 2>&1; then
  echo "PASS: bridge br0 exists"
  if ip link show br0 | grep -q 'state UP\|UP,LOWER_UP\|,UP'; then
    echo "PASS: bridge br0 is up"
  else
    echo "FAIL: bridge br0 is down — run: ip link set br0 up"
    fail=1
  fi
else
  echo "FAIL: bridge br0 not found — run ./setup.sh or README Step 2"
  fail=1
fi

if ip netns exec web ip -4 addr show veth-web 2>/dev/null | grep -q '10.0.1.10/24'; then
  echo "PASS: web has 10.0.1.10/24 on veth-web"
else
  echo "FAIL: 10.0.1.10/24 not configured in namespace web"
  fail=1
fi

if ip netns exec db ip -4 addr show veth-db 2>/dev/null | grep -q '10.0.1.20/24'; then
  echo "PASS: db has 10.0.1.20/24 on veth-db"
else
  echo "FAIL: 10.0.1.20/24 not configured in namespace db"
  fail=1
fi

echo
echo "-- Step 5: ping from web to db --"
if ip netns exec web ping -c2 10.0.1.20 >/dev/null 2>&1; then
  echo "PASS: web (10.0.1.10) can ping db (10.0.1.20) across br0"
else
  echo "FAIL: ping from web to db failed — check the veth pairs are enslaved to br0 and up"
  fail=1
fi

if ip netns exec db ping -c2 10.0.1.10 >/dev/null 2>&1; then
  echo "PASS: db (10.0.1.20) can ping web (10.0.1.10) across br0"
else
  echo "FAIL: ping from db to web failed"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — you have a working VPC subnet. Run ./cleanup.sh when done."
else
  echo "One or more checks failed."
fi
exit "$fail"
