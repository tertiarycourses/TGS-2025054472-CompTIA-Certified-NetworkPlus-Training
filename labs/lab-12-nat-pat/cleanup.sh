#!/usr/bin/env bash
# Lab 12 — reverse everything the lab created (README Step 6).
# Tolerant: keep going even if something is already gone.
set -uo pipefail

echo "== Removing the NAT rule this lab added =="
# Delete the exact rule, repeatedly, in case setup.sh was run more than once.
# This is safer than flushing POSTROUTING wholesale: any other NAT rule on the
# box survives. If you prefer the README's blunt version, run:
#     iptables -t nat -F POSTROUTING
removed=0
while iptables -t nat -C POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE 2>/dev/null; do
  iptables -t nat -D POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE
  removed=$((removed + 1))
done
echo "removed $removed MASQUERADE rule(s) for 10.1.1.0/24"

echo "== Current nat POSTROUTING chain =="
iptables -t nat -L POSTROUTING -n --line-numbers 2>/dev/null || true

echo "== Deleting namespace a and the veth pair =="
ip netns del a 2>/dev/null && echo "deleted netns a" || echo "netns a already gone"
ip link del h-a 2>/dev/null && echo "deleted h-a" || true

echo "== Flushing stale conntrack entries for the lab subnet =="
command -v conntrack >/dev/null 2>&1 && conntrack -D -s 10.1.1.0/24 >/dev/null 2>&1 || true

echo "Cleanup done — no NAT rules from this lab remain."
