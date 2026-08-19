#!/usr/bin/env bash
# Lab 10 — objective pass/fail check.
# Tolerant on purpose: one failed check must not abort the remaining checks.
set -uo pipefail

fails=0
check() {  # check <description> <command...>
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "PASS: $desc"
  else
    echo "FAIL: $desc"
    fails=$((fails + 1))
  fi
}

echo "== Lab 10 verification =="

check "bonding kernel module is loaded" \
  bash -c "lsmod | grep -q '^bonding'"
check "bond0 interface exists" \
  ip link show bond0
check "bond0 is in 802.3ad (LACP) mode" \
  bash -c "cat /proc/net/bonding/bond0 | grep -qi '802.3ad'"
check "miimon polling is configured (100 ms)" \
  bash -c "cat /proc/net/bonding/bond0 | grep -qi 'MII Polling Interval'"

# The Test-it check from the README: /proc/net/bonding/bond0 lists the slaves
# and each one reports link up.
if [ -r /proc/net/bonding/bond0 ]; then
  slaves=$(grep -c '^Slave Interface:' /proc/net/bonding/bond0 2>/dev/null || echo 0)
  up=$(grep -c '^MII Status: up' /proc/net/bonding/bond0 2>/dev/null || echo 0)
  echo "-- bond0 reports $slaves slave interface(s); $up 'MII Status: up' line(s) --"
  if [ "$slaves" -ge 1 ]; then
    echo "PASS: bond0 has $slaves enslaved interface(s)"
  else
    echo "FAIL: bond0 has no slaves — do Step 3 (expected in Killercoda, which has only eth0)"
    fails=$((fails + 1))
  fi
  # up counts the bond itself plus each healthy slave.
  if [ "$up" -ge $((slaves + 1)) ]; then
    echo "PASS: bond0 and all $slaves slave(s) report MII Status: up"
  else
    echo "FAIL: not every slave reports 'MII Status: up' in /proc/net/bonding/bond0"
    fails=$((fails + 1))
  fi
else
  echo "FAIL: /proc/net/bonding/bond0 not readable — bond0 was never created"
  fails=$((fails + 1))
fi

echo
if [ "$fails" -eq 0 ]; then
  echo "PASS: Lab 10 complete — bond0 is up in 802.3ad mode with all slaves up."
  exit 0
fi
echo "FAIL: $fails check(s) failed."
echo "NOTE: on Killercoda (single NIC) the slave checks are expected to fail unless"
echo "      you ran Step 3 by hand. The mode/module checks above are the ones that"
echo "      must pass in the playground."
exit 1
