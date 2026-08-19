#!/usr/bin/env bash
# Lab 8 — Static Routing Between Two Subnets
# Builds the topology of README Steps 1-5:  a (10.1.1.2) <-> r1 <-> b (10.2.2.2)
# Idempotent: safe to re-run (it removes any previous run first).
set -euo pipefail

echo "== Step 0: remove any previous run =="
for n in a r1 b; do
  ip netns del "$n" 2>/dev/null || true
done

echo "== Step 1: create three namespaces =="
ip netns add a
ip netns add r1
ip netns add b

echo "== Step 2: wire A<->R1 and B<->R1 with veth pairs =="
ip link add a-r type veth peer name r-a
ip link add b-r type veth peer name r-b
ip link set a-r netns a
ip link set r-a netns r1
ip link set b-r netns b
ip link set r-b netns r1

echo "== Step 3: assign IPs (two different subnets) =="
ip netns exec a  ip addr add 10.1.1.2/24 dev a-r
ip netns exec r1 ip addr add 10.1.1.1/24 dev r-a
ip netns exec r1 ip addr add 10.2.2.1/24 dev r-b
ip netns exec b  ip addr add 10.2.2.2/24 dev b-r
for n in a r1 b; do ip netns exec $n ip link set lo up; done
ip netns exec a  ip link set a-r up
ip netns exec r1 ip link set r-a up
ip netns exec r1 ip link set r-b up
ip netns exec b  ip link set b-r up

echo "== Step 4: enable IP forwarding on the router =="
ip netns exec r1 sysctl -w net.ipv4.ip_forward=1

echo "== Step 5: add static routes on the end hosts =="
ip netns exec a ip route add 10.2.2.0/24 via 10.1.1.1
ip netns exec b ip route add 10.1.1.0/24 via 10.2.2.1

echo
echo "Topology ready. Now run ./verify.sh"
