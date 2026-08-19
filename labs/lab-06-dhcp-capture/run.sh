#!/usr/bin/env bash
# Lab 6 — DHCP Lease Capture (DORA)
# Runs the capture + release + renew sequence from README steps 1-5.
# Each command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — Install the tools =="
apt update && apt install -y isc-dhcp-client tcpdump

echo
echo "== Step 2 — Start a capture for DHCP ports (UDP 67 server / 68 client) =="
tcpdump -i eth0 -nn -v 'port 67 or port 68' &
sleep 2

echo
echo "== Step 3 — Release the current lease (sends DHCPRELEASE) =="
dhclient -v -r eth0

echo
echo "== Step 4 — Request a new lease — watch for DISCOVER, OFFER, REQUEST, ACK =="
dhclient -v eth0
sleep 3

echo
echo "== Step 5 — Stop the capture =="
kill %1 2>/dev/null || true

echo
echo "Look back through the tcpdump output above for the four DORA messages:"
echo "  1. DHCPDISCOVER  (broadcast 0.0.0.0 -> 255.255.255.255)"
echo "  2. DHCPOFFER     (server proposes an IP)"
echo "  3. DHCPREQUEST   (client confirms which offer)"
echo "  4. DHCPACK       (server confirms the lease)"
echo
echo "Confirm the new lease with: ip -4 addr show eth0"
