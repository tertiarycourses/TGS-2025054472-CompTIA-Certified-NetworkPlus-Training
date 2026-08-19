#!/usr/bin/env bash
# Lab 9 — objective pass/fail check.
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

echo "== Lab 9 verification =="

check "8021q kernel module is loaded" \
  bash -c "lsmod | grep -q '^8021q'"
check "eth0.10 exists with VLAN id 10" \
  bash -c "ip -d link show eth0.10 | grep -q 'vlan.*id 10'"
check "eth0.20 exists with VLAN id 20" \
  bash -c "ip -d link show eth0.20 | grep -q 'vlan.*id 20'"
check "eth0.10 carries 192.168.10.1/24" \
  bash -c "ip -4 addr show dev eth0.10 | grep -q '192.168.10.1/24'"
check "eth0.20 carries 192.168.20.1/24" \
  bash -c "ip -4 addr show dev eth0.20 | grep -q '192.168.20.1/24'"
check "eth0.10 is up" \
  bash -c "ip link show eth0.10 | grep -q 'state UP\|UP,LOWER_UP\|,UP'"
check "eth0.20 is up" \
  bash -c "ip link show eth0.20 | grep -q 'state UP\|UP,LOWER_UP\|,UP'"

# The Test-it check from the README: a tagged frame must be visible on the wire.
echo "-- capturing tagged frames on eth0 for 5s --"
cap=$(mktemp)
if command -v tcpdump >/dev/null 2>&1; then
  timeout 6 tcpdump -i eth0 -nn -e vlan -c 5 >"$cap" 2>/dev/null &
  tdpid=$!
  sleep 1
  ping -c3 -I eth0.10 192.168.10.1 >/dev/null 2>&1 || true
  wait "$tdpid" 2>/dev/null || true
  if grep -q 'vlan 10' "$cap"; then
    echo "PASS: tcpdump saw a frame tagged 'vlan 10' on eth0"
  else
    echo "FAIL: no 'vlan 10' tag captured on eth0 (see Step 5 — run tcpdump by hand)"
    fails=$((fails + 1))
  fi
else
  echo "FAIL: tcpdump not installed — run 'apt install -y tcpdump' (Step 5)"
  fails=$((fails + 1))
fi
rm -f "$cap"

echo
if [ "$fails" -eq 0 ]; then
  echo "PASS: Lab 9 complete — both VLAN sub-interfaces are up and tagging."
  exit 0
fi
echo "FAIL: $fails check(s) failed."
exit 1
