#!/usr/bin/env bash
# Lab 10 — reverse everything the lab created (README Step 5).
# Tolerant: keep going even if the bond is already gone.
set -uo pipefail

echo "== Releasing slaves from bond0 =="
if [ -r /proc/net/bonding/bond0 ]; then
  for s in $(awk '/^Slave Interface:/ {print $3}' /proc/net/bonding/bond0); do
    ip link set "$s" nomaster 2>/dev/null && echo "released $s" || echo "could not release $s"
    ip link set "$s" up 2>/dev/null || true
  done
else
  # The README's literal Step 5 command, for the single-NIC playground case.
  ip link set eth0 nomaster 2>/dev/null || true
fi

echo "== Deleting bond0 =="
ip link del bond0 2>/dev/null && echo "deleted bond0" || echo "bond0 already gone"

echo "Cleanup done — NICs are standalone again."
echo "Note: the 'bonding' module stays loaded; it is harmless and unloading it"
echo "      requires no bonds to exist ('modprobe -r bonding' if you want to)."
