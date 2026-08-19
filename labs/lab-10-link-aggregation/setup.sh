#!/usr/bin/env bash
# Lab 10 — Link Aggregation (LACP Bond)
# Runs README Steps 1-2 only: install ifenslave, load the bonding driver,
# create bond0. It deliberately STOPS before Step 3.
#
# WHY: Step 3 enslaves eth0, which is the only NIC in the Killercoda
# playground — doing that disconnects your shell. Enslaving is a decision you
# make consciously, so this script never does it for you. Run Step 3 by hand
# (on a multi-NIC VM) after reading the warning in the README.
set -euo pipefail

echo "== Step 1: install ifenslave and load the bonding driver =="
apt update && apt install -y ifenslave
modprobe bonding mode=802.3ad miimon=100

echo "== Step 2: create the bond interface =="
if ip link show bond0 >/dev/null 2>&1; then
  echo "bond0 already exists — leaving it alone (setup is idempotent)"
else
  ip link add bond0 type bond mode 802.3ad
fi

echo
echo "bond0 created in 802.3ad (LACP) mode."
echo "Step 3 (enslaving a NIC) is NOT run automatically — see the README warning."
echo "Next: ./verify.sh   then, if you are on a multi-NIC VM, do Step 3 by hand."
