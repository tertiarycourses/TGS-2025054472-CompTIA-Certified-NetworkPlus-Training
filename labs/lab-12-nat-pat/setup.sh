#!/usr/bin/env bash
# Lab 12 — NAT and PAT with iptables
# Runs README Steps 1-3: build the namespace, enable forwarding, add MASQUERADE.
# Idempotent: safe to re-run (it removes the previous run first).
set -euo pipefail

echo "== Step 0: remove any previous run =="
ip netns del a 2>/dev/null || true
ip link del h-a 2>/dev/null || true
# Drop only the exact rule this lab adds, so other NAT rules survive.
while iptables -t nat -C POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE 2>/dev/null; do
  iptables -t nat -D POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE
done

echo "== Step 1: re-create the namespace from Lab 7 (or 8) =="
ip netns add a
ip link add a-h type veth peer name h-a
ip link set a-h netns a
ip addr add 10.1.1.1/24 dev h-a
ip link set h-a up
ip netns exec a ip addr add 10.1.1.2/24 dev a-h
ip netns exec a ip link set a-h up
ip netns exec a ip link set lo up
ip netns exec a ip route add default via 10.1.1.1

echo "== Step 2: enable forwarding on the host =="
sysctl -w net.ipv4.ip_forward=1

echo "== Step 3: add the MASQUERADE rule (PAT) =="
iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE

echo
echo "NAT gateway ready. Now run ./verify.sh"
