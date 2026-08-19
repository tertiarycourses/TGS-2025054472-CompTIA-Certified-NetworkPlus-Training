#!/usr/bin/env bash
# Lab 9 — 802.1Q VLAN Tagging
# Runs README Steps 1-3: load 8021q, create eth0.10 / eth0.20, address them.
# Idempotent: removes any previous sub-interfaces first.
set -euo pipefail

echo "== Step 0: remove any previous run =="
for i in eth0.10 eth0.20; do
  ip link del "$i" 2>/dev/null || true
done

echo "== Step 1: load the 802.1Q kernel module =="
modprobe 8021q
lsmod | grep 8021q

echo "== Step 2: create two VLAN sub-interfaces on eth0 =="
ip link add link eth0 name eth0.10 type vlan id 10
ip link add link eth0 name eth0.20 type vlan id 20

echo "== Step 3: assign each VLAN its own subnet =="
ip addr add 192.168.10.1/24 dev eth0.10
ip addr add 192.168.20.1/24 dev eth0.20
ip link set eth0.10 up
ip link set eth0.20 up

echo
echo "VLAN sub-interfaces ready. Now run ./verify.sh"
