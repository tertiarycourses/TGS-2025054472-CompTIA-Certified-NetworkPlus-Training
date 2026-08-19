#!/usr/bin/env bash
# Lab 33 — MTU and Path-MTU Discovery
# Runs the DF-bit probe sequence from README steps 1-5.
# Every command below is exactly what the README shows.
# The script LOWERS eth0's MTU in Step 4 and restores it in Step 5.
# If it is interrupted, run ./cleanup.sh to put the MTU back to 1500.
set -euo pipefail

echo "== Step 1 — See your interface MTU =="
ip -brief link show eth0

echo
echo "== Step 2 — Largest payload that fits a 1500-byte MTU: 1500 - 28 = 1472 =="
ping -M do -s 1472 -c2 8.8.8.8 || true

echo
echo "== Step 3 — Force 'fragmentation needed' with an oversized payload =="
echo "   expect: ping: local error: message too long, mtu=1500"
ping -M do -s 1500 -c2 8.8.8.8 || true

echo
echo "== Step 4 — Lower the interface MTU to 1400 and retest =="
ip link set eth0 mtu 1400
ip -brief link show eth0
ping -M do -s 1400 -c2 8.8.8.8 || true
echo "   now the largest payload that fits is 1400 - 28 = 1372"
ping -M do -s 1372 -c2 8.8.8.8 || true

echo
echo "== Step 5 — Restore the MTU =="
ip link set eth0 mtu 1500
ip -brief link show eth0

echo
echo "MTU restored to 1500. If this script was interrupted, run ./cleanup.sh."
