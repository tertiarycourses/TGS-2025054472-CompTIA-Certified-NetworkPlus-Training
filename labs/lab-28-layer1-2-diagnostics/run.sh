#!/usr/bin/env bash
# Lab 28 — Layer 1/2 Diagnostics with ip and ethtool
# Runs the diagnostic sequence from README steps 1-5.
# Every command below is exactly what the README shows.
# Step 6 (forcing speed/duplex) is deliberately NOT run — it can drop the
# Killercoda primary NIC. Read it in the README instead.
set -euo pipefail

echo "== Step 1 — Install ethtool =="
apt update && apt install -y ethtool

echo
echo "== Step 2 — Check operational state =="
ip -brief link show

echo
echo "== Step 3 — Inspect link parameters (Speed / Duplex / Auto-neg / Link detected) =="
ethtool eth0 || true

echo
echo "== Step 4 — Check error counters =="
ip -s link show eth0
ethtool -S eth0 | grep -iE 'err|drop|crc|frame' || echo "(driver exposes no matching counters — normal on a virtual NIC)"

echo
echo "== Step 5 — Bounce the interface =="
ip link set eth0 down
sleep 1
ip link set eth0 up
sleep 3
ip -brief link show

echo
echo "== Step 6 — Force speed/duplex — EXAMPLE ONLY, not executed =="
echo "  # ethtool -s eth0 speed 1000 duplex full autoneg off"

echo
echo "Now open data/interface-errors.csv and complete the 'likely cause' column."
