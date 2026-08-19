#!/usr/bin/env bash
# Lab 33 — restore eth0's MTU to the standard Ethernet 1500 (README Step 5).
# Run this if run.sh was interrupted while the MTU was still lowered to 1400.
# Tolerant: reports state even if nothing needed changing.
set -uo pipefail

current=$(cat /sys/class/net/eth0/mtu 2>/dev/null || echo "unknown")
echo "eth0 MTU before cleanup: $current"

if [ "$current" = "1500" ]; then
  echo "Already 1500 — nothing to restore."
else
  ip link set eth0 mtu 1500 && echo "Restored eth0 MTU to 1500" || echo "Could not set MTU — are you root?"
fi

ip -brief link show eth0
echo "Cleanup done — the box is back to its pre-lab state."
