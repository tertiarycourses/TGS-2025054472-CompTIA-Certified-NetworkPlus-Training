#!/usr/bin/env bash
# Lab 8 — objective pass/fail check.
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

echo "== Lab 8 verification =="

for n in a r1 b; do
  if ip netns list | grep -qw "$n"; then
    echo "PASS: namespace $n exists"
  else
    echo "FAIL: namespace $n missing — run ./setup.sh"
    fails=$((fails + 1))
  fi
done

check "a has 10.1.1.2/24 on a-r" \
  bash -c "ip netns exec a ip -4 addr show dev a-r | grep -q '10.1.1.2/24'"
check "b has 10.2.2.2/24 on b-r" \
  bash -c "ip netns exec b ip -4 addr show dev b-r | grep -q '10.2.2.2/24'"
check "router r1 has ip_forward=1" \
  bash -c "ip netns exec r1 sysctl -n net.ipv4.ip_forward | grep -q '^1$'"
check "a has a static route to 10.2.2.0/24 via 10.1.1.1" \
  bash -c "ip netns exec a ip route | grep -q '10.2.2.0/24 via 10.1.1.1'"
check "b has a static route to 10.1.1.0/24 via 10.2.2.1" \
  bash -c "ip netns exec b ip route | grep -q '10.1.1.0/24 via 10.2.2.1'"

# The Test-it check from the README: A pings B across the router.
check "a can ping 10.2.2.2 across router r1" \
  ip netns exec a ping -c2 -W2 10.2.2.2

echo
if [ "$fails" -eq 0 ]; then
  echo "PASS: Lab 8 complete — subnet A reaches subnet B through R1."
  exit 0
fi
echo "FAIL: $fails check(s) failed."
exit 1
