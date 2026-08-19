#!/usr/bin/env bash
# Lab 31 — ARP and the IPv6 Neighbour Table
# Runs the sequence from README steps 1-6.
# Every command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — View the current neighbour table =="
ip neigh

echo
echo "== Step 2 — Probe the default gateway with arping =="
apt update && apt install -y iputils-arping
arping -I eth0 -c2 "$(ip route | awk '/default/ {print $3}')" || true

echo
echo "== Step 3 — Duplicate address detection on our own IP =="
arping -D -I eth0 -c2 "$(ip -4 -o addr show eth0 | awk '{print $4}' | cut -d/ -f1)" || true

echo
echo "== Step 4 — Add a static ARP entry =="
ip neigh replace 10.0.0.99 lladdr de:ad:be:ef:00:01 dev eth0
ip neigh

echo
echo "== Step 5 — Flush the table =="
ip neigh flush all
ip neigh
echo "(the table repopulates as soon as you generate traffic)"
ping -c2 "$(ip route | awk '/default/ {print $3}')" >/dev/null 2>&1 || true
ip neigh

echo
echo "== Step 6 — IPv6 neighbour discovery =="
ip -6 neigh
ndisc6 ff02::1 eth0 2>/dev/null || apt install -y ndisc6

echo
echo "Record what you saw in data/arp-table.csv — look for INCOMPLETE, FAILED and duplicate MACs."
