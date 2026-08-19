#!/usr/bin/env bash
# Lab 35 — environment prep: make sure tc, the netem module and iperf3 are ready
# before you start shaping eth0. Idempotent — safe to re-run.
set -euo pipefail

echo "== Checking tc (iproute2) =="
command -v tc >/dev/null 2>&1 && echo "tc present: $(tc -V 2>&1 | head -1)" || apt install -y iproute2

echo
echo "== Loading the sch_netem kernel module =="
modprobe sch_netem 2>/dev/null && echo "sch_netem loaded" || echo "sch_netem built in or already loaded"
lsmod | grep -E '^sch_netem' || true

echo
echo "== Installing iperf3 (used in README Step 5) =="
apt update && apt install -y iperf3

echo
echo "== Clearing any qdisc left over from a previous run =="
tc qdisc del dev eth0 root 2>/dev/null && echo "removed a leftover qdisc" || echo "no leftover qdisc on eth0"

echo
echo "== Current qdisc on eth0 =="
tc qdisc show dev eth0

echo
echo "Setup complete. Run ./run.sh — and ALWAYS finish with ./cleanup.sh."
