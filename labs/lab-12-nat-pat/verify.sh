#!/usr/bin/env bash
# Lab 12 — objective pass/fail check.
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

echo "== Lab 12 verification =="

check "namespace a exists" \
  bash -c "ip netns list | grep -qw a"
check "host side h-a carries 10.1.1.1/24" \
  bash -c "ip -4 addr show dev h-a | grep -q '10.1.1.1/24'"
check "namespace a carries 10.1.1.2/24 on a-h" \
  bash -c "ip netns exec a ip -4 addr show dev a-h | grep -q '10.1.1.2/24'"
check "namespace a has a default route via 10.1.1.1" \
  bash -c "ip netns exec a ip route | grep -q 'default via 10.1.1.1'"
check "host has net.ipv4.ip_forward=1" \
  bash -c "sysctl -n net.ipv4.ip_forward | grep -q '^1$'"
check "MASQUERADE rule for 10.1.1.0/24 out of eth0 is present" \
  iptables -t nat -C POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE
check "namespace a can ping 8.8.8.8 through the NAT" \
  ip netns exec a ping -c2 -W3 8.8.8.8

# The Test-it check from the README: conntrack must show the translation.
if command -v conntrack >/dev/null 2>&1; then
  # Generate a little traffic so there is something to see.
  ip netns exec a ping -c2 -W3 8.8.8.8 >/dev/null 2>&1 || true
  if conntrack -L 2>/dev/null | grep -q 'src=10.1.1.2'; then
    echo "PASS: conntrack shows a translated flow from src=10.1.1.2"
    conntrack -L 2>/dev/null | grep 'src=10.1.1.2' | head -3
  else
    echo "FAIL: conntrack has no entry for src=10.1.1.2 (Step 5)"
    fails=$((fails + 1))
  fi
else
  echo "FAIL: conntrack not installed — run 'apt install -y conntrack' (Step 5)"
  fails=$((fails + 1))
fi

echo
if [ "$fails" -eq 0 ]; then
  echo "PASS: Lab 12 complete — PAT is translating 10.1.1.0/24 out of eth0."
  exit 0
fi
echo "FAIL: $fails check(s) failed."
exit 1
