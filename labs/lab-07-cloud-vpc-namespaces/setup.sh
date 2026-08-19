#!/usr/bin/env bash
# Lab 7 — Simulating a Cloud VPC with Network Namespaces
# Builds the topology from README steps 1-4: two namespaces, a bridge,
# two veth pairs and addresses in 10.0.1.0/24.
# Each command below is exactly what the README shows.
#
# Idempotent: run ./cleanup.sh first if a previous run is still in place.
set -euo pipefail

echo "== Step 0 — Removing any leftovers from a previous run =="
ip netns del web 2>/dev/null || true
ip netns del db  2>/dev/null || true
ip link del br0  2>/dev/null || true
ip link del veth-web 2>/dev/null || true
ip link del veth-db  2>/dev/null || true

echo
echo "== Step 1 — Create two namespaces (representing two VMs) =="
ip netns add web
ip netns add db

echo
echo "== Step 2 — Create a bridge (the VPC switch) =="
ip link add br0 type bridge
ip link set br0 up

echo
echo "== Step 3 — Connect each namespace to the bridge with a veth pair =="
ip link add veth-web type veth peer name br-web
ip link add veth-db  type veth peer name br-db

ip link set br-web master br0
ip link set br-db  master br0
ip link set br-web up
ip link set br-db  up

ip link set veth-web netns web
ip link set veth-db  netns db

echo
echo "== Step 4 — Assign IPs in the same /24 subnet =="
ip netns exec web ip addr add 10.0.1.10/24 dev veth-web
ip netns exec db  ip addr add 10.0.1.20/24 dev veth-db
ip netns exec web ip link set veth-web up
ip netns exec db  ip link set veth-db  up
ip netns exec web ip link set lo up
ip netns exec db  ip link set lo up

echo
echo "Topology built:"
echo "  web (10.0.1.10/24) --veth-web---[br0]---veth-db-- db (10.0.1.20/24)"
echo
echo "Now run ./verify.sh — or README Step 5 by hand."
