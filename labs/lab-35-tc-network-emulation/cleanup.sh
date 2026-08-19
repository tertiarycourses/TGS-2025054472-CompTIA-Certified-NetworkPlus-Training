#!/usr/bin/env bash
# Lab 35 — MANDATORY cleanup. Removes the eth0 root qdisc (README Step 6) and
# stops the backgrounded iperf3 server from Step 5.
#
# If you skip this, eth0 stays delayed / lossy / rate-limited and EVERY later
# lab on this box will look broken. Tolerant: keep going on any failure.
set -uo pipefail

echo "== Qdisc on eth0 before cleanup =="
tc qdisc show dev eth0

echo
echo "== Deleting the eth0 root qdisc =="
tc qdisc del dev eth0 root 2>/dev/null && echo "root qdisc deleted" || echo "no root qdisc to delete (already clean)"

echo
echo "== Stopping the backgrounded iperf3 server (Step 5: iperf3 -s -D) =="
pkill -f 'iperf3 -s' 2>/dev/null && echo "iperf3 server stopped" || echo "no iperf3 server running"

echo
echo "== Qdisc on eth0 after cleanup =="
tc qdisc show dev eth0
echo "(a plain pfifo_fast / fq_codel / noqueue line means eth0 is unshaped)"

echo
echo "== Sanity ping — RTT should be back to its Step 1 baseline =="
ping -c3 8.8.8.8 || true

echo
echo "Cleanup done — the box is back to its pre-lab state."
